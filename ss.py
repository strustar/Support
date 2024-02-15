import streamlit as st
import Sidebar, General, Calculate, Cover, style, Detail, Summary
from General import Wood, Joist, Yoke, Vertical, Horizontal, Bracing
# from Sidebar import In

import os
os.system('cls')  # 터미널 창 청소, clear screen
### * -- Set page config
st.set_page_config(page_title = "System support 구조검토", page_icon = "🌈", layout = "centered",    # centered, wide
                    initial_sidebar_state="expanded",
                    # runOnSave = True,
                    menu_items = {        #   initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
                        # 'Get Help': 'https://www.extremelycoolapp.com/help',
                        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
                        # 'About': "# This is a header. This is an *extremely* cool app!"
                    })

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'

In = Sidebar.Sidebar(h4, h5)
style.input(In)

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
