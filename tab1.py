import streamlit as st
import numpy as np
import table

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'

def Tab(In, color, fn, Wood, Joist, Yoke):
    border1 = '<hr style="border-top: 5px double ' + color + '; margin-top: 0px; margin-bottom:30px; border-radius: 10px">'
    border2 = '<hr style="border-top: 2px solid ' + color + '; margin-top:30px; margin-bottom:30px; border-radius: 10px">'
    
    st.markdown(border1, unsafe_allow_html=True) ############
    st.write(h4, '1. 설계하중 산정')
    st.write(s1, '1) 연직하중 (고정하중 + 작업하중)' + '$\qquad$ :orange[ <근거 : 1.6.2 연직하중 (KDS 21 50 00 : 2022)>]')
    [In.design_load, In.dead_load] = table.Load(fn, In.thick_height, In.concrete_weight, In.wood_weight)    
    st.write('###### $\quad \qquad$', '*콘크리트 타설 높이가 0.5m 미만인 경우 :blue[2.5kN/m²], 0.5m 이상 1m 미만인 경우 :blue[3.5kN/m²], 1m 이상인 경우 :blue[5kN/m² 이상] 적용')

    st.write(s1, '2) 수평하중 (P$_h$)' + '$\qquad$ :orange[ <근거 : 1.6.5 수평하중 (KDS 21 50 00 : 2022)>]')
    Ph = In.dead_load*1e3*0.02;  Phx = Ph*In.slab_Y/1e3;  Phy = Ph*In.slab_X/1e3
    st.write(s2, '➣ 수평하중은 고정하중의 :blue[2% 이상], 수평방향으로 단위길이당 :blue[1.5kN/m 이상] 중에 큰 값의 하중이 상단에 작용하는 것으로 한다.')    
    st.write(s2, f'➣ 수평하중 = 고정하중의 2% = (콘크리트 자중 + 거푸집 자중) × 0.02 = {In.dead_load*1e3:.1f} kN/m² × 0.02 = {Ph:.3f} kN/m²')
    st.write(s3, f'✦ X방향 : 수평하중 × Y방향 슬래브 길이 = {Ph:.3f} kN/m² × {In.slab_Y/1e3:.2f} m = {Phx:.3f} kN/m')
    st.write(s3, f'✦ Y방향 : 수평하중 × X방향 슬래브 길이 = {Ph:.3f} kN/m² × {In.slab_X/1e3:.2f} m = {Phy:.3f} kN/m')
    
    st.write(s1, '3) 풍하중')
    st.write(s2, '➣ 3D 상세 구조 해석에 적용된 풍하중 참고')

    st.markdown(border2, unsafe_allow_html=True) ############
    st.write(h4, '2. 사용부재 및 설치간격')
    table.Input(fn, In)

    st.markdown(border2, unsafe_allow_html=True) ############
    st.write(h4, '3. 거푸집 널의 변형기준' + '$\qquad$ :orange[ <근거 : 1.9 변형기준 (KDS 21 50 00 : 2022)>]')
    table.Wood_Deformation(fn, In)

    st.markdown(border2, unsafe_allow_html=True) ############
    opt = ['합판','장선 간격', '4. '];  Check(In, opt, fn, Wood, Joist, Yoke)
    st.markdown(border2, unsafe_allow_html=True)
    opt = ['장선','멍에 간격', '5. '];  Check(In, opt, fn, Wood, Joist, Yoke)
    st.markdown(border2, unsafe_allow_html=True)
    opt = ['멍에','수직재 간격', '6. '];  Check(In, opt, fn, Wood, Joist, Yoke)

    st.markdown(border2, unsafe_allow_html=True) ############
    

