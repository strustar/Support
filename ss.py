# import openpyxl as ox
# import xlwings as xw
import streamlit as st
import numpy as np
import sidebar, tab0, tab1, table

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

# 줄바꿈 처리 & 모든 텍스트 진하게
st.markdown("""
    <style>
        .element-container {
            white-space: nowrap;
            overflow-x: visible;}
        h1, h2, h3, h4, h5, h6, p, span, stTextInput > div > div > input {
        font-weight: bold !important;}
    </style>
    """, unsafe_allow_html=True)

# 스타일 정의 및 적용
st.markdown("""
    <style>
        .element-container {
            white-space: nowrap;
            overflow-x: visible;}
        h1, h2, h3, h4, h5, h6, p, span, stTextInput > div > div > input {
        font-weight: bold !important;}

        .sidebar .css-17eq0hr {
            background-color: blue;}
        .css-17eq0hr h1, .css-17eq0hr h2, .css-17eq0hr h3, .css-17eq0hr h4, .css-17eq0hr h5, .css-17eq0hr h6, .css-17eq0hr p, .css-17eq0hr span {
            color: red !important;}
    </style>
    """, unsafe_allow_html=True)

# Adding custom style with font
fn1 = 'Nanum Gothic';  fn2 = 'Gungsuhche';  fn3 = 'Lora';  fn4 = 'Noto Sans KR'
font_style = """
    <style>
        /* CSS to set font for everything except code blocks */
        body, h1, h2, h3, h4, h5, h6, p, blockquote {font-family: 'Nanum Gothic', sans-serif !important;}
        font-weight: bold !important;
        /* CSS to set font for code blocks */
        .highlight pre, .highlight tt, pre, tt {font-family: 'Courier New', Courier, monospace;}

        /* Font size for titles (h1 to h6) */
        h1 {font-size: 32px;}
        h2 {font-size: 28px;}
        h3 {font-size: 24px;}
        h4 {font-size: 20px;}
        h5 {font-size: 16px;}
        h6 {font-size: 14px;}
        /* Font size for body text */
        body {font-size: 16px;}
    </style>
"""
st.markdown(font_style, unsafe_allow_html=True)

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5+'$\quad$';  s2 = h5+'$\qquad$';  s3 = h5+'$\quad \qquad$'  #s12 = '$\enspace$'  공백 : \,\:\;  # ⁰¹²³⁴⁵⁶⁷⁸⁹  ₀₁₂₃₄₅₆₇₈₉

st.sidebar.title(':blue[[Information : 입력값]]')
In = sidebar.Sidebar(h2, h4)
##### tab ===========================================================================================================
tab = st.tabs([h4+':blue[Ⅱ. 단면제원 검토 💻⭕]', h4+':green[Ⅰ. 설계조건 📝✍️]', h4+':orange[Ⅲ. 시스템 서포터 검토 🏛️🏗️]', h4+':green[Ⅳ. 구조검토 결과 🎯✅ ]' ])
with tab[1]:
    [Wood, Joist, Yoke] = tab0.Tab(In, 'green', fn1, s1, s2, s3, h4, h5)    

