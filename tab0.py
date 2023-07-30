import streamlit as st
import numpy as np
import table

class Wood: pass
class Joist: pass
class Yoke: pass
class Vertical: pass
class Horizontal: pass
class Bracing: pass

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'

def Tab(In, color, fn):
    border1 = '<hr style="border-top: 5px double ' + color + '; margin-top: 0px; margin-bottom:30px; border-radius: 10px">'
    border2 = '<hr style="border-top: 2px solid '  + color + '; margin-top:30px; margin-bottom:30px; border-radius: 10px">'    

    st.markdown(border1, unsafe_allow_html=True)
    st.write(h4, '1. 검토 개요 및 주의사항')
    
    st.markdown(border2, unsafe_allow_html=True)
    st.write(h4, '1. 적용기준')
    st.write(s1, '1) 가시설물 설계 일반사항 (국토교통부, :blue[KDS 21 10 00 : 2022])')
    st.write(s1, '2) 거푸집 및 동바리 설계기준 (국토교통부, :blue[KDS 21 50 00 : 2022])')
    st.write(s1, '3) 강구조 부재 설계기준(허용응력설계법) (국토교통부, :blue[KDS 14 30 10 : 2019])')
    st.write(s1, '4) 거푸집 및 동바리 안전작업지침 등 (한국산업안전보건공단)')
    st.write(s1, '5) 콘크리트 표준시방서 (한국콘크리트학회, 2016)')        
    
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

    st.write(s1, '2) 수평하중 **[:blue[아래 두값 중 큰 값 적용]]**')
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
    table.Info(fn, '합판', In.wood, Ib_Q, I, S, E, fba, fsa, 40)
    [Wood.A, Wood.I, Wood.S, Wood.E, Wood.fba, Wood.fsa, Wood.Ib_Q] = [A, I, S, E, fba, fsa, Ib_Q]


    E = 210e3;  fba = 181.5;  fsa = 110  ### 장선, 멍에 공통
    st.write(s1, '2) 장선')    
    b = In.joist_b;  h = In.joist_h;  t = In.joist_t;  b1 = (b - 2*t);  h1 = (h - 2*t)
    A = b*h - b1*h1
    I = b*h**3/12 - b1*h1**3/12
    S = I/(In.joist_h/2)    
    table.Info(fn, '장선', In.joist, A, I, S, E, fba, fsa, 40)
    [Joist.A, Joist.I, Joist.S, Joist.E, Joist.fba, Joist.fsa] = [A, I, S, E, fba, fsa]

    
    st.write(s1, '3) 멍에')    
    b = In.yoke_b;  h = In.yoke_h;  t = In.yoke_t;  b1 = (b - 2*t);  h1 = (h - 2*t)
    A = b*h - b1*h1
    I = b*h**3/12 - b1*h1**3/12
    S = I/(In.yoke_h/2)    
    table.Info(fn, '멍에', In.yoke, A, I, S, E, fba, fsa, 40)
    [Yoke.A, Yoke.I, Yoke.S, Yoke.E, Yoke.fba, Yoke.fsa] = [A, I, S, E, fba, fsa]

    st.markdown(border2, unsafe_allow_html=True)
    d = In.vertical_d;  t = In.vertical_t;  d1 = d - 2*t
    A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(In.vertical_d/2);  r = np.sqrt(I/A)

    [Vertical.A, Vertical.I, Vertical.S, Vertical.E, Vertical.r, Vertical.Fy] = [A, I, S, 210e3, r, 355]

    return Wood, Joist, Yoke, Vertical
