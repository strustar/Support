import streamlit as st
import re
sb = st.sidebar

class In:
    pass

In.ok = ':blue[∴ OK] (🆗✅)';  In.ng = ':red[∴ NG] (❌)'
In.space = '<div style="margin:0px">'
In.background_color = 'linen'
In.col_span_ref = [1, 1];  In.col_span_okng = [5, 1]  # 근거, OK(NG) 등 2열 배열 간격 설정
In.font_h1 = '28px';  In.font_h2 = '24px';  In.font_h3 = '22px';  In.font_h4 = '20px';  In.font_h5 = '18px';  In.font_h6 = '15px'

color = 'green'
In.border1 = f'<hr style="border-top: 2px solid {color}; margin-top:30px; margin-bottom:30px; margin-right: -30px">'  # 1줄
In.border2 = f'<hr style="border-top: 5px double {color}; margin-top: 0px; margin-bottom:30px; margin-right: -30px">' # 2줄

def word_wrap_style(span, txt, fs):  # 자동 줄바꿈 등    
    return st.markdown(span + f'<div style="white-space:pre-line; display:inline-block; font-size: {fs}; line-height: 1.8; text-indent: 0em">{txt}</div>', unsafe_allow_html=True)    
    # return st.markdown(span + f'<span style="white-space:pre-line; display:inline; font-size: {fs}; line-height: 2; padding-left: 0px; text-indent: 10em">{txt}</span>', unsafe_allow_html=True)    