def Check(In, opt, fn, Wood, Joist, Yoke):
    width_str = '단위폭 1mm' if '합판' in opt[0] else opt[0] + ' 간격'    

    if '합판' in opt[0]:
        [A, I, S, E, fba, fsa, Ib_Q, section] = [Wood.A, Wood.I, Wood.S, Wood.E, Wood.fba, Wood.fsa, Wood.Ib_Q, In.wood]        
        color = 'magenta';  L_jyv = rf'\textcolor{{{color}}}{{L_j}}'
        w_str = 'ω_w';  img = 'wood.png';  L = [1, In.Lj]
        
    if '장선' in opt[0]:
        [A, I, S, E, fba, fsa, Ib_Q, section] = [Joist.A, Joist.I, Joist.S, Joist.E, Joist.fba, Joist.fsa, Joist.Ib_Q, In.joist]
        color = 'green';  L_jyv = rf'\textcolor{{{color}}}{{L_y}}'
        w_str = 'ω_j';  img = 'joist.png';  L = [In.Lj, In.Ly]

    if '멍에' in opt[0]:
        [A, I, S, E, fba, fsa, Ib_Q, section] = [Yoke.A, Yoke.I, Yoke.S, Yoke.E, Yoke.fba, Yoke.fsa, Yoke.Ib_Q, In.yoke]
        color = 'blue';  L_jyv = rf'\textcolor{{{color}}}{{L_v}}'    
        w_str = 'ω_y';  img = 'yoke.png';  L = [In.Ly, In.Ly]

    w = In.design_load*L[0]
    L_jyv1 = opt[1] + rf'($\bm{{{L_jyv}}}$) 검토'
    L_jyv2 = rf'$\bm{{{{{L_jyv}}} }} \bm{{\textcolor{{{color}}}{{\; = {L[1]:0.1f} \pmb{{\rm{{\; mm}}}} }} }}$'
    st.write(h4, opt[2] + opt[0] + ' 및 ' + L_jyv1)
    table.Info(fn, opt[0], section, A, Ib_Q, I, S, E, fba, fsa, 20)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(s1, '1) 개요')
        st.write(s2, '➣ 등분포 하중을 받는 단순보로 계산한다.')
        st.write(s2, '➣ ' + L_jyv2)
        st.write(s1, '2) ' + opt[0] + rf'에 재하되는 하중 ($\bm{{{w_str}}}$) [폭 : {width_str}]')
        st.write(s2, rf'➣ $\bm{{{{{w_str}}} = }}$ 설계 하중 x ' + width_str)
        precision = 4 if '합판' in opt[0] else 2
        st.write(s2, rf'➣ $\bm {{\small {{{{{w_str} = {In.design_load:0.4f}}} }} }}$ N/mm² x  {L[0]:0.1f} mm $\bm{{=}}$ {w:.{precision}f} N/mm')
    with col2:
        st.image(img, width=500)

    st.write(s1, '3) ' + L_jyv1)    
    st.write(s2, '① 휨응력 검토')  #\color{red}, \textcolor{blue}{}(범위 지정), \bm, \textbf, \boldsymbol [\pmb], \small, \normalize, \Large, \large    
    st.write(s3, rf'$\bm{{\quad M_{{max}} \; = \; \Large{{\frac{{{w_str} {L_jyv}^2}}{{8}}}} \normalsize \; \leq \; f_{{ba}}\,S}}$')
    num_str = rf"$\bm{{\large{{\sqrt{{\frac{{8 \times {fba:.1f} \times {S:,.1f}}}{{{w:.4f}}} }} }} \normalsize \; = \;}}$";  Lm = (8*fba*S/w)**(1/2)
    st.write(s3, rf'$\bm{{\quad {L_jyv} \; \leq \; \Large\sqrt{{\frac{{8\,f_{{ba}}\,S}}{{{w_str}}}}} \normalsize \; = \;}} $', num_str + f'{Lm:,.1f} mm')
    [lgeq, okng] = ['\leq', In.ok] if L[1] <= Lm else ['\geq', In.ng]
    st.write(s3, '$\quad$', L_jyv2, rf'$\bm{{\; {lgeq} \;}}$' + f'{Lm:,.1f} mm $\qquad$' + okng)

    st.write(s2, '② 변형 검토 (표면 등급 : :blue[', In.level, '] )' + '$\qquad$ :orange[ <근거 : 1.9 변형기준 (KDS 21 50 00 : 2022)>]')
    Ld1 = (384*E*I*L[1]/(5*w*In.d1))**(1/4);  Ld2 = (384*E*I*In.d2/(5*w))**(1/4)
    st.write(s3, 'a. 상대변형 기준')    
    st.write(s3, rf'$\bm{{\quad \delta_{{max}} \;= \; \Large{{\frac{{5\,{{{w_str}}} {L_jyv}^4}}{{384\,E\,I}}}} \normalsize{{\; \leq \;}}}} $', In.d1_str)
    num_str = rf"$\bm{{\large{{\sqrt[4]{{\frac{{384 \times {E:,.1f} \times {I:,.1f} \times {L[1]:,.1f}}}{{5 \times {w:,.4f} \times 360 }}}} }} \; \normalsize = \;}}$"
    st.write(s3, rf'$\bm{{\quad {L_jyv} \; \leq \; \Large\sqrt[4]{{\frac{{384\,E\,I\,L_n}}{{{{5\,{{{w_str}}}}}\,{{{In.d1:.0f}}} }}}} \; \normalsize = \;}} $', num_str + f'{Ld1:,.1f} mm')
    [lgeq, okng] = ['\leq', In.ok] if L[1] <= Ld1 else ['\geq', In.ng]
    st.write(s3, '$\quad$', L_jyv2, rf'$\bm{{\; {lgeq} \;}}$' + f'{Ld1:,.1f} mm $\qquad$' + okng)

    st.write(s3, 'b. 절대변형 기준')
    st.write(s3, rf'$\bm{{\quad \delta_{{max}} \; = \; \Large{{\frac{{5\,{{{w_str}}} {L_jyv}^4}}{{384\,E\,I}}}} \normalsize \; \leq \;}} $', In.d2_str)
    num_str = rf'$\bm{{\large{{\sqrt[4]{{\frac{{384 \times {E:,.1f} \times {I:,.1f} \times 3}}{{5 \times {w:,.4f} }}}} }} \normalsize \; = \;}}$'
    st.write(s3, rf'$\bm{{\quad {L_jyv} \; \leq \; \Large\sqrt[4]{{\frac{{384\,E\,I\,{{{In.d2:.0f}}}}}{{5\,{{{w_str}}} }}}} \normalsize \; = \;}} $', num_str + rf'{Ld2:,.1f} mm')
    [lgeq, okng] = ['\leq', In.ok] if L[1] <= Ld2 else ['\geq', In.ng]
    st.write(s3, '$\quad$', L_jyv2, rf'$\bm{{\; {lgeq} \;}}$' + f'{Ld2:,.1f} mm $\qquad$' + okng)

    st.write(s2, '③ 전단 검토')
    Vmax = w*L[1]/2;  fs = Vmax/Ib_Q
    # fs_str = 'Ib/Q' if '합판' in opt[0] else 'A'
    num_str = rf'$\boldsymbol{{\large{{\frac{{ {w:,.4f} \times {L[1]:,.1f}}}{{2}} }} \normalsize \; = \;}} $'    
    st.write(s3, rf'$\bm{{\quad V_{{max}} \; = \; \Large{{\frac{{ {{{w_str}}} {L_jyv}}}{{2}}}} \normalsize \; = \;}} $', num_str, rf'{Vmax:,.2f} N')        
    [lgeq, okng] = ['\leq', In.ok] if fs <= fsa else ['\geq', In.ng]
    num_str = rf'$\bm{{\large{{\frac{{ {Vmax:,.1f}}}{{{Ib_Q:,.1f}}} }} \normalsize \; = \;}} $'
    st.write(s3, rf'$\boldsymbol{{\quad f_s \; = \; \Large{{\frac{{V_{{max}}}}{{Ib/Q}} }} \normalsize \; = \;}}$', num_str, f'{fs:.2f} MPa', rf'$\: \bm \; {lgeq} \;$', f'{fsa:.2f} MPa', r'$\bm {( \; = \; f_{sa})} \qquad$', okng)