with tab[0]:
    [t_load, Lj, Ly, Ls] = tab1.Tab(In, 'blue', fn1, s1, s2, s3, h4, h5, Wood, Joist, Yoke)

    st.write(h4, '5. 동바리 (수직재) 검토')
    KL = In.KL;  Fy = In.sp_fy
    style = '동바리';  section = f'𝜙{In.sp_d:,.1f}×{In.sp_t:,.1f}t'
    t = In.sp_t;  d = In.sp_d;  d1 = d - 2*t
    A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  r = np.sqrt(I/A);  E = 200.e3    
    table.Info(fn1, style, section, A, I, r, E, Fy, -1, 20)
    
    st.write(s1, '1) 1본당 작용하중 (P)')
    st.write(s2, '➣ P = 설계 하중 x 멍에 간격 x 동바리 간격');  P = t_load*Ly*Ls
    st.write(s2, f'➣ P = {t_load:.4f} N/mm² x {Ly:,.1f} mm x {Ls:,.1f} mm = {P/1e3:,.1f} kN/EA')

    st.write(s1, '2) 허용압축응력 (${F_{ca}}$) 산정' + '$\qquad$ :orange[ <근거 : 4.4.3 허용압축응력 (KDS 14 30 10 : 2019)>]')
    st.write(s2, f'➣ 유효 좌굴길이 : KL = {KL:,.1f} mm' + '$\qquad$ :orange[ <근거 : 4.4.2 좌굴길이와 세장비 (KDS 14 30 10 : 2019)>]')
    num_str = rf'$\large\frac{{{KL:,.1f}}}{{{r:,.1f}}}$ = ';  lamda = KL/r
    okng = '$\: \leq \:$ 200 (최대 세장비) $\qquad$ :blue[OK]' if lamda <= 200 else '$\: \geq \:$ 200 (최대 세장비) $\qquad$ :red[NG]'
    st.write(s2, rf'➣ 세장비 : $\lambda = \Large{{\frac{{KL}}{{r}}}}$ = ' + num_str + f'{lamda:,.1f}', okng)
    num_str = rf'$\large\sqrt{{\frac{{2 \pi^2 \times {E:,.0f}}}{{{Fy:,.1f}}}}}$ = ';  Cc = np.sqrt(2*np.pi**2*E/Fy)
    st.write(s2, rf'➣ 한계 세장비 : $C_c = \Large\sqrt{{\frac{{2 \pi^2 E}}{{F_y}}}}$ = ' + num_str + f'{Cc:,.1f}')

    if lamda <= Cc:
        a = (1 - lamda**2/(2*Cc**2)) *Fy;  b = 5/3 + 3*lamda/(8*Cc) - lamda**3/(8*Cc**3)
        Fca = a/b
        st.write(s2, rf'➣ ${{KL/r \: \leq \: C_c}}$' + '이므로 : ' + rf'$F_{{ca}} = {{\Large{{\frac{{\left[1 - \frac{{(KL/r)^2}}{{2 C_c^2}}\right] F_y}} {{\frac{{5}}{{3}} + \frac{{3 (KL/r)}}{{8 C_c}} - \frac{{(KL/r)^3}}{{8 C_c^3}} }}  }}}} \normalsize = $' + f'{Fca:,.1f} MPa')
    else:
        Fca = 12*np.pi**2 *E/(23*lamda**2)
        st.write(s2, rf'➣ ${{KL/r \: \geq \: C_c}}$' + '이므로 : ' + rf'$F_{{ca}} = {{\Large{{\frac{{12 \pi^2 E}}{{23 (KL/r)^2}} }}  }} \normalsize = $' + f'{Fca:,.1f} MPa')
    
    st.write(s1, '3) 허용 하중 및 안전율 검토' + '$\qquad$ :orange[ <근거 : 1.8 안전율 (KDS 21 50 00 : 2022)>]')
    Pa = Fca*A;  SF = Pa/P
    st.write(s2, rf'➣ 허용 하중 : $P_a = F_{{ca}} \times A$ = {Fca:,.1f} MPa x {A:,.1f} mm² = {Pa/1e3:,.1f} kN')
    okng = '$\: \geq \:$ 2.5 (안전율*) $\qquad$ :blue[OK]' if SF >= 2.5 else '$\: \leq \:$ 2.5 (안전율*) $\qquad$ :red[NG]'
    st.write(s2, rf'➣ 안전율 : $S.F = \Large\frac{{P_a}}{{P}} \normalsize = \large\frac{{ {Pa/1e3:,.1f} }}{{ {P/1e3:,.1f} }} \normalsize = \: $' + f'{SF:.1f}', okng)
    st.write('###### $\quad \qquad$', '*단품 동바리 안전율 3.0, 조립식 동바리 안전율 2.5적용')

    border2 = '<hr style="border-top: 2px solid ' + 'blue' + '; margin-top:30px; margin-bottom:30px; border-radius: 10px">'
    st.markdown(border2, unsafe_allow_html=True)
    st.write(h4, '6. 가새재 (경사재) 검토')


