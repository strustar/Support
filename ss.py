# import openpyxl as ox
# import xlwings as xw
import streamlit as st
import numpy as np
import sidebar, tab0, tab1

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


# 줄바꿈 처리
st.markdown("""
    <style>
        .element-container {
            white-space: nowrap;
            overflow-x: visible;
        }
    </style>
    """, unsafe_allow_html=True)


# Adding custom style with font
fn1 = 'Nanum Gothic';  fn2 = 'Gungsuhche';  fn3 = 'Lora';  fn4 = 'Noto Sans KR'
font_style = """
    <style>
        /* CSS to set font for everything except code blocks */
        body, h1, h2, h3, h4, h5, h6, p, blockquote {font-family: 'Nanum Gothic', sans-serif !important;}
        /* CSS to set font for code blocks */
        .highlight pre, .highlight tt, pre, tt {font-family: 'Courier New', Courier, monospace;}

        /* Font size for titles (h1 to h6) */
        h1 {font-size: 32px;}
        h2 {font-size: 28px;}
        h3 {font-size: 24px;}
        h4 {font-size: 20px;}
        h5 {font-size: 16px;}
        h6 {font-size: 12px;}
        /* Font size for body text */
        body {font-size: 16px;}
    </style>
"""
st.markdown(font_style, unsafe_allow_html=True)

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5+'$\quad$';  s2 = h5+'$\qquad$';  s3 = h5+'$\quad \qquad$'  #s12 = '$\enspace$'  공백 : \,\:\;  # ⁰¹²³⁴⁵⁶⁷⁸⁹  ₀₁₂₃₄₅₆₇₈₉

In = sidebar.Sidebar(h2, h4)
##### tab ===========================================================================================================
tab = st.tabs([h5+':blue[Ⅱ. 단면제원 검토 💻⭕]', h5+':green[Ⅰ. 설계조건 📝✍️]', h5+':orange[Ⅲ. 시스템 서포터 검토 🏛️🏗️]', h5+':green[Ⅳ. 구조검토 결과 🎯✅ ]' ])
with tab[1]:
    [Wood, Joist, Yoke] = tab0.Tab(In, 'green', fn1, s1, s2, s3, h4, h5)    

with tab[0]:
    [t_load, Lj, Ly, Ls] = tab1.Tab(In, 'blue', fn1, s1, s2, s3, h4, h5, Wood, Joist, Yoke)
    st.write(h4, '5. 서포트 검토 (수직재)')
    st.write(s1, '1) 1본당 작용하중 (P)')
    st.write(s2, '➣ P = 설계 하중 x 멍에 간격 x 서포트 간격');  P = t_load*Ly*Ls
    st.write(s2, '➣ P = {:.4f}'.format(t_load) + ' N/mm² x '+ str(round(Ly)) +' mm x '+ str(round(Ls)) + ' mm = {:.1f}'.format(P/1e3) + ' kN/EA')

    st.write(s1, '2) 허용압축응력 ($\pmb{F_{ca}}$) 산정' + ':orange[  <근거 : 4.4.2 좌굴길이와 세장비 & 4.4.3 허용압축응력 (KDS 14 30 10 : 2019)>]')
    st.write(s2, '➣ 유효 좌굴길이 : KL = ' + str(round(In.KL)) + ' mm')
    t = In.sp_t;  d = In.sp_d;  d1 = d - 2*t
    A = np.pi*(d**2 - d1**2)/4
    I = np.pi*(d**4 - d1**4)/64
    r = np.sqrt(I/A)
    st.write(s2, '➣ 세장비 : $\lambda$ = ' + str(round(In.KL)) + ' mm')




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
    "Name": ["Alice", "Bob"],
    "Info": ["Info 1", "Info 2"],
}
df = pd.DataFrame(data)

# 이미지를 포함할 셀에 HTML <img> 태그 삽입
df.loc[df["Name"] == "Alice", "Info"] = f'<img src="data:image/jpeg;base64,{encoded_image}" width="560px" height="160px" />'

# 데이터프레임을 HTML 테이블로 변환
html_table = df.to_html(escape=False, index=False)
st.write(html_table, unsafe_allow_html=True)
# 스트림릿에서 HTML 테이블 렌더링



# # import re
# # pattern = r"\d+\.?\d*" #정수 : r'\d+'
# # jj = re.findall(pattern, jw)
# import streamlit as st

# # 변수 설정
# red_variable = r"\textcolor{blue}{L_k}"
# Ljm = 10  # 값을 대신 입력하세요.

# # 포맷을 사용하여 문자열에 변수 삽입
# formatted_string = r"$\bm{{\quad\textcolor{{red}}{{{}}}\leq \Large\sqrt{{\frac{{8\,f_{{ba}}\,S}}{{ω}}}} \normalsize = \:}} $".format(red_variable) + '{:.1f}'.format(Ljm) + ' mm'

# st.write(s3, r"$\bm{{\quad\textcolor{{red}}{{{}}}\leq \Large\sqrt{{\frac{{8\,f_{{ba}}\,S}}{{ω}}}} \normalsize = \:}} $".format(red_variable) + '{:.1f}'.format(Ljm) + ' mm')

# name = "Alice"
# age = 25
# string = f"My name is {name} and I'm {age} years old."
# string
# string = "He said, \"Hello, World!\""
# string

