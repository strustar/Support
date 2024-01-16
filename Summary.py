import streamlit as st
import Table, Detail

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'

def Info(In):
    # st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.title(':green[Ⅳ. 검토 결과 ✅]')
    st.markdown(In.border2, unsafe_allow_html=True) ########### border ##########
    
    st.write(h4, '1. 검토 의견')
    st.write(s1, '➣ 구조검토 결과 :blue[변위와 내력이 허용범위 이내인 것을 확인함]')
    
    st.write(h4, '2. 요약')
    st.write(s1, '➣ 부재 설치간격은 설치가 가능한 :blue[최대간격]으로, 제시된 :blue[간격 이하로 설치]하더라도 :blue[구조적으로 안전]함')
    Table.Summary(In)
        