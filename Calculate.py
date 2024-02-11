import streamlit as st
import numpy as np
from Sidebar import word_wrap_style
import Table, userFcn

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$';  s4 = h5 + '$\qquad \qquad$'

def Info(In, Wood, Joist, Waling, Yoke, Vertical, Horizontal, Bracing):    
    ###! 설계풍속(qH) 산정용
    z = In.Z
    if 'A' in In.Kzr_txt:
        zb = 20;  Zg = 550;  alpha = 0.33;  Kzr_txt = 'A'
        In.Kzr = 0.58 if z <= zb else 0.22*z**alpha
        Kzr_text = rf'∴ $\small K_{{zr}} = 0.22 z^{{\alpha}} = 0.22 × {z:,.1f}^{{{alpha:.2f}}}$ = {In.Kzr:.2f}'
    if 'B' in In.Kzr_txt:
        zb = 15;  Zg = 450;  alpha = 0.22;  Kzr_txt = 'B'
        In.Kzr = 0.81 if z <= zb else 0.45*z**alpha
        Kzr_text = rf'∴ $\small K_{{zr}} = 0.45 z^{{\alpha}} = 0.45 × {z:,.1f}^{{{alpha:.2f}}}$ = {In.Kzr:.2f}'
    if 'C' in In.Kzr_txt:
        zb = 10;  Zg = 350;  alpha = 0.15;  Kzr_txt = 'C'
        In.Kzr = 1.0 if z <= zb else 0.71*z**alpha
        Kzr_text = rf'∴ $\small K_{{zr}} = 0.71 z^{{\alpha}} = 0.71 × {z:,.1f}^{{{alpha:.2f}}}$ = {In.Kzr:.2f}'
    if 'D' in In.Kzr_txt:
        zb =  5;  Zg = 250;  alpha = 0.10;  Kzr_txt = 'D'
        In.Kzr = 1.13 if z <= zb else 0.98*z**alpha
        Kzr_text = rf'∴ $\small K_{{zr}} = 0.98 z^{{\alpha}} = 0.98 × {z:,.1f}^{{{alpha:.2f}}}$ = {In.Kzr:.2f}'
    In.Kzr_txt = Kzr_txt
    In.Tw = 1 / (1 - 0.6**(1/In.N))
    In.Iw = 0.60 if In.N <= 1 else 0.56 + 0.1*np.log(In.Tw)

    In.VH = In.V0*In.KD*In.Kzr*In.Kzt*In.Iw
    In.qH = 1.225*In.VH**2 / 2

    ###! 가스트영향계수(GD) 산정용
    B = max(In.X, In.Y);  H = In.Z    
    IH = 0.1*(H/Zg)**(-alpha-0.05) if H > zb else 0.1*(zb/Zg)**(-alpha-0.05)
    LH = 100*(H/30)**(0.5) if H > 30 else 100
    k = 0.33 if H >= B else -0.33
    gammaD = IH*(3 + 3*alpha) / (2 + alpha)
    BD = 1 - 1 / (1 + 5.1*(LH/np.sqrt(H*B))**1.3 * (B/H)**k)**(1/3)
    GD = 1 + 4*gammaD*np.sqrt(BD)
    In.wind2 = In.qH*GD / 1e3   # kN/m2

    ###! 비계의 풍력계수(Cf) 산정용
    if '비계' in In.type:
        gamma = 1 - In.phi if '①' in In.gamma else 0
        if In.phi <= 0.1:
            C0 = 0.1
        elif In.phi <= 0.3:
            C0 = 0.1 + 2*(In.phi - 0.1)
        elif In.phi <= 0.5:
            C0 = 0.5 + 3.5*(In.phi - 0.3)
        elif In.phi <= 0.7:
            C0 = 1.2 + 2*(In.phi - 0.5)
        elif In.phi <= 1.0:
            C0 = 1.6 + 4/3*(In.phi - 0.7)
        
        if '①' in In.Rsh:
            Rsh = 0.5813 + 0.013*(In.Lv/In.Lh) - 0.0001*(In.Lv/In.Lh)**2
            txt = 'l/h'
        if '②' in In.Rsh:
            Rsh = 0.5813 + 0.013*(2*In.Z*1e3/In.Lv) - 0.0001*(2*In.Z*1e3/In.Lv)**2
            txt = '2H/l'
        if Rsh < 0.58: Rsh = 0.58
        if Rsh > 1.0: Rsh = 1.0
        F = 1 + 0.31*In.phi
        In.Cf = (0.11 + 0.09*gamma + 0.945*C0*Rsh)*F
        In.wind2 = In.qH*GD*In.Cf / 1e3   # kN/m2
    
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.title(':blue[Ⅱ. 구조 검토 ✍️]')
    st.markdown(In.border2, unsafe_allow_html=True) ########### border ##########

    st.write(h4, '1. 설계조건')
    if '비계' in In.type:
        col = st.columns([1.2, 1])
        In.fastener_Ly = In.fastener_Ny*In.Lw
        In.fastener_Lz = In.fastener_Nz*In.Lh
        In.fastener_Lz1 = In.Lbottom + (In.fastener_Nz - 1)*In.Lh
        with col[0]:
            st.write(s1, '✦ 수직재 간격 (작업발판 규격)')
            st.write(s2, f'￭ 장선방향 간격 : {In.Lj:,.0f} mm')
            st.write(s2, f'￭ 띠장방향 간격 : {In.Lw:,.0f} mm (= 수평재 좌굴길이)')
            st.write(s1, '✦ 수평재 간격 (작업발판 규격)')
            st.write(s2, f'￭ 기준층 높이 : {In.Lh:,.0f} mm (= 수직재 좌굴길이)')
            st.write(s2, f'￭ 최하층 높이 : {In.Lbottom:,.0f} mm')
            st.write(s1, '✦ 벽연결용 철물 설치 간격')
            st.write(s2, f'￭ 띠장방향 : {In.fastener_Ly:,.0f} mm')
            st.write(s2, f'￭ 높이방향 : {In.fastener_Lz1:,.0f} mm (처음 간격), {In.fastener_Lz:,.0f} mm')

            st.write('')  ## 빈줄 공간
            st.write(s1, f'✦ 비계 스팬 : {In.X*1e3:,.0f} mm × {In.Y*1e3:,.0f} mm × {In.Z*1e3:,.0f} mm')
            st.write(s1, '&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [장선방향 길이 × 띠장방향 길이 × 높이]')            
            st.write(s1, f'✦ 작업발판 중량 : {In.working_weight1:,.2f} kN/m²')
            st.write(s1, f'✦ 작업하중 : {In.working_weight2:,.2f} kN/m² (:blue[{In.working_txt}])')
        with col[1]:
            st.image('Images/scaffolding.png', width=470)
        
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        st.write(h4, '2. 설계하중 산정')
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '1) 연직하중 (고정하중 + 작업하중)')
        with col2: st.write(h5, ':orange[ <근거 : 1.6.2 연직하중 (KDS 21 60 00 : 2022)>]')

        st.write(s2, '➣ 고정하중은 비계 자중과 작업발판의 자중을 합한 하중이다.')
        st.write(s3, '￭ 비계 자중은 수평하중 산정 및 수직재 검토시 필요함')
        word_wrap_style(s2+' ', '➣ 작업하중은 근로자와 근로자가 사용하는 자재, 공구 등을 포함하며, 경작업, 중작업, 돌 붙입 공사 등과 같이 구분하여 적용한다.', In.font_h5)
        st.write(s2, '➣ :blue[발판, 장선, 띠장 검토]를 위한 연직하중 산정')
        Table.Load(In, 'vertical')
        word_wrap_style(s2, '*작업하중은 경작업에 대해서는 :blue[1.25kN/m² 이상], 중작업에 대해서는 :blue[2.5kN/m² 이상], 돌 붙임 공사 등 무거운 작업인 경우 :blue[3.5kN/m² 이상] 적용', '15px')

        st.write('')  ## 빈줄 공간
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '2) 수평하중')
        with col2: st.write(h5, ':orange[ <근거 : 1.6.3 수평하중 (KDS 21 60 00 : 2022)>]')
        
        st.write(s2, '➣ :blue[수평하중 산정 및 수직재 검토]를 위한 연직하중 산정')
        Table.Load(In, 'scaffolding')
        word_wrap_style(s2, rf'$\,$ ➣ 수평하중은 :blue[연직하중의 5%]에 해당하는 수평하중의 영향과 :blue[풍하중에 대한 영향] 중에 :blue[큰 값의 하중]에 대해서 검토한다.', In.font_h5)
        
        Hx = In.wind2*In.Lw*In.Lh / 1e6;  Hy = In.wind2*In.Lj*In.Lh / 1e6
        In.Hx = max(Hx, In.Pv1*0.05);     In.Hy = max(Hy, In.Pv1*0.05)
        st.write(s3, f'① 연직하중의 5% : {In.Pv1:.1f} kN × 5% = {In.Pv1*0.05:,.2f} kN ( = H$_{{x}}$ = H$_{{y}}$)')
        st.write(s3, f'② 풍하중')
        st.write(s4, f'￭ X방향 : H$_x$ = $q_f$ × 띠장방향 간격 × 기준층 높이  = {In.wind2:.3f} × {In.Lw/1e3:,.2f} × {In.Lh/1e3:,.2f} = {Hx:,.2f} kN')
        st.write(s4, f'￭ Y방향 : H$_y$ = $q_f$ × 장선방향 간격 × 기준층 높이  = {In.wind2:.3f} × {In.Lj/1e3:,.2f} × {In.Lh/1e3:,.2f} = {Hy:,.2f} kN')
        st.write(s3, f'✦ 위의 ①, ②중에서 큰 값  ∴ H$_x$ = {In.Hx:.2f} kN, H$_y$ = {In.Hy:.2f} kN')

    else:   # 동바리
        if '슬래브' in In.type:  txt = f'✦ 슬래브 두께 : {In.slab_t:,.0f} mm'
        if '보'     in In.type:  txt = f'✦ 보의 치수 : {In.beam_b:,.0f} mm × {In.beam_h:,.0f} mm &nbsp; [폭 × 높이]'
        st.write(s1, txt)
        st.write(s1, f'✦ 동바리 스팬 : {In.X*1e3:,.0f} mm × {In.Y*1e3:,.0f} mm &nbsp; [X방향 길이 × Y방향 길이]')
        st.write(s1, f'✦ 동바리 높이 : {In.Z*1e3:,.0f} mm')
        st.write(s1, f'✦ 거푸집 널의 변형기준 [표면 등급] : {In.level}')
        st.write(s1, f'✦ 콘크리트 단위중량 : {In.concrete_weight:,.1f} kN/m³')
        st.write(s1, f'✦ 거푸집 단위중량 : {In.wood_weight:,.1f} kN/m²')
        
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        st.write(h4, '2. 설계하중 산정')
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '1) 연직하중 (고정하중 + 작업하중)')
        with col2: st.write(h5, ':orange[ <근거 : 1.6.2 연직하중 (KDS 21 50 00 : 2022)>]')

        st.write(s2, '➣ 고정하중은 철근콘크리트와 거푸집의 무게를 합한 하중이다.')    
        word_wrap_style(s2+' ', '➣ 작업하중은 작업원, 경량의 장비하중, 충격하중, 기타 콘크리트 타설에 필요한 자재 및 공구 등의 하중을 포함한다.', In.font_h5)
        Table.Load(In, 'vertical')
        word_wrap_style(s2, '*작업하중은 콘크리트 타설 높이가 0.5m 미만인 경우 :blue[2.5kN/m²], 0.5m 이상 1m 미만인 경우 :blue[3.5kN/m²], 1m 이상인 경우 :blue[5kN/m² 이상] 적용', '15px')
        
        st.write('')  ## 빈줄 공간
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '2) 수평하중')
        with col2: st.write(h5, ':orange[ <근거 : 1.6.5 수평하중 (KDS 21 50 00 : 2022)>]')    
        
        word_wrap_style(s2, rf'$\,$ ➣ 수평하중은 :blue[고정하중의 2% 이상], 수평방향으로 단위길이당 :blue[1.5kN/m 이상] 중에 :blue[큰 값의 하중]이 상단에 작용하는 것으로 한다.', In.font_h5)
        st.write(s2, f'➣ 고정하중의 2% : (콘크리트 자중 + 거푸집 자중) × 0.02 = {In.dead_load*1e3:.1f} kN/m² × 0.02 = {In.dead_load*1e3*0.02:.3f} kN/m²')
        Table.Load(In, 'horizontal')
        st.write(s3, f'￭ ∴ X방향 수평하중 (H$_x$) = {In.Hx:.1f} kN')
        st.write(s3, f'￭ ∴ Y방향 수평하중 (H$_y$) = {In.Hy:.1f} kN')        
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################

    st.write('')  ## 빈줄 공간
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '3) 풍하중')
    if '비계' in In.type:
        with col1: st.write(s2, rf'➣ 설계풍압 : $\small {{p_f =  q_H \; G_D \; C_f}}$ = {In.qH:,.1f} × {GD:.3f} × {In.Cf:.3f} = {In.wind2*1e3:,.1f} N/m$^2$ = {In.wind2:,.3f} kN/m$^2$')
        with col2: st.write(h5, ':orange[<근거 : 1.6.4 풍하중 (KDS 21 60 00 : 2022)>]')
    else:
        with col1: st.write(s2, rf'➣ 설계풍압 : $\small p_f = q_H \; G_D$ = {In.qH:,.1f} × {GD:.3f} = {In.wind2*1e3:,.1f} N/m$^2$ = {In.wind2:,.3f} kN/m$^2$')
        with col2: st.write(h5, ':orange[<근거 : 1.6.4 풍하중 (KDS 21 50 00 : 2022)>]')

    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '① 속도압 ($q_H$)')
    with col2: st.write(h5, ':orange[<근거 : 5.5 속도압 (KDS 41 12 00 : 2022)>]')
    
    st.write(s2, rf'기준높이 $\small H$에서의 속도압($\small q_H$)은 다음과 같이 산정한다.')    
    st.write(s2, rf'➣ $q_{{H}} \; = \; \large{{\frac{{1}}{2}}} \small \, \rho \, V^2_H$ [N/m$^2$] $\; = \; \large{{\frac{{1}}{2}}} \small × 1.225 × {In.VH:.1f}^2$ [N/m$^2$] = {In.qH:,.1f} N/m$^2$ = {In.qH/1e3:,.3f} kN/m$^2$')
    
    st.write(s3, rf'￭ $\rho$ : 공기밀도로써 균일하게 1.225 kg/m$^3$으로 한다.')
    st.write(s3, rf'￭ $\small V_H$ : 설계풍속 [m/s] [5.5.1]')

    st.write('')  ## 빈줄 공간
    if '비계' in In.type:
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.write(s2, rf'➣ $\small{{V_{{H}} \; = \; V_0 \, K_D \, K_{{zr}} \, K_{{zt}} \, I_w(T)}}$ [m/s] = {In.V0:.1f} × {In.KD:.2f} × {In.Kzr:.2f} × {In.Kzt:.2f} × {In.Iw:.2f} = {In.VH:,.1f} m/s')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s3, rf'￭ $\small V_0$ = {In.V0:,.1f}m/s : 기본풍속 [5.5.2]')
    with col2: st.write(h5, ':green[[제주도 등 섬 제외 28~42m/s로 분포]]')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s3, rf'￭ $\small K_D$ = {In.KD:,.2f} : 풍향계수 [5.5.3]')
    with col2: st.write(h5, ':green[[최솟값 0.85]]')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s3, rf'￭ $\small K_{{zr}}$  = {In.Kzr:,.2f} : 풍속고도분포계수 [5.5.4]')
    with col2: st.write(h5, ':green[[최댓값 1.765, 아래 참조]]')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s3, rf'￭ $\small K_{{zt}}$ = {In.Kzt:,.2f} : 지형계수 [5.5.5]')
    with col2: st.write(h5, ':green[[평탄한 지역에 대한 지형계수는 1.0이다]]')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s3, rf'￭ $\small I_w (T)$ = {In.Iw:,.2f} : 건축구조물의 중요도계수')
    with col2: st.write(h5, ':green[[존치기간 1년이하 0.6, 아래 참조]]')
    
    st.write('')  ## 빈줄 공간
    st.write(s2, r'➣ 풍속고도분포계수($\small K_{zr}$)')
    st.write(s3, '￭ 표 5.5-1 지표면조도구분')
    Table.Kzr(In, '표1')
    st.write(s3, r'￭ 표 5.5-2 평탄한 지역에 대한 풍속고도분포계수 $\small K_{zr}$')
    Table.Kzr(In, '표2')
    col = st.columns([1, 2])
    with col[0]:
        st.write(h6, r':blue[$\qquad \qquad 1) \, \small z$ : 지표면에서의 높이 (m)]')
        st.write(h6, r':blue[$\qquad \qquad 2) \, \small z_b$ : 대기경계층시작 높이 (m)]')
    with col[1]:
        st.write(h6, r':blue[$\qquad \qquad 3) \, \small Z_g$ : 기준경도풍 높이 (m)]')
        st.write(h6, r':blue[$\qquad \qquad 4) \, \small \alpha$ : 풍속고도분포지수]')

    if '비계' not in In.type:
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.write(s3, r'￭ 표 5.5-3 $\small z_b, Z_g, \alpha$')
    Table.Kzr(In, '표3')

    if z <= zb:
        st.write(s3, rf'⇒ 지표면조도구분이 :blue[{Kzr_txt}]이고, 높이 $\small z$({z:.1f}m) ≤ $\small z_{{b}}$({zb:.1f}m) 이므로')
        st.write(s3, rf'∴ $\small K_{{zr}}$ = {In.Kzr:.2f}')
    else:
        st.write(s3, rf'⇒ 지표면조도구분이 :blue[{Kzr_txt}]이고, 높이 $\small z_{{b}}$({zb:.1f}m) ≤ z({z:.1f}m) ≤ $\small Z_{{g}}$({Zg:.1f}m) 이므로')
        st.write(s3, Kzr_text)

    st.write('')  ## 빈줄 공간
    if '비계' in In.type:
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s2, r'➣ 가시설물의 재현기간에 따른 중요도계수($\small I_w$)')
    with col2: st.write(h5, ':orange[<근거 : 1.6.4 풍하중 (KDS 21 50 00 : 2022)>]')    
    st.write(s3, rf'￭ 존치기간(N)이 1년 이하의 경우에는 0.60을 적용하고, 이 외 기간에 대해서는 다음 식에 의해 산정.')
    st.write(s3, rf'￭ $\small I_w = 0.56 + 0.1 \ln(T_w)$')
    st.write(s3, rf'￭ $\small T_{{w}} \; = \; \large{{\frac{{1}}{{1 \,-\, (P)^\frac{{1}}{{N}}}} }}$')
    st.write(s3, rf'￭ $\small T_w$ : 재현기간(년), $\quad \small N$ : 가시설물의 존치기간(년), $\quad \small P$ : 비초과 확률(60%)')
    st.write('')
    if In.N <= 1:
        st.write(s3, rf'⇒ 존치기간(N)이 1년 이하이므로')
        st.write(s3, rf'∴ $\small I_{{W}}$ = {In.Iw:.2f}')
    else:
        st.write(s3, rf'⇒ 존치기간(N)이 1년을 초과하므로 다음과 같이 산정한다.')
        st.write(s3, rf'∴ $\small I_{{W}} = 0.56 + 0.1 \ln(T_W) = 0.56 + 0.1 × \ln({In.Tw:.2f})$ = {In.Iw:.2f}')
        st.write(s3, rf' where, $\left[\small T_{{w}} \; = \; \large{{\frac{{1}}{{1 \,-\, (P)^\frac{{1}}{{N}}}} }}\; \small = \; \large{{\frac{{1}}{{1 \,-\, (0.6)^\frac{{1}}{{{In.N:.1f}}}}} }} \small \;= \;{In.Tw:.2f} \right]$')

    st.write('')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '② 가스트영향계수 ($G_D$)')
    with col2: st.write(h5, ':orange[<근거 : 5.6 가스트영향계수 (KDS 41 12 00 : 2022)>]')    
    word_wrap_style(s2, r'대부분 건축구조물의 풍방향 고유진동수($\small n_D$)가 1Hz를 초과하기 때문에, 바람에 의한 동적 효과를 무시할 수 있는 강체 건축구조물로 볼 수 있다.', In.font_h5)
    st.write(s2, rf'➣ $\small{{G_D = 1 + 4 \, \gamma_D \sqrt{{B_D}} }} = 1 + 4 × {gammaD:.3f} × \sqrt{{{BD:.3f}}} = {GD:.3f}$')
    st.write(s3, rf'￭ $\small \gamma_D$ : 풍속변동계수 [식 5.6-1.c]')
    st.write(s3, rf'￭ $\small B_D$ : 비공진계수 [식 5.6-1.d]')

    st.write('')
    st.write(s2, rf'➣ $\small \gamma_D = \left( \large{{\frac{{3 + 3\alpha}}{{2 + \alpha}} }} \right) I_H = \left( \large{{\frac{{3 + 3 × {alpha:.2f}}}{{2 + {alpha:.2f}}} }} \right) \small × {IH:.3f} = {gammaD:.3f} $')
    st.write(s3, rf'￭ $\small I_H$ : 기준높이(H)에서의 난류강도 [식 5.5-3.a]')
    st.write(s3, r'￭ $I_H = \begin{cases} {\small 0.1 \left( \large \frac{H}{Z_g} \right)^{-\alpha - 0.05} } & \small \text{for} & \small z_b < H ≤ Z_g \\[12pt] {\small 0.1 \left( \large \frac{z_b}{Z_g} \right)^{-\alpha - 0.05} } & \small \text{for} & \small H ≤ z_b \end{cases}$')
    if H > zb:
        st.write(s3, rf'⇒ $\small z_b < H ≤ Z_g$ 이므로')        
        st.write(s3, rf'∴ $\small I_{{H}} = 0.1 \left( \large \frac{{H}}{{Z_g}} \right)^{{-\alpha - 0.05}} = 0.1 × \left( \large \frac{{{H:.1f}}}{{{Zg:.1f}}} \right)^{{{-alpha:.2f} - 0.05}} = {IH:.3f}$')        
    else:
        st.write(s3, rf'⇒ $H ≤ z_b$ 이므로')        
        st.write(s3, rf'∴ $\small I_{{H}} = 0.1 \left( \large \frac{{z_b}}{{Z_g}} \right)^{{-\alpha - 0.05}} = 0.1 × \left( \large \frac{{{zb:.1f}}}{{{Zg:.1f}}} \right)^{{{-alpha:.2f} - 0.05}} = {IH:.3f}$')        
    
    st.write(s2, rf'➣ $\small B_D = 1 - \left[ \large{{\frac{{1}}{{\left[ 1 \; + \; 5.1 \left( \frac{{L_H}}{{\sqrt{{HB}}}} \right)^{{1.3}} \left( \frac{{B}}{{H}} \right)^{{k}} \right]^\frac{{1}}{{3}} }} }} \right] = {BD:.3f} $')
    st.write(s3, rf'￭ $\small L_H$ : 기준높이(H)에서의 난류스케일(m) [식 5.6-1.e]')
    st.write(s3, r'￭ $L_H = \begin{cases} {\small 100 \left( \large \frac{H}{30} \right)^{0.5} } & \small \text{for} & \small 30m < H ≤ Z_g \\[12pt] \small 100 & \small \text{for} & \small H ≤ 30m \end{cases}$')
    if H > 30:
        st.write(s3, rf'⇒ $\small 30m < H ≤ Z_g$ 이므로')        
        st.write(s3, rf'∴ $\small L_{{H}} = \small 100 \left( \large \frac{{H}}{{30}} \right)^{{0.5}} = \small 100 × \left( \large \frac{{{H:.1f}}}{{30}} \right)^{{0.5}} = {LH:.1f}$')
    else:
        st.write(s3, rf'⇒ $\small H ≤ 30m$ 이므로')        
        st.write(s3, rf'∴ $\small L_{{H}} = {LH:.1f}$')
    
    st.write('')
    st.write(s3, r'￭ $k = \begin{cases} {\small 0.33} & \small \text{for} & \small H ≥ B \\[12pt] \small -0.33 & \small \text{for} & \small{H < B} \end{cases}$')
    if H >= B:
        st.write(s3, rf'⇒ $\small H ≥ B$ 이므로')        
        st.write(s3, rf'∴ $\small k = {k:.2f}$')
    else:
        st.write(s3, rf'⇒ $\small H < B$ 이므로')        
        st.write(s3, rf'∴ $\small k = {k:.2f}$')

    if '비계' in In.type:
        st.write('')
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '③ 풍력계수 ($C_f$)')
        with col2: st.write(h5, ':orange[<근거 : 1.6.4 (3) 풍력계수 (KDS 21 60 00 : 2022)>]')
        word_wrap_style(s2, '세장한 부재들로 이루어져 충실률이 낮고 보호망이나 패널 등을 붙여서 사용하는 안전 시설물의 풍력계수는 충실률에 따라 다음과 같이 산정한다.', In.font_h5)
        st.write(s2, rf'➣ $\small{{C_f = (0.11 + 0.09\, \gamma + 0.945 C_{0} R)F }}$ = (0.11 + 0.09×{gamma:.2f} + 0.945×{C0:.2f}×{Rsh:,.2f})×{F:,.2f} = {In.Cf:.3f}')
        st.write(s3, rf'￭ $\small \gamma$ = {gamma:,.2f} : 보호망, 네트 등의 풍력저감계수')
        st.write(s3, rf'￭ $\small C_0$ = {C0:,.2f} : 안전시설물의 기본풍력계수')
        st.write(s3, rf'￭ $\small R_{{sh}} = 0.5813 + 0.013({txt}) - 0.0001({txt})^{{2}}$ = {Rsh:,.2f} : 안전시설물의 형상보정계수')
        st.write(s3, rf'￭ $\small F = 1.0 + 0.31\phi = {F:,.2f}$ : 비계 위치에 대한 보정계수 (정압 최댓값 사용)')
        st.write(s3, rf'￭ $\small F = -1.0$ : 비계 위치에 대한 보정계수 (부압 최댓값 사용)')

    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '3. 사용부재 및 설치간격')
    Table.Input(In)
    
    if '비계' in In.type:
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        st.write(h4, '4. 작업발판 검토')
        st.image('Images/working2.png', width=900)

        st.write(s1, '1) 개요')
        st.write(s2, '➣ 등분포 하중을 받는 단순보로 계산한다.')
        st.write(s2, f'➣ 작업발판 치수 : {In.Lj:,.0f} mm × {In.Lw:,.0f} mm');  Pa = In.P * In.Lj            
        st.write(s2, f'➣ P$_a$ = {In.P:.0f} N/mm × {In.Lj:,.0f} mm = {Pa:,.0f} N')
        st.write(s3, '￭ 작업발판의 휨강도 (P$_a$) = 안전인증기준 [N/mm] × 나비 [장선방향 길이, mm]')        

        st.write('')  ## 빈줄 공간
        st.write(s1, '2) 작업발판에 재하되는 하중');  w = In.design_load * In.Lj
        st.write(s2, f'➣ $w$ = 설계하중 × 장선방향 길이')
        st.write(s2, f'➣ $w$ = {In.design_load:,.4f} N/mm² × {In.Lj:,.0f} mm = {w:,.2f} N/mm')

        st.write('')  ## 빈줄 공간
        st.write(s1, '3) 휨강도 검토');  Mmax = w * In.Lw**2 / 8 /1e6;  Ma = Pa * In.Lw / 4 / 1e6   # kN m
        st.write(s2, rf'➣ $M_{{max}} \; = \; \large{{\frac{{w L_w^2}}{{8}}}} \normalsize \; = \; \large{{\frac{{{w:,.2f} × {In.Lw:,.0f}^2}}{{8}} }}$ = {Mmax:,.2f} kN&#8226;m')
        st.write(s2, rf'➣ $M_{{a}} \; = \; \large{{\frac{{P_a L_w}}{{4}}}} \normalsize \; = \; \large{{\frac{{{Pa:,.0f} × {In.Lw:,.0f}}}{{4}} }}$ = {Ma:,.2f} kN&#8226;m')
        SF = Ma / Mmax
        [lgeq, okng] = ['\geq', In.ok] if SF >= 2.0 else ['\leq', In.ng]
        [col1, col2] = st.columns(In.col_span_okng)
        with col1: st.write(s2, '➣ 안전율 검토 $\; : \;$ ', rf'S.F = $\large\frac{{M_a}}{{{{M_{{max}}}}}} \normalsize = \large\frac{{ {Ma:,.2f} }}{{ {Mmax:,.2f} }} \normalsize = \: $' + f'{SF:.1f}', rf'$\; {lgeq} \;$ 2.0 (휨 안전율) $\qquad$')
        with col2: st.write(h5, okng)

        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        opt = ['장선','', '5. '];  userFcn.Check(In, opt, In.joist, Joist)
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        opt = ['띠장','', '6. '];  userFcn.Check(In, opt, In.waling, Waling)

        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        opt = ['수직재', '7. '];  Vertical.Fca = userFcn.Check_Support(In, opt, In.vertical, Vertical)
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        opt = ['수평재', '8. '];  Horizontal.Fca = userFcn.Check_Support(In, opt, In.horizontal, Horizontal)
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        opt = ['가새재', '9. '];  Bracing.Fca = userFcn.Check_Support(In, opt, In.bracing, Bracing)

        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        st.write(h4, '10. 벽연결용 철물 및 받침철물 검토')
        st.write('')  ## 빈줄 공간
        st.write(s1, '1) 벽연결용 철물 설치 간격')
        st.write(s2, f'➣ 띠장방향 : {In.fastener_Ny*In.Lw:,.0f} mm')
        st.write(s2, f'➣ 높이방향 : {In.fastener_Nz*In.Lh:,.0f} mm (최대 간격)')
        st.write('')  ## 빈줄 공간
        st.write(s1, '2) 풍하중에 의한 벽연결용 철물 압축력 및 인장력')
        st.write(s2, '➣ 압축력, 인장력 중에서 최대값')
        st.write(s2, '➣ $\small{{P_w}}$ = 설계풍압 x 면적 / 허용응력증가계수* = $\small{{p_f}}$ x 띠장방향 간격 x 높이방향 간격 / 1.25');  Pw = In.wind2 * In.fastener_Ly * In.fastener_Lz / 1e6 / 1.25
        st.write(s3, rf'￭ $\small{{P_w}}$ = {In.wind2:,.3f} kN/m² x {In.fastener_Ly/1e3:,.1f} m x {In.fastener_Lz/1e3:,.1f} m / 1.25 = {Pw:,.1f} kN')
        st.write('###### $\quad \qquad$', ':blue[*풍하중 고려시 허용응력증가계수 1.25 적용]')

        st.write('')  ## 빈줄 공간
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '3) 안전율 검토')
        with col2: st.write(h5, ':orange[ <근거 : 2.7.4 벽연결용 철물 (KDS 21 60 00 : 2022)> ]')
        st.write(s2, '➣ 벽연결용 철물의 압축성능 및 인장성능 : 9.81 kN')
        SF = 9.81 / Pw
        [lgeq, okng] = ['\geq', In.ok] if SF >= 3.0 else ['\leq', In.ng]
        [col1, col2] = st.columns(In.col_span_okng)
        with col1:
            st.write(s2, '➣ 안전율 검토 $\; : \;$ ', rf'$S.F = \large\frac{{9.81}}{{P_w}} \normalsize = \large\frac{{9.81}}{{ {Pw:,.1f} }} \normalsize = \: $' + f'{SF:.1f}', rf'$\; {lgeq} \;$ 3.0 (안전율*) $\qquad$')
        with col2: st.write(h5, okng)        
        st.write('###### $\quad \qquad$', ':blue[*인장 안전율 2.0, 압축 안전율 3.0에서 최댓값 적용]')

        st.write('')  ## 빈줄 공간
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '4) 받침철물 검토')
        with col2: st.write(h5, ':orange[ <근거 : 2.7.2 받침철물 (KDS 21 60 00 : 2022)> ]')
        st.write(s2, '➣ 받침철물의 압축성능 : 40 kN')        
        SF = 40 / In.Pv2
        [lgeq, okng] = ['\geq', In.ok] if SF >= 3.0 else ['\leq', In.ng]
        [col1, col2] = st.columns(In.col_span_okng)
        with col1:
            st.write(s2, '➣ 안전율 검토 $\; : \;$ ', rf'$S.F = \large\frac{{40.0}}{{P}} \normalsize = \large\frac{{40.0}}{{ {In.Pv2:,.1f} }} \normalsize = \: $' + f'{SF:.1f}', rf'$\; {lgeq} \;$ 3.0 (안전율*) $\qquad$')
        with col2: st.write(h5, okng)
        st.write('###### $\quad \qquad$', ':blue[*압축 안전율 3.0 적용]')

    else:   # 동바리
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(h4, '4. 거푸집 널의 변형기준')
        with col2: st.write(h4, ':orange[ <근거 : 1.9 변형기준 (KDS 21 50 00 : 2022)>]')
        Table.Wood_Deformation(In)

        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########    
        opt = ['합판','장선 간격', '5. '];  userFcn.Check(In, opt, In.wood, Wood)
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        opt = ['장선','멍에 간격', '6. '];  userFcn.Check(In, opt, In.joist, Joist)
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        opt = ['멍에','수직재 간격', '7. '];  userFcn.Check(In, opt, In.yoke, Yoke)
        
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        opt = ['수직재', '8. '];  Vertical.Fca = userFcn.Check_Support(In, opt, In.vertical, Vertical)
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        opt = ['수평재', '9. '];  Horizontal.Fca = userFcn.Check_Support(In, opt, In.horizontal, Horizontal)
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        opt = ['가새재', '10. '];  Bracing.Fca = userFcn.Check_Support(In, opt, In.bracing, Bracing)
    