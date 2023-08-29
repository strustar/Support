import streamlit as st
import numpy as np
import pandas as pd
import Sidebar, General, Calculate, Table, style
from Sidebar import In

### * -- Set page config
# emoji: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# https://zzsza.github.io/mlops/2021/02/07/python-streamlit-dashboard/  유용한 사이트
st.set_page_config(page_title = "System support 구조검토", page_icon = "🌈", layout = "centered",    # centered, wide
                    initial_sidebar_state="expanded",
                    # runOnSave = True,
                    menu_items = {        #   initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
                        # 'Get Help': 'https://www.extremelycoolapp.com/help',
                        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
                        # 'About': "# This is a header. This is an *extremely* cool app!"
                    })
### * -- Set page config

css_intro = """
<style>
    .boxed {
        border: 3px solid blue;
        border-radius: 100px;
        padding: 20px;
        padding-left: 30px;
        margin: 20px;
        margin-left: -30px;
        margin-right: 0px;
        margin-top: 30px;
        margin-bottom: 0px;
        font-size: 22px;
        # line-height: 1.5;
        background-color: yellow;
        color: black;
        width: 515px;
        # height: 100px;
    }
    .small {
        color: green;
        padding: 10px;
        font-size: 16px;
        display: inline-block;
        # text-decoration: underline;
        # line-height: 1.2;
    }
</style>
"""
txt =''' ￭ 계속해서 실시간 업데이트 되고 있습니다.
    <br> ￭ 궁금한 사항은 이메일로 문의 해 주세요 (건양대 손병직)
    <br> ￭ 이메일 문의 환영 (<a href="mailto:strustar@konyang.ac.kr">strustar@konyang.ac.kr</a>)
'''
txt1 ='''￭ 표 등이 겹쳐서 보일 때는 새로 고침을 해 주세요
    <br> ￭ Edge, Chrome 브라우저 등에서 실행
    <br> ￭ Light Mode, Dark Mode 둘 다 가능 (Light Mode 추천)
    <br> ￭ 브라우저 특성상 잘 안보일 수 있습니다. (Edge 브라우저 추천)
'''
[col1, col2] = st.columns([1.15,1])
st.markdown(css_intro, unsafe_allow_html=True)
with col1:
    st.markdown(f'<div class="boxed"> [가칭] 동바리 설계 자동화 프로그램 (초안)<br><span class="small">{txt}</span></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="boxed"> ✦ 프로그램 사용 유의사항<br><span class="small">{txt1}</span></div>', unsafe_allow_html=True)


# 메인바 윗쪽 여백 줄이기 & 텍스트, 숫자 상자 스타일,  # Adding custom style with font
css = f""" <style>
    .block-container {{
        margin-top: 20px;
        padding-top: 0px;
        max-width: 1000px !important;
    }}
    .element-container {{
            white-space: nowrap;            
            overflow-x: visible;            
            }}
    input[type="text"] {{
        padding: 6px;
        padding-left: 15px;
        background-color: {In.background_color};
        font-size: {In.font_h5};
        font-weight: bold !important;
        border: 1px solid black !important;
        border-radius: 100px;
    }}
    
    input[type="number"] {{
        padding: 5px;
        padding-left: 15px;
        # color: blue;
        background-color: {In.background_color};
        font-size: {In.font_h5};
        font-weight: bold !important;
        border: 1px solid black !important;
        border-radius: 100px;
        # width: 100%
    }}
    # input[type="number"]::-ms-clear {{
    #     display: none; /* 숫자 입력창 오른쪽에 있는 지우기(x) 버튼을 숨깁니다 */
    # }}
    [data-testid=stSidebar] {{
        background-color: whitesmoke !important;
        /* border: 3px dashed lightblue !important; */
        font-weight: bold !important;        
        padding: 5px !important;
        margin-top: -100px !important;        
        padding-bottom: 100px !important;
        height: 110% !important;
        # max-width: 600px !important;  /* 사이드바의 최대 크기를 조절합니다 */
        width: 100% !important;  /* 이렇게 하면 사이드 바 폭을 고정할수 있음. */
    }}
        /* CSS to set font for everything except code blocks */
        body, h1, h2, h3, h4, h5, h6, p, blockquote {{
            font-family: 'Nanum Gothic', sans-serif; font-weight: bold !important; font-size: 16px !important;}}

        /* Font size for titles (h1 to h6) */
        h1 {{font-size: {In.font_h1} !important;}}
        h2 {{font-size: {In.font_h2} !important;}}
        h3 {{font-size: {In.font_h3} !important;}}
        h4 {{font-size: {In.font_h4} !important;}}
        h5 {{font-size: {In.font_h5} !important;}}
        h6 {{font-size: {In.font_h6} !important;}}
</style> """
st.markdown(css, unsafe_allow_html=True)

# 왼쪽 사이드바 인쇄하지 않기 설정
st.markdown("""
<style>
@media print {
    [data-testid=stSidebar] {
        display: none;
    }
}
</style>
""", unsafe_allow_html=True)

