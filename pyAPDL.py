import streamlit as st
import numpy as np
from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core import convert_script
# from ansys.dpf import post
from PIL import Image
import pyvista as pv
import sys
import os

class In:
    pass
In.joist_b = 50.0;  In.joist_h = 50;  In.joist_t = 2.3;  In.Lj = 150.0  # Unit : N, mm
In.yoke_b = 75;  In.yoke_h = 125;  In.yoke_t = 3.2;  In.Ly = 914
In.vertical_d = 60.5;  In.vertical_t = 2.6;  In.Lv = 914
In.horizontal_d = 42.7;  In.horizontal_t = 2.2;  In.Lh = 1725
In.bracing_d = 42.7;  In.bracing_t = 2.2

In.slab_X = 8;  In.slab_Y = 12;  In.height = 9.5  # Unit : m
In.dead_load = 10;  In.design_load = 12.5;  In.hx = 0.2;  In.hy = 0.2;  In.wind = 0.3  # kN/m2

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '

factor = 1e3
LC = 1 # Load Case
if LC == 1:
    ver = In.design_load;  horx = In.hx;  hory = In.hy
if LC == 2:  # 풍하중
    ver = In.dead_load;  horx = In.wind;  hory = In.wind
P = ver*In.Ly*In.Lv/factor  # kN/m2 = 1e3 N/(mm*mm*1e6) *mm*mm = N / 1e3
Hx = horx*In.Ly*In.Lh/factor
Hy = hory*In.Lv*In.Lh/factor

working_dir = 'pyAPDL';  jobname = 'file'
ma = launch_mapdl(run_location = working_dir, jobname = jobname, override = True)

