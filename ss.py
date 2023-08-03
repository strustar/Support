import streamlit as st
import numpy as np
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
        margin-top: 30px;
        margin-bottom: 0px;
        font-size: 22px;
        # line-height: 1.5;
        background-color: yellow;
        color: black;
        width: 520px;
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
    <br> ￭ 이메일 문의 환영 ((<a href="mailto:strustar@konyang.ac.kr">strustar@konyang.ac.kr</a>))
'''
txt1 ='''￭ 표 등이 겹쳐서 보일 때는 새로 고침을 해 주세요
    <br> ￭ Edge, Chrome 브라우저 등에서 실행
    <br> ￭ Light Mode, Dark Mode 둘 다 가능 (Light Mode 추천)
    <br> ￭ 브라우저 특성상 잘 안보일 수 있습니다. (Edge 브라우저 추천)
'''
[col1, col2] = st.columns([1.2,1])
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
h = h4;  tab = st.tabs([h+':blue[Ⅱ. 구조 검토 💻⭕]', h+':green[Ⅰ. 일반 사항 📝✍️]', h+':red[Ⅲ. 요약 ✅]', h+':orange[Ⅳ. 상세 해석 🎯 ]', h+':green[Ⅴ. 참고]'])
with tab[1]:
    # st.title(':red[작성중... (일반 사항 페이지 입니다.)]')
    [Wood, Joist, Yoke, Vertical, Horizontal, Bracing] = General.Tab(In, 'green')

with tab[0]:
    Calculate.Info(In, 'blue', Wood, Joist, Yoke, Vertical, Horizontal, Bracing)

with tab[2]:
    st.title(':red[작성중... (요약 페이지 입니다.)]')
with tab[3]:
    st.title(':red[작성중... (ANSYS 상용 프로그램을 이용한 3차원 상세 구조해석)]')


border2 = '<hr style="border-top: 2px solid ' + 'blue' + '; margin-top:30px; margin-bottom:30px; border-radius: 10px">'
st.markdown(border2, unsafe_allow_html=True)
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
