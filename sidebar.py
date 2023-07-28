import streamlit as st
import numpy as np
sb = st.sidebar

##### sidebar =======================================================================================================
def Sidebar(h2, h4):
    class In:
        pass

    sb.write(h2, '✤ 공사명')    
    In.title = sb.text_input('숨김', placeholder='공사명을 입력하세요', label_visibility='collapsed')    

    sb.write(h2, '✤ 검토 유형')    
    In.type = sb.radio('숨김', ('슬래브', '보하부', '기타(작성중...)'), horizontal=True, label_visibility='collapsed', key='0')

    border = '<hr style="border-top: 1px solid purple; margin-top:15px; margin-bottom:15px;">'
    sb.markdown(border, unsafe_allow_html=True)
    
    sb.write(h2, '1. ' + In.type)  # ￭
    [col1, col2, col3] = sb.columns(3)
    with col1:
        In.height = st.number_input(h4 + '✦ 층고 [mm]', min_value = 100., value = 9500., step = 100., format = '%f')
    with col2:
        if '슬래브' in In.type:  In.slab_t = st.number_input(h4 + '✦ 두께 [mm]', min_value = 50., value = 350., step = 10., format = '%f')
        if '보하부' in In.type:  In.beam_w = st.number_input(h4 + '✦ 보의 폭 [mm]', min_value = 50., value = 500., step = 10., format = '%f')
    with col3:
        if '슬래브' not in In.type:  In.beam_h = st.number_input(h4 + '✦ 보의 높이 [mm]', min_value = 50., value = 900., step = 10., format = '%f')
    In.thick_height = In.slab_t if '슬래브' in In.type else In.beam_h    


    sb.write(h2, '2. 거푸집용 합판')
    w_s = '합판'
    [col1, col2] = sb.columns([3,2], gap = "small")
    with col1:
        w_t = st.radio(h4 + '￭ 합판 두께 [mm]', (12., 15., 18.), horizontal=True, key='1')
    with col2:
        w_angle = st.radio(h4 + '￭ 하중 방향 [각도]', (0, 90), horizontal=True, key='2')

    sb.write(h2, '3. 장선 & 멍에')
    sb.selectbox(h4 + ':green[장선 규격 [mm]]', ('50×50×2.0t', '50×50×2.3t'))

    j_s = ['각형강관','각형강관'];  j_b = np.zeros(2);  j_h = np.zeros(2);  j_t = np.zeros(2);  typ = ['장선', '멍에']
    for i in [0, 1]:
        sb.write(h2, str(round(i+3))+'. ' + typ[i])

        [col1, col2, col3] = sb.columns(3)
        with col1:
            j_b[i] = st.number_input(h4 + ':green[폭 [mm]]', min_value = 10., value = 50.+25*i, step = 5., format = '%f')
        with col2:
            j_h[i] = st.number_input(h4 + ':green[높이 [mm]]', min_value = 10., value = 50.+75*i, step = 5., format = '%f')
        with col3:
            j_t[i] = st.number_input(h4 + ':green[두께 [mm]]', min_value = 1., value = 2.+0.9*i, step = 0.1, format = '%.1f')

        
    sb.write(h2, '5. 수직재')
    [col1, col2, col3] = sb.columns(3, gap = "small")
    with col1:
        sp_d = st.number_input(h4+':green[직경 [mm]]', min_value = 10., value = 60.5, step = 2., format = '%f')
    with col2:
        sp_t = st.number_input(h4+':green[두께 [mm]]', min_value = 1., value = 2.6, step = 0.1, format = '%f')
    with col3:
        sp_fy = st.number_input(h4+':green[항복강도 [MPa]]', min_value = 10., value = 355., step = 10., format = '%f')

    sb.write(h2, ':blue[6. 간격 여유 설정 (기본 : 85%)]')
    [col1, col2, col3] = sb.columns(3)
    with col1:
        j_margin = st.number_input(h4+':green[장선 간격 여유 [%]]', min_value = 10., value = 85., step = 5., format = '%f')
    with col2:
        y_margin = st.number_input(h4+':green[멍에 간격 여유 [%]]', min_value = 10., value = 85., step = 5., format = '%f')
    with col3:
        s_margin = st.number_input(h4+':green[동바리 간격 여유 [%]]', min_value = 10., value = 85., step = 5., format = '%f')

    sb.write(h2, ':blue[7. 자중]')
    [col1, col2] = sb.columns(2)
    with col1:
        s_weight = st.number_input(h4+':green[콘크리트 단위중량 [kN/m³]]', min_value = 10., value = 24., step = 1., format = '%f')
    with col2:
        w_weight = st.number_input(h4+':green[거푸집 단위중량 [kN/m²]]', min_value = 0.1, value = 0.4, step = 0.1, format = '%f')

    sb.write(h2, ':blue[8. 거푸집 널의 변형기준]')
    [col1, col2] = sb.columns(2)
    with col1:
        level = st.radio(h4+':green[표면의 등급]', ('A급', 'B급', 'C급'), horizontal=True)
        if 'A' in level:  d1 = 360;  d2 = '3mm'
        if 'B' in level:  d1 = 270;  d2 = '6mm'
        if 'C' in level:  d1 = 180;  d2 = '13mm'
        d1 = r'$\,\bm{\Large\frac{L_n}{'+str(d1)+'}}$'
        
    with col2:        
        st.write(h4+'➣ 상대변형 :', d1)
        st.write(h4+'➣ 절대변형 :', d2)

    sb.write(h2, ':blue[9. 동바리 (Support)]')    
    [col1, col2] = sb.columns([1,1], gap = "small")
    with col1:
        Ln = st.number_input(h4+':green[순간격 [mm] (Ln) ]', min_value = 50., value = 1500., step = 100., format = '%f')
    with col2:
        KL = st.number_input(h4+':green[수평 연결재 간격 [mm] (KL) ]', min_value = 50., value = 1800., step = 100., format = '%f')

    [In.s_weight, In.w_weight, In.w_s, In.w_t, In.w_angle, In.level, In.d1, In.d2] = [s_weight, w_weight, w_s, w_t, w_angle, level, d1, d2]
    [In.j_s, In.j_b, In.j_h, In.j_t] = [j_s, j_b, j_h, j_t]
    [In.j_margin, In.y_margin, In.s_margin, In.Ln, In.KL, In.sp_d, In.sp_t, In.sp_fy] = [j_margin, y_margin, s_margin, Ln, KL, sp_d, sp_t, sp_fy]
    return In