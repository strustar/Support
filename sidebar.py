import streamlit as st
import re
sb = st.sidebar
class In:
    pass
In.ok = ':blue[OK] (🆗✅)'
In.ng = '∴ :red[NG] (❌)'

##### sidebar =======================================================================================================
def Sidebar(h2, h4):    
    sb.write(h2, '✤ 공사명')    
    In.title = sb.text_input('숨김', placeholder='공사명을 입력하세요', label_visibility='collapsed')

    sb.write(h2, '✤ 검토 유형')    
    In.type = sb.radio('숨김', ('슬래브', '보하부', '기타(작성중...)'), horizontal=True, label_visibility='collapsed', key='0')

    border = '<hr style="border-top: 2px solid purple; margin-top:15px; margin-bottom:15px;">'
    sb.markdown(border, unsafe_allow_html=True)
    
    ### 슬라브 or 보하부 (￭)
    sb.write(h2, '1. ' + In.type)
    [col1, col2, col3] = sb.columns(3, gap = 'medium')
    with col1:
        In.height = st.number_input(h4 + '✦ 층고 [mm]', min_value = 100., value = 9500., step = 100., format = '%f')
    with col2:
        if '슬래브' in In.type:  In.slab_t = st.number_input(h4 + '✦ 두께 [mm]', min_value = 50., value = 400., step = 10., format = '%f')
        if '보하부' in In.type:  In.beam_b = st.number_input(h4 + '✦ 보의 폭 [mm]', min_value = 50., value = 500., step = 10., format = '%f')
    with col3:
        if '슬래브' not in In.type:  In.beam_h = st.number_input(h4 + '✦ 보의 높이 [mm]', min_value = 50., value = 900., step = 10., format = '%f')
    In.thick_height = In.slab_t if '슬래브' in In.type else In.beam_h    

    ### 거푸집용 합판
    sb.write(h2, '2. 거푸집용 합판')    
    [col1, col2] = sb.columns([3,2], gap = "medium")
    with col1:
        In.wood_t = st.radio(h4 + '￭ 합판 두께 [mm]', (12, 15, 18), horizontal=True)
    with col2:
        In.wood_angle = st.radio(h4 + '￭ 하중 방향 [각도]', (0, 90), horizontal=True, index = 1)

    ### 장선 & 멍에, 수직재, 수평재, 가새재
    col = sb.columns(2, gap = 'medium')
    with col[0]:
        st.write(h2, '3. 장선 & 멍에')  # 🔳🔘
        In.joist = st.selectbox(h4 + '✦ 장선 규격 [mm] [SPSR400]', ('🔲 50×50×2.0t', '🔲 50×50×2.3t'), index = 1)
        In.yoke = st.selectbox(h4 + '✦ 멍에 규격 [mm] [SPSR400]', ('🔲 75×125×2.9t', '🔲 75×125×3.2t'), index = 1)
    with col[1]:
        st.write(h2, '4. 수직재, 수평재, 가새재')
        In.vertical = st.selectbox(h4 + '✦ 수직재 규격 [mm] [SKT500]', ('🔘 𝜙60.5×2.5t', '🔘 𝜙60.5×2.6t'), index = 1)        
        In.horizontal = st.selectbox(h4 + '✦ 수평재 규격 [mm] [SKT400]', ('🔘 𝜙42.7×2.2t', '🔘 𝜙42.7×2.3t'))
        In.bracing = st.selectbox(h4 + '✦ 가새재 규격 [mm] [SKT400]', ('🔘 𝜙42.7×2.2t', '🔘 𝜙42.7×2.3t'))

    temp = re.findall(r'\d+\.?\d*', In.joist);  temp = [float(num) for num in temp];  [In.joist_b, In.joist_h, In.joist_t] = temp
    temp = re.findall(r'\d+\.?\d*', In.yoke);   temp = [float(num) for num in temp];  [In.yoke_b,  In.yoke_h,  In.yoke_t] = temp
    
    temp = re.findall(r'\d+\.?\d*', In.vertical);    temp = [float(num) for num in temp];  [In.vertical_d,   In.vertical_t] = temp
    temp = re.findall(r'\d+\.?\d*', In.horizontal);  temp = [float(num) for num in temp];  [In.horizontal_d, In.horizontal_t] = temp
    temp = re.findall(r'\d+\.?\d*', In.bracing);     temp = [float(num) for num in temp];  [In.bracing_d,    In.bracing_t] = temp
    
    ### 간격
    sb.write(h2, ':blue[5. 간격 설정]')
    col = sb.columns(3, gap = 'medium')
    with col[0]:
        In.Lj = st.number_input(h4 + '✦ 장선 간격 [mm]', min_value = 10., value = 150., step = 10., format = '%f')
    with col[1]:
        In.Ly = st.selectbox(h4 + '✦ 멍에 간격 [mm]*', (1829, 1524, 1219, 914, 610, 305), index = 3)
        st.write('###### $\,$', rf':blue[*멍에 간격 = 수직재 간격 = 수평재 좌굴길이 ($\rm{{KL_h}}$)]')
        st.write('###### $\,$', rf':blue[**수평재 간격 = 수직재 좌굴길이 ($\rm{{KL_v}}$)]')
    with col[2]:
        In.Lh = st.selectbox(h4 + '✦ 수평재 간격 [mm]**', (1725, 1291, 863, 432, 216), index = 0)
        In.Ls = In.Ly;  In.KLh = In.Ly;  In.KLv = In.Lh
    
    ### 거푸집 널의 변형기준
    sb.write(h2, ':blue[6. 거푸집 널의 변형기준]')
    [col1, col2] = sb.columns([1.5, 1])
    with col1:        
        level = st.radio(h4 + ':green[표면 등급]', ('A급', 'B급', 'C급'))
        if 'A' in level:  d1 = 360;  d2 = 3
        if 'B' in level:  d1 = 270;  d2 = 6
        if 'C' in level:  d1 = 180;  d2 = 13        
    with col2:
        st.write('');  In.d1_str = r'$\,\bm{\Large\frac{L_n}{'+str(d1)+'}}$';  In.d2_str = str(d2) + 'mm'
        st.write(h4, '$\quad$➣ 상대변형 :', In.d1_str)
        st.write(h4, '$\quad$➣ 절대변형 :', In.d2_str)
        [In.level, In.d1, In.d2] = [level, d1, d2]

    ### 자중
    sb.write(h2, ':blue[7. 자중]')
    [col1, col2] = sb.columns(2)
    with col1:
        In.concrete_weight = st.number_input(h4+':green[콘크리트 단위중량 [kN/m³]]', min_value = 10., value = 24., step = 1., format = '%f')
    with col2:
        In.wood_weight = st.number_input(h4+':green[거푸집 단위중량 [kN/m²]]', min_value = 0.1, value = 0.4, step = 0.1, format = '%f')
 
    return In