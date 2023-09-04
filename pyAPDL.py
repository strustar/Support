import streamlit as st
import numpy as np
from ansys.mapdl.core import launch_mapdl
# from ansys.dpf import post
import pyvista as pv
from PIL import Image
import sys
import os

class In:
    pass
In.joist_b = 50.0;  In.joist_h = 50;  In.joist_t = 2.3;  In.Lj = 150.0
In.yoke_b = 75;  In.yoke_h = 125;  In.yoke_t = 3.2;  In.Ly = 914
In.vertical_d = 60.5;  In.vertical_t = 2.6;  In.Lv = 914
In.horizontal_d = 42.7;  In.horizontal_t = 2.2;  In.Lh = 1725
In.bracing_d = 42.7;  In.bracing_t = 2.2

In.slab_X = 8;  In.slab_Y = 12;  In.height = 9.5  # Unit : m
In.dead_load = 10;  In.design_load = 12.5;  In.hx = 0.2;  In.hy = 0.2;  In.wind = 0.3  # kN/m2


h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
working_dir = 'Support_apdl';  jobname = working_dir;  mapdl = launch_mapdl(run_location = working_dir, jobname = jobname, override = True)

def analysis():
    mapdl.sys('del/q/f *.png')    # png 모든 파일 지우기
    mapdl.plopts('date','off')

    # !! ===============================================> Preprocessing 
    mapdl.clear();  mapdl.prep7();  factor = 1e3

    xea = int(np.ceil(In.slab_X*factor/In.Lv) + 1);  yea = int(np.ceil(In.slab_Y*factor/In.Ly) + 1);  zea = int(np.ceil(In.height*factor/In.Lh) + 1)
    xea,yea,zea

    mapdl.k(1, 0,0,0)
    mapdl.kgen(xea, 1,1,1, In.Lv,0,0, 1)
    mapdl.kgen(yea, 'all','','', 0,In.Ly,0, 100)
    mapdl.kgen(zea, 'all','','', 0,0,In.Lh, 10000)
    # mapdl.allsel()    

    for i in range(1, xea + 1):   # 수직재
        for j in range(1, yea + 1):
            for k in range(1, zea):
                mapdl.l(i + 100*(j-1) + 10000*(k-1), i + 10000 + 100*(j-1) + 10000*(k-1))    
    mapdl.allsel();  mapdl.cm('ver',  'line')

    for i in range(1, xea):   # 수평재 1
        for j in range(1, yea + 1):
            for k in range(1, zea):
                mapdl.l(i + 10000 + 100*(j-1) + 10000*(k-1), i + 10001 + 100*(j-1) + 10000*(k-1))
    for i in range(1, xea + 1):   # 수평재 2
        for j in range(1, yea):
            for k in range(1, zea):
                mapdl.l(i + 10000 + 100*(j-1) + 10000*(k-1), i + 10100 + 100*(j-1) + 10000*(k-1))
    mapdl.allsel();  mapdl.cmsel('u', 'ver');  mapdl.cm('hor',  'line')

    for i in range(1, xea, 2):   # 가새재
        for j in range(1, yea + 1, 2):
            for k in range(1, zea, 2):
                mapdl.l(i + 100*(j-1) + 10000*(k-1), i + 10001 + 100*(j-1) + 10000*(k-1))
    mapdl.allsel();  mapdl.cmsel('u', 'ver');  mapdl.cmsel('u', 'hor');  mapdl.cm('bra',  'line')
    mapdl.vup('', 'z')
    mapdl.view('', 1,-1,1)
    mapdl.allsel();  mapdl.nummrg('all')

    i = 1;  mapdl.et(i, 'beam188');  mapdl.mp('ex', i, 200e3);  mapdl.mp('prxy', i, 0.3)
    i = 2;  mapdl.et(i, 'beam188');  mapdl.mp('ex', i, 200e3);  mapdl.mp('prxy', i, 0.3)
    i = 3;  mapdl.et(i, 'beam188');  mapdl.mp('ex', i, 200e3);  mapdl.mp('prxy', i, 0.3)
    mapdl.sectype(1, 'beam', 'ctube');  mapdl.secdata(In.vertical_d/2 - In.vertical_t, In.vertical_d/2)
    mapdl.sectype(2, 'beam', 'ctube');  mapdl.secdata(In.horizontal_d/2 - In.horizontal_t, In.horizontal_d/2)
    mapdl.sectype(3, 'beam', 'ctube');  mapdl.secdata(In.bracing_d*0.99/2 - In.bracing_t, In.bracing_d*0.99/2)

    # mapdl.lplot(vtk=True)

    mapdl.cmsel('s', 'ver');  mapdl.latt(1,'',1,'','',1);  mapdl.lesize('all', 200);  mapdl.lmesh('all')
    ver = mapdl.mesh.grid    
    mapdl.cmsel('s', 'hor');  mapdl.latt(1,'',1,'','',2);  mapdl.lesize('all', 200);  mapdl.lmesh('all')
    hor = mapdl.mesh.grid
    mapdl.cmsel('s', 'bra');  mapdl.latt(1,'',1,'','',3);  mapdl.lesize('all', 200);  mapdl.lmesh('all')
    bra = mapdl.mesh.grid;  mesh = bra    

    mapdl.esel('s', 'sec', '', 1);  mapdl.cm('v', 'elem')
    mapdl.esel('s', 'sec', '', 2);  mapdl.cm('h', 'elem')
    mapdl.esel('s', 'sec', '', 3);  mapdl.cm('b', 'elem')
    # mapdl.lplot('all', show_line_numbering = False)    # mesh.plot()

    plotter = pv.Plotter(off_screen = True)
    # plotter = pv.Plotter(off_screen = False)
    plotter.add_mesh(bra, color = 'magenta', line_width = 6, opacity = 1, label = 'Bracing')
    plotter.add_mesh(hor, color = 'blue', line_width = 6, opacity = 0.5, label = 'Horizontal')
    plotter.add_mesh(ver, color = 'green', line_width = 8, opacity = 1, label = 'Vertical')
    plotter.add_legend(bcolor = 'w', face = None, size = (0.15, 0.15), border = True)
    # plotter.add_title('Modelling', font_size = 54, color = 'k')
    # model_png = 'Images/model.png';  plotter.show(screenshot = model_png, window_size = (1920*2,1080*2), )    
    
    # model_png = Image.open(model_png)    # img = img.resize((2000, 2000))
    # st.write(h4, '[Modelling]')    
    # st.image(model_png)  #, width = 1500
    mapdl.finish()
    # !! ===============================================> Preprocessing


    # !! ===============================================> Solution
    mapdl.run('/solu')
    mapdl.nsel('s', 'loc', 'z', 0)
    mapdl.d('all', 'all', 0)

    mapdl.allsel()
    mapdl.cmsel('s', 'v')
    mapdl.nsle('s')
    mapdl.nsel('r', 'loc', 'z', In.Lh*(zea - 1))    
    mapdl.f('all', 'fz', -1)
    mapdl.allsel()
    
    mapdl.pbc('f','',1)
    # mapdl.open_gui()
    output = mapdl.solve()    
    # output
    mapdl.finish()
    # !! ===============================================> Solution

    # !! ===============================================> Postprocessing
    mapdl.run('/post1')
    mapdl.set('last')
    mapdl.plnsol('u', 'sum')

    mapdl.etable('Fx1', 'SMISC', 1)
    mapdl.etable('Fx2', 'SMISC', 14)

    mapdl.cmsel('s', 'v')
    mapdl.show('png','REV')    
    mapdl.gfile(2400)
    mapdl.plls('Fx1', 'Fx2', 0.5, 0, 0) 
    mapdl.show('close')

    mapdl.cmsel('s', 'v')
    mapdl.esort('etab', 'Fx1')
    f = mapdl.get('Fx_max', 'sort','','min')
    'f', f
    



    # f = mapdl.get('f', 'elem', 3, 'smisc', '2')
    # f

    # result = mapdl.result
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


    mapdl.exit()
    sys.exit()


    
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


    # result = mapdl.result
    # plotter = pv.Plotter(off_screen=True)  # Modify this line
    # image_filename = 'plot.png'
    # _ = result.plot_principal_nodal_stress(
    #     0,
    #     "SEQV",
    #     cpos="xy",
    #     background="w",
    #     text_color="k",
    #     add_text=False,
    #     screenshot=image_filename  # Add this line
    # )
    # # Use Streamlit to display the image in a web page
    # st.image(image_filename)

try:
    analysis()
    mapdl.exit()
except Exception as e:  # Catch any exception.
    print(f"###################### An error occurred: {e}")
    a = f"###################### An error occurred: {e}"
    a
    # traceback.print_exc()
    exc_type, exc_value, exc_traceback = sys.exc_info()
    exc_type, exc_value, exc_traceback
    mapdl.exit()
