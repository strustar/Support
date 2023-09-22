import streamlit as st
import numpy as np
from Sidebar import word_wrap_style
import Table

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'

def Info(In, Wood, Joist, Yoke, Vertical, Horizontal, Bracing):
    st.title(':blue[Ⅱ. 구조 검토 ✍️]')
    st.markdown(In.border2, unsafe_allow_html=True) ########### border ##########

    st.write(h4, '1. 설계하중 산정')    
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '1) 연직하중 (고정하중 + 작업하중)')
    with col2: st.write(h5, ':orange[ <근거 : 1.6.2 연직하중 (KDS 21 50 00 : 2022)>]')

    st.write(s2, '➣ 고정하중은 철근콘크리트와 거푸집의 무게를 합한 하중이다.')
    st.write(s2, '➣ 작업하중은 작업원, 경량의 장비하중, 충격하중, 기타 콘크리트 타설에 필요한 자재 및 공구 등의 하중을 포함한다.')    
    Table.Load(In, 'vertical')    
    st.write('###### $\quad \qquad$', '*작업하중은 콘크리트 타설 높이가 0.5m 미만인 경우 :blue[2.5kN/m²], 0.5m 이상 1m 미만인 경우 :blue[3.5kN/m²], 1m 이상인 경우 :blue[5kN/m² 이상] 적용')
    
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
    st.write(s1, '3) 풍하중')
    st.write(s2, '➣ 3D 상세 구조 해석에 적용된 풍하중 참고')    

    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '2. 사용부재 및 설치간격')
    Table.Input(In)

    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(h4, '3. 거푸집 널의 변형기준')
    with col2: st.write(h4, ':orange[ <근거 : 1.9 변형기준 (KDS 21 50 00 : 2022)>]')
    Table.Wood_Deformation(In)

    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    opt = ['합판','장선 간격', '4. '];  Check(In, opt, In.wood, Wood)
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    opt = ['장선','멍에 간격', '5. '];  Check(In, opt, In.joist, Joist)
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    opt = ['멍에','수직재 간격', '6. '];  Check(In, opt, In.yoke, Yoke)

    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    opt = ['수직재', '7. '];  Check_Support(In, opt, In.vertical, Vertical)
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    opt = ['수평재', '8. '];  Check_Support(In, opt, In.horizontal, Horizontal)
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    opt = ['가새재', '9. '];  Check_Support(In, opt, In.bracing, Bracing)
    
    
def Check_Support(In, opt, section, Support):
    [A, I, S, E, r, Fy] = [Support.A, Support.I, Support.S, Support.E, Support.r, Support.Fy]
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
    Table.Info('수직재', section, A, -1, I, S, E, r, Fy, 20)
    

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
    txt = '3) 가새재 수량' if '가새재' in opt[0] else '3) 안전율 검토'    
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, txt)
    with col2: st.write(h5, ':orange[ <근거 : 1.8 안전율 (KDS 21 50 00 : 2022)>]')

    if '가새재' in opt[0]:
        Pa = Fca*A/1e3*np.cos(np.pi/3)  # 가새재 최대 경사(60도) 고려
        EAx = In.Hx/Pa;  EAy = In.Hy/Pa        
        st.write(s2, '➣ 허용압축하중* $\; : \;$', rf'$\bm{{\small{{P_a = \rm{{cos(60°)}} \times F_{{ca}} \times A}} }}$ = 0.5 x {Fca:,.1f} MPa x {A:,.1f} mm² = {Pa:,.1f} kN')
        st.write(s2, '➣ X방향 가새재 수량 $\; : \;$',  rf'$\bm{{\large\frac{{X방향 수평하중}}{{허용압축하중}} \normalsize = \large\frac{{ {In.Hx:,.1f} }}{{ {Pa:,.1f} }} \normalsize = \: }}$' + f'{EAx:.1f} EA 이상')
        st.write(s2, '➣ Y방향 가새재 수량 $\; : \;$',  rf'$\bm{{\large\frac{{Y방향 수평하중}}{{허용압축하중}} \normalsize = \large\frac{{ {In.Hy:,.1f} }}{{ {Pa:,.1f} }} \normalsize = \: }}$' + f'{EAy:.1f} EA 이상')
        st.write('###### $\quad \qquad$', ':blue[*가새재의 최대 각도(60°)를 고려한 허용압축하중]')
    else:
        Pa = Fca*A/1e3;  SF = Pa/Load        
        st.write(s2, '➣ 허용압축하중 $\; : \;$', rf'$\bm{{\small{{P_a = F_{{ca}} \times A}} }}$ = {Fca:,.1f} MPa x {A:,.1f} mm² = {Pa:,.1f} kN')
        [lgeq, okng] = ['\geq', In.ok] if SF >= 2.5 else ['\leq', In.ng]
        [col1, col2] = st.columns(In.col_span_okng)
        with col1: st.write(s2, '➣ 안전율 검토 $\; : \;$ ', rf'$\bm{{S.F = \large\frac{{P_a}}{{{Load_str}}} \normalsize = \large\frac{{ {Pa:,.1f} }}{{ {Load:,.1f} }} \normalsize = \: }}$' + f'{SF:.1f}', rf'$\; {lgeq} \;$ 2.5 (안전율*) $\qquad$')
        with col2: st.write(h5, okng)        
        st.write('###### $\quad \qquad$', ':blue[*단품 동바리 안전율 3.0, 조립식 동바리 안전율 2.5 적용]')


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
        w_str = 'ω_y';  img = 'Images/yoke.png';  L = [In.Ly, In.Ly]

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
    st.write(s1, '3) 휨응력 검토') #\color{red}, \textcolor{blue}{}, \bm, \textbf, \boldsymbol [\pmb], \small, \normalize, \Large, \large ①②③
    st.write(s2, rf'✦ $\bm{{M_{{max}} \; = \; \Large{{\frac{{{w_str} {L_jyv}^2}}{{8}}}} \normalsize \; \leq \; f_{{ba}}\,S}}$')
    num_str = rf"$\bm{{\large{{\sqrt{{\frac{{8 \times {fba:.1f} \times {S:,.1f}}}{{{w:.4f}}} }} }} \normalsize \; = \;}}$";  Lm = (8*fba*S/w)**(1/2)
    st.write(s2, rf'✦ $\bm{{{L_jyv} \; \leq \; \Large\sqrt{{\frac{{8\,f_{{ba}}\,S}}{{{w_str}}}}} \normalsize \; = \;}} $', num_str + f'{Lm:,.1f} mm')
    [lgeq, okng] = ['\leq', In.ok] if L[1] <= Lm else ['\geq', In.ng]
    [col1, col2] = st.columns(In.col_span_okng)
    with col1: st.write(s2, '✦ ', L_jyv2, rf'$\bm{{\; {lgeq} \;}}$' + f'{Lm:,.1f} mm $\qquad$')
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

    st.write(s2, '② 절대변형 검토')
    st.write(s3, rf'✦ $\bm{{\delta_{{max}} \; = \; \Large{{\frac{{5\,{{{w_str}}} {L_jyv}^4}}{{384\,E\,I}}}} \normalsize \; \leq \;}} $', In.d2_str)
    num_str = rf'$\bm{{\large{{\sqrt[4]{{\frac{{384 \times {E:,.1f} \times {I:,.1f} \times 3}}{{5 \times {w:,.4f} }}}} }} \normalsize \; = \;}}$'
    st.write(s3, rf'✦ $\bm{{{L_jyv} \; \leq \; \Large\sqrt[4]{{\frac{{384\,E\,I\,{{{In.d2:.0f}}}}}{{5\,{{{w_str}}} }}}} \normalsize \; = \;}} $', num_str + rf'{Ld2:,.1f} mm')
    [lgeq, okng] = ['\leq', In.ok] if L[1] <= Ld2 else ['\geq', In.ng]
    [col1, col2] = st.columns(In.col_span_okng)
    with col1: st.write(s3, '✦ ', L_jyv2, rf'$\bm{{\; {lgeq} \;}}$' + f'{Ld2:,.1f} mm $\qquad$')
    with col2: st.write(h5, okng)    

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    st.write(s1, '5) 전단응력 검토')
    Vmax = w*L[1]/2;  fs = Vmax/Ib_Q
    # fs_str = 'Ib/Q' if '합판' in opt[0] else 'A'
    num_str = rf'$\boldsymbol{{\large{{\frac{{ {w:,.4f} \times {L[1]:,.1f}}}{{2}} }} \normalsize \; = \;}} $'    
    st.write(s2, rf'✦ $\bm{{V_{{max}} \; = \; \Large{{\frac{{ {{{w_str}}} {L_jyv}}}{{2}}}} \normalsize \; = \;}} $', num_str, rf'{Vmax:,.2f} N')        
    [lgeq, okng] = ['\leq', In.ok] if fs <= fsa else ['\geq', In.ng]
    num_str = rf'$\bm{{\large{{\frac{{ {Vmax:,.1f}}}{{{Ib_Q:,.1f}}} }} \normalsize \; = \;}} $'
    [col1, col2] = st.columns(In.col_span_okng)
    with col1:     st.write(s2, rf'✦ $\boldsymbol{{f_s \; = \; \Large{{\frac{{V_{{max}}}}{{Ib/Q}} }} \normalsize \; = \;}}$', num_str, f'{fs:.2f} MPa', rf'$\: \bm \; {lgeq} \;$', f'{fsa:.2f} MPa', r'$\bm {( \; = \; f_{sa})} \qquad$')
    with col2: st.write(h5, okng)    

