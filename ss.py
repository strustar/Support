import streamlit as st
import numpy as np
import pandas as pd
import Sidebar, General, Calculate, Cover, style, Detail, Summary
from General import Wood, Joist, Yoke, Vertical, Horizontal, Bracing
from Sidebar import In

import os
os.system('cls')  # 터미널 창 청소, clear screen
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
        max-width: 600px !important;  /* 사이드바의 최대 크기를 조절합니다 */
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

# 왼쪽 사이드바 인쇄하지 않기 설정 등
st.markdown("""
<style>
@media print {
    [data-testid=stSidebar] {
        display: none;
    }
    header, footer, .no-print {display:none}
    @page {
        size: A4;
        margin-left: 50px;
    }
    body {
        width: 100%; /* 전체 너비 사용 */
    }
    @page :first {
        page-number: 0;
    }
    @page {
        counter-increment: page;
    }
    .page:after {
        content: counter(page);
    }
    # .print{zoom: 78%}   # 동작이 안됨 ??
    # body {   # 동작이 안됨 ??
    #     font-size: 24px;
    #     color: blue;
    #     background-dolor: red;
    # }
}
</style>
""", unsafe_allow_html=True)

# 페이지 간 구분을 위한 CSS 스타일 정의
page_break_style = """
<style>
.page-break {
    page-break-before: always;
}
</style>
"""
st.markdown(page_break_style, unsafe_allow_html=True)


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
In = Sidebar.Sidebar(h4, h5)

# def Report():
if ('보고서' in In.select) or ('표지' in In.select):
    Cover.Contents()
    st.write('');  st.write('');  st.write('')
if ('보고서' in In.select) or ('일반 사항' in In.select):
    [Wood, Joist, Yoke, Vertical, Horizontal, Bracing] = General.Tab(In)
    st.write('');  st.write('');  st.write('')
if ('보고서' in In.select) or ('구조 검토' in In.select):
    Calculate.Info(In, Wood, Joist, Yoke, Vertical, Horizontal, Bracing)
    st.write('');  st.write('');  st.write('')
if ('보고서' in In.select) or ('상세' in In.select):
    Detail.Analysis(In, h4, h5, s1, s2, 'result', Vertical, Horizontal, Bracing)   # opt : both, result, code
    st.write('');  st.write('');  st.write('')
if ('보고서' in In.select) or ('결과' in In.select):
    Summary.Info(In)
    st.write('');  st.write('');  st.write('')
if '부 록' in In.select:
    Detail.Analysis(In, h4, h5, s1, s2, 'code', '', '', '')   # opt : both, result, code

# ##### tab ==========================================================================================
# if __name__ == "streamlit.script_runner":    # 스트림릿 웹상
#     h = '#### ';  tab = st.tabs([h+':green[Ⅰ. 일반 사항 ✍️]', h+':blue[Ⅱ. 구조 검토 💻]', h+':orange[Ⅲ. 상세 구조해석 🎯]', h+':green[Ⅳ. 검토 결과 ✅]', h+':blue[⭕ 보고서]'])
#     with tab[0]:    
#         [Wood, Joist, Yoke, Vertical, Horizontal, Bracing] = General.Tab(In)
        
#     with tab[1]:
#         Calculate.Info(In, Wood, Joist, Yoke, Vertical, Horizontal, Bracing)
        
#     with tab[2]:
#         Detail.Analysis(In, h4, h5, s1, s2, 'both', Vertical, Horizontal, Bracing)   # opt : both, result, code

#     with tab[3]:
#         st.title(':green[Ⅳ. 검토 결과 ✅]')
        
#     with tab[4]:  # 보고서
#         Report()
# else:    # 보고서 작성용
#     Report()


# st.title(':green[Ⅴ. 참고] (참고사항, 작성중....)')
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


# st.markdown(In.border2, unsafe_allow_html=True)
# # ============================================================================================================================================
# st.write('Example (아래는 나중에 참조할 사항)')


# text = 'Hello Streamlit!'
# latex_formula = r'\(E = mc^2\)'  # Example LaTeX formula
# html_code = f"""
# <!DOCTYPE html>
# <html>
#     <head>
#         <style>
#             .container {{
#                 background-color: yellow;
#                 font-family: Arial, sans-serif;
#                 font-weight: bold;
#                 padding: 5px 20px;
#                 border: 3px solid green;
#                 border-radius: 100px;
#                 display: inline-block;
#                 margin: 20px;
#                 width: 550px
#             }}
#         </style>
#         <!-- Adding MathJax library to enable rendering LaTeX -->
#         <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
#         <script id="MathJax-script" async
#             src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
#         </script>
#     </head>

#     <body>
#         <div class="container">
#             <h2>{text}</h2>
#             <p>Welcome to the world of custom HTML content in Streamlit apps.</p>
#             <p>LaTeX formula: {latex_formula}</p>  <!-- Adding LaTeX formula -->
#         </div>
#     </body>
# </html>"""
# st.components.v1.html(html_code, width=650, height=200)

