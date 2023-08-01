import streamlit as st
import re
sb = st.sidebar
class In:
    pass
In.ok = ':blue[OK] (🆗✅)'
In.ng = ':red[NG] (❌)'
In.space = '<div style="margin:0px">'

##### sidebar =======================================================================================================
def Sidebar(h2, h4):    
    sb.write(h2, '✤ 공사명')    
    In.title = sb.text_input('숨김', placeholder='공사명을 입력하세요', label_visibility='collapsed')

    sb.write(h2, '✤ 검토 유형')    
    In.type = sb.radio('숨김', ('슬래브', '보 (단멍에)', '기타(작성중...)'), horizontal=True, label_visibility='collapsed')

    border = '<hr style="border-top: 2px solid purple; margin-top:15px; margin-bottom:15px;">'
    sb.markdown(border, unsafe_allow_html=True)
    
    ### 슬라브 or 보 (￭)
    sb.write(h2, '1. ' + In.type)
    [col1, col2, col3] = sb.columns(3, gap = 'medium')
    with col1:
        if '슬래브' in In.type:  In.slab_t = st.number_input(h4 + '✦ 두께 [mm]', min_value = 50., value = 400., step = 10., format = '%0.f')
        if '보' in In.type:
            In.beam_b = st.number_input(h4 + '✦ 보의 폭 [mm]', min_value = 50., value = 500., step = 10., format = '%f')
            In.beam_h = st.number_input(h4 + '✦ 보의 높이 [mm]', min_value = 50., value = 900., step = 10., format = '%f')        
        # In.height = st.number_input(h4 + '✦ 층고 [mm]', min_value = 100., value = 9500., step = 100., format = '%f')
    with col2:
        In.slab_X = st.number_input(h4 + '✦ X 방향 길이 [m]', min_value = 1., value = 8., step = 0.1, format = '%.1f')        
        
    with col3:
        In.slab_Y = st.number_input(h4 + '✦ Y 방향 길이 [m]', min_value = 1., value = 8., step = 0.1, format = '%.1f')
    In.thick_height = In.slab_t if '슬래브' in In.type else In.beam_h    

    ### 거푸집용 합판
    sb.write(h2, '2. 거푸집용 합판')    
    [col1, col2] = sb.columns([3,2], gap = "medium")
    with col1:
        In.wood_t = st.radio(h4 + '￭ 합판 두께 [mm]', (12, 15, 18), horizontal=True)
    with col2:
        In.wood_angle = st.radio(h4 + '￭ 하중 방향 [각도]', (0, 90), horizontal=True, index = 1)

    sb.write(h2, '3. 장선 규격 및 간격 [mm] [SPSR400]')  # 🔳🔘
    col = sb.columns([3,2], gap = 'medium')
    with col[0]:
        In.joist = st.selectbox(h4 + '✦ 장선 규격 [mm]', ('🔲 50×50×2.0t', '🔲 50×50×2.3t'), index = 1, label_visibility='collapsed')
    with col[1]:
        In.Lj = st.number_input(h4 + '✦ 장선 간격 [mm]', min_value = 10., value = 150., step = 10., format = '%f', label_visibility='collapsed')

    sb.write(h2, '4. 멍에 규격 및 간격 [mm] [SPSR400]')
    col = sb.columns([3,2], gap = 'medium')
    with col[0]:
        In.yoke = st.selectbox(h4 + '✦ 멍에 규격 [mm]', ('🔲 75×125×2.9t', '🔲 75×125×3.2t'), index = 1, label_visibility='collapsed')
    with col[1]:
        In.Ly = st.selectbox(h4 + '✦ 멍에 간격 [mm]*', (1829, 1524, 1219, 914, 610, 305), index = 3, label_visibility='collapsed')

    sb.write(h2, '5. 수직재 규격 및 간격* [mm] [SKT500]')
    col = sb.columns([3,2], gap = 'medium')
    with col[0]:
        In.vertical = st.selectbox(h4 + '✦ 수직재 규격 [mm]', ('🔘 𝜙60.5×2.5t', '🔘 𝜙60.5×2.6t'), index = 1, label_visibility='collapsed')
        st.write('###### $\,$', rf':blue[*수직재 간격 = 수평재 좌굴길이 ($\rm{{KL_h}}$)]')
    with col[1]:
        In.Lv = st.selectbox(h4 + '✦ 수직재 간격 [mm]', (1829, 1524, 1219, 914, 610, 305), index = 3, label_visibility='collapsed')

    sb.write(h2, '6. 수평재 규격 및 간격** [mm] [SKT400]')
    col = sb.columns([3,2], gap = 'medium')
    with col[0]:
        In.horizontal = st.selectbox(h4 + '✦ 수평재 규격 [mm]', ('🔘 𝜙42.7×2.2t', '🔘 𝜙42.7×2.3t'), label_visibility='collapsed')
        st.write('###### $\,$', rf':blue[**수평재 간격 = 수직재 좌굴길이 ($\rm{{KL_v}}$)]')
    with col[1]:
        In.Lh = st.selectbox(h4 + '✦ 수평재 간격 [mm]', (1725, 1291, 863, 432, 216), index = 0, label_visibility='collapsed')

    sb.write(h2, '7. 가새재 규격 [mm] [SKT400]')
    col = sb.columns([3,2], gap = 'medium')
    with col[0]:
        In.bracing = st.selectbox(h4 + '✦ 가새재 규격 [mm]', ('🔘 𝜙42.7×2.2t', '🔘 𝜙42.7×2.3t'), label_visibility='collapsed')

    temp = re.findall(r'\d+\.?\d*', In.joist);  temp = [float(num) for num in temp];  [In.joist_b, In.joist_h, In.joist_t] = temp
    temp = re.findall(r'\d+\.?\d*', In.yoke);   temp = [float(num) for num in temp];  [In.yoke_b,  In.yoke_h,  In.yoke_t] = temp
    
    temp = re.findall(r'\d+\.?\d*', In.vertical);    temp = [float(num) for num in temp];  [In.vertical_d,   In.vertical_t] = temp
    temp = re.findall(r'\d+\.?\d*', In.horizontal);  temp = [float(num) for num in temp];  [In.horizontal_d, In.horizontal_t] = temp
    temp = re.findall(r'\d+\.?\d*', In.bracing);     temp = [float(num) for num in temp];  [In.bracing_d,    In.bracing_t] = temp
    In.KLh = In.Lv;  In.KLv = In.Lh
    
    ### 거푸집 널의 변형기준    
    [col1, col2] = sb.columns([3,2])
    with col1:
        st.write(h2, '8. 거푸집 널의 변형기준 [표면 등급]')
        level = st.radio(h4 + ':green[표면 등급]', ('A급', 'B급', 'C급'), label_visibility='collapsed')
        if 'A' in level:  d1 = 360;  d2 = 3
        if 'B' in level:  d1 = 270;  d2 = 6
        if 'C' in level:  d1 = 180;  d2 = 13        
    with col2:
        st.write('');  In.d1_str = r'$\,\bm{\Large\frac{L_n}{'+str(d1)+'}}$';  In.d2_str = str(d2) + 'mm'
        st.write(h4, '$\quad$➣ 상대변형 :', In.d1_str)
        st.write(h4, '$\quad$➣ 절대변형 :', In.d2_str)
        [In.level, In.d1, In.d2] = [level, d1, d2]

    ### 자중
    sb.write(h2, '9. 자중')
    [col1, col2] = sb.columns(2)
    with col1:
        In.concrete_weight = st.number_input(h4+':green[콘크리트 단위중량 [kN/m³]]', min_value = 10., value = 24., step = 1., format = '%f')
    with col2:
        In.wood_weight = st.number_input(h4+':green[거푸집 단위중량 [kN/m²]]', min_value = 0.1, value = 0.4, step = 0.1, format = '%f')
 
    return In