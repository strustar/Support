import streamlit as st
import numpy as np
import pandas as pd
from ansys.mapdl.core import launch_mapdl

import os;  import json
os.system('cls')  # 터미널 창 청소, clear screen

# 실행중인 프로그램(ANSYS) 강제 종료  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import subprocess
subprocess.run(['taskkill', '/F', '/IM', 'ANSYS*'])
subprocess.run(['taskkill', '/F', '/IM', 'APDL*'])
# 실행중인 프로그램(ANSYS) 강제 종료  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Input 불러오기
xea = 18;  zea = 20;  yea = 4  # X 절점개수 18, Z 절점개수 20
Lv = 305;  Ly = 610;  Lh = 863   # Lh : Check!!
vertical_d = 60.5;    vertical_t = 2.6
horizontal_d = 42.7;  horizontal_t = 2.3
bracing_d = 42.7;     bracing_t = 2.3

# slab_X = Lv*17;  slab_Y = Ly*3       !$  height = 9500
dead_load = 0.1372;  design_load = 0.1422;  Hx2 = 0.915e-3;  Hy2 = 8.232e-3;  wind2 = 0.286e-3  # N/mm2
Ex = 200e3

dataZ = np.full((zea+1, xea+1), None)   # +1은 빈공간, 정보 등, X간격 동일 : In.Lv
dataZ[1:, 0] = [1 + (i-1)*100 for i in range(1, 20+1)]
dataZ[ 1, 1:] = 0
dataZ[ 2, 1:] = 200
dataZ[ 3, 1:] = 216
dataZ[ 4, 1:] = 1291 + 216
dataZ[ 5, 1:-1] = 1725 - dataZ[4, 1]
dataZ[ 6, 1:-2] = 432
dataZ[ 7, 1:-3] = 216
dataZ[ 8, 1:-4] = 432
dataZ[ 9, 1:-5] = 216
dataZ[10, 1:-6] = 216
dataZ[11, 1:-7] = 216
dataZ[12, 1:-7] = 216
dataZ[13, 1:-8] = 216
dataZ[14, 1:-9] = 432
dataZ[15, 1:-10] = 216
dataZ[16, 1:-11] = 216
dataZ[17, 1:-12] = 432
dataZ[18, 1:-13] = 216
dataZ[19, 1:-14] = 432
dataZ[20, 1:-15] = 216
dataZ

load_loc = [None]
for i in range(1, xea+1):
    s = 0
    for k in range(1, zea+1):
        if dataZ[k, i] == None:  continue
        s += dataZ[k, i]
    load_loc.append(s)
# Input 불러오기

working_dir = 'pyAPDL';  jobname = 'file'
ma = launch_mapdl(run_location = working_dir, jobname = jobname, override = True)
ma.sys('del/q/f *.png')    # png 모든 파일 지우기
ma.plopts('date','off')    # 날짜 지우기
ma.run("/device,text,1,150")  # 레전드 키우기

# Reverse Video - white
ma.rgb('INDEX',100,100,100, 0)
ma.rgb('INDEX',80,80,80, 13)
ma.rgb('INDEX',60,60,60, 14)
ma.rgb('INDEX',0,0,0, 15)

