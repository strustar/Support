import streamlit as st
import streamlit.components.v1 as components

from datetime import date
today = date.today() # 오늘 날짜 가져오기

def Contents():
# Define some variables
    # print("Year and month:", today.strftime("%Y-%m"))
    title = " &nbsp; &nbsp; &nbsp; 구 조 검 토 보 고 서 &nbsp; &nbsp; &nbsp;"
    c1 = "현장명 : "
    c2 = "ㅇㅇ산업(주)"
    c3 = "시스템 동바리"
    c4 = today.strftime("%Y-%m")
    c5 = "작성 : ㅇㅇㅇ (인)"
    c6 = "검토 : ㅇㅇㅇ (인)"
    c7 = "승인 : 토목구조기술사 ㅇㅇㅇ (인)"
    c8 = "겉 표지 포멧 협의 등"

    # Write the HTML code
    html_code = f"""
        <div style = "font-weight: bold;  text-align: center;  background-color: white;  margin: 0px;  padding: 10px;  border: 5px double blue; ">
            <div style = "display:inline-block; color: black; font-size: 24px;">
                <p style = "color: blue; font-size: 32px; border: 3px solid black; padding-top: 10px; padding-bottom: 10px">{title}</p>            
                <p style = "margin-top:120px">{c1}</p>
                <p style = "margin-top: 80px">{c2}</p>
                <p style = "margin-top: 30px">{c3}</p>
                <p style = "margin-top:100px">{c4}</p>
                <p style = "margin-top:100px">{c5}</p>
                <p style = "margin-top: 30px">{c6}</p>
                <p style = "margin-top: 30px">{c7}</p>
                <p style = "margin-top:330px;  color: red;  font-size: 32px;  ">{c8}</p>
            </div>
        </div>
    """    
    components.html(html_code, width = 1000, height = 1400, scrolling = True)
    
    html_code = f"""        
        <div style="font-weight: bold; text-align: center; background-color: white; margin: 0px; padding: 10px; ">
            <div style="display:inline-block; ">
                <p style="color: blue; font-size: 32px; border: 3px solid black; padding-left: 80px;  padding-right: 80px; padding-bottom: 10px; padding-top: 10px">목 &nbsp; 차</p>
            </div>
        </div>
    """    
    components.html(html_code, height = 150)
    
    c1   = 'Ⅰ. 일반 사항'
    c1_1 = '1. 검토 개요 및 주의사항'
    c1_2 = '2. 사용부재 제원'
    c1_3 = '3. 설계조건'
    c1_4 = '4. 설계하중 및 하중조합'
    c1_5 = '5. 적용기준 및 참고문헌'
    
    c2   = 'Ⅱ. 구조 검토'
    c2_1 = '1. 설계조건'
    c2_2 = '2. 설계하중 산정'
    c2_3 = '3. 사용부재 및 설치간격'
    c2_4 = '4. 거푸집 널의 변형기준'
    c2_5 = '5. 합판 및 장선 간격 검토'
    c2_6 = '6. 장선 및 멍에 간격 검토'
    c2_7 = '7. 멍에 및 수직재 간격 검토'
    c2_8 = '8. 수직재 검토'
    c2_9 = '9. 수평재 검토'
    c2_10= '10. 가새재 검토'
 
    c3   = 'Ⅲ. 상세 구조해석'
    c3_1 = '1. 하중 조합'
    c3_2 = '2. 변위 및 응력 검토'
    c3_3 = '3. 단면력 집계'
    c3_4 = '4. 수직재 검토'
    c3_5 = '5. 수평재 검토'
    c3_6 = '6. 가새재 검토'    
    c3_7 = '7. 상세 구조해석 결과'
    
    c4   = 'Ⅳ. 검토 결과'
    # c4_1 = '1. 해석 결과 요약'
    
    st.write('');  st.write('');  st.write('')
    st.write('# ' + c1);  st.write('')
    col = st.columns([1, 1])    
    with col[0]:
        st.write('##  &nbsp;&nbsp;&nbsp;' + c1_1)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c1_2)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c1_3)
    with col[1]:
        st.write('##  &nbsp;&nbsp;&nbsp;' + c1_4)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c1_5)
        
    st.write('');  st.write('');  st.write('')
    st.write('# ' + c2);  st.write('')
    col = st.columns([1, 1])    
    with col[0]:
        st.write('##  &nbsp;&nbsp;&nbsp;' + c2_1)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c2_2)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c2_3)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c2_4)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c2_5)
    with col[1]:
        st.write('##  &nbsp;&nbsp;&nbsp;' + c2_6)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c2_7)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c2_8)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c2_9)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c2_10)
        
    st.write('');  st.write('');  st.write('')
    st.write('# ' + c3);  st.write('')
    col = st.columns([1, 1])    
    with col[0]:
        st.write('##  &nbsp;&nbsp;&nbsp;' + c3_1)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c3_2)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c3_3)
    with col[1]:        
        st.write('##  &nbsp;&nbsp;&nbsp;' + c3_4)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c3_5)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c3_6)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c3_7)
    
    st.write('');  st.write('');  st.write('')
    st.write('# ' + c4);  st.write('')
    
    st.write('');  st.write('');  st.write('')
    st.write('');  st.write('');  st.write('')
    st.write('');  st.write('');  st.write('')
    st.write('');  st.write('');  st.write('')
    st.write('');  st.write('');  st.write('')

