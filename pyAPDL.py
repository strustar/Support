import streamlit as st
import numpy as np
from ansys.mapdl.core import launch_mapdl
# from ansys.mapdl.core import convert_script
# from ansys.dpf import post
# from PIL import Image
# import pyvista as pv
import sys
import os

# 스트림릿 웹상에서 실행되지 않게
if __name__ != "streamlit.script_runner":
    a = 3
    a

# !! ===============================================> Web상에서만 실행~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 실행중인 프로그램(ANSYS) 강제 종료  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import subprocess
subprocess.run(['taskkill', '/F', '/IM', 'ANSYS*'])
subprocess.run(['taskkill', '/F', '/IM', 'APDL*'])
# 실행중인 프로그램(ANSYS) 강제 종료  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class In:
    pass
In.joist_b = 50.0;  In.joist_h = 50;  In.joist_t = 2.3;  In.Lj = 150.0  # Unit : N, mm
In.yoke_b = 75;  In.yoke_h = 125;  In.yoke_t = 3.2;  In.Ly = 914

In.vertical_d = 60.5;  In.vertical_t = 2.6;  In.Lv = 914
In.horizontal_d = 42.7;  In.horizontal_t = 2.2;  In.Lh = 1725
In.bracing_d = 42.7;  In.bracing_t = 2.2

In.slab_X = 4;  In.slab_Y = 6;  In.height = 6  # Unit : m
In.dead_load = 10;  In.design_load = 12.5;  In.hx = 0.375;  In.hy = 0.25;  In.wind = 0.286  # kN/m2

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
In.ok = ':blue[∴ OK] (🆗✅)';  In.ng = ':red[∴ NG] (❌)'
In.space = '<div style="margin:0px">'
In.background_color = 'linen'
In.col_span_ref = [1, 1];  In.col_span_okng = [5, 1]  # 근거, OK(NG) 등 2열 배열 간격 설정
In.font_h1 = '28px';  In.font_h2 = '24px';  In.font_h3 = '22px';  In.font_h4 = '20px';  In.font_h5 = '18px';  In.font_h6 = '15px'

color = 'green'
In.border1 = f'<hr style="border-top: 2px solid {color}; margin-top:30px; margin-bottom:30px; margin-right: -30px">'  # 1줄
In.border2 = f'<hr style="border-top: 5px double {color}; margin-top: 0px; margin-bottom:30px; margin-right: -30px">' # 2줄

working_dir = 'pyAPDL';  jobname = 'file';  ma = launch_mapdl(run_location = working_dir, jobname = jobname, override = True)
ma.sys('del/q/f *.png')    # png 모든 파일 지우기

