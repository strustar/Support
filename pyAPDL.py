import streamlit as st
import numpy as np
from ansys.mapdl.core import launch_mapdl

import os;  import json
os.system('cls')  # 터미널 창 청소, clear screen

# 스트림릿 웹상에서 실행되지 않게
if __name__ != "streamlit.script_runner":
    a = 3
    a

# 실행중인 프로그램(ANSYS) 강제 종료  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import subprocess
subprocess.run(['taskkill', '/F', '/IM', 'ANSYS*'])
subprocess.run(['taskkill', '/F', '/IM', 'APDL*'])
# 실행중인 프로그램(ANSYS) 강제 종료  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class In:
    pass
with open('Input.json', 'r') as f:
    item = json.load(f)        

eshape_th = 2.5
In.Ly = item['Ly']
In.vertical_d = item['vertical_d'];      In.vertical_t = item['vertical_t'];      In.Lv = item['Lv']
In.horizontal_d = item['horizontal_d'];  In.horizontal_t = item['horizontal_t'];  In.Lh = item['Lh']
In.bracing_d = item['bracing_d'];        In.bracing_t = item['bracing_t']
In.slab_X = item['slab_X'];              In.slab_Y = item['slab_Y'];              In.height = item['height']  # Unit : m
In.dead_load = item['dead_load'];        In.design_load = item['design_load']     # N/mm2
In.Hx2 = item['Hx2'];                    In.Hy2 = item['Hy2'];                    In.wind2 = item['wind2']  # kN/m2
        
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