# 모든 글씨 및 라텍스 수식 진하게 설정
st.markdown('''
<style>
    .main * {
        # font-size: 26pt !important;
        font-weight: bold !important;
        # font-family: Arial !important;            
    }
    # .mjx-chtml {
    #     font-size: 36pt !important;
    # }
</style>
''', unsafe_allow_html=True)

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'  #s12 = '$\enspace$'  공백 : \,\:\;  # ⁰¹²³⁴⁵⁶⁷⁸⁹  ₀₁₂₃₄₅₆₇₈₉

style.radio(In.background_color, '32%')
st.sidebar.write(h2, ':blue[[Information : 입력값 📘]]')
In = Sidebar.Sidebar(h4, h5)
##### tab ===========================================================================================================
h = '#### ';  tab = st.tabs([h+':blue[Ⅱ. 구조 검토 💻]', h+':green[Ⅰ. 일반 사항 ✍️]', h+':red[Ⅲ. 요약 ✅]', h+':orange[Ⅳ. 상세 해석 🎯 ]', h+':green[Ⅴ. 참고]'])
with tab[2]:
    # st.title(':red[작성중... (일반 사항 페이지 입니다.)]')
    [Wood, Joist, Yoke, Vertical, Horizontal, Bracing] = General.Tab(In)
with tab[1]:
    Calculate.Info(In, Wood, Joist, Yoke, Vertical, Horizontal, Bracing)
with tab[2]:
    st.title(':red[Ⅲ. 요약 ✅] (작성중....)')
with tab[0]:
    import os
    st.title(':orange[Ⅳ. 상세 해석 🎯] (ANSYS 상용 프로그램을 이용한 3차원 상세 구조해석, 작성중...)')


    # file_path = 'Analysis/Support.inp';  encoding = 'utf-8'
    # with open(file_path, 'r', encoding = encoding) as f:
    #     lines = f.readlines()
        
    # for i in range(20):  # 앞에만 검색해서 변경
    #     if "joist" in lines[i]:
    #         lines[i] = f'joist_b = {In.joist_b}  $  joist_h = 50  $  joist_t = 2.3  $  Lj = {In.Lj}\n'
    #         # break    
    # # with open(file_path, "w", encoding = encoding) as f:
    # #     f.writelines(lines)

    # st.write(h3, '[Modelling]')
    # st.image('Analysis/tt000.bmp', width=1000)
    # remote_image_url = "https://raw.githubusercontent.com/strustar/Support/main/Analysis/tt000.png"
    # st.image(remote_image_url, width=1000)

    # st.image('https://github.com/strustar/Support/main/Analysis/joist.png', width=1000)

with tab[4]:
    st.title(':green[Ⅴ. 참고] (참고사항, 작성중....)')
# if 'Ⅰ' in In.select:
#     [Wood, Joist, Yoke, Vertical, Horizontal, Bracing] = General.Tab(In, 'green')
# if 'Ⅱ' in In.select:
#     from General import Wood, Joist, Yoke, Vertical, Horizontal, Bracing
#     Calculate.Info(In, 'blue', Wood, Joist, Yoke, Vertical, Horizontal, Bracing)
# if 'Ⅲ' in In.select:
#     st.title(':red[작성중... (요약 페이지 입니다.)]')
# if 'Ⅳ' in In.select:
#     st.title(':red[작성중... (ANSYS 상용 프로그램을 이용한 3차원 상세 구조해석)]')
# if 'Ⅴ' in In.select:
#     st.title(':red[작성중... (참고 사항)]')

from ansys.mapdl.core import launch_mapdl
import pyvista as pv
from PIL import Image

working_dir = 'pymapdl';  jobname = 'Support_apdl';  mapdl = launch_mapdl(run_location = working_dir, jobname = jobname, override = True)

