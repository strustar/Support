import streamlit as st
import numpy as np
import table

def Tab(In, color, fn, s1, s2, s3, h4, h5):
    border1 = '<hr style="border-top: 5px double ' + color + '; margin-top: 0px; margin-bottom:30px; border-radius: 10px">'
    border2 = '<hr style="border-top: 2px solid '  + color + '; margin-top:30px; margin-bottom:30px; border-radius: 10px">'
    [s_weight, w_weight, w_s, w_t, w_angle] = [In.s_weight, In.w_weight, In.w_s, In.w_t, In.w_angle]
    [j_s, j_b, j_h, j_d, j_t] = [In.j_s, In.j_b, In.j_h, In.j_d, In.j_t]

    st.markdown(border1, unsafe_allow_html=True)
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
    A = w_t*1;  E = 11e3;  fba = 16.8;  fsa = 0.63
    if w_t == 12:
        if w_angle == 0:  I = 90;  S =13;  Ib_Q = 10
        if w_angle ==90:  I = 20;  S = 6;  Ib_Q = 5.1
    if w_t == 15:
        if w_angle == 0:  I =160;  S =18;  Ib_Q = 11.5
        if w_angle ==90:  I = 40;  S = 8;  Ib_Q = 6
    if w_t == 18:
        if w_angle == 0:  I =250;  S =23;  Ib_Q = 14.8
        if w_angle ==90:  I =100;  S =13;  Ib_Q = 8
    section = str(w_t)+' / '+str(w_angle)+'°'
    table.Info(fn, w_s, section, Ib_Q, I, S, E, fba, fsa, 40)
    class Wood:
        pass
    [Wood.A, Wood.I, Wood.S, Wood.E, Wood.fba, Wood.fsa, Wood.Ib_Q, Wood.section] = [A, I, S, E, fba, fsa, Ib_Q, section]

    
    st.write(s1, '2) 장선')
    if '목재' in j_s[0]:
        section = str(round(j_b[0]))+'×'+str(round(j_h[0]))
        A = j_b[0]*j_h[0];  I = j_b[0]*j_h[0]**3/12;  S = I/(j_h[0]/2)
        E = 11e3;  fsa = 0.78    
        fba = 10.6 if j_h[0] >= 120 else 13
    if '각형' in j_s[0]:
        section = str(round(j_b[0]))+'×'+str(round(j_h[0]))+'×'+str(round(j_t[0],1))+'t'
        b = j_b[0];  h = j_h[0];  b1 = (j_b[0]-2*j_t[0]);  h1 = (j_h[0]-2*j_t[0])
        A = b*h - b1*h1
        I = b*h**3/12 - b1*h1**3/12
        S = I/(j_h[0]/2)
        E = 200.e3;  fba = 160;  fsa = 95.
    if '원형' in j_s[0]:
        section = '𝜙'+str(round(j_d[0],1))+'×'+str(round(j_t[0],1))+'t'
        d = j_d[0];  d1 = (j_d[0]-2*j_t[0])
        A = np.pi*(d**2-d1**2)/4
        I = np.pi*(d**4-d1**4)/64
        S = I/(j_d[0]/2)
        E = 200e3;  fba = 240;  fsa = 95
    table.Info(fn, j_s[0], section, A, I, S, E, fba, fsa, 40)
    class Joist:
        pass
    [Joist.A, Joist.I, Joist.S, Joist.E, Joist.fba, Joist.fsa, Joist.section] = [A, I, S, E, fba, fsa, section]

    
    st.write(s1, '3) 멍에')
    if '목재' in j_s[1]:
        section = str(round(j_b[1]))+'×'+str(round(j_h[1]))
        A = j_b[1]*j_h[1];  I = j_b[1]*j_h[1]**3/12;  S = I/(j_h[1]/2)
        E = 11e3;  fsa = 0.78
        fba = 10.6 if j_h[1] >= 120 else 13
    if '각형' in j_s[1]:
        section = str(round(j_b[1]))+'×'+str(round(j_h[1]))+'×'+str(round(j_t[1],1))+'t'
        b = j_b[1];  h = j_h[1];  b1 = (j_b[1]-2*j_t[1]);  h1 = (j_h[1]-2*j_t[1])
        A = b*h - b1*h1
        I = b*h**3/12 - b1*h1**3/12
        S = I/(j_h[1]/2)
        E = 200e3;  fba = 160;  fsa = 95
    if '원형' in j_s[1]:
        section = '𝜙'+str(round(j_d[1],1))+'×'+str(round(j_t[1],1))+'t'
        d = j_d[1];  d1 = (j_d[1]-2*j_t[1])
        A = np.pi*(d**2-d1**2)/4
        I = np.pi*(d**4-d1**4)/64
        S = I/(j_d[1]/2)
        E = 200e3;  fba = 240;  fsa = 95
    table.Info(fn, j_s[1], section, A, I, S, E, fba, fsa, 40)
    class Yoke:
        pass
    [Yoke.A, Yoke.I, Yoke.S, Yoke.E, Yoke.fba, Yoke.fsa, Yoke.section] = [A, I, S, E, fba, fsa, section]

    st.markdown(border2, unsafe_allow_html=True)
    return Wood, Joist, Yoke