results = [];  verticals = [];  horizontals = [];  bracings = []
def analysis(In, LC):   # Load Case
    factor = 1e3
    if LC == 1:
        ver = In.design_load;  horx = In.Hx2;    hory = In.Hy2
    if LC == 2:  # 풍하중
        ver = In.dead_load;    horx = In.wind2;  hory = In.wind2
    
    P = ver*In.Ly*In.Lv                                          # N/mm2 *mm *mm
    Hx = horx*In.Ly*In.Lh/factor;  Hy = hory*In.Lv*In.Lh/factor  # kN/m2 = 1e3 N/(mm*mm*1e6) *mm*mm = N / 1e3

    # !! ===============================================> Preprocessing 
    ma.clear();  ma.prep7()

    # !!! Modelling
    xea = int(np.ceil(In.slab_X*factor/In.Lv) + 1)
    yea = int(np.ceil(In.slab_Y*factor/In.Ly) + 1)
    zea = int(np.ceil(In.height*factor/In.Lh) + 1)    

    ma.k(1, 0,0,0)
    ma.kgen(xea, 1,1,1, In.Lv,0,0, 1)
    ma.kgen(yea, 'all','','', 0,In.Ly,0, 100)
    ma.kgen(zea, 'all','','', 0,0,In.Lh, 10000)
    # ma.allsel()    

    for i in range(1, xea + 1):   # 수직재
        for j in range(1, yea + 1):
            for k in range(1, zea):
                ma.l(i + 100*(j-1) + 10000*(k-1), i + 10000 + 100*(j-1) + 10000*(k-1))    
    ma.allsel();  ma.cm('ver',  'line');  ma.color('line', 'magenta')

    for i in range(1, xea):   # 수평재 (x방향)
        for j in range(1, yea + 1):
            for k in range(1, zea):
                ma.l(i + 10000 + 100*(j-1) + 10000*(k-1), i + 10001 + 100*(j-1) + 10000*(k-1))
    for i in range(1, xea + 1):   # 수평재 (y방향)
        for j in range(1, yea):
            for k in range(1, zea):
                ma.l(i + 10000 + 100*(j-1) + 10000*(k-1), i + 10100 + 100*(j-1) + 10000*(k-1))
    ma.allsel();  ma.cmsel('u', 'ver');  ma.cm('hor',  'line');  ma.color('line', 'cyan')

    for i in range(1, xea, 2):   # 가새재
        for j in range(1, yea + 1, 2):
            for k in range(1, zea, 2):
                ma.l(i + 100*(j-1) + 10000*(k-1), i + 10001 + 100*(j-1) + 10000*(k-1))
    ma.allsel();  ma.cmsel('u', 'ver');  ma.cmsel('u', 'hor');  ma.cm('bra', 'line');  ma.color('line', 'blue')
    ma.vup('', 'z');  ma.view('', 1, -1, 1)
    ma.allsel();  ma.nummrg('all')
    # !!! Modelling

    # !!! Attributes & Meshing
    i = 1;  ma.et(i, 'beam188');  ma.mp('ex', i, 200e3);  ma.mp('prxy', i, 0.3)
    ma.sectype(1, 'beam', 'ctube');  ma.secdata(In.vertical_d/2 - In.vertical_t, In.vertical_d/2)
    ma.sectype(2, 'beam', 'ctube');  ma.secdata(In.horizontal_d/2 - In.horizontal_t, In.horizontal_d/2)
    ma.sectype(3, 'beam', 'ctube');  ma.secdata(In.bracing_d*0.99/2 - In.bracing_t, In.bracing_d*0.99/2)    

    ma.cmsel('s', 'ver');  ma.latt(1,'',1,'','',1)
    ma.cmsel('s', 'hor');  ma.latt(1,'',1,'','',2)
    ma.cmsel('s', 'bra');  ma.latt(1,'',1,'','',3)
    ma.allsel();  ma.lesize('all', 200);  ma.lmesh('all')

    ma.esel('s', 'sec', '', 1);  ma.cm('v', 'elem');  ma.color('elem', 'magenta')
    ma.esel('s', 'sec', '', 2);  ma.cm('h', 'elem');  ma.color('elem', 'cyan')
    ma.esel('s', 'sec', '', 3);  ma.cm('b', 'elem');  ma.color('elem', 'blue')    
        
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
    ma.cmsel('s', 'v')
    ma.nsle('s')
    ma.nsel('r', 'loc', 'z', In.Lh*(zea - 1))    
    ma.f('all', 'fz', -P)

    ma.allsel()
    ma.cmsel('s', 'v')
    ma.nsle('s')
    ma.nsel('r', 'loc', 'z', In.Lh*(zea - 1))
    ma.nsel('r', 'loc', 'y', 0)
    ma.f('all', 'fy', Hy)

    ma.allsel()
    ma.cmsel('s', 'v')
    ma.nsle('s')
    ma.nsel('r', 'loc', 'z', In.Lh*(zea - 1))
    ma.nsel('r', 'loc', 'x', In.Lv*(xea - 1))
    ma.f('all', 'fx', -Hx)

    ma.allsel('all');  ma.eshape(0.1)
    ma.vscale('','',1)  # 하중 재하시 화살표 크기 동일하게 (작은 것은 안보이는 현상 발생)
    ma.pbc('f',1);  ma.pbc('u',1);  ma.pbc('rot',1)  # ma.replot()
    ma.eplot(vtk=False, off_screen=True)    # png_bc  001.png

    # png_model = os.path.join(working_dir, jobname + '000.png')
    # png_bc = os.path.join(working_dir, jobname + '001.png')
        
    output = ma.solve()    
    # output
    ma.finish()
    # !! ===============================================> Solution


    # !! ===============================================> Postprocessing
    ma.post1()
    ma.set('last')
    # ma.open_gui()
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
        if i == 3:  opt = 'b'        
        section_force('Fx1', 'Fx2', fact, opt)   # Fx, 004.png
        section_force('My1', 'My2', fact, opt)   # My, 005.png
        section_force('Mz1', 'Mz2', fact, opt)   # Mz, 006.png
        section_force('SFz1', 'SFz2', fact, opt)   # SFz, 007.png
        section_force('SFy1', 'SFy2', fact, opt)   # SFy, 008.png
        
    results.append(result)
    verticals.append(vertical)
    horizontals.append(horizontal)
    bracings.append(bracing)

analysis(In, 1)  # Load Case
analysis(In, 2)  # Load Case

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
