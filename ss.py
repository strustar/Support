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
h = '#### ';  tab = st.tabs([h+':green[Ⅰ. 일반 사항 ✍️]', h+':blue[Ⅱ. 구조 검토 💻]', h+':red[Ⅲ. 요약 ✅]', h+':orange[Ⅳ. 상세 해석 🎯 ]', h+':green[Ⅴ. 참고]'])
with tab[0]:
    # st.title(':red[작성중... (일반 사항 페이지 입니다.)]')
    [Wood, Joist, Yoke, Vertical, Horizontal, Bracing] = General.Tab(In)
with tab[1]:
    Calculate.Info(In, Wood, Joist, Yoke, Vertical, Horizontal, Bracing)
with tab[2]:
    st.title(':red[Ⅲ. 요약 ✅] (작성중....)')
with tab[3]:    
    st.title(':orange[Ⅳ. 상세 해석 🎯] (ANSYS 상용 프로그램을 이용한 3차원 상세 구조해석)')
    st.markdown(In.border2, unsafe_allow_html=True) ########### border ##########  #st.markdown('\n')
    
    h = '##### ';  tabtab = st.tabs([h+':orange[해석 결과]', h+':blue[해석 코드]'])
    with tabtab[0]:
        import os;  import json

        uz = [];  seqv = [];  Fx1 = [];  Fx2 = []
        My1 = [];  My2 = [];  Mz1 = [];  Mz2 = []
        SFz1 = [];  SFz2 = [];  SFy1 = [];  SFy2 = []
        with open('Images/result.json', 'r') as f:
            result = json.load(f)        
        for item in result:
            uz.append(np.abs(item['uz']));  seqv.append(np.abs(item['seqv']))
            Fx1.append(item['Fx1']/1e3);    Fx2.append(item['Fx2']/1e3)
            My1.append(item['My1']/1e6);    My2.append(item['My2']/1e6)
            Mz1.append(item['Mz1']/1e6);    Mz2.append(item['Mz2']/1e6)
            SFz1.append(item['SFz1']/1e3);  SFz2.append(item['SFz2']/1e3)
            SFy1.append(item['SFy1']/1e3);  SFy2.append(item['SFy2']/1e3)
            
        working_dir = 'Images';  jobname = 'file';  png = []
        for i in range(0,18):
            if i < 10:  name = os.path.join(working_dir, jobname + '00' + str(i) + '.png')
            if i >= 10: name = os.path.join(working_dir, jobname + '0' + str(i) + '.png')
            png.append(name)
        
        [col1, col2] = st.columns(In.col_span_ref)
        with col1:
            st.write(h4, '[해석 모델]')    
            st.image(png[0])
        with col2:
            st.write(h4, '[경계조건 및 하중조건]')    
            st.image(png[1])
        
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        [col1, col2] = st.columns(In.col_span_ref)        
        with col1:
            st.write(h4, '[Load Case 1 (LC1)]')
            st.write(h5, f':blue[[Displacement (u$_z$, 변위 (mm)]]')            
            st.write(s1, f'➣ 최대 변위 : {uz[0]:,.3f} mm')
            st.image(png[2])

            st.write(h5, f':blue[[von Mises Stress ($\sigma_{{eqv}}$, 등가응력 (MPa)]]')
            st.write(s1, f'➣ 최대 등가응력 : {seqv[0]:,.1f} MPa')
            st.image(png[3])
        with col2:
            st.write(h4, '[Load Case 2 (LC2) : 풍하중 고려]')
            st.write(h5, f':blue[[Displacement (u$_z$, 변위 (mm)]]')
            st.write(s1, f'➣ 최대 변위 : {uz[1]:,.3f} mm')
            st.image(png[2+9])

            st.write(h5, f':blue[[von Mises Stress ($\sigma_{{eqv}}$, 등가응력 (MPa)]]')
            st.write(s1, f'➣ 최대 등가응력 : {seqv[1]:,.1f} MPa')
            st.image(png[3+9])

        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        [col1, col2] = st.columns(In.col_span_ref)        
        with col1:
            st.write(h4, '[Load Case 1 (LC1)]')
            st.write(h5, f':blue[[Axial Force (F$_x$, 축방향력 (N)]]')            
            st.write(s1, f'➣ 최대 축방향력 : {Fx1[0]:,.3f} kN')
            st.write(s1, f'➣ 최소 축방향력 : {Fx2[0]:,.3f} kN')
            st.image(png[4])
            
            st.write(h5, f':blue[[Moment (M$_z$, 모멘트 (N·mm)]]')            
            st.write(s1, f'➣ 최대 모멘트 : {Mz1[0]:,.3f} kN·m')
            st.write(s1, f'➣ 최소 모멘트 : {Mz2[0]:,.3f} kN·m')
            st.image(png[5])

            st.write(h5, f':blue[[Moment (M$_y$, 모멘트 (N·mm)]]')
            st.write(s1, f'➣ 최대 모멘트 : {My1[0]:,.3f} kN·m')
            st.write(s1, f'➣ 최소 모멘트 : {My2[0]:,.3f} kN·m')
            st.image(png[6])

            st.write(h5, f':blue[[Shear Force (S$_z$, 전단력 (N)]]')
            st.write(s1, f'➣ 최대 전단력 : {SFz1[0]:,.3f} kN')
            st.write(s1, f'➣ 최소 전단력 : {SFz2[0]:,.3f} kN')
            st.image(png[7])

            st.write(h5, f':blue[[Shear Force (S$_y$, 전단력 (N)]]')
            st.write(s1, f'➣ 최대 전단력 : {SFy1[0]:,.3f} kN')
            st.write(s1, f'➣ 최소 전단력 : {SFy2[0]:,.3f} kN')
            st.image(png[8])

        with col2:
            st.write(h4, '[Load Case 2 (LC2) : 풍하중 고려]')
            st.write(h5, f':blue[[Axial Force (F$_x$, 축방향력 (N)]]')            
            st.write(s1, f'➣ 최대 축방향력 : {Fx1[1]:,.3f} kN')
            st.write(s1, f'➣ 최소 축방향력 : {Fx2[1]:,.3f} kN')
            st.image(png[4+9])

            st.write(h5, f':blue[[Moment (M$_z$, 모멘트 (N·mm)]]')            
            st.write(s1, f'➣ 최대 모멘트 : {Mz1[1]:,.3f} kN·m')
            st.write(s1, f'➣ 최소 모멘트 : {Mz2[1]:,.3f} kN·m')
            st.image(png[5+9])

            st.write(h5, f':blue[[Moment (M$_y$, 모멘트 (N·mm)]]')            
            st.write(s1, f'➣ 최대 모멘트 : {My1[1]:,.3f} kN·m')
            st.write(s1, f'➣ 최소 모멘트 : {My2[1]:,.3f} kN·m')
            st.image(png[6+9])

            st.write(h5, f':blue[[Shear Force (S$_z$, 전단력 (N)]]')
            st.write(s1, f'➣ 최대 전단력 : {SFz1[1]:,.3f} kN')
            st.write(s1, f'➣ 최소 전단력 : {SFz2[1]:,.3f} kN')
            st.image(png[7+9])

            st.write(h5, f':blue[[Shear Force (S$_y$, 전단력 (N)]]')
            st.write(s1, f'➣ 최대 전단력 : {SFy1[1]:,.3f} kN')
            st.write(s1, f'➣ 최소 전단력 : {SFy2[1]:,.3f} kN')
            st.image(png[8+9])

    with tabtab[1]:
        file_path = 'pyAPDL.py';  encoding = 'utf-8'    
        with open(file_path, 'r', encoding = encoding) as f:
            lines = f.readlines()
        code_string = ''.join(lines)
        st.code(code_string, line_numbers=True)
        

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
