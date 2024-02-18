import streamlit as st
import Sidebar, General, Calculate, Cover, Detail, Summary

import os, sys
os.system('cls')  # 터미널 창 청소, clear screen
sys.path.append('D:\\Work_Python\\Common')  # 공통 스타일 변수 디렉토리 추가
import commonStyle    # print(sys.path)

### * -- Set page config
st.set_page_config(page_title="System support 구조검토", page_icon="🌈", layout="centered",   # centered, wide
                    initial_sidebar_state="expanded", # runOnSave = True,
                    menu_items = {
                        # 'Get Help': 'https://www.extremelycoolapp.com/help',
                        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
                        # 'About': "# This is a header. This is an *extremely* cool app!"
                    })

In = Sidebar.Sidebar()
commonStyle.input_box(In)
commonStyle.watermark(In)

if ('보고서' in In.select) or ('표지' in In.select):
    Cover.Contents()
    st.write('');  st.write('');  st.write('')
if ('보고서' in In.select) or ('일반 사항' in In.select):
    [Wood, Joist, Waling, Yoke, Vertical, Horizontal, Bracing] = General.Info(In)
    st.write('');  st.write('');  st.write('')
if ('보고서' in In.select) or ('구조 검토' in In.select):
    Calculate.Info(In, Wood, Joist, Waling, Yoke, Vertical, Horizontal, Bracing)
    st.write('');  st.write('');  st.write('')
if ('보고서' in In.select) or ('상세' in In.select):
    Detail.Analysis(In, 'result', Vertical, Horizontal, Bracing)   # opt : both, result, code
    st.write('');  st.write('');  st.write('')
if ('보고서' in In.select) or ('결과' in In.select):
    Summary.Info(In)
    st.write('');  st.write('');  st.write('')
if '부 록' in In.select:
    Detail.Analysis(In, 'code', '', '', '')   # opt : both, result, code
