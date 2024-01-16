import streamlit as st
import numpy as np
from Sidebar import word_wrap_style
import Table

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'

def Info(In, Wood, Joist, Yoke, Vertical, Horizontal, Bracing):
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.title(':blue[Ⅱ. 구조 검토 ✍️]')
    st.markdown(In.border2, unsafe_allow_html=True) ########### border ##########

    st.write(h4, '1. 설계조건')
    if '슬래브' in In.type:  txt = f'✦ 슬래브 두께 : {In.slab_t:,.0f} mm'
    if '보'     in In.type:  txt = f'✦ 보의 치수 : {In.beam_b:,.0f} mm × {In.beam_h:,.0f} mm &nbsp; [폭 × 높이]'
    st.write(s1, txt)
    txt = f'✦ 동바리 스팬 : {In.slab_X*1e3:,.0f} mm × {In.slab_Y*1e3:,.0f} mm &nbsp; [X방향 길이 × Y방향 길이]'
    st.write(s1, txt)
    txt = f'✦ 동바리 높이 : {In.height*1e3:,.0f} mm'
    st.write(s1, txt)
    txt = f'✦ 거푸집 널의 변형기준 [표면 등급] : {In.level}'
    st.write(s1, txt)
    txt = f'✦ 콘크리트 단위중량 : {In.concrete_weight:,.1f} kN/m³'
    st.write(s1, txt)
    txt = f'✦ 거푸집 단위중량 : {In.wood_weight:,.1f} kN/m²'
    st.write(s1, txt)
        
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '2. 설계하중 산정')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '1) 연직하중 (고정하중 + 작업하중)')
    with col2: st.write(h5, ':orange[ <근거 : 1.6.2 연직하중 (KDS 21 50 00 : 2022)>]')

    st.write(s2, '➣ 고정하중은 철근콘크리트와 거푸집의 무게를 합한 하중이다.')
    txt = '➣ 작업하중은 작업원, 경량의 장비하중, 충격하중, 기타 콘크리트 타설에 필요한 자재 및 공구 등의 하중을 포함한다.'
    word_wrap_style(s2+' ', txt, In.font_h5)
    # st.write(s2, '➣ 작업하중은 작업원, 경량의 장비하중, 충격하중, 기타 콘크리트 타설에 필요한 자재 및 공구 등의 하중을 포함한다.')    
    Table.Load(In, 'vertical')    
    txt = '*작업하중은 콘크리트 타설 높이가 0.5m 미만인 경우 :blue[2.5kN/m²], 0.5m 이상 1m 미만인 경우 :blue[3.5kN/m²], 1m 이상인 경우 :blue[5kN/m² 이상] 적용'
    word_wrap_style(s2, txt, '15px')
    # st.write('###### $\quad \qquad$', '*작업하중은 콘크리트 타설 높이가 0.5m 미만인 경우 :blue[2.5kN/m²], 0.5m 이상 1m 미만인 경우 :blue[3.5kN/m²], 1m 이상인 경우 :blue[5kN/m² 이상] 적용')
    
    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간    # st.write('&nbsp;', unsafe_allow_html=True)
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '2) 수평하중 (H)')
    with col2: st.write(h5, ':orange[ <근거 : 1.6.5 수평하중 (KDS 21 50 00 : 2022)>]')
    
    txt = rf'$\,$ ➣ 수평하중은 고정하중의 :blue[2% 이상], 수평방향으로 단위길이당 :blue[1.5kN/m 이상] 중에 큰 값의 하중이 상단에 작용하는 것으로 한다.'
    word_wrap_style(s2, txt, In.font_h5)
    st.write(s2, f'➣ 고정하중의 2% : (콘크리트 자중 + 거푸집 자중) × 0.02 = {In.dead_load*1e3:.1f} kN/m² × 0.02 = {In.dead_load*1e3*0.02:.3f} kN/m²')
    Table.Load(In, 'horizontal')
    st.write(s2, f'➣ ∴ X방향 수평하중 (H$_{{x}}$) = {In.Hx:.1f} kN')
    st.write(s2, f'➣ ∴ Y방향 수평하중 (H$_{{y}}$) = {In.Hy:.1f} kN')
    
    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################

    ###! 설계풍속 산정용
    z = In.height
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
    In.Iw = 0.56 + 0.1*np.log(In.Tw)

    In.VH = In.V0*In.KD*In.Kzr*In.Kzt*In.Iw
    In.qH = 1.225*In.VH**2 / 2

    ###! 가스트영향계수 산정용
    B = max(In.slab_X, In.slab_Y);  H = In.height    
    IH = 0.1*(H/Zg)**(-alpha-0.05) if H > zb else 0.1*(zb/Zg)**(-alpha-0.05)
    LH = 100*(H/30)**(0.5) if H > 30 else 100
    k = 0.33 if H >= B else -0.33
    gammaD = IH*(3 + 3*alpha) / (2 + alpha)
    BD = 1 - 1 / (1 + 5.1*(LH/np.sqrt(H*B))**1.3 * (B/H)**k)**(1/3)
    GD = 1 + 4*gammaD*np.sqrt(BD)
    In.wind2 = In.qH*GD / 1e3   # kN/m2

    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '3) 풍하중 (W)')
    with col1: st.write(s2, rf'➣ 설계풍압 = $\small q_{{H}} \; G_D$ = {In.qH:,.1f} × {GD:.3f} = {In.wind2*1e3:,.1f} N/m$^2$ = {In.wind2:,.3f} kN/m$^2$')
    with col2: st.write(h5, ':orange[<근거 : 1.6.4 풍하중 (KDS 21 50 00 : 2022)>]')

    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '① 속도압 ($q_H$)')
    with col2: st.write(h5, ':orange[<근거 : 5.5 속도압 (KDS 41 12 00 : 2022)>]')
    
    st.write(s2, rf'기준높이 $\small H$에서의 속도압($\small q_H$)은 다음과 같이 산정한다.')    
    st.write(s2, rf'➣ $\bm{{q_{{H}} \; = \; \Large{{\frac{{1}}{2}}} \small \, \rho \, V^2_H}}$ [N/m$^2$] = {In.qH:,.1f} N/m$^2$ = {In.qH/1e3:,.3f} kN/m$^2$')
    
    st.write(s3, rf'￭ $\rho$ : 공기밀도로써 균일하게 1.225 kg/m$^3$으로 한다.')
    st.write(s3, rf'￭ $\small V_H$ : 설계풍속 [m/s] [5.5.1]')

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간    
    st.write(s2, rf'➣ $\bm{{\small{{V_{{H}} \; = \; V_0 \, K_D \, K_{{zr}} \, K_{{zt}} \, I_w(T)}} }}$ [m/s] = {In.V0:.1f} × {In.KD:.2f} × {In.Kzr:.2f} × {In.Kzt:.2f} × {In.Iw:.2f} = {In.VH:,.1f} m/s')
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
    
    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
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

    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.write(s3, r'￭ 표 5.5-3 $\small z_b, Z_g, \alpha$')
    Table.Kzr(In, '표3')

    if z <= zb:
        st.write(s3, rf'⇒ 지표면조도구분이 :blue[{Kzr_txt}]이고, 높이 $\small z$({z:.1f}m) ≤ $\small z_{{b}}$({zb:.1f}m) 이므로')
        st.write(s3, rf'∴ $\small K_{{zr}}$ = {In.Kzr:.2f}')
    else:
        st.write(s3, rf'⇒ 지표면조도구분이 :blue[{Kzr_txt}]이고, 높이 $\small z_{{b}}$({zb:.1f}m) ≤ z({z:.1f}m) ≤ $\small Z_{{g}}$({Zg:.1f}m) 이므로')
        st.write(s3, Kzr_text)

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s2, r'➣ 가시설물의 재현기간에 따른 중요도계수($\small I_w$)')
    with col2: st.write(h5, ':orange[<근거 : 1.6.4 풍하중 (KDS 21 50 00 : 2022)>]')    
    st.write(s3, rf'￭ 존치기간(N)이 1년 이하의 경우에는 0.60을 적용하고, 이 외 기간에 대해서는 다음 식에 의해 산정.')
    st.write(s3, rf'￭ $\small I_w = 0.56 + 0.1 \ln(T_w)$')
    st.write(s3, rf'￭ $\bm{{\small T_{{w}} \; = \; \Large{{\frac{{1}}{{1 \,-\, (P)^\frac{{1}}{{N}}}} }} }}$')
    st.write(s3, rf'￭ $\small T_w$ : 재현기간(년), $\quad \small N$ : 가시설물의 존치기간(년), $\quad \small P$ : 비초과 확률(60%)')
    st.write('')
    if In.N <= 1:
        st.write(s3, rf'⇒ 존치기간(N)이 1년 이하이므로')
        st.write(s3, rf'∴ $\small I_{{W}}$ = 0.60')
    else:
        st.write(s3, rf'⇒ 존치기간(N)이 1년을 초과하므로 다음과 같이 산정한다.')
        st.write(s3, rf'∴ $\small I_{{W}} = 0.56 + 0.1 \ln(T_W) = 0.56 + 0.1 × \ln({In.Tw:.2f})$ = {In.Iw:.2f}')
        st.write(s3, rf' where, $\left[\small T_{{w}} \; = \; \Large{{\frac{{1}}{{1 \,-\, (P)^\frac{{1}}{{N}}}} }}\; \small = \; \Large{{\frac{{1}}{{1 \,-\, (0.6)^\frac{{1}}{{{In.N:.1f}}}}} }} \small \;= \;{In.Tw:.2f} \right]$')

    st.write('')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '② 가스트영향계수 ($G_D$)')
    with col2: st.write(h5, ':orange[<근거 : 5.6 가스트영향계수 (KDS 41 12 00 : 2022)>]')    
    word_wrap_style(s2, r'대부분 건축구조물의 풍방향 고유진동수($\small n_D$)가 1Hz를 초과하기 때문에, 바람에 의한 동적 효과를 무시할 수 있는 강체 건축구조물로 볼 수 있다.', In.font_h5)
    st.write(s2, rf'➣ $\bm{{\small{{G_D = 1 + 4 \, \gamma_D \sqrt{{B_D}} }} }} = 1 + 4 × {gammaD:.3f} × \sqrt{{{BD:.3f}}} = {GD:.3f}$')
    st.write(s3, rf'￭ $\small \gamma_D$ : 풍속변동계수 [식 5.6-1.c]')
    st.write(s3, rf'￭ $\small B_D$ : 비공진계수 [식 5.6-1.d]')

    st.write('')
    st.write(s2, rf'➣ $\small \gamma_D = \left( \Large{{\frac{{3 + 3\alpha}}{{2 + \alpha}} }} \right) I_H = \left( \Large{{\frac{{3 + 3 × {alpha:.2f}}}{{2 + {alpha:.2f}}} }} \right) \small × {IH:.3f} = {gammaD:.3f} $')
    st.write(s3, rf'￭ $\small I_H$ : 기준높이(H)에서의 난류강도 [식 5.5-3.a]')
    st.write(s3, r'￭ $I_H = \begin{cases} {0.1 \left( \Large \frac{H}{Z_g} \right)^{-\alpha - 0.05} } & \small \text{for} & \small z_b < H ≤ Z_g \\[12pt] {0.1 \left( \Large \frac{z_b}{Z_g} \right)^{-\alpha - 0.05} } & \small \text{for} & \small H ≤ z_b \end{cases}$')
    if H > zb:
        st.write(s3, rf'⇒ $z_b < H ≤ Z_g$ 이므로')        
        st.write(s3, rf'∴ $\small I_{{H}} = 0.1 \left( \Large \frac{{H}}{{Z_g}} \right)^{{-\alpha - 0.05}} = 0.1 × \left( \Large \frac{{{H:.1f}}}{{{Zg:.1f}}} \right)^{{{-alpha:.2f} - 0.05}} = {IH:.3f}$')        
    else:
        st.write(s3, rf'⇒ $H ≤ z_b$ 이므로')        
        st.write(s3, rf'∴ $\small I_{{H}} = 0.1 \left( \Large \frac{{z_b}}{{Z_g}} \right)^{{-\alpha - 0.05}} = 0.1 × \left( \Large \frac{{{zb:.1f}}}{{{Zg:.1f}}} \right)^{{{-alpha:.2f} - 0.05}} = {IH:.3f}$')        

    # st.write(s2, rf'➣ $\small B_D = 1 - \left[ \Large{{\frac{{1}}{{\left[ 1 \; + \; 5.1 \left( \frac{{L_H}}{{\sqrt{{HB}}}} \right)^{{1.3}} \left( \frac{{B}}{{H}} \right)^{{k}} \right]^\frac{{1}}{{3}} }} }} \right] = \small 1 - \left[ \Large{{\frac{{1}}{{\left[ 1 \; + \; 5.1 \left( \frac{{{LH:.1f}}}{{\sqrt{{{H:.1f} × {B:.1f}}}}} \right)^{{1.3}} \left( \frac{{{B:.1f}}}{{{H:.1f}}} \right)^{{{k:.2f}}} \right]^\frac{{1}}{{3}} }} }} \right] = {BD:.3f} $')
    st.write(s2, rf'➣ $\small B_D = 1 - \left[ \Large{{\frac{{1}}{{\left[ 1 \; + \; 5.1 \left( \frac{{L_H}}{{\sqrt{{HB}}}} \right)^{{1.3}} \left( \frac{{B}}{{H}} \right)^{{k}} \right]^\frac{{1}}{{3}} }} }} \right] = {BD:.3f} $')
    st.write(s3, rf'￭ $\small L_H$ : 기준높이(H)에서의 난류스케일(m) [식 5.6-1.e]')
    st.write(s3, r'￭ $L_H = \begin{cases} {100 \left( \Large \frac{H}{30} \right)^{0.5} } & \small \text{for} & \small 30m < H ≤ Z_g \\[12pt] 100 & \small \text{for} & \small H ≤ 30m \end{cases}$')
    if H > 30:
        st.write(s3, rf'⇒ $30m < H ≤ Z_g$ 이므로')        
        st.write(s3, rf'∴ $\small L_{{H}} = 100 \left( \Large \frac{{H}}{{30}} \right)^{{0.5}} = 100 × \left( \Large \frac{{{H:.1f}}}{{30}} \right)^{{0.5}} = {LH:.1f}$')
    else:
        st.write(s3, rf'⇒ $H ≤ 30m$ 이므로')        
        st.write(s3, rf'∴ $\small L_{{H}} = {LH:.1f}$')
    
    st.write('')
    st.write(s3, r'￭ $k = \begin{cases} {0.33} & \small \text{for} & \small H ≥ B \\[12pt] -0.33 & \small \text{for} & \small{H < B} \end{cases}$')
    if H >= B:
        st.write(s3, rf'⇒ $\small H ≥ B$ 이므로')        
        st.write(s3, rf'∴ $\small k = {k:.2f}$')
    else:
        st.write(s3, rf'⇒ $\small H < B$ 이므로')        
        st.write(s3, rf'∴ $\small k = {k:.2f}$')


    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '3. 사용부재 및 설치간격')
    Table.Input(In)

    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(h4, '4. 거푸집 널의 변형기준')
    with col2: st.write(h4, ':orange[ <근거 : 1.9 변형기준 (KDS 21 50 00 : 2022)>]')
    Table.Wood_Deformation(In)

    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########    
    opt = ['합판','장선 간격', '5. '];  Check(In, opt, In.wood, Wood)
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########    
    opt = ['장선','멍에 간격', '6. '];  Check(In, opt, In.joist, Joist)
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    opt = ['멍에','수직재 간격', '7. '];  Check(In, opt, In.yoke, Yoke)
    
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    opt = ['수직재', '8. '];  Vertical.Fca = Check_Support(In, opt, In.vertical, Vertical)
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    opt = ['수평재', '9. '];  Horizontal.Fca = Check_Support(In, opt, In.horizontal, Horizontal)
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    opt = ['가새재', '10. '];  Bracing.Fca = Check_Support(In, opt, In.bracing, Bracing)
    
    
def Check_Support(In, opt, section, Support):
    [A, I, S, E, r, Fy, Ib_Q] = [Support.A, Support.I, Support.S, Support.E, Support.r, Support.Fy, Support.Ib_Q]
    P = In.design_load*In.Ly*In.Lv/1e3;  H = max(In.Hx, In.Hy)  #kN    

    if '수직재' in opt[0]:
        Load_str = 'P';   Load = P
        KL_str = 'KL_v';  KL = In.KLv;  KL_cal = ''
    if '수평재' in opt[0]:
        Load_str = 'H';   Load = H
        KL_str = 'KL_h';  KL = In.KLh;  KL_cal = ''
    if '가새재' in opt[0]:
        Load_str = 'H';   Load = H
        KL_str = 'KL_d';  KL = np.sqrt(In.KLv**2 + In.KLh**2)
        KL_cal = rf'$\bm{{\small{{\sqrt{{ {In.KLv:.1f}^2 + {In.KLh:.1f}^2 }} }}}}$ = '        

    st.write(h4, opt[1] + opt[0] + ' 검토')
    Table.Info(opt[0], section, A, Ib_Q, I, S, E, r, Fy, 20)
    

    if '수직재' in opt[0]:
        st.write(s1, '1) 1본당 작용하중 (P)')
        st.write(s2, '➣ P = 설계 하중 x 멍에 간격 x 동바리 간격')
        st.write(s2, rf'➣ P = {In.design_load:.4f} N/mm² x {In.Ly:,.1f} mm x {In.Lv:,.1f} mm = {P:,.1f} kN/EA')
    else:
        st.write(s1, '1) 수평하중 (H)')
        st.write(s2, f'➣ X방향 수평하중 (H$_{{x}}$) = {In.Hx:.1f} kN')
        st.write(s2, f'➣ Y방향 수평하중 (H$_{{y}}$) = {In.Hy:.1f} kN')

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간    
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '2) 허용압축응력 (' + r'$\bm{\small{{F_{ca}}}}$' + ') 산정')
    with col2: st.write(h5, ':orange[ <근거 : 4.4.3 허용압축응력 (KDS 14 30 10 : 2019)> ]')
        
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s2, '➣ 유효 좌굴길이 ')
    with col2: st.write(h5, ':orange[ <근거 : 4.4.2 좌굴길이와 세장비 (KDS 14 30 10 : 2019)> ]')
    # st.write("<div style='text-align: right; color: blue'>우측 정렬 예시</div>", unsafe_allow_html=True)  # 우측 정렬 예시

    st.write(s3, rf'￭ $\bm{{\small{{{KL_str}}} }} = $', KL_cal, f'{KL:,.1f} mm')
    num_str = rf'$\bm{{\large{{\frac{{{KL:,.1f}}}{{{r:,.1f}}}}} }} \; = \;$';  lamda = KL/r    
    [lgeq, okng] = ['\leq', In.ok] if lamda <= 200 else ['\geq', In.ng]
    st.write(s2, '➣ 세장비')
    [col1, col2] = st.columns(In.col_span_okng)
    with col1:     st.write(s3, rf'￭ $\bm{{\lambda = \large{{\frac{{{KL_str}}}{{r}}}} }}$ = ' + num_str + f'{lamda:,.1f}', rf'$\; {lgeq} \:$ 200 (최대 세장비) $\qquad$')
    with col2: st.write(h5, okng)

    num_str = rf'$\bm{{\large\sqrt{{\frac{{2 \pi^2 \times {E:,.0f}}}{{{Fy:,.1f}}}}} }}$ = ';  Cc = np.sqrt(2*np.pi**2*E/Fy)
    st.write(s2, '➣ 한계 세장비')
    st.write(s3, rf'￭ $\bm{{C_c = \large\sqrt{{\frac{{2 \pi^2 E}}{{F_y}}}} }}$ = ' + num_str + f'{Cc:,.1f}')

    if lamda <= Cc:
        a = (1 - lamda**2/(2*Cc**2)) *Fy;  b = 5/3 + 3*lamda/(8*Cc) - lamda**3/(8*Cc**3)
        a_str = rf'\left[1 - \large\frac{{(KL/r)^2}}{{2 C_c^2}}\right] F_y'
        b_str = rf'\large\frac{{5}}{{3}} + \frac{{3 (KL/r)}}{{8 C_c}} - \frac{{(KL/r)^3}}{{8 C_c^3}}'
        Fca = a/b;  lgeq = '\leq'
    else:
        a = 12*np.pi**2 *E;  b = 23*lamda**2
        a_str = '12 \pi^2 E';  b_str = '23 (KL/r)^2'
        Fca = a/b;  lgeq = '\geq'
    st.write(s2, '➣ ' + rf'$\bm{{ \lambda = \large{{\frac{{{KL_str}}}{{r}} \normalsize \; {lgeq} \; C_c}} }}$', ' 이므로')
    st.write(s3, rf'￭ $\bm{{F_{{ca}} = {{\large{{\frac{{{a_str}}}{{{b_str}}} }} }} \normalsize \; = \;}}$' + f'{Fca:,.1f} MPa')

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    txt = f'3) {opt[0]} 수량' if '수직재' not in opt[0] else '3) 안전율 검토'    
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, txt)
    with col2: st.write(h5, ':orange[ <근거 : 1.8 안전율 (KDS 21 50 00 : 2022)>]')

    if '수직재' in opt[0]:
        Pa = Fca*A/1e3;  SF = Pa/Load        
        st.write(s2, '➣ 허용압축하중 $\; : \;$', rf'$\bm{{\small{{P_a = F_{{ca}} \times A}} }}$ = {Fca:,.1f} MPa x {A:,.1f} mm² = {Pa:,.1f} kN')
        [lgeq, okng] = ['\geq', In.ok] if SF >= 2.5 else ['\leq', In.ng]
        [col1, col2] = st.columns(In.col_span_okng)
        with col1: st.write(s2, '➣ 안전율 검토 $\; : \;$ ', rf'$\bm{{S.F = \large\frac{{P_a}}{{{Load_str}}} \normalsize = \large\frac{{ {Pa:,.1f} }}{{ {Load:,.1f} }} \normalsize = \: }}$' + f'{SF:.1f}', rf'$\; {lgeq} \;$ 2.5 (안전율*) $\qquad$')
        with col2: st.write(h5, okng)        
        st.write('###### $\quad \qquad$', ':blue[*단품 동바리 안전율 3.0, 조립식 동바리 안전율 2.5 적용]')
    else:
        if '수평재' in opt[0]:  Pa = Fca*A/1e3
        if '가새재' in opt[0]:  Pa = Fca*A/1e3*np.cos(np.pi/3)  # 가새재 최대 경사(60도) 고려        
        EAx = In.Hx/Pa;  EAy = In.Hy/Pa
        if '수평재' in opt[0]:  txt1 = '';  txt2 = '';  txt3 = ''
        if '가새재' in opt[0]:  txt1 = '*';  txt2 = rf'\rm{{cos(60°)}} \times';  txt3 = '0.5 x '
        st.write(s2, f'➣ 허용압축하중{txt1} $\; : \;$', rf'$\bm{{\small{{P_a = {txt2} F_{{ca}} \times A}} }}$ = {txt3} {Fca:,.1f} MPa x {A:,.1f} mm² = {Pa:,.1f} kN')
        st.write(s2, f'➣ X방향 {opt[0]} 수량 $\; : \;$',  rf'$\bm{{\large\frac{{X방향 수평하중}}{{허용압축하중}} \normalsize = \large\frac{{ {In.Hx:,.1f} }}{{ {Pa:,.1f} }} \normalsize = \: }}$' + f'{EAx:.1f} EA 이상')
        st.write(s2, f'➣ Y방향 {opt[0]} 수량 $\; : \;$',  rf'$\bm{{\large\frac{{Y방향 수평하중}}{{허용압축하중}} \normalsize = \large\frac{{ {In.Hy:,.1f} }}{{ {Pa:,.1f} }} \normalsize = \: }}$' + f'{EAy:.1f} EA 이상')
        if '가새재' in opt[0]:  st.write('###### $\quad \qquad$', ':blue[*가새재의 최대 각도(60°)를 고려한 허용압축하중]')
        
    return Fca


