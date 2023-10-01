import streamlit as st

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'

def Info(In):
    st.title(':green[Ⅳ. 검토 결과 ✅]')
    st.markdown(In.border2, unsafe_allow_html=True) ########### border ##########
    
    st.write(h4, '1. 검토 결과')
    st.write(s1, '➣ 구조검토 결과 :red[내력과 변위가 허용범위 이내인 것을 확인함]')
    
    st.write(h4, '2. 요약')