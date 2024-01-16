import streamlit as st
import re

class In:
    pass

In.ok = ':blue[∴ OK] (🆗✅)';  In.ng = ':red[∴ NG] (❌)'
In.space = '<div style="margin:0px">'
In.background_color = 'linen'
In.col_span_ref = [1, 1];  In.col_span_okng = [5, 1]  # 근거, OK(NG) 등 2열 배열 간격 설정
In.font_h1 = '30px';  In.font_h2 = '28px';  In.font_h3 = '26px';  In.font_h4 = '24px';  In.font_h5 = '20px';  In.font_h6 = '16px'

color = 'green'
In.border1 = f'<hr style="border-top: 2px solid {color}; margin-top:30px; margin-bottom:30px; margin-right: -30px">'  # 1줄
In.border2 = f'<hr style="border-top: 5px double {color}; margin-top: 0px; margin-bottom:30px; margin-right: -30px">' # 2줄
In.bracing_analysis = 'NO : 없음(상세구조해석에서 없음)'  # or OK

def word_wrap_style(span, txt, fs):  # 자동 줄바꿈 등    
    return st.markdown(span + f'<div style="white-space:pre-line; display:inline-block; font-size: {fs}; line-height: 1.8; text-indent: 0em; text-align: justify">{txt}</div>', unsafe_allow_html=True)    
    # return st.markdown(span + f'<span style="white-space:pre-line; display:inline; font-size: {fs}; line-height: 2; padding-left: 0px; text-indent: 10em">{txt}</span>', unsafe_allow_html=True)    

