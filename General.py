import streamlit as st
import numpy as np
from Sidebar import word_wrap_style
import Table

class Wood: pass
class Joist: pass
class Yoke: pass
class Vertical: pass
class Horizontal: pass
class Bracing: pass

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'

def Tab(In, color):
    border1 = '<hr style="border-top: 5px double ' + color + '; margin-top: 0px; margin-bottom:30px; border-radius: 10px">'
    border2 = '<hr style="border-top: 2px solid '  + color + '; margin-top:30px; margin-bottom:30px; border-radius: 10px">'    

    st.markdown(border1, unsafe_allow_html=True)
    st.write(h4, '1. 검토 개요 및 주의사항')    
    txt = ':red[ [공사명을 입력하세요 (좌측 사이드바에서 입력)] ]' if In.title == '' else f':blue[ {In.title} ]'
    txt = f'본 검토서는 {txt} 현장에서 의뢰한 시스템 동바리에 대한 구조 안전성 검토를 위한 것임.'
    word_wrap_style(s1, txt, In.font_h5)

    txt = f'￭ 본 검토서는 시공사에서 제시한 시공조건 및 도면을 근거로 검토하였음. 따라서, 현장 여건이 변경되는 경우에는 반드시 검토자와 협의 후 시공하여야 함.'
    word_wrap_style(s1, txt, In.font_h5)

    txt = f'￭ 본 공사는 ":blue[2. 적용기준]"에 제시된 설계기준 및 시공기준을 따라 시공하여야 하며, 거푸집 및 동바리에 적용되는 각종 안전작업지침 및 설치지침에 따라 시공하여야 함.'
    word_wrap_style(s1, txt, In.font_h5)
    
    st.markdown(border2, unsafe_allow_html=True)
    st.write(h4, '2. 적용기준 및 참고문헌')
    st.write(s1, '￭ 가시설물 설계 일반사항 (KDS 21 10 00 : 2022, 국토교통부)')
    st.write(s1, '￭ 거푸집 및 동바리 설계기준 (KDS 21 50 00 : 2022, 국토교통부)')
    st.write(s1, '￭ 강구조 설계 일반사항(허용응력설계법) (KDS 14 30 05 : 2019, 국토교통부)')
    st.write(s1, '￭ 강구조 부재 설계기준(허용응력설계법) (KDS 14 30 10 : 2019, 국토교통부)')
    st.write(s1, '￭ 건축물 설계하중 (KDS 41 12 00 : 2022, 국토교통부)')
    st.write(s1, '￭ 비계 및 안전시설물 설계기준 (KDS 21 60 00 : 2022, 국토교통부)')
    st.write('')

    st.write(s1, '￭ 거푸집 및 동바리 (KCS 14 20 12 : 2022, 국토교통부)')
    st.write(s1, '￭ 가설공사 일반사항 (KCS 21 10 00 : 2022, 국토교통부)')
    st.write(s1, '￭ 거푸집 및 동바리공사 일반사항 (KCS 21 50 05 : 2023, 국토교통부)')
    st.write(s1, '￭ 초고층 고주탑 공사용 거푸집 및 동바리 (KCS 21 50 10 : 2022, 국토교통부)')
    st.write(s1, '￭ 노출 콘크리트용 거푸집 및 동바리 (KCS 21 50 15 : 2022, 국토교통부)')
    st.write(s1, '￭ 기타 콘크리트용 거푸집 및 동바리 (KCS 21 50 20 : 2022, 국토교통부)')
    st.write(s1, '￭ 비계공사 일반사항 (KCS 21 60 05 : 2022, 국토교통부)')
    st.write(s1, '￭ 비계 (KCS 21 60 10 : 2022, 국토교통부)')
    st.write('')

    st.write(s1, '￭ 시스템 동바리 안전작업 지침 (2020, 한국산업안전보건공단)')
    st.write(s1, '￭ 파이프 서포트 동바리 안전작업 지침 (2020, 한국산업안전보건공단)')
    st.write(s1, '￭ 거푸집 동바리 구조검토 및 설치 안전보건작업 지침 (2015, 한국산업안전보건공단)')
    
    
    st.markdown(border2, unsafe_allow_html=True)
    st.write(h4, '2. 설계하중')  # \enspace : 1/2 em space, \quad : 1 em space, \qquad : 2 em space
    st.write(h5, ':orange[<근거 : 1.6 설계하중 (KDS 21 50 00 : 2022)>]')
    st.write(s1, '1) 연직하중 (고정하중 + 작업하중)')

    st.write(s2, '① 고정하중')
    st.write(s3, '➣ 보통 콘크리트 자중 : :blue[24kN/m³ 이상] 적용')    
    st.write(s3, '➣ 거푸집 자중 : :blue[0.4kN/m² 이상] 적용')

    st.write(s2, '② 작업하중 (작업원, 경량의 장비하중, 충격하중, 기타 콘크리트 타설에 필요한 자재 및 공구 등)')
    # st.write(s3, '➣ :blue[2.5kN/㎡ 이상] 적용, 전동식 카트장비 사용시 :blue[3.8kN/m² 이상] 적용')  # 바뀐 설계기준에는 없음??
    st.write(s3, '➣ 콘크리트 타설 높이가 0.5m 미만인 경우 :blue[2.5kN/m²], 0.5m 이상 1m 미만인 경우 :blue[3.5kN/m²], 1m 이상인 경우 :blue[5kN/m² 이상] 적용')

    st.write(s2, '③ 최소 연직하중')
    st.write(s3, '➣ 콘크리트 타설 높이와 관계없이 최소 :blue[5kN/m² 이상] 적용, ??바뀐 설계기준에는 없음?? 전동식카트 사용시 최소 :blue[6.3kN/m² 이상] 적용')

    st.write(s1, '2) 수평하중 [:blue[아래 두값 중 큰 값 적용]]')
    st.write(s2, '① 동바리 상단에 고정하중의 :blue[2% 이상]')
    st.write(s2, '② 동바리 상단에 수평방향으로 단위길이당 :blue[1.5kN/m 이상]')
    
    st.markdown(border2, unsafe_allow_html=True)
    st.write(h4, '3. 사용재료')
    st.write(h5, ':orange[<근거 : 2.2 거푸집 널 & 2.3 장선 및 멍에 (KDS 21 50 00 : 2022)>]')
    # st.info('**<근거 : 2.2 거푸집 널 & 2.3 장선 및 멍에 (KDS 21 50 00 :2022)>]**')

    st.write(s1, '1) 거푸집 널')
    A = In.wood_t*1;  E = 11e3;  fba = 16.8;  fsa = 0.63
    if In.wood_t == 12:
        if In.wood_angle == 0:  I = 90;  S =13;  Ib_Q = 10
        if In.wood_angle ==90:  I = 20;  S = 6;  Ib_Q = 5.1
    if In.wood_t == 15:
        if In.wood_angle == 0:  I =160;  S =18;  Ib_Q = 11.5
        if In.wood_angle ==90:  I = 40;  S = 8;  Ib_Q = 6
    if In.wood_t == 18:
        if In.wood_angle == 0:  I =250;  S =23;  Ib_Q = 14.8
        if In.wood_angle ==90:  I =100;  S =13;  Ib_Q = 8
    In.wood = str(In.wood_t)+' / '+str(In.wood_angle)+'°'
    Table.Info('합판', In.wood, A, Ib_Q, I, S, E, fba, fsa, 40)
    [Wood.A, Wood.I, Wood.S, Wood.E, Wood.fba, Wood.fsa, Wood.Ib_Q] = [A, I, S, E, fba, fsa, Ib_Q]


    E = 210e3;  fba = 181.5;  fsa = 110  ### 장선, 멍에 공통
    st.write(s1, '2) 장선')    
    b = In.joist_b;  h = In.joist_h;  t = In.joist_t;  b1 = (b - 2*t);  h1 = (h - 2*t)
    A = b*h - b1*h1
    I = b*h**3/12 - b1*h1**3/12
    S = I/(In.joist_h/2)
    A1 = b*t;  A2 = 2*t*(h/2 - t);  y1 = (h - t)/2;  y2 = (h/2 - t)/2    # 전단상수, 전단 단면적 계산
    y_bar = (A1*y1 + A2*y2)/(A1 + A2);  Q = A/2*y_bar;  Ib_Q = I*(2*t)/Q
    Table.Info('장선', In.joist, A, Ib_Q, I, S, E, fba, fsa, 40)
    [Joist.A, Joist.I, Joist.S, Joist.E, Joist.fba, Joist.fsa, Joist.Ib_Q] = [A, I, S, E, fba, fsa, Ib_Q]

    
    st.write(s1, '3) 멍에')    
    b = In.yoke_b;  h = In.yoke_h;  t = In.yoke_t;  b1 = (b - 2*t);  h1 = (h - 2*t)
    A = b*h - b1*h1
    I = b*h**3/12 - b1*h1**3/12
    S = I/(In.yoke_h/2)    
    A1 = b*t;  A2 = 2*t*(h/2 - t);  y1 = (h - t)/2;  y2 = (h/2 - t)/2    # 전단상수, 전단 단면적 계산
    y_bar = (A1*y1 + A2*y2)/(A1 + A2);  Q = A/2*y_bar;  Ib_Q = I*(2*t)/Q    
    Table.Info('멍에', In.yoke, A, Ib_Q, I, S, E, fba, fsa, 40)
    [Yoke.A, Yoke.I, Yoke.S, Yoke.E, Yoke.fba, Yoke.fsa, Yoke.Ib_Q] = [A, I, S, E, fba, fsa, Ib_Q]

    # 수직재, 수평재, 가새재 (중공 원형)
    st.markdown(border2, unsafe_allow_html=True)
    d = In.vertical_d;  t = In.vertical_t;  d1 = d - 2*t
    A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(In.vertical_d/2);  r = np.sqrt(I/A)
    [Vertical.A, Vertical.I, Vertical.S, Vertical.E, Vertical.r, Vertical.Fy] = [A, I, S, 210e3, r, 355]

    d = In.horizontal_d;  t = In.horizontal_t;  d1 = d - 2*t
    A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(In.horizontal_d/2);  r = np.sqrt(I/A)
    [Horizontal.A, Horizontal.I, Horizontal.S, Horizontal.E, Horizontal.r, Horizontal.Fy] = [A, I, S, 210e3, r, 235]

    d = In.bracing_d;  t = In.bracing_t;  d1 = d - 2*t
    A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(In.bracing_d/2);  r = np.sqrt(I/A)
    [Bracing.A, Bracing.I, Bracing.S, Bracing.E, Bracing.r, Bracing.Fy] = [A, I, S, 210e3, r, 235]

    return Wood, Joist, Yoke, Vertical, Horizontal, Bracing