border2 = '<hr style="border-top: 2px solid ' + 'blue' + '; margin-top:30px; margin-bottom:30px; border-radius: 10px">'
st.markdown(border2, unsafe_allow_html=True)
# ============================================================================================================================================
st.write('Example (아래는 나중에 참조할 사항)')

import streamlit as st

h4 = "합판"
radio_labels = ["12.0 mm", "15.0 mm", "18.0 mm"]

# Radio 버튼을 감싸고 있는 div 태그의 클래스를 추가 (불필요한 클래스 제거)
import streamlit as st

st.markdown(
    """
<style>
div.row-widget.stRadio > div[role='radiogroup'] {
    display: flex;
    flex-direction: row;
}
div.row-widget.stRadio > div[role='radiogroup'] > label {
    display: inline-flex;
    align-items: center;
    padding: 10px 20px;
    margin-right: 5px;
    background-color: lightblue;
    border: 1px solid black;
    border-radius: 5px;
}
div.row-widget.stRadio > div[role='radiogroup'] > label:hover {
    background-color: #dcdde1;
}

div.row-widget.stRadio > div[role='radiogroup'] > label input[type=radio] {
    display: none;
}

div.row-widget.stRadio > div[role='radiogroup'] > label span.custom-radio {
    width: 20px;
    height: 20px;
    display: inline-block;
    background-color: transparent;
    border: 1px solid black;
    border-radius: 50%;
    cursor: pointer;
}

div.row-widget.stRadio > div[role='radiogroup'] > label input[type=radio]:checked + span.custom-radio {
    background-color: green;
    color: green;
}
</style>
""",
    unsafe_allow_html=True,
)






container = st.container()

with container:
    st.radio(h4 + ' 두께 [mm]', radio_labels, key="thickness_options", help="라디오버튼 1")





import streamlit as st
import pandas as pd
# from tabulate import tabulate

# 샘플 데이터 프레임 선언
data = {r"$\pi\beta$": ["$e^{i \pi} + 1 = 0$", "This is an example text"],
        "Column2": [r'$\pmb{{\quad M = \Large{{\frac{{{0}\textcolor{{red}}{{{1}}}^2}}{{8}}}} \normalsize \leq f_{{ba}}\,S}} $'.format('w_w', 'tt'), r"$\frac{\partial f}{\partial x}$"]}
df = pd.DataFrame(data)

# 상단에 DataFrame을 택스트로 표시합니다
st.markdown(df.to_markdown(), unsafe_allow_html=True)
# st.write(df.style.set_properties(**{'font-weight': 'bold', 'font-size': '28px'}))


import base64
import streamlit as st
import pandas as pd

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def create_image_element(img, alt_text=""):
    return f'<img src="data:image/png;base64,{img}" alt="{alt_text}">'

image_data = get_base64_encoded_image("aa.png")

latex_expr1 = r"$$e^{i \pi} + 1 = $$"

# 테이블 헤더 구성
header_data = {'1': [latex_expr1], '': [create_image_element(image_data)]}
header_df = pd.DataFrame(header_data)

# 표와 셀의 크기를 조정하는 CSS 추가
st.markdown(r'''
<style>
    table {
        table-layout: fixed;
        width: 100%;
        height: 100%;
        border:none;
        # border-collapse: collapse; /* 테두리 충돌 문제를 수정하기 위해 추가 */
        }
    th, td {
        width: 250px;
        height: 50px;
        # word-wrap: break-word;
        text-align: left;
        vertical-align: top;
        border: 1px solid #FF0000; /* 빨간색 테두리 */
        }
    img {
        width:550px;
        # max-width: 100%;
        # max-height: 100%;
        }
    # table, th, td {
    #     border: none !important;
    #     }
    # th {
    #     border-bottom: none !important;
    #     }
</style>
''', unsafe_allow_html=True)