sb = st.sidebar
side_border = '<hr style="border-top: 2px solid purple; margin-top:15px; margin-bottom:15px;">'
##### sidebar =======================================================================================================
def Sidebar(h4, h5):
    html_code = "<span style='background-color: yellow; font-size: 20px'> 문의 사항은 언제든지 아래 이메일로 문의 주세요^^</span>"
    st.sidebar.markdown(html_code, unsafe_allow_html=True)
    html_code = "<span style='background-color: yellow; font-size: 20px'> 📧📬 : strustar@konyang.ac.kr (건양대 손병직)</span>"
    st.sidebar.markdown(html_code, unsafe_allow_html=True)

    h4 = h5
    sb.write('# ', ':blue[[Information : 입력값 📘]]')
    sb.write(h4, '✤ 선택 [Ⅰ, Ⅱ, Ⅲ, Ⅳ, Ⅴ]')
    In.select = sb.selectbox(h5 + '✦ 숨김', ('O. 표지 및 목차 📝', 'Ⅰ. 일반 사항 ✍️', 'Ⅱ. 구조 검토 💻⭕', 'Ⅲ. 상세 구조해석 🎯', 'Ⅳ. 검토 결과 ✅', '[부 록]', '[전체 보고서]'), index = 6, label_visibility='collapsed')
    
    # sb.write(h4, '✤ 공사명')
    # In.title = sb.text_input('숨김', placeholder='공사명을 입력하세요', label_visibility='collapsed')

    sb.write(h4, '✤ 검토 유형 [시스템 동바리 & 시스템 비계]')
    In.type = sb.radio('숨김', ('슬래브', '보 (단멍에)', '시스템 비계'), horizontal=True, label_visibility='collapsed', index=1)

    if 'dddcc/' in In.type:
    # if '비계/' in In.type:
        pass
    else:   # 동바리
        ### 슬라브 or 보 (￭)
        sb.markdown(side_border, unsafe_allow_html=True)   #  구분선 ------------------------------------
        sb.write(h4, ':green[✤ ' + In.type + ']')
        [col1, col2, col3] = sb.columns(3, gap = 'medium')    
        with col1:
            if '슬래브' in In.type:  In.slab_t = st.number_input(h5 + '✦ 두께 [mm]', min_value = 50., value = 400., step = 10., format = '%0.f')
            else:  # if '보' in In.type:
                In.beam_b = st.number_input(h5 + '✦ 보의 폭 [mm]', min_value = 50., value = 600., step = 10., format = '%f')
                In.beam_h = st.number_input(h5 + '✦ 보의 높이 [mm]', min_value = 50., value = 700., step = 10., format = '%f')
        with col2:
            In.slab_X = st.number_input(h5 + '✦ X 방향 길이 [m]', min_value = 0.1, value = 9., step = 0.1, format = '%.1f')        
            
        with col3:
            In.slab_Y = st.number_input(h5 + '✦ Y 방향 길이 [m]', min_value = .1, value = 23.5, step = 0.1, format = '%.1f')
            In.height = st.number_input(h5 + '✦ 높이 [m]', min_value = .1, value = 5.3, step = 0.1, format = '%.1f')
        In.thick_height = In.slab_t if '슬래브' in In.type else In.beam_h

        ### 거푸집용 합판
        sb.markdown(side_border, unsafe_allow_html=True)   #  구분선 ------------------------------------
        sb.write(h4, ':green[✤ ' + '거푸집용 합판 두께 [mm] 및 하중방향 [°]' + ']')
        [col1, col2] = sb.columns([3,2], gap = "medium")
        with col1:
            In.wood_t = st.radio(h5 + '￭ 합판 두께 [mm]', (12, 15, 18), horizontal=True, label_visibility='collapsed')
        with col2:
            In.wood_angle = st.radio(h5 + '￭ 하중 방향 [각도]', (0, 90), horizontal=True, index = 0, label_visibility='collapsed')
        In.wood = str(In.wood_t)+' / '+str(In.wood_angle)+'°'

        sb.write(h4, ':green[✤ ' + '장선 규격 및 간격 [mm] [SPSR400]' + ']')  # 🔳🔘
        col = sb.columns([3,2], gap = 'medium')
        with col[0]:
            In.joist = st.selectbox(h5 + '✦ 장선 규격 [mm]', ('🔲 50×50×2.0t', '🔲 50×50×2.3t'), index = 0, label_visibility='collapsed')
        with col[1]:
            In.Lj = st.number_input(h5 + '✦ 장선 간격 [mm]', min_value = 10., value = 215., step = 10., format = '%f', label_visibility='collapsed')

        sb.write(h4, ':green[✤ ' + '멍에 규격 및 간격 [mm] [SPSR400]' + ']')
        col = sb.columns([3,2], gap = 'medium')
        with col[0]:
            In.yoke = st.selectbox(h5 + '✦ 멍에 규격 [mm]', ('🔲 75×125×2.9t', '🔲 75×125×3.2t'), index = 0, label_visibility='collapsed')
        with col[1]:
            In.Ly = st.selectbox(h5 + '✦ 멍에 간격 [mm]*', (1829, 1524, 1219, 914, 610, 305), index = 4, label_visibility='collapsed')

        sb.write(h4, ':green[✤ ' + '수직재 규격 및 간격* [mm] [STK500]' + ']')
        col = sb.columns([3,2], gap = 'medium')
        with col[0]:
            In.vertical = st.selectbox(h5 + '✦ 수직재 규격 [mm]', ('🔘 𝜙60.5×2.5t', '🔘 𝜙60.5×2.6t'), index = 1, label_visibility='collapsed')
            st.write('###### $\,$', rf':blue[*수직재 간격 = 수평재 좌굴길이 ($\rm{{KL_h}}$)]')
        with col[1]:
            In.Lv = st.selectbox(h5 + '✦ 수직재 간격 [mm]', (1829, 1524, 1219, 914, 610, 305), index = 2, label_visibility='collapsed')

        sb.write(h4, ':green[✤ ' + '수평재 규격 및 간격** [mm] [STK400]' + ']')
        col = sb.columns([3,2], gap = 'medium')
        with col[0]:
            In.horizontal = st.selectbox(h5 + '✦ 수평재 규격 [mm]', ('🔘 𝜙42.7×2.2t', '🔘 𝜙42.7×2.3t'), index = 0, label_visibility='collapsed')
            st.write('###### $\,$', rf':blue[**수평재 간격 = 수직재 좌굴길이 ($\rm{{KL_v}}$)]')
        with col[1]:
            In.Lh = st.selectbox(h5 + '✦ 수평재 간격 [mm]', (1725, 1291, 863, 432, 216), index = 0, label_visibility='collapsed')

        sb.write(h4, ':green[✤ ' + '가새재 규격 [mm] [STK400]' + ']')
        col = sb.columns([3,2], gap = 'medium')
        with col[0]:
            In.bracing = st.selectbox(h5 + '✦ 가새재 규격 [mm]', ('🔘 𝜙42.7×2.2t', '🔘 𝜙42.7×2.3t'), index = 0, label_visibility='collapsed')

        temp = re.findall(r'\d+\.?\d*', In.joist);  temp = [float(num) for num in temp];  [In.joist_b, In.joist_h, In.joist_t] = temp
        temp = re.findall(r'\d+\.?\d*', In.yoke);   temp = [float(num) for num in temp];  [In.yoke_b,  In.yoke_h,  In.yoke_t] = temp
        
        temp = re.findall(r'\d+\.?\d*', In.vertical);    temp = [float(num) for num in temp];  [In.vertical_d,   In.vertical_t] = temp
        temp = re.findall(r'\d+\.?\d*', In.horizontal);  temp = [float(num) for num in temp];  [In.horizontal_d, In.horizontal_t] = temp
        temp = re.findall(r'\d+\.?\d*', In.bracing);     temp = [float(num) for num in temp];  [In.bracing_d,    In.bracing_t] = temp
        In.KLh = In.Lv;  In.KLv = In.Lh
        
        ### 거푸집 널의 변형기준
        sb.markdown(side_border, unsafe_allow_html=True)   #  구분선 ------------------------------------
        [col1, col2] = sb.columns([3,2])
        with col1:            
            st.write(h4, ':green[✤ ' + '거푸집 널의 변형기준 [표면 등급]' + ']')
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
        sb.markdown(side_border, unsafe_allow_html=True)   #  구분선 ------------------------------------
        sb.write(h4, ':green[✤ ' + '자중' + ']')
        [col1, col2] = sb.columns(2)
        with col1:
            In.concrete_weight = st.number_input('###### ￭ 콘크리트 단위중량 [kN/m³]', min_value = 10., value = 24., step = 1., format = '%.1f')
        with col2:
            In.wood_weight = st.number_input('###### ￭ 거푸집 단위중량 [kN/m²]', min_value = 0.1, value = 0.4, step = 0.1, format = '%.1f')

        ### 풍하중
        sb.markdown(side_border, unsafe_allow_html=True)   #  구분선 ------------------------------------
        sb.write('#### :green[✤ ' + '풍하중 [KDS 41 12 00, 5. 풍하중]' + ']')
        sb.write(r'##### 1. 설계풍속 [5.5.1] : $\bm{{\small{{V_{H} = V_{0} K_{D} K_{zr} K_{zt} I_{W}(T) }} }}$ [m/s]')
        col = sb.columns([1, 1])
        with col[0]:
            In.V0 = st.number_input('##### ' + r'￭ $\bm{{\small{{V_{0}}} }}$ [5.5.2]', value = 36., step = 2., format = '%.1f')
            st.write('###### :blue[기본풍속 [m/s]]')
            st.write('###### :blue[내륙 지역 : 28 ~ 42 m/s 분포]')
            st.write('###### :blue[섬 지역 : 46 ~ 50 m/s 분포]')            
        with col[1]:
            In.KD = st.number_input('##### ' + r'￭ $\bm{{\small{{K_{D}}} }}$ [5.5.3]', value = 1., step = 0.05, format = '%.2f')
            st.write('###### :blue[풍향계수 : 최솟값 0.85]')

        In.Kzr_txt = sb.selectbox('##### ' + '￭ 지표면조도구분 [5.5.4]', ['A : 대도시 중심부에서 고층건축구조물(10층 이상)이 밀집해 있는 지역', 'B : 수목⋅높이 3.5m 정도의 주택과 같은 건축구조물이 밀집해 있는 지역, 중층건물(4~9층)이 산재해 있는 지역', 'C : 높이 1.5~10 m 정도의 장애물이 산재해 있는 지역, 수목⋅저층건축구조물이 산재해 있는 지역', 'D : 장애물이 거의 없고, 주변 장애물의 평균높이가 1.5 m 이하인 지역, 해안, 초원, 비행장'], index=2)
        sb.write(r'###### :blue[풍속고도분포계수 ($\bm{{\small{{K_{zr}}} }}$) 산정 : 최댓값 1.765]')
        
        col = sb.columns([1, 1])
        with col[0]:
            In.Kzt = st.number_input('##### ' + r'￭ $\bm{{\small{{K_{zt}}} }}$ [5.5.5]', value = 1., step = 0.1, format = '%.1f')
            st.write('###### :blue[지형계수 : 평탄한 지형 1.0]')            
        with col[1]:
            In.N = st.number_input('##### ' + r'￭ 존치기간 (N) [년] [5.5.6]', value = 1.0, step = 0.5, format = '%.1f')
            st.write(r'###### :blue[중요도계수 ($\bm{{\small{{I_{W}}} }}$) 산정]')
            st.write(r'###### :blue[KDS 21 50 00, 1.6.4]')
            st.write(r'###### :blue[존치기간이 1년 이하의 경우 : 0.60]')

        sb.write('')
        sb.write(r'##### 2. 가스트영향계수 [5.6.2] : $\bm{{\small{{G_{D} = 1 + 4 \, \gamma_{D} \sqrt{B_{D}} }} }}$')
        sb.write(r'###### :blue[- 건축구조물의 풍방향 고유진동수($\bm{{\small{{n_{D}}} }}$)가 1Hz를 초과하는 경우 (대부분)]')
        sb.write('###### :blue[- 바람에 의한 동적 효과를 무시할 수 있는 강체 건축구조물 등]')
        sb.write('###### :blue[- 지표면조도구분 [5.5.4] 등이 결정되면 자동 계산]')

        if '비계' in In.type:
            sb.write('')
            sb.write(r'##### 3. 풍력계수 : $\bm{{\small{{C_{f} = (0.11 + 0.09\, \gamma + 0.945 C_{0} R)F }} }}$')
            sb.write('###### :blue[- 비계의 경우만 해당 [KDS 21 60 00, 1.6.4]]')
            col = sb.columns([1, 1])
            with col[0]:
                In.phi = st.number_input('##### ' + r'￭ 충실률 ($\bm{{\small{{\phi}} }}$)', value = 0.3, step = 0.05, format = '%.2f')            
                st.write(r'###### :blue[충실률 : 유효수압면적 / 외곽 전면적]')
                st.write(r'###### :blue[풍력저감계수($\bm{{\small{{\gamma}} }}$)와 기본풍력계수($\bm{{\small{{C_{0}}} }}$) 산정시 이용]')
            
            In.gamma = sb.selectbox('##### ' + r'￭ 풍력저감계수 ($\bm{{\small{{\gamma}} }}$)',['① 쌍줄비계에서 후면비계에 적용하는 풍력저감계수', '② 쌍줄비계의 전면이나 외줄비계에 적용하는 풍력저감계수' ], index=0)
            sb.write(r'###### :blue[①의 경우 : $\bm{{\small{{\gamma = 1 - \phi}} }}$]')
            sb.write(r'###### :blue[②의 경우 : $\bm{{\small{{\gamma = 0}} }}$]')

            In.Rsh = sb.selectbox('##### ' + '￭ 형상보정계수 (R)',['① 망이나 패널이 지면과 공간을 두고 설치되는 경우', '② 망이나 패널이 지면에 붙어서 설치되는 경우' ], index=0)
            sb.write(r'###### :blue[형상보정계수 : 0.6 ~ 1.0 사이의 값을 가짐]')

            In.F = sb.selectbox('##### ' + '￭ 비계 위치에 대한 보정계수 (F)',['① 독립적으로 지지되는 비계 (정압, 부압)', '② 구조물에 지지되는 비계 (정압, 부압)' ], index=0)
            sb.write(r'###### :blue[①의 경우 (정압, 부압) : F = 1.0]')
            sb.write(r'###### :blue[②의 경우 (정압): F = 1.0 ~ (1.0 + 0.31$\bm{{\small{{\phi}} }}$)]')
            sb.write(r'###### :blue[②의 경우 (부압): F = (-1.0 + 0.38$\bm{{\small{{\phi}} }}$) ~ -1.0]')
        

    return In