##### sidebar =======================================================================================================
def Sidebar(h4, h5):
    sb.write(h4, '✤ 선택 [Ⅰ, Ⅱ, Ⅲ, Ⅳ, Ⅴ]')
    In.select = sb.selectbox(h5 + '✦ 숨김', ('Ⅰ. 일반 사항 📝✍️', 'Ⅱ. 구조 검토 💻⭕', 'Ⅲ. 요약 ✅', 'Ⅳ. 상세 해석 🎯', 'Ⅴ. 참고'), index = 1, label_visibility='collapsed')
    
    sb.write(h4, '✤ 공사명')    
    In.title = sb.text_input('숨김', placeholder='공사명을 입력하세요', label_visibility='collapsed')

    sb.write(h4, '✤ 검토 유형')    
    In.type = sb.radio('숨김', ('슬래브', '보 (단멍에)', '기타(작성중...)'), horizontal=True, label_visibility='collapsed')

    border = '<hr style="border-top: 2px solid purple; margin-top:15px; margin-bottom:15px;">'
    sb.markdown(border, unsafe_allow_html=True)
    
    ### 슬라브 or 보 (￭)
    sb.write(h4, '1. ' + In.type)
    [col1, col2, col3] = sb.columns(3, gap = 'medium')
    with col1:
        if '슬래브' in In.type:  In.slab_t = st.number_input(h5 + '✦ 두께 [mm]', min_value = 50., value = 400., step = 10., format = '%0.f')
        if '보' in In.type:
            In.beam_b = st.number_input(h5 + '✦ 보의 폭 [mm]', min_value = 50., value = 500., step = 10., format = '%f')
            In.beam_h = st.number_input(h5 + '✦ 보의 높이 [mm]', min_value = 50., value = 900., step = 10., format = '%f')        
        # In.height = st.number_input(h5 + '✦ 층고 [mm]', min_value = 100., value = 9500., step = 100., format = '%f')
    with col2:
        In.slab_X = st.number_input(h5 + '✦ X 방향 길이 [m]', min_value = 1., value = 8., step = 0.1, format = '%.1f')        
        
    with col3:
        In.slab_Y = st.number_input(h5 + '✦ Y 방향 길이 [m]', min_value = 1., value = 8., step = 0.1, format = '%.1f')
    In.thick_height = In.slab_t if '슬래브' in In.type else In.beam_h    

    ### 거푸집용 합판
    sb.write(h4, '2. 거푸집용 합판')    
    [col1, col2] = sb.columns([3,2], gap = "medium")
    with col1:
        In.wood_t = st.radio(h5 + '￭ 합판 두께 [mm]', (12, 15, 18), horizontal=True)
    with col2:
        In.wood_angle = st.radio(h5 + '￭ 하중 방향 [각도]', (0, 90), horizontal=True, index = 1)
    In.wood = str(In.wood_t)+' / '+str(In.wood_angle)+'°'

    sb.write(h4, '3. 장선 규격 및 간격 [mm] [SPSR400]')  # 🔳🔘
    col = sb.columns([3,2], gap = 'medium')
    with col[0]:
        In.joist = st.selectbox(h5 + '✦ 장선 규격 [mm]', ('🔲 50×50×2.0t', '🔲 50×50×2.3t'), index = 1, label_visibility='collapsed')
    with col[1]:
        In.Lj = st.number_input(h5 + '✦ 장선 간격 [mm]', min_value = 10., value = 150., step = 10., format = '%f', label_visibility='collapsed')

    sb.write(h4, '4. 멍에 규격 및 간격 [mm] [SPSR400]')
    col = sb.columns([3,2], gap = 'medium')
    with col[0]:
        In.yoke = st.selectbox(h5 + '✦ 멍에 규격 [mm]', ('🔲 75×125×2.9t', '🔲 75×125×3.2t'), index = 1, label_visibility='collapsed')
    with col[1]:
        In.Ly = st.selectbox(h5 + '✦ 멍에 간격 [mm]*', (1829, 1524, 1219, 914, 610, 305), index = 3, label_visibility='collapsed')

    sb.write(h4, '5. 수직재 규격 및 간격* [mm] [SKT500]')
    col = sb.columns([3,2], gap = 'medium')
    with col[0]:
        In.vertical = st.selectbox(h5 + '✦ 수직재 규격 [mm]', ('🔘 𝜙60.5×2.5t', '🔘 𝜙60.5×2.6t'), index = 1, label_visibility='collapsed')
        st.write('###### $\,$', rf':blue[*수직재 간격 = 수평재 좌굴길이 ($\rm{{KL_h}}$)]')
    with col[1]:
        In.Lv = st.selectbox(h5 + '✦ 수직재 간격 [mm]', (1829, 1524, 1219, 914, 610, 305), index = 3, label_visibility='collapsed')

    sb.write(h4, '6. 수평재 규격 및 간격** [mm] [SKT400]')
    col = sb.columns([3,2], gap = 'medium')
    with col[0]:
        In.horizontal = st.selectbox(h5 + '✦ 수평재 규격 [mm]', ('🔘 𝜙42.7×2.2t', '🔘 𝜙42.7×2.3t'), label_visibility='collapsed')
        st.write('###### $\,$', rf':blue[**수평재 간격 = 수직재 좌굴길이 ($\rm{{KL_v}}$)]')
    with col[1]:
        In.Lh = st.selectbox(h5 + '✦ 수평재 간격 [mm]', (1725, 1291, 863, 432, 216), index = 0, label_visibility='collapsed')

    sb.write(h4, '7. 가새재 규격 [mm] [SKT400]')
    col = sb.columns([3,2], gap = 'medium')
    with col[0]:
        In.bracing = st.selectbox(h5 + '✦ 가새재 규격 [mm]', ('🔘 𝜙42.7×2.2t', '🔘 𝜙42.7×2.3t'), label_visibility='collapsed')

    temp = re.findall(r'\d+\.?\d*', In.joist);  temp = [float(num) for num in temp];  [In.joist_b, In.joist_h, In.joist_t] = temp
    temp = re.findall(r'\d+\.?\d*', In.yoke);   temp = [float(num) for num in temp];  [In.yoke_b,  In.yoke_h,  In.yoke_t] = temp
    
    temp = re.findall(r'\d+\.?\d*', In.vertical);    temp = [float(num) for num in temp];  [In.vertical_d,   In.vertical_t] = temp
    temp = re.findall(r'\d+\.?\d*', In.horizontal);  temp = [float(num) for num in temp];  [In.horizontal_d, In.horizontal_t] = temp
    temp = re.findall(r'\d+\.?\d*', In.bracing);     temp = [float(num) for num in temp];  [In.bracing_d,    In.bracing_t] = temp
    In.KLh = In.Lv;  In.KLv = In.Lh
    
    ### 거푸집 널의 변형기준    
    [col1, col2] = sb.columns([3,2])
    with col1:
        st.write(h4, '8. 거푸집 널의 변형기준 [표면 등급]')
        level = st.radio(h5 + ':green[표면 등급]', ('A급', 'B급', 'C급'), label_visibility='collapsed')
        if 'A' in level:  d1 = 360;  d2 = 3
        if 'B' in level:  d1 = 270;  d2 = 6
        if 'C' in level:  d1 = 180;  d2 = 13        
    with col2:
        st.write('');  In.d1_str = r'$\,\bm{\Large\frac{L_n}{'+str(d1)+'}}$';  In.d2_str = str(d2) + 'mm'
        st.write(h5, '$\quad$➣ 상대변형 :', In.d1_str)
        st.write(h5, '$\quad$➣ 절대변형 :', In.d2_str)
        [In.level, In.d1, In.d2] = [level, d1, d2]

    ### 자중
    sb.write(h4, '9. 자중')
    [col1, col2] = sb.columns(2)
    with col1:
        In.concrete_weight = st.number_input(h5+':green[콘크리트 단위중량 [kN/m³]]', min_value = 10., value = 24., step = 1., format = '%f')
    with col2:
        In.wood_weight = st.number_input(h5+':green[거푸집 단위중량 [kN/m²]]', min_value = 0.1, value = 0.4, step = 0.1, format = '%f')
 
    return In