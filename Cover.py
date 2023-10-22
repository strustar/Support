import streamlit as st
import streamlit.components.v1 as components

from datetime import date
today = date.today() # 오늘 날짜 가져오기

def Contents():
    c0 = '<u>문서번호 : 23-10-001</u>'
    title = "&nbsp; &nbsp; &nbsp; 시스템동바리 구조검토보고서 &nbsp; &nbsp; &nbsp;"
    c1 = "팔당대교~와부 도로건설 공사"
    c2 = "<u>교대날개벽</u>"
    c3 = today.strftime("%Y. %m")
    c4 = "우림산업(주)"
    
    html_code = f"""        
        <div style = "font-weight: bold;  text-align: center;  background-color: white;  margin: 0px;  padding: 10px ">
            <p style = "text-align: left;  font-size: 20px">{c0}</p>
            <div style = "display:inline-block; color: black; font-size: 28px;">                
                <p style = "color: blue; font-size: 38px; border: 3px solid black; margin-top: 80px;  padding-top: 10px; padding-bottom: 10px">{title}</p>            
                <p style = "margin-top:120px;  font-size: 32px">{c1}</p>
                <p style = "margin-top: 40px;  font-size: 32px;  color: blue;">{c2}</p>
                <p style = "margin-top:240px">{c3}</p>
                <p style = "margin-top:240px;  margin-bottom:200px">{c4}</p>
            </div>
        </div>
        <table style = 'text-align: center;  width: 100%;  border-collapse: collapse;  border: 2px solid black;  font-weight: bold;  font-size: 28px'>
            <tr style = 'width: 100%;  border-collapse: collapse;  border: 2px solid black;  font-size: 20px'>
                <td style = 'border-collapse: collapse;  border: 2px solid black;  width: 8%;  padding: 20px'> 작<br><br>성 </td>
                <td style = 'border-collapse: collapse;  border: 2px solid black;  width:26%'> 우림산업(주)<br><br>박 순 태</td>
                <td style = 'border-collapse: collapse;  border: 2px solid black;  width:15%'> </td>
                <td style = 'border-collapse: collapse;  border: 2px solid black;  width:.1%'> </td>
                <td style = 'border-collapse: collapse;  border: 2px solid black;  width: 8%'> 승<br><br>인 </td>
                <td style = 'border-collapse: collapse;  border: 2px solid black;  width:27%'> 토목구조기술사<br><br>김 상 현</td>
                <td style = 'border-collapse: collapse;  border: 2px solid black;  width:15%'> </td>
            </tr>
        </table>
    """    
    components.html(html_code, width = 1000, height = 1400, scrolling = True)
    
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    html_code = f"""
        <div style="font-weight: bold; text-align: center; background-color: white; margin: 0px; padding: 10px; ">
            <div style="display:inline-block; ">
                <p style="color: blue; font-size: 36px; padding-left: 80px;  padding-right: 80px; padding-bottom: 10px; padding-top: 10px"><u>목 &nbsp; 차</p>
            </div>
        </div>
    """    
    components.html(html_code, height = 150)
    
    c1   = ':blue[Ⅰ. 일반 사항]'
    c1_1 = '1. 검토 개요 및 주의사항'
    c1_2 = '2. 사용부재 제원'
    c1_3 = '3. 설계조건'
    c1_4 = '4. 설계하중 및 하중조합'
    c1_5 = '5. 적용기준 및 참고문헌'
    
    c2   = ':blue[Ⅱ. 구조 검토]'
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
 
    c3   = ':blue[Ⅲ. 상세 구조해석]'
    c3_1 = '1. 하중 조합'
    c3_2 = '2. 변위 및 응력 검토'
    c3_3 = '3. 단면력 집계'
    c3_4 = '4. 수직재 검토'
    c3_5 = '5. 수평재 검토'
    c3_6 = '6. 가새재 검토'    
    c3_7 = '7. 상세 구조해석 결과'
    
    c4   = ':blue[Ⅳ. 검토 결과]'
    c4_1 = '1. 검토 의견'
    c4_2 = '2. 요 약'
    
    c5   = ':blue[[부 록]]'
    c5_1   = '# ANSYS 상세 구조해석 코드'
    
    s1 = '###  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
    s2 = '###  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
    st.write('');  st.write('')
    st.write('## &nbsp;&nbsp;' + c1)
    col = st.columns([1, 1])    
    with col[0]:
        st.write(s1 + c1_1)
        st.write(s1 + c1_2)
        st.write(s1 + c1_3)
    with col[1]:
        st.write(s2 + c1_4)
        st.write(s2 + c1_5)
        
    st.write('');  st.write('')
    st.write('## &nbsp;&nbsp;' + c2)
    col = st.columns([1, 1])    
    with col[0]:
        st.write(s1 + c2_1)
        st.write(s1 + c2_2)
        st.write(s1 + c2_3)
        st.write(s1 + c2_4)
        st.write(s1 + c2_5)
    with col[1]:
        st.write(s2 + c2_6)
        st.write(s2 + c2_7)
        st.write(s2 + c2_8)
        st.write(s2 + c2_9)
        st.write(s2 + c2_10)
        
    st.write('');  st.write('')
    st.write('## &nbsp;&nbsp;' + c3)
    col = st.columns([1, 1])    
    with col[0]:
        st.write(s1 + c3_1)
        st.write(s1 + c3_2)
        st.write(s1 + c3_3)
    with col[1]:
        st.write(s2 + c3_4)
        st.write(s2 + c3_5)
        st.write(s2 + c3_6)
        st.write(s2 + c3_7)
    
    st.write('');  st.write('')
    st.write('## &nbsp;&nbsp;' + c4)
    col = st.columns([1, 1])    
    with col[0]:
        st.write(s1 + c4_1)
    with col[1]:
        st.write(s2 + c4_2)
            
    # st.write('');  st.write('')
    # st.write('## &nbsp;&nbsp;' + c5)
    # st.write(s1 + c5_1)
        
    # st.write('');  st.write('');  st.write('')


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 나중에 참조??
def Contents_first():
    c0 = '<u>문서번호 : 23-10-001</u>'
    title = "&nbsp; &nbsp; &nbsp; 시스템동바리 구조검토보고서 &nbsp; &nbsp; &nbsp;"
    c1 = "고속국도 제29호선 세종~포천 건설공사"
    c2 = "<u>교대날개벽</u>"
    c3 = today.strftime("%Y. %m")
    c4 = "우림산업(주) [http://slrental.co.kr]"
    c5 = "(검토) 박순태 &nbsp; (인) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; (승인) 김상현 &nbsp; (인)"
    c6 = "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 우림산업(주) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 토목구조기술사"
    
    html_code = f"""        
        <div style = "font-weight: bold;  text-align: center;  background-color: white;  margin: 0px;  padding: 10px;  border: 5px double blue; ">
            <p style = "text-align: left;  font-size: 20px">{c0}</p>
            <div style = "display:inline-block; color: black; font-size: 28px;">                
                <p style = "color: blue; font-size: 38px; border: 3px solid black; margin-top: 80px;  padding-top: 10px; padding-bottom: 10px">{title}</p>            
                <p style = "margin-top:120px">{c1}</p>
                <p style = "margin-top: 40px">{c2}</p>
                <p style = "margin-top:280px">{c3}</p>
                <p style = "margin-top:280px">{c4}</p>
                <p style = "margin-top: 80px">{c5}</p>
                <p style = "margin-bottom: 40px;  padding-top: 0px;  font-size: 20px">{c6}</p>
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
    c4_1 = '1. 검토 결과'
    c4_2 = '2. 요 약'
    
    c5   = '[부 록]'
    c5_1   = '# ANSYS 상세 구조해석 코드'
    
    st.write('');  st.write('')
    st.write('# ' + c1)
    col = st.columns([1, 1])    
    with col[0]:
        st.write('##  &nbsp;&nbsp;&nbsp;' + c1_1)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c1_2)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c1_3)
    with col[1]:
        st.write('##  &nbsp;&nbsp;&nbsp;' + c1_4)
        st.write('##  &nbsp;&nbsp;&nbsp;' + c1_5)
        
    st.write('');  st.write('')
    st.write('# ' + c2)
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
        
    st.write('');  st.write('')
    st.write('# ' + c3)
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
    
    st.write('');  st.write('')
    st.write('# ' + c4)
    col = st.columns([1, 1])    
    with col[0]:
        st.write('##  &nbsp;&nbsp;&nbsp;' + c4_1)
    with col[1]:        
        st.write('##  &nbsp;&nbsp;&nbsp;' + c4_2)
            
    st.write('');  st.write('')
    st.write('# ' + c5)
    st.write('##  &nbsp;&nbsp;&nbsp;' + c5_1)
        
    st.write('');  st.write('');  st.write('')