def analysis():
    working_dir = 'pymapdl';  jobname = 'Support_apdl'
    # !! ===============================================> Preprocessing    
    mapdl.clear();  mapdl.prep7();  factor = 1e3

    xea = int(np.ceil(In.slab_X*factor/In.Lv) + 1);  yea = int(np.ceil(In.slab_Y*factor/In.Ly) + 1);  zea = int(np.ceil(In.height*factor/In.Lh) + 1)

    mapdl.k(1, 0,0,0)
    mapdl.kgen(xea, 1,1,1, In.Lv,0,0, 1)
    mapdl.kgen(yea, 'all','','', 0,In.Ly,0, 100)
    mapdl.kgen(zea, 'all','','', 0,0,In.Lh, 10000)
    # mapdl.allsel()
    # xea,yea,zea

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

    mapdl.et(1, 'beam188');  mapdl.mp('ex', 1, 200e3);  mapdl.mp('prxy', 1, 0.3)
    mapdl.sectype(1, 'beam', 'ctube');  mapdl.secdata(In.vertical_d/2 - In.vertical_t, In.vertical_d/2)
    mapdl.sectype(2, 'beam', 'ctube');  mapdl.secdata(In.horizontal_d/2 - In.horizontal_t, In.horizontal_d/2)
    mapdl.sectype(3, 'beam', 'ctube');  mapdl.secdata(In.bracing_d/2 - In.bracing_t, In.bracing_d/2)

    mapdl.cmsel('s', 'ver');  mapdl.latt(1,'',1,'','',1);  mapdl.lesize('all', 200);  mapdl.lmesh('all')
    ver = mapdl.mesh.grid    
    mapdl.cmsel('s', 'hor');  mapdl.latt(1,'',1,'','',2);  mapdl.lesize('all', 200);  mapdl.lmesh('all')
    hor = mapdl.mesh.grid
    mapdl.cmsel('s', 'bra');  mapdl.latt(1,'',1,'','',3);  mapdl.lesize('all', 200);  mapdl.lmesh('all')
    bra = mapdl.mesh.grid;  mesh = bra
    mapdl.allsel();  mapdl.nummrg('all')

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
    model_png = 'Images/model.png';  plotter.show(screenshot = model_png, window_size = (1920*2,1080*2), )    
    
    model_png = Image.open(model_png)    # img = img.resize((2000, 2000))
    st.write(h4, '[Modelling]')    
    st.image(model_png)  #, width = 1500
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
    output = mapdl.solve()
    # output
    mapdl.finish()
    # !! ===============================================> Solution

    # !! ===============================================> Postprocessing
    mapdl.run('/post1')
    mapdl.set('last')
    mapdl.plnsol('u', 'sum')

    from ansys.dpf import post
    from ansys.dpf.post import examples

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
    mapdl.exit()


# # Create a simple sphere
# sphere = pv.Sphere()

# # Plot and save an image file
# plotter = pv.Plotter(off_screen=True)
# plotter.add_mesh(sphere)
# plotter.show(screenshot='Images\screenshot.png')

# # Display the image using streamlit
# img = Image.open('Images\screenshot.png')
# # img = img.resize((500,500))
# st.image(img)


# import streamlit as st

# from PIL import Image


# # Define an element type
# mapdl.et(1, 'SOLID186')

# # Define a material type
# mapdl.mp('EX', 1, 210E9) # Young's modulus
# mapdl.mp('DENS', 1, 7800) # Density
# mapdl.mp('NUXY', 1, 0.3) # Poisson's ratio

# # Create a block
# vnum = mapdl.blc4(width=1, height=4, depth=9)

# # Mesh the block
# mapdl.esize(0.5)
# mapdl.vmesh(vnum)

# # Check the number of elements
# num_elem = mapdl.mesh.n_elem
# st.write(f"Number of elements: {num_elem}")

# # Convert the mesh to VTK format for visualization with pyvista
# mesh = mapdl.mesh._grid  # get the VTK grid
# # vnum
# # mesh

# if mesh is None:
#     st.write("Failed to visualize the volume.")
# else:
#     # Use pyvista's plotter to visualize the volume and save screenshot.
#     p = pv.Plotter(off_screen=True)
#     p.add_lines(mesh)
#     p.show(screenshot='mesh.png')

#     # Load the image with PIL and display it with Streamlit.
#     image = Image.open('mesh.png')
#     st.image(image)



    
# mapdl.vplot(show_lines=True, show_bounds=True)

st.markdown(In.border2, unsafe_allow_html=True)
# ============================================================================================================================================
st.write('Example (아래는 나중에 참조할 사항)')


text = 'Hello Streamlit!'
latex_formula = r'\(E = mc^2\)'  # Example LaTeX formula
html_code = f"""
<!DOCTYPE html>
<html>
    <head>
        <style>
            .container {{
                background-color: yellow;
                font-family: Arial, sans-serif;
                font-weight: bold;
                padding: 5px 20px;
                border: 3px solid green;
                border-radius: 100px;
                display: inline-block;
                margin: 20px;
                width: 550px
            }}
        </style>
        <!-- Adding MathJax library to enable rendering LaTeX -->
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
        </script>
    </head>

    <body>
        <div class="container">
            <h2>{text}</h2>
            <p>Welcome to the world of custom HTML content in Streamlit apps.</p>
            <p>LaTeX formula: {latex_formula}</p>  <!-- Adding LaTeX formula -->
        </div>
    </body>
</html>"""
st.components.v1.html(html_code, width=650, height=200)



# import streamlit as st
# import pandas as pd
# # from tabulate import tabulate

# # 샘플 데이터 프레임 선언
# data = {r"$\pi\beta$": ["$e^{i \pi} + 1 = 0$", "This is an example text"],
#         "Column2": [r'$\bm{{\quad M = \large{{\frac{{{0}\textcolor{{red}}{{{1}}}^2}}{{8}}}} \normalsize \leq f_{{ba}}\,S}} $'.format('w_w', 'tt'), r"$\frac{\partial f}{\partial x}$"]}
# df = pd.DataFrame(data)

# # 상단에 DataFrame을 택스트로 표시합니다
# st.markdown(df.to_markdown(), unsafe_allow_html=True)
# # st.write(df.style.set_properties(**{'font-weight': 'bold', 'font-size': '28px'}))