results = []
def analysis(In, LC):   # Load Case
    factor = 1e3
    if LC == 1:
        ver = In.design_load;  horx = In.hx;  hory = In.hy
    if LC == 2:  # 풍하중
        ver = In.dead_load;  horx = In.wind;  hory = In.wind
    P = ver*In.Ly*In.Lv/factor;  Hx = horx*In.Ly*In.Lh/factor;  Hy = hory*In.Lv*In.Lh/factor  # kN/m2 = 1e3 N/(mm*mm*1e6) *mm*mm = N / 1e3

    ma.plopts('date','off')    # 날짜 지우기    

    # Reverse Video - white
    ma.rgb('INDEX',100,100,100, 0)
    ma.rgb('INDEX',80,80,80, 13)
    ma.rgb('INDEX',60,60,60, 14)
    ma.rgb('INDEX',0,0,0, 15)

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
    ma.vup('', 'z');  ma.view('', 1,-1,1)
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
        
    ma.allsel();  ma.eshape(3)  # ma.replot()    
    # ma.eplot(vtk=False, background='k', show_edges=False, smooth_shading=True, color = 'blue', edge_color='red',
    #             window_size=[1920, 1080], savefig=savefig, style='surface', render_lines_as_tubes=True, line_width=5,
    #             off_screen=True)
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

    # [col1, col2] = st.columns(In.col_span_ref)
    # with col1:
    #     st.write(h4, '[해석 모델]')    
    #     st.image(png_model)
    # with col2:
    #     st.write(h4, '[경계조건 및 하중조건]')    
    #     st.image(png_bc)    
        
    output = ma.solve()    
    # output
    ma.finish()
    # !! ===============================================> Solution


    # !! ===============================================> Postprocessing
    ma.post1()
    ma.set('last')
    # ma.open_gui()
    result = {'Load Case':LC, 'uz':0, 'seqv':0, 'Fx1': 0, 'Fx2': 0, 'My1':0, 'My2':0, 'Mz1':0, 'Mz2':0, 'SFz1':0, 'SFz2':0, 'SFy1':0, 'SFy2':0}

    ma.show('png')
    ma.graphics('power')
    # ma.gfile(2400)
    ma.eshape(3)    
    ma.plnsol('u', 'z')   # Uz, 002.png
    result['uz'] = ma.get('uz_max', 'plnsol',0,'min')
    ma.show('close')

    ma.show('png')
    ma.graphics('power')
    # ma.gfile(2400)
    ma.eshape(3)    
    ma.plnsol('s', 'eqv')  # seqv, 003.png
    result['seqv'] = ma.get('seqv_max', 'plnsol',0,'max')
    ma.show('close')
    # ma.post_processing.plot_nodal_eqv_stress(off_screen=True, savefig='tt7.png')        
    # ma.post_processing.plot_nodal_displacement(component='z', off_screen=True, savefig='tt1.png')
    # ma.post_processing.plot_nodal_values('s','eqv', off_screen=True, savefig='tt2.png')

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
        
    def section_force(s1, s2, fact):
        if 'Fx' in s1:
            ma.cmsel('s', 'v')
        else:
            ma.allsel()
        ma.show('png')
        # ma.gfile(2400)
        ma.plls(s1, s2, fact, 0, 0) 
        ma.esort('etab', s1)
        result[s1] = ma.get('max', 'sort',0,'max')
        result[s2] = ma.get('min', 'sort',0,'min')
        ma.show('close')

    fact = 1
    section_force('Fx1', 'Fx2', fact)   # Fx, 004.png
    section_force('My1', 'My2', fact)   # My, 005.png
    section_force('Mz1', 'Mz2', fact)   # Mz, 006.png
    section_force('SFz1', 'SFz2', fact)   # SFz, 007.png
    section_force('SFy1', 'SFy2', fact)   # SFy, 008.png
    result

    results.append(result)


    # # ma.exit()
    # sys.exit()


    # # # Access MAPDL database : This feature does not work in the Ansys 2023 R1.
    # # elems = ma.db.elems
    # # nodes = ma.db.nodes
    # # elems, nodes

    # p = ma.parameters
    # p
    # g = ma.geometry
    # print(g)
    # g
    # m = ma.mesh
    # m
    

    # ma.exit()
    # sys.exit()


    # # f = ma.get('f', 'elem', 3, 'smisc', '2')
    # # f

    # # result = ma.result
    # # nnum, disp = result.nodal_displacement(0)
    # # nnum, disp

    # # # Create a structured grid (replace this with your actual mesh)
    # # # grid = pv.StructuredGrid()
    # # grid = result.mesh._grid

    # # # Add displacement data to the grid
    # # grid.point_array["Displacement"] = disp

    # # p = pv.Plotter()
    # # p.add_mesh(grid, scalars = 'Displacement')
    # # p.show()




    
    # rst_file = os.path.join(working_dir, jobname + '.rst')
    # simulation = post.load_simulation(rst_file)
    # simulation = post.StaticMechanicalSimulation(rst_file)

    # solution = post.load_solution(rst_file)
    # print('a', simulation.results)
    # print('b', solution)
    # mesh = simulation.mesh
    # print(mesh)

    # d = post.displacement.Displacement.x
    # d
    
    # displacement = simulation.displacement()    
    # print(displacement)

    # displacement1 = solution.displacement() 
    # uy = displacement1.y
    # u = uy.get_data_at_field()
    # print(u)
    # print(displacement1)


    # displacement.plot(screenshot = 'tt.png', off_screen = True)
    # st.image('tt.png')

    # # stress_z = simulation.nodal_force(components= "X")
    # stress_z = simulation.reaction_force(components= "X")
    # stress_z.plot(screenshot = 'tt1.png', off_screen = True)
    # st.image('tt1.png')
    # # st.pyplot(fig)


    # result = ma.result
analysis(In, 1)  # Load Case
analysis(In, 2)  # Load Case

import json
with open('result.json', 'w') as f:
    json.dump(results, f, indent=4)

# try:
#     analysis()
#     ma.exit()
# except Exception as e:  # Catch any exception.
#     print(f"###################### An error occurred: {e}")
#     a = f"###################### An error occurred: {e}"
#     a
#     # traceback.print_exc()
#     exc_type, exc_value, exc_traceback = sys.exc_info()
#     exc_type, exc_value, exc_traceback
#     ma.exit()


# pyVista 예시
# ver = ma.mesh.grid
# plotter = pv.Plotter(off_screen = True)    
# plotter.add_mesh(bra, color = 'magenta', line_width = 6, opacity = 1, label = 'Bracing')
# plotter.add_mesh(hor, color = 'blue', line_width = 6, opacity = 0.5, label = 'Horizontal')
# plotter.add_mesh(ver, color = 'green', line_width = 8, opacity = 1, label = 'Vertical')
# plotter.add_legend(bcolor = 'w', face = None, size = (0.15, 0.15), border = True)
# plotter.add_title('Modelling', font_size = 54, color = 'k')
# model_png = 'Images/model.png';  plotter.show(screenshot = model_png, window_size = (1920*2,1080*2), )    

# model_png = Image.open(model_png)    # img = img.resize((2000, 2000))
# st.write(h4, '[Modelling]')    
# st.image(model_png)  #, width = 1500