def analysis():
    ma.sys('del/q/f *.png')    # png 모든 파일 지우기
    ma.plopts('date','off')    # 날짜 지우기
    ma.vscale('','',1)  # 하중 재하시 화살표 크기 동일하게 (작은 것은 안보이는 현상 발생)

    # Reverse Video - white
    ma.rgb('INDEX',100,100,100, 0)
    ma.rgb('INDEX',80,80,80, 13)
    ma.rgb('INDEX',60,60,60, 14)
    ma.rgb('INDEX',0,0,0, 15)

    # !! ===============================================> Preprocessing 
    ma.clear();  ma.prep7()

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

    for i in range(1, xea):   # 수평재 1
        for j in range(1, yea + 1):
            for k in range(1, zea):
                ma.l(i + 10000 + 100*(j-1) + 10000*(k-1), i + 10001 + 100*(j-1) + 10000*(k-1))
    for i in range(1, xea + 1):   # 수평재 2
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

    i = 1;  ma.et(i, 'beam188');  ma.mp('ex', i, 200e3);  ma.mp('prxy', i, 0.3)
    i = 2;  ma.et(i, 'beam188');  ma.mp('ex', i, 200e3);  ma.mp('prxy', i, 0.3)
    i = 3;  ma.et(i, 'beam188');  ma.mp('ex', i, 200e3);  ma.mp('prxy', i, 0.3)
    ma.sectype(1, 'beam', 'ctube');  ma.secdata(In.vertical_d/2 - In.vertical_t, In.vertical_d/2)
    ma.sectype(2, 'beam', 'ctube');  ma.secdata(In.horizontal_d/2 - In.horizontal_t, In.horizontal_d/2)
    ma.sectype(3, 'beam', 'ctube');  ma.secdata(In.bracing_d*0.99/2 - In.bracing_t, In.bracing_d*0.99/2)    

    ma.cmsel('s', 'ver');  ma.latt(1,'',1,'','',1);  ma.lesize('all', 200);  ma.lmesh('all')    
    ma.cmsel('s', 'hor');  ma.latt(1,'',1,'','',2);  ma.lesize('all', 200);  ma.lmesh('all')    
    ma.cmsel('s', 'bra');  ma.latt(1,'',1,'','',3);  ma.lesize('all', 200);  ma.lmesh('all')    

    ma.esel('s', 'sec', '', 1);  ma.cm('v', 'elem');  ma.color('elem', 'magenta')
    ma.esel('s', 'sec', '', 2);  ma.cm('h', 'elem');  ma.color('elem', 'cyan')
    ma.esel('s', 'sec', '', 3);  ma.cm('b', 'elem');  ma.color('elem', 'blue')
    # ma.lplot('all', show_line_numbering = False)    # mesh.plot()
    
    ma.cmsel('all')
    ma.allsel('all')
    ma.eshape(3)
    ma.replot()    
    
    # savefig = 'pyAPDL\ss.png'
    savefig = 'ss.png'
    ma.cmsel('all')
    ma.eshape(3)
    # ma.eplot(vtk=False, background='k', show_edges=False, smooth_shading=True, color = 'blue', edge_color='red',
    #             window_size=[1920, 1080], savefig=savefig, style='surface', render_lines_as_tubes=True, line_width=5,
    #             off_screen=True)
    ma.eplot(vtk=False, off_screen=True)
    
    st.image('pyAPDL/file000.png')

    # ma.allsel('all')
    # ma.show('png')
    # # ma.pngr('orient', 'horiz')
    # ma.gfile(2400)
    # ma.replot()
    # ma.eshape(1)
    # # ma.plls('Fx1', 'Fx2', 0.5, 0, 0) 
    # ma.show('close')


    ma.exit()
    sys.exit()

    ma.finish()
    # !! ===============================================> Preprocessing


    # !! ===============================================> Solution
    ma.run('/solu')
    ma.nsel('s', 'loc', 'z', 0)
    ma.d('all', 'all', 0)

    ma.allsel()
    ma.cmsel('s', 'v')
    ma.nsle('s')
    ma.nsel('r', 'loc', 'z', In.Lh*(zea - 1))    
    ma.f('all', 'fz', -1)
    ma.allsel()
    
    ma.pbc('f','',1)
    # ma.open_gui()
    output = ma.solve()    
    # output
    ma.finish()
    # !! ===============================================> Solution

    # !! ===============================================> Postprocessing
    ma.run('/post1')
    ma.set('last')
    ma.plnsol('u', 'sum')

    ma.etable('Fx1', 'SMISC', 1)
    ma.etable('Fx2', 'SMISC', 14)

    ma.cmsel('s', 'v')
    ma.show('png','REV')    
    ma.gfile(2400)
    ma.plls('Fx1', 'Fx2', 0.5, 0, 0) 
    ma.show('close')

    ma.cmsel('s', 'v')
    ma.esort('etab', 'Fx1')
    f = ma.get('Fx_max', 'sort','','min')
    'f', f
    



    # f = ma.get('f', 'elem', 3, 'smisc', '2')
    # f

    # result = ma.result
    # nnum, disp = result.nodal_displacement(0)
    # nnum, disp

    # # Create a structured grid (replace this with your actual mesh)
    # # grid = pv.StructuredGrid()
    # grid = result.mesh._grid

    # # Add displacement data to the grid
    # grid.point_array["Displacement"] = disp

    # p = pv.Plotter()
    # p.add_mesh(grid, scalars = 'Displacement')
    # p.show()




    
    rst_file = os.path.join(working_dir, jobname + '.rst')
    simulation = post.load_simulation(rst_file)
    simulation = post.StaticMechanicalSimulation(rst_file)

    solution = post.load_solution(rst_file)
    print('a', simulation.results)
    print('b', solution)
    mesh = simulation.mesh
    print(mesh)

    d = post.displacement.Displacement.x
    d
    
    displacement = simulation.displacement()    
    print(displacement)

    displacement1 = solution.displacement() 
    uy = displacement1.y
    u = uy.get_data_at_field()
    print(u)
    print(displacement1)


    displacement.plot(screenshot = 'tt.png', off_screen = True)
    st.image('tt.png')

    # stress_z = simulation.nodal_force(components= "X")
    stress_z = simulation.reaction_force(components= "X")
    stress_z.plot(screenshot = 'tt1.png', off_screen = True)
    st.image('tt1.png')
    # st.pyplot(fig)


    # result = ma.result
analysis()
ma.exit()

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