def Check(In, opt, section, WJY):
    [A, I, S, E, fba, fsa, Ib_Q] = [WJY.A, WJY.I, WJY.S, WJY.E, WJY.fba, WJY.fsa, WJY.Ib_Q]
    width_str = '단위폭 1mm' if '합판' in opt[0] else opt[0] + ' 간격'    

    if '합판' in opt[0]:        
        color = 'magenta';  L_jyv = rf'\textcolor{{{color}}}{{L_j}}'
        w_str = 'ω_w';  img = 'Images/wood.png';  L = [1, In.Lj]
        
    if '장선' in opt[0]:        
        color = 'green';  L_jyv = rf'\textcolor{{{color}}}{{L_y}}'
        w_str = 'ω_j';  img = 'Images/joist.png';  L = [In.Lj, In.Ly]

    if '멍에' in opt[0]:        
        color = 'blue';  L_jyv = rf'\textcolor{{{color}}}{{L_v}}'    
        w_str = 'ω_y';  img = 'Images/yoke.png';  L = [In.Ly, In.Lv]

    w = In.design_load*L[0]
    L_jyv1 = opt[1] + rf'($\bm{{{L_jyv}}}$) 검토'
    L_jyv2 = rf'$\bm{{{{{L_jyv}}} }} \bm{{\textcolor{{{color}}}{{\; = {L[1]:0.1f} \pmb{{\rm{{\; mm}}}} }} }}$'
    st.write(h4, opt[2] + opt[0] + ' 및 ' + L_jyv1)
    Table.Info(opt[0], section, A, Ib_Q, I, S, E, fba, fsa, 20)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(s1, '1) 개요')
        st.write(s2, '➣ 등분포 하중을 받는 단순보로 계산한다.')
        st.write(s2, '➣ ' + L_jyv2)

        st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
        st.write(s1, '2) ' + opt[0] + rf'에 재하되는 하중 ($\bm{{{w_str}}}$) [폭 : {width_str}]')
        st.write(s2, rf'➣ $\bm{{{{{w_str}}} = }}$ 설계 하중 x ' + width_str)
        precision = 4 if '합판' in opt[0] else 2
        st.write(s2, rf'➣ $\bm {{\small {{{{{w_str} = {In.design_load:0.4f}}} }} }}$ N/mm² x  {L[0]:0.1f} mm $\bm{{=}}$ {w:.{precision}f} N/mm')
    with col2:
        st.image(img, width=500)

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    st.write(s1, '3) 응력 검토') #\color{red}, \textcolor{blue}{}, \bm, \textbf, \boldsymbol [\pmb], \small, \normalize, \Large, \large ①②③
    st.write(s2, '① 휨응력 검토')
    Mmax = w*L[1]**2/8;  fb = Mmax/S
    num_str = rf'$\boldsymbol{{\large{{\frac{{ {w:,.4f} \times {L[1]:,.1f}^2}}{{8}} }} \normalsize \; = \;}} $'
    st.write(s3, rf'✦ $\bm{{M_{{max}} \; = \; \Large{{\frac{{{w_str} {L_jyv}^2}}{{8}}}} \normalsize \; = \;}} $', num_str, rf'{Mmax:,.1f} N&#8226;mm')
    [lgeq, okng] = ['\leq', In.ok] if fb <= fba else ['\geq', In.ng]
    num_str = rf'$\bm{{\large{{\frac{{ {Mmax:,.1f}}}{{{S:,.1f}}} }} \normalsize \; = \;}} $'
    [col1, col2] = st.columns(In.col_span_okng)
    with col1:     st.write(s3, rf'✦ $\boldsymbol{{f_b \; = \; \Large{{\frac{{M_{{max}}}}{{S}} }} \normalsize \; = \;}}$', num_str, f'{fb:.1f} MPa', rf'$\: \bm \; {lgeq} \;$', f'{fba:.1f} MPa', r'$\bm {( \; = \; f_{ba})} \qquad$')
    with col2: st.write(h5, okng)
    
    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    st.write(s2, '② 전단응력 검토')
    Vmax = w*L[1]/2;  fs = Vmax/Ib_Q
    # fs_str = 'Ib/Q' if '합판' in opt[0] else 'A'
    num_str = rf'$\boldsymbol{{\large{{\frac{{ {w:,.4f} \times {L[1]:,.1f}}}{{2}} }} \normalsize \; = \;}} $'
    st.write(s3, rf'✦ $\bm{{V_{{max}} \; = \; \Large{{\frac{{ {{{w_str}}} {L_jyv}}}{{2}}}} \normalsize \; = \;}} $', num_str, rf'{Vmax:,.2f} N')        
    [lgeq, okng] = ['\leq', In.ok] if fs <= fsa else ['\geq', In.ng]
    num_str = rf'$\bm{{\large{{\frac{{ {Vmax:,.1f}}}{{{Ib_Q:,.1f}}} }} \normalsize \; = \;}} $'
    [col1, col2] = st.columns(In.col_span_okng)
    with col1:     st.write(s3, rf'✦ $\boldsymbol{{f_s \; = \; \Large{{\frac{{V_{{max}}}}{{Ib/Q}} }} \normalsize \; = \;}}$', num_str, f'{fs:.2f} MPa', rf'$\: \bm \; {lgeq} \;$', f'{fsa:.2f} MPa', r'$\bm {( \; = \; f_{sa})} \qquad$')
    with col2: st.write(h5, okng)

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '4) 변형 검토 (표면 등급 : :blue[', In.level, '] )')
    with col2: st.write(h5, ':orange[ <근거 : 1.9 변형기준 (KDS 21 50 00 : 2022)>]')

    Ld1 = (384*E*I*L[1]/(5*w*In.d1))**(1/4);  Ld2 = (384*E*I*In.d2/(5*w))**(1/4)
    st.write(s2, '① 상대변형 검토')
    st.write(s3, rf'✦ $\bm{{\delta_{{max}} \;= \; \Large{{\frac{{5\,{{{w_str}}} {L_jyv}^4}}{{384\,E\,I}}}} \normalsize{{\; \leq \;}}}} $', In.d1_str)
    num_str = rf"$\bm{{\large{{\sqrt[4]{{\frac{{384 \times {E:,.1f} \times {I:,.1f} \times {L[1]:,.1f}}}{{5 \times {w:,.4f} \times 360 }}}} }} \; \normalsize = \;}}$"
    st.write(s3, rf'✦ $\bm{{{L_jyv} \; \leq \; \Large\sqrt[4]{{\frac{{384\,E\,I\,L_n}}{{{{5\,{{{w_str}}}}}\,{{{In.d1:.0f}}} }}}} \; \normalsize = \;}} $', num_str + f'{Ld1:,.1f} mm')
    [lgeq, okng] = ['\leq', In.ok] if L[1] <= Ld1 else ['\geq', In.ng]
    [col1, col2] = st.columns(In.col_span_okng)
    with col1: st.write(s3, '✦ ', L_jyv2, rf'$\bm{{\; {lgeq} \;}}$' + f'{Ld1:,.1f} mm $\qquad$')
    with col2: st.write(h5, okng)    

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    st.write(s2, '② 절대변형 검토')
    st.write(s3, rf'✦ $\bm{{\delta_{{max}} \; = \; \Large{{\frac{{5\,{{{w_str}}} {L_jyv}^4}}{{384\,E\,I}}}} \normalsize \; \leq \;}} $', In.d2_str)
    num_str = rf'$\bm{{\large{{\sqrt[4]{{\frac{{384 \times {E:,.1f} \times {I:,.1f} \times 3}}{{5 \times {w:,.4f} }}}} }} \normalsize \; = \;}}$'
    st.write(s3, rf'✦ $\bm{{{L_jyv} \; \leq \; \Large\sqrt[4]{{\frac{{384\,E\,I\,{{{In.d2:.0f}}}}}{{5\,{{{w_str}}} }}}} \normalsize \; = \;}} $', num_str + rf'{Ld2:,.1f} mm')
    [lgeq, okng] = ['\leq', In.ok] if L[1] <= Ld2 else ['\geq', In.ng]
    [col1, col2] = st.columns(In.col_span_okng)
    with col1: st.write(s3, '✦ ', L_jyv2, rf'$\bm{{\; {lgeq} \;}}$' + f'{Ld2:,.1f} mm $\qquad$')
    with col2: st.write(h5, okng)    