st.markdown(header_df.to_markdown(index=False), unsafe_allow_html=True)




import base64
import pandas as pd
import streamlit as st

# 폴더에 있는 이미지 파일 경로
path_to_image = "aa.png"

# 이미지를 열고 base64로 인코딩
with open(path_to_image, "rb") as f:
    encoded_image = base64.b64encode(f.read()).decode()

# 데이터프레임 생성
data = {
    "Name": ["Alice", rf"$$$\\\alpha$$$ Bob"],
    "Info": ["Info 1",  rf"$$\alpha$$ Bob"],
}
df = pd.DataFrame(data)

# 이미지를 포함할 셀에 HTML <img> 태그 삽입
df.loc[df["Name"] == "Alice", "Info"] = f'<img src="data:image/jpeg;base64,{encoded_image}" width="560px" height="160px" />'

# 데이터프레임을 HTML 테이블로 변환
html_table = df.to_html(escape=False, index=False)
st.write(html_table, unsafe_allow_html=True)
# 스트림릿에서 HTML 테이블 렌더링


import streamlit as st

def create_boxed_text(text, box_width='auto', box_height='auto', font_weight='normal', font_size='16px', padding='10px'):
    box_template = '''
    <style>
    .box {{
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: lightblue;
        border-radius: 80px;
        border: 2px solid darkblue;
        padding: 5px;
        margin: 10px;
        box-shadow: 2px 2px 5px rgba(255, 0, 0, 0.7);
        width: {box_width};
        height: {box_height};
    }}
    .text {{
        font-weight: {font_weight};
        font-size: {font_size};
        padding: {padding};
    }}
    </style>
    <div class="box"><div class="text">{text}</div></div>
    '''

    return box_template.format(box_width=box_width, box_height=box_height, font_weight=font_weight, font_size=font_size, text=text, padding=padding)

text = "1. 슬래브"
boxed_text = create_boxed_text(text, box_width='300px', box_height='50px', font_weight='bold', font_size='18px', padding='10px')

st.markdown(boxed_text, unsafe_allow_html=True)




# import base64

# def get_base64_encoded_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# image_data = get_base64_encoded_image("aa.png")

# image_width = 550  # 원하는 이미지 너비
# image_height = 150  # 원하는 이미지 높이
# top_margin = 25  # 원하는 상단 여백
# left_margin = 525  # 원하는 좌측 여백

# st.markdown('''
#     <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
#     <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
#     ''', unsafe_allow_html=True)

# left_lines = [
#     rf"Left line 1: \( \alpha x_i + y \)",
#     r"<b>Left line 2 is a bit longer: \( \frac{{x}}{{y}} \)</b>",
#     r"<b>Left line 3 is much longer than the previous line: \( \int_{{0}}^{{1}} x^{{\gamma}} dx \)</b>",
#     r"<b>Left line 4: \( \lambda^{{i\pi}} + 1 = 0 \)</b>"
# ]

# left_text_with_line_breaks = '<br>'.join(left_lines)

# box_template = f'''
# <style>
# .box {{
#     display: flex;
#     align-items: center;
#     background-color: lightblue;
#     border-radius: 80px;
#     border: 2px solid darkblue;
#     padding: 5px;
#     margin: 10px;
#     box-shadow: 2px 2px 5px rgba(255, 0, 0, 0.7);
#     width: 1500px;
#     height: 200px;
# }}
# .text {{
#     margin: 0 10px;
# }}
# </style>
# <div class="box"><div id="math-text" class="text">{left_text_with_line_breaks}</div><img src="data:image/png;base64,{image_data}" alt="이미지" style="width:{image_width}px;height:{image_height}px;"></div>
# '''

# st.markdown(box_template, unsafe_allow_html=True)

import random
import pandas as pd
import streamlit as st

df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)
st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)