eshape_th = 2.
results = [];  verticals = [];  horizontals = [];  bracings = []
def analysis(LC):   # Load Case    
    if LC == 1:
        ver = design_load;  horx = Hx2;    hory = Hy2
    if LC == 2:  # 풍하중
        ver = dead_load;    horx = wind2;  hory = wind2    
    P = ver*Ly*Lv                            # N/mm2 *mm *mm
    Hx = horx*Ly*Lh;  Hy = hory*Lv*Lh        # N/mm2 *mm *mm

    # import sys
    # sys.exit()    
    # !! ===============================================> Preprocessing 
    ma.clear();  ma.prep7()
    for i in range(1, xea+1):
        z = 0
        for k in range(1, zea+1):
            if dataZ[k, i] == None:  continue
            z += dataZ[k, i]
            ma.k(i-1 + dataZ[k, 0], Lv*(i-1),0, z)
    ma.kgen(yea, 'all','','', 0,Ly,0, 10000)
        
    for i in range(1, xea+1):   # 수직재
        for j in range(1, yea+1):
            for k in range(1, zea):
                if dataZ[k  , i] == None:  continue
                if dataZ[k+1, i] == None:  continue
                ma.l(i + 100*(k-1) + (j-1)*10000, i + 100*k + (j-1)*10000)
    ma.allsel();  ma.cm('ver',  'line');  ma.color('line', 'magenta')

    for i in range(1, xea):   # 수평재 (X방향)
        for j in range(1, yea+1):
            for k in range(2, zea+1):
                if dataZ[k, i  ] == None:  continue
                if dataZ[k, i+1] == None:  continue
                if k == 4 and i <= 16:  continue
                if k == 6 and i <= 14:  continue
                if k == 7 and i <= 13:  continue
                if k == 8 and i <= 12:  continue
                if k == 9 and i <= 11:  continue
                if k ==10 and i <= 10:  continue
                
                if k ==12 and i <=  9:  continue
                if k ==13 and i <=  8:  continue
                if k ==14 and i <=  7:  continue
                if k ==15 and i <=  6:  continue
                if k ==16 and i <=  5:  continue
                
                if k ==18 and i <=  4:  continue
                if k ==19 and i <=  3:  continue                
                ma.l(i + 100*(k-1) + 10000*(j-1), i + 1 + 100*(k-1) + 10000*(j-1))                
    for i in range(1, xea+1):   # 수평재 (Y방향)
        for j in range(1, yea):
            for k in range(2, zea+1):
                if dataZ[k, i] == None:  continue
                if k == 4 and i <= 16:  continue
                if k == 6 and i <= 14:  continue
                if k == 7 and i <= 13:  continue
                if k == 8 and i <= 12:  continue
                if k == 9 and i <= 11:  continue
                if k ==10 and i <= 10:  continue
                
                if k ==12 and i <=  9:  continue
                if k ==13 and i <=  8:  continue
                if k ==14 and i <=  7:  continue
                if k ==15 and i <=  6:  continue
                if k ==16 and i <=  5:  continue
                
                if k ==18 and i <=  4:  continue
                if k ==19 and i <=  3:  continue
                ma.l(i + 100*(k-1) + 10000*(j-1), i + 100*(k-1) + 10000*j)
    ma.allsel();  ma.cmsel('u', 'ver');  ma.cm('hor',  'line');  ma.color('line', 'cyan')

    ma.vup('', 'z');  ma.view('', 1, -1, 1)
    ma.allsel();  ma.nummrg('all')
    # ma.lplot(vtk=False, off_screen=True)    
    # !!! Modelling

    # !!! Attributes & Meshing
    i = 1;  ma.et(i, 'beam188');  ma.mp('ex', i, Ex);  ma.mp('prxy', i, 0.3)
    ma.sectype(1, 'beam', 'ctube');  ma.secdata(vertical_d/2 - vertical_t, vertical_d/2)
    ma.sectype(2, 'beam', 'ctube');  ma.secdata(horizontal_d/2 - horizontal_t, horizontal_d/2)
    # ma.sectype(3, 'beam', 'ctube');  ma.secdata(bracing_d/2 - bracing_t, bracing_d/2)

    ma.cmsel('s', 'ver');  ma.latt(1,'',1,'','',1)
    ma.cmsel('s', 'hor');  ma.latt(1,'',1,'','',2)
    # ma.cmsel('s', 'bra');  ma.latt(1,'',1,'','',3)
    ma.allsel();  ma.lesize('all', 200);  ma.lmesh('all')

    ma.esel('s', 'sec', '', 1);  ma.cm('v', 'elem');  ma.color('elem', 'magenta')
    ma.esel('s', 'sec', '', 2);  ma.cm('h', 'elem');  ma.color('elem', 'cyan')
    # ma.esel('s', 'sec', '', 3);  ma.cm('b', 'elem');  ma.color('elem', 'blue')    
        
    ma.allsel();  ma.eshape(eshape_th)  # ma.replot()
    ma.eplot(vtk=False, off_screen=True)  # png_model 000.png
    # !!! Attributes & Meshing
    ma.finish()
    # !! ===============================================> Preprocessing

    # !! ===============================================> Solution
    ma.slashsolu()
    ma.nsel('s', 'loc', 'z', 0)
    ma.d('all', 'all', 0)

    ma.allsel()
    for j in range(yea+1):
        for i in range(1, xea+1):
            ma.nsel('s', 'loc', 'z', load_loc[i])
            ma.nsel('r', 'loc', 'x', (i-1)*Lv)
            ma.nsel('r', 'loc', 'y', (j-1)*Ly)
            ma.f('all', 'fz', -P)

    ma.allsel()    
    for i in range(1, xea+1):
        ma.nsel('s', 'loc', 'z', load_loc[i])
        ma.nsel('r', 'loc', 'x', (i-1)*Lv)
        ma.nsel('r', 'loc', 'y', 0)
        ma.f('all', 'fy', Hy)

    ma.allsel()    
    for j in range(yea+1):        
        ma.nsel('s', 'loc', 'z', load_loc[i])
        ma.nsel('r', 'loc', 'x', (xea-1)*Lv)
        ma.nsel('r', 'loc', 'y', (j-1)*Ly)
        ma.f('all', 'fx', -Hx)

    ma.allsel('all');  ma.eshape(0.1)
    ma.vscale('','',1)  # 하중 재하시 화살표 크기 동일하게 (작은 것은 안보이는 현상 발생)
    ma.pbc('f',1);  ma.pbc('u',1);  ma.pbc('rot',1)  # ma.replot()
    ma.eplot(vtk=False, off_screen=True)    # png_bc  001.png    

    png_model = os.path.join(working_dir, jobname + '000.png')
    png_bc = os.path.join(working_dir, jobname + '001.png')
    st.image(png_model)
    st.image(png_bc)
    
    # ma.open_gui()
    output = ma.solve()    
    # output
    ma.finish()
    # !! ===============================================> Solution

    # !! ===============================================> Postprocessing
    ma.post1()
    ma.set('last')
    result = {'Load Case':LC, 'uz':0, 'seqv':0, 'Fx1': 0, 'Fx2': 0, 'My1':0, 'My2':0, 'Mz1':0, 'Mz2':0, 'SFz1':0, 'SFz2':0, 'SFy1':0, 'SFy2':0}
    vertical = {'Load Case':LC, 'Fx1': 0, 'Fx2': 0, 'My1':0, 'My2':0, 'Mz1':0, 'Mz2':0, 'SFz1':0, 'SFz2':0, 'SFy1':0, 'SFy2':0}
    horizontal = {'Load Case':LC, 'Fx1': 0, 'Fx2': 0, 'My1':0, 'My2':0, 'Mz1':0, 'Mz2':0, 'SFz1':0, 'SFz2':0, 'SFy1':0, 'SFy2':0}
    bracing = {'Load Case':LC, 'Fx1': 0, 'Fx2': 0, 'My1':0, 'My2':0, 'Mz1':0, 'Mz2':0, 'SFz1':0, 'SFz2':0, 'SFy1':0, 'SFy2':0}

    ma.show('png')
    ma.graphics('power')
    # ma.gfile(2400)
    ma.eshape(eshape_th)    
    ma.plnsol('u', 'z')   # Uz, 002.png
    result['uz'] = round(ma.get('uz_max', 'plnsol',0,'min'), 3)    
    ma.show('close')

    ma.show('png')
    ma.graphics('power')
    # ma.gfile(2400)
    ma.eshape(eshape_th)    
    ma.plnsol('s', 'eqv')  # seqv, 003.png
    result['seqv'] = round(ma.get('seqv_max', 'plnsol',0,'max'), 1)
    ma.show('close')
        
    st.image(os.path.join(working_dir, jobname + '002.png'))
    st.image(os.path.join(working_dir, jobname + '003.png'))

    # ma.open_gui()

    ma.etable('Fx1', 'SMISC', 1)
    ma.etable('Fx2', 'SMISC', 14)

    ma.etable('My1', 'SMISC', 2)
    ma.etable('My2', 'SMISC', 15)
    ma.etable('Mz1', 'SMISC', 3)
    ma.etable('Mz2', 'SMISC', 16)

    ma.etable('SFz1', 'SMISC', 5)
    ma.etable('SFz2', 'SMISC', 18)
    ma.etable('SFy1', 'SMISC', 6)
    ma.etable('SFy2', 'SMISC', 19)
        
    def section_force(s1, s2, fact, opt):
        if 'total' in opt:
            if 'Fx' in s1:
                ma.cmsel('s', 'v')
            else:
                ma.allsel()
            ma.show('png')
            # ma.gfile(2400)
            ma.plls(s1, s2, fact, 0, 0) 
            ma.esort('etab', s1)
            result[s1] = round(ma.get('max', 'sort',0,'max'), 1)
            result[s2] = round(ma.get('min', 'sort',0,'min'), 1)
            ma.show('close')
        else:
            ma.cmsel('s', opt)
            ma.plls(s1, s2, fact, 0, 0) 
            ma.esort('etab', s1)
            mx = round(ma.get('max', 'sort',0,'max'), 1);  mn = round(ma.get('min', 'sort',0,'min'), 1)            
            if 'v' in opt:
                vertical[s1] = mx
                vertical[s2] = mn
            if 'h' in opt:
                horizontal[s1] = mx
                horizontal[s2] = mn
            if 'b' in opt:
                bracing[s1] = mx
                bracing[s2] = mn

    fact = 1
    for i in range(4):
        if i == 0:  opt = 'total'
        if i == 1:  opt = 'v'
        if i == 2:  opt = 'h'
        # if i == 3:  opt = 'b'
        section_force('Fx1', 'Fx2', fact, opt)   # Fx, 004.png
        section_force('My1', 'My2', fact, opt)   # My, 005.png
        section_force('Mz1', 'Mz2', fact, opt)   # Mz, 006.png
        section_force('SFz1', 'SFz2', fact, opt)   # SFz, 007.png
        section_force('SFy1', 'SFy2', fact, opt)   # SFy, 008.png
        
    results.append(result)
    verticals.append(vertical)
    horizontals.append(horizontal)
    bracings.append(bracing)
    

analysis(1)  # Load Case
analysis(2)  # Load Case

import json
with open('Result.json', 'w') as f:
    json.dump(results, f, indent=4)
with open('Vertical.json', 'w') as f:
    json.dump(verticals, f, indent=4)
with open('Horizontal.json', 'w') as f:
    json.dump(horizontals, f, indent=4)
with open('Bracing.json', 'w') as f:
    json.dump(bracings, f, indent=4)

# 실행중인 프로그램(ANSYS) 강제 종료  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import subprocess
subprocess.run(['taskkill', '/F', '/IM', 'ANSYS*'])
subprocess.run(['taskkill', '/F', '/IM', 'APDL*'])
# 실행중인 프로그램(ANSYS) 강제 종료  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'해석 끝, 성공'
# pyVista 예시
# ver = ma.mesh.grid
# plotter = pv.Plotter(off_screen = True)    
# plotter.add_mesh(bra, color = 'magenta', line_width = 6, opacity = 1, label = 'Bracing')
# plotter.add_mesh(hor, color = 'blue', line_width = 6, opacity = 0.5, label = 'Horizontal')
# plotter.add_mesh(ver, color = 'green', line_width = 8, opacity = 1, label = 'Vertical')
# plotter.add_legend(bcolor = 'w', face = None, size = (0.15, 0.15), border = True)
# plotter.add_title('Modelling', font_size = 54, color = 'k')
# model_png = 'Images/model.png';  plotter.show(screenshot = model_png, window_size = (1920*2,1080*2), )    

    # rst_file = os.path.join(working_dir, jobname + '.rst')
    # simulation = post.load_simulation(rst_file)
    # simulation = post.StaticMechanicalSimulation(rst_file)

    # solution = post.load_solution(rst_file)
    # d = post.displacement.Displacement.x
    # displacement = simulation.displacement()    
    # displacement.plot(screenshot = 'tt.png', off_screen = True)

    # # stress_z = simulation.nodal_force(components= "X")
