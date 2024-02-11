import streamlit as st
import numpy as np
import Table

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$';  s4 = h5 + '$\qquad \qquad$'

def Check(In, opt, section, WJY):
    [A, I, S, E, fba, fsa, Ib_Q] = [WJY.A, WJY.I, WJY.S, WJY.E, WJY.fba, WJY.fsa, WJY.Ib_Q]

    if '비계' in In.type:
        if '장선' in opt[0]:
            color = 'magenta';  L = [In.Lj, In.Lw];  w = In.design_load*L[1];  div2 = ''
            L_str = [rf'\textcolor{{magenta}}{{L_j}}', rf'\textcolor{{green}}{{L_w}}']
            L_jw = rf'$\textcolor{{{color}}}{{L_j \; = {L[0]:,.0f} \rm{{\; mm}}}}$'
    
        if '띠장' in opt[0]:
            color = 'green';  L = [In.Lw, In.Lj];  w = In.design_load*L[1]/2;  div2 = ' / 2'
            L_str = [rf'\textcolor{{green}}{{L_w}}', rf'\textcolor{{magenta}}{{L_j}} / 2']
            L_jw = rf'$\textcolor{{{color}}}{{L_w \; = {L[0]:,.0f} \rm{{\; mm}}}}$'    
        
        st.write(h4, opt[2] + opt[0] + ' 검토')
        Table.Info(opt[0], section, A, Ib_Q, I, S, E, fba, fsa, 20)

        st.write(s1, '1) 개요')
        st.write(s2, '➣ 등분포 하중을 받는 단순보로 계산한다.')
        st.write(s2, '➣ ' + L_jw)

        st.write('')  ## 빈줄 공간
        st.write(s1, '2) ' + opt[0] + '에 재하되는 하중')
        st.write(s2, rf'➣ $w$ = 설계 하중 x ' + f'${L_str[1]}$')
        st.write(s2, rf'➣ $\small{{ w = {In.design_load:.4f} }}$ N/mm² x  {L[1]:,.0f} mm {div2} = {w:.2f} N/mm')

        st.write('')  ## 빈줄 공간
        st.write(s1, '3) 응력 검토')
        st.write(s2, '① 휨응력 검토')
        Mmax = w*L[0]**2/8;  fb = Mmax/S
        num_str = rf'$\large{{\frac{{ {w:,.2f} × {L[0]:,.0f}^2}}{{8}} }} \normalsize \; = \;$'
        st.write(s3, rf'✦ $M_{{max}} \; = \; \large{{\frac{{ w {L_str[0]}^2 }} {{8}} }} \normalsize \; = \;$', num_str, rf'{Mmax:,.1f} N&#8226;mm')
        [lgeq, okng] = ['\leq', In.ok] if fb <= fba else ['\geq', In.ng]
        num_str = rf'$\large{{\frac{{ {Mmax:,.1f}}}{{{S:,.1f}}} }} \normalsize \; = \;$'
        [col1, col2] = st.columns(In.col_span_okng)
        with col1:
            st.write(s3, rf'✦ $f_b \; = \; \large{{\frac{{M_{{max}}}}{{S}} }} \normalsize \; = \;$', num_str, f'{fb:.1f} MPa', rf'$\: \; {lgeq} \;$', f'{fba:.1f} MPa', r'$( \; = \; f_{ba})$')
        with col2: st.write(h5, okng)

        st.write('')  ## 빈줄 공간
        st.write(s2, '② 전단응력 검토')
        Vmax = w*L[0]/2;  fs = Vmax/Ib_Q        
        num_str = rf'$\large{{\frac{{ {w:,.4f} × {L[0]:,.0f}}}{{2}} }} \normalsize \; = \;$'
        st.write(s3, rf'✦ $V_{{max}} \; = \; \large{{\frac{{ w {L_str[0]} }}{{2}}}} \normalsize \; = \;$', num_str, rf'{Vmax:,.1f} N')
        [lgeq, okng] = ['\leq', In.ok] if fs <= fsa else ['\geq', In.ng]
        num_str = rf'$\large{{\frac{{ {Vmax:,.1f}}}{{{Ib_Q:,.1f}}} }} \normalsize \; = \;$'
        [col1, col2] = st.columns(In.col_span_okng)
        with col1:     st.write(s3, rf'✦ $f_s \; = \; \large{{\frac{{V_{{max}}}}{{Ib/Q}} }} \normalsize \; = \;$', num_str, f'{fs:.1f} MPa', rf'$\: \; {lgeq} \;$', f'{fsa:.1f} MPa', r'$( \; = \; f_{sa})$')
        with col2: st.write(h5, okng)

        st.write('')  ## 빈줄 공간
        st.write(s1, '4) 변형 검토')
        dmax = 5*w*L[0]**4 / (384*E*I);  da = L[0] / 100
        num_str = rf'$\large{{\frac{{5 × {w:,.4f} × {L[0]:,.0f}^4}}{{384 × {E:,.0f} × {I:,.0f} }} }} \normalsize \; = \;$'
        st.write(s2, rf'✦ $\delta_{{max}} \;= \; \large{{\frac{{5\, w {L_str[0]}^4}}{{384\,E\,I}}}} \normalsize{{\; = \;}}$', num_str, f'{dmax:,.2f} mm')
        st.write(s2, rf'✦ 허용변위 : $\delta_a \;= \; \large{{\frac{{{L_str[0]}}}{{100}}}} \normalsize{{\; = \;}} \large \frac{{{L[0]:,.0f}}}{{100}} \small = {da:,.2f}$ mm')

        [lgeq, okng] = ['\leq', In.ok] if dmax <= da else ['\geq', In.ng]
        [col1, col2] = st.columns(In.col_span_okng)
        with col1: st.write(s2, rf'✦ ∴ $\delta_{{max}} \; {lgeq} \; \delta_{{a}}$')
        with col2: st.write(h5, okng)  

    else:    # 동바리
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
        L_jyv2 = rf'${L_jyv} \textcolor{{{color}}}{{\; = {L[1]:,.1f} \rm{{\; mm}}}}$'

        st.write(h4, opt[2] + opt[0] + ' 및 ' + opt[1] + f'(${L_jyv}$) 검토')
        Table.Info(opt[0], section, A, Ib_Q, I, S, E, fba, fsa, 20)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(s1, '1) 개요')
            st.write(s2, '➣ 등분포 하중을 받는 단순보로 계산한다.')
            st.write(s2, '➣ ' + L_jyv2)

            st.write('')  ## 빈줄 공간
            st.write(s1, '2) ' + opt[0] + f'에 재하되는 하중 (${w_str}$) [폭 : {width_str}]')
            st.write(s2, rf'➣ ${w_str} = $ 설계 하중 x ' + width_str)
            precision = 4 if '합판' in opt[0] else 2
            st.write(s2, rf'➣ $\small{{ {w_str} = {In.design_load:.4f}}}$ N/mm² x  {L[0]:,.1f} mm = {w:.{precision}f} N/mm')
        with col2:
            st.image(img, width=500)

        st.write('')  ## 빈줄 공간
        st.write(s1, '3) 응력 검토')
        st.write(s2, '① 휨응력 검토')
        Mmax = w*L[1]**2/8;  fb = Mmax/S
        num_str = rf'$\large{{\frac{{ {w:,.4f} × {L[1]:,.1f}^2}}{{8}} }} \normalsize \; = \;$'
        st.write(s3, rf'✦ $M_{{max}} \; = \; \large{{\frac{{{w_str} {L_jyv}^2}}{{8}}}} \normalsize \; = \;$', num_str, rf'{Mmax:,.1f} N&#8226;mm')
        [lgeq, okng] = ['\leq', In.ok] if fb <= fba else ['\geq', In.ng]
        num_str = rf'$\large{{\frac{{ {Mmax:,.1f}}}{{{S:,.1f}}} }} \normalsize \; = \;$'
        [col1, col2] = st.columns(In.col_span_okng)
        with col1:
            st.write(s3, rf'✦ $f_b \; = \; \large{{\frac{{M_{{max}}}}{{S}} }} \normalsize \; = \;$', num_str, f'{fb:.1f} MPa', rf'$ \: \; {lgeq} \;$', f'{fba:.1f} MPa', r'$( \; = \; f_{ba})$')
        with col2: st.write(h5, okng)
        
        st.write('')  ## 빈줄 공간
        st.write(s2, '② 전단응력 검토')
        Vmax = w*L[1]/2;  fs = Vmax/Ib_Q
        # fs_str = 'Ib/Q' if '합판' in opt[0] else 'A'
        num_str = rf'$\large{{\frac{{ {w:,.4f} × {L[1]:,.1f}}}{{2}} }} \normalsize \; = \;$'
        st.write(s3, rf'✦ $V_{{max}} \; = \; \large{{\frac{{ {{{w_str}}} {L_jyv}}}{{2}}}} \normalsize \; = \;$', num_str, rf'{Vmax:,.2f} N')        
        [lgeq, okng] = ['\leq', In.ok] if fs <= fsa else ['\geq', In.ng]
        num_str = rf'$\large{{\frac{{ {Vmax:,.1f}}}{{{Ib_Q:,.1f}}} }} \normalsize \; = \;$'
        [col1, col2] = st.columns(In.col_span_okng)
        with col1:     st.write(s3, rf'✦ $f_s \; = \; \large{{\frac{{V_{{max}}}}{{Ib/Q}} }} \normalsize \; = \;$', num_str, f'{fs:.2f} MPa', rf'$\: \; {lgeq} \;$', f'{fsa:.2f} MPa', r'$( \; = \; f_{sa})$')
        with col2: st.write(h5, okng)

        st.write('')  ## 빈줄 공간
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '4) 변형 검토 (표면 등급 : :blue[', In.level, '] )')
        with col2: st.write(h5, ':orange[ <근거 : 1.9 변형기준 (KDS 21 50 00 : 2022)>]')

        Ld1 = (384*E*I*L[1]/(5*w*In.d1))**(1/4);  Ld2 = (384*E*I*In.d2/(5*w))**(1/4)
        st.write(s2, '① 상대변형 검토')
        st.write(s3, rf'✦ $\delta_{{max}} \;= \; \large{{\frac{{5\,{{{w_str}}} {L_jyv}^4}}{{384\,E\,I}}}} \normalsize{{\; \leq \;}}$', In.d1_str)
        num_str = rf"$\large{{\sqrt[4]{{\frac{{384 × {E:,.1f} × {I:,.1f} × {L[1]:,.1f}}}{{5 × {w:,.4f} × 360 }}}} }} \; \normalsize = \;$"
        st.write(s3, rf'✦ ${L_jyv} \; \leq \; \large\sqrt[4]{{\frac{{384\,E\,I\,L_n}}{{{{5\,{{{w_str}}}}}\,{{{In.d1:.0f}}} }}}} \; \normalsize = \;$', num_str + f'{Ld1:,.1f} mm')
        [lgeq, okng] = ['\leq', In.ok] if L[1] <= Ld1 else ['\geq', In.ng]
        [col1, col2] = st.columns(In.col_span_okng)
        with col1: st.write(s3, '✦ ', L_jyv2, rf'$\; {lgeq} \;$' + f'{Ld1:,.1f} mm')
        with col2: st.write(h5, okng)    

        st.write('')  ## 빈줄 공간
        st.write(s2, '② 절대변형 검토')
        st.write(s3, rf'✦ $\delta_{{max}} \; = \; \large{{\frac{{5\,{{{w_str}}} {L_jyv}^4}}{{384\,E\,I}}}} \normalsize \; \leq \;$', In.d2_str)
        num_str = rf'$\large{{\sqrt[4]{{\frac{{384 × {E:,.1f} × {I:,.1f} × 3}}{{5 × {w:,.4f} }}}} }} \normalsize \; = \;$'
        st.write(s3, rf'✦ ${L_jyv} \; \leq \; \large\sqrt[4]{{\frac{{384\,E\,I\,{{{In.d2:.0f}}}}}{{5\,{{{w_str}}} }}}} \normalsize \; = \;$', num_str + rf'{Ld2:,.1f} mm')
        [lgeq, okng] = ['\leq', In.ok] if L[1] <= Ld2 else ['\geq', In.ng]
        [col1, col2] = st.columns(In.col_span_okng)
        with col1: st.write(s3, '✦ ', L_jyv2, rf'$\; {lgeq} \;$' + f'{Ld2:,.1f} mm')
        with col2: st.write(h5, okng)    

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!수직재, 수평재, 가새재 체크  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Check_Support(In, opt, section, Support):
    [A, I, S, E, r, Fy, Ib_Q] = [Support.A, Support.I, Support.S, Support.E, Support.r, Support.Fy, Support.Ib_Q]    

    P = In.Pv2 if '비계' in In.type else In.design_load*In.Ly*In.Lv/1e3 #kN
    H = max(In.Hx, In.Hy)  #kN
    if '수직재' in opt[0]:
        Load_str = 'P';   Load = P
        KL_str = 'KL_v';  KL = In.KLv;  KL_cal = ''
    if '수평재' in opt[0]:
        Load_str = 'H';   Load = H
        KL_str = 'KL_h';  KL = In.KLh;  KL_cal = ''
    if '가새재' in opt[0]:
        Load_str = 'H';   Load = H
        KL_str = 'KL_d';  KL = np.sqrt(In.KLv**2 + In.KLh**2)
        KL_cal = rf'$\small{{\sqrt{{ {In.KLv:,.0f}^2 + {In.KLh:,.0f}^2 }} }}$ = '

    if '비계' in In.type and '수평재' in opt[0]:
        st.write(h4, opt[1] + opt[0] + '(띠장) 검토')
    else:
        st.write(h4, opt[1] + opt[0] + ' 검토')
    Table.Info(opt[0], section, A, Ib_Q, I, S, E, r, Fy, 20)

    if '수직재' in opt[0]:
        st.write(s1, '1) 1본당 작용하중 (P)')
        if '비계' in In.type:
            st.write(s2, rf'➣ P = {P:,.1f} kN/EA &nbsp; [:green[Ⅱ. 2 설계하중 산정] 참조]')
        else:  # 동바리
            st.write(s2, '➣ P = 설계 하중 x 멍에 간격 x 수직재 간격')
            st.write(s2, rf'➣ P = {In.design_load:.4f} N/mm² x {In.Ly:,.1f} mm x {In.Lv:,.1f} mm = {P:,.1f} kN/EA')
    else:
        st.write(s1, '1) 수평하중 (H)')
        st.write(s2, f'➣ X방향 수평하중 (H$_{{x}}$) = {In.Hx:.2f} kN')
        st.write(s2, f'➣ Y방향 수평하중 (H$_{{y}}$) = {In.Hy:.2f} kN')

    st.write('')  ## 빈줄 공간
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '2) 허용압축응력 (' + r'$\small{{F_{ca}}}$' + ') 산정')
    with col2: st.write(h5, ':orange[ <근거 : 4.4.3 허용압축응력 (KDS 14 30 10 : 2019)> ]')
    
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s2, '➣ 유효 좌굴길이 ')
    with col2: st.write(h5, ':orange[ <근거 : 4.4.2 좌굴길이와 세장비 (KDS 14 30 10 : 2019)> ]')
    st.write(s3, rf'￭ $\small{{{KL_str}}} = $', KL_cal, f'{KL:,.1f} mm')
    num_str = rf'$\large{{\frac{{{KL:,.1f}}}{{{r:,.1f}}}}} \; = \;$';  lamda = KL/r    
    [lgeq, okng] = ['\leq', In.ok] if lamda <= 200 else ['\geq', In.ng]
    st.write(s2, '➣ 세장비')
    [col1, col2] = st.columns(In.col_span_okng)
    with col1:
        st.write(s3, rf'￭ $\lambda = \large{{\frac{{{KL_str}}}{{r}}}}$ = ' + num_str + f'{lamda:,.1f}', rf'$\; {lgeq} \:$ 200 (최대 세장비)')
    with col2: st.write(h5, okng)

    num_str = rf'$\large\sqrt{{\frac{{2 \pi^2 × {E:,.0f}}}{{{Fy:,.1f}}}}}$ = ';  Cc = np.sqrt(2*np.pi**2*E/Fy)
    st.write(s2, '➣ 한계 세장비')
    st.write(s3, rf'￭ $C_c = \large\sqrt{{\frac{{2 \pi^2 E}}{{F_y}}}}$ = ' + num_str + f'{Cc:,.1f}')

    if lamda <= Cc:
        a = (1 - lamda**2/(2*Cc**2)) *Fy;  b = 5/3 + 3*lamda/(8*Cc) - lamda**3/(8*Cc**3)
        a_str = rf'\left[1 - \large\frac{{(KL/r)^2}}{{2 C_c^2}}\right] F_y'
        b_str = rf'\large\frac{{5}}{{3}} + \frac{{3 (KL/r)}}{{8 C_c}} - \frac{{(KL/r)^3}}{{8 C_c^3}}'
        Fca = a/b;  lgeq = '\leq'
    else:
        a = 12*np.pi**2 *E;  b = 23*lamda**2
        a_str = '12 \pi^2 E';  b_str = '23 (KL/r)^2'
        Fca = a/b;  lgeq = '\geq'
    st.write(s2, '➣ ' + rf'$\lambda = \large{{\frac{{{KL_str}}}{{r}} \normalsize \; {lgeq} \; C_c}}$', ' 이므로')
    st.write(s3, rf'￭ $F_{{ca}} = {{\large{{\frac{{{a_str}}}{{{b_str}}} }} }} \normalsize \; = \;$' + f'{Fca:,.1f} MPa')

    st.write('')  ## 빈줄 공간    
    [col1, col2] = st.columns(In.col_span_ref)    

    if '비계' in In.type:
        with col1: st.write(s1, '3) 안전율 검토')
        with col2: st.write(h5, ':orange[ <근거 : 3.1 (3) 안전율 (KDS 21 60 00 : 2022)>]')
        Pa = Fca*A/1e3*np.cos(np.pi/3) if '가새재' in opt[0] else Fca*A/1e3  # 가새재 최대 경사(60도) 고려
        SF = Pa/Load
        txt1 = '';  txt2 = '';  txt3 = ''
        if '가새재' in opt[0]:  txt1 = '**';  txt2 = rf'\rm{{cos(60°)}} ×';  txt3 = '0.5 x '
        st.write(s2, f'➣ 허용압축하중{txt1} $\; : \;$', rf'$\small{{P_a = {txt2} F_{{ca}} × A}}$ = {txt3} {Fca:,.1f} MPa x {A:,.1f} mm² = {Pa:,.1f} kN')
        [lgeq, okng] = ['\geq', In.ok] if SF >= 3.0 else ['\leq', In.ng]
        [col1, col2] = st.columns(In.col_span_okng)
        with col1:
            st.write(s2, '➣ 안전율 검토 $\; : \;$ ', rf'$S.F = \large\frac{{P_a}}{{{Load_str}}} \normalsize = \large\frac{{ {Pa:,.1f} }}{{ {Load:,.1f} }} \normalsize = \: $' + f'{SF:.1f}', rf'$\; {lgeq} \;$ 3.0 (안전율*) $\qquad$')
        with col2: st.write(h5, okng)        
        st.write('###### $\quad \qquad$', ':blue[*인장, 휨 안전율 2.0, 전단, 압축 안전율 3.0 적용]')
        if '가새재' in opt[0]:  st.write('###### $\quad \qquad$', ':blue[**가새재의 최대 각도(60°)를 고려한 허용압축하중]')
    
    else:   # 동바리
        if '수직재' in opt[0]:
            with col1: st.write(s1, '3) 안전율 검토')
            with col2: st.write(h5, ':orange[ <근거 : 1.8 안전율 (KDS 21 50 00 : 2022)>]')
            Pa = Fca*A/1e3;  SF = Pa/Load        
            st.write(s2, '➣ 허용압축하중 $\; : \;$', rf'$\small{{P_a = F_{{ca}} × A}}$ = {Fca:,.1f} MPa x {A:,.1f} mm² = {Pa:,.1f} kN')
            [lgeq, okng] = ['\geq', In.ok] if SF >= 2.5 else ['\leq', In.ng]
            [col1, col2] = st.columns(In.col_span_okng)
            with col1:
                st.write(s2, '➣ 안전율 검토 $\; : \;$ ', rf'$S.F = \large\frac{{P_a}}{{{Load_str}}} \normalsize = \large\frac{{ {Pa:,.1f} }}{{ {Load:,.1f} }} \normalsize = \: $' + f'{SF:.1f}', rf'$\; {lgeq} \;$ 2.5 (안전율*) $\qquad$')
            with col2: st.write(h5, okng)
            st.write('###### $\quad \qquad$', ':blue[*단품 동바리 안전율 3.0, 조립식 동바리 안전율 2.5 적용]')
        else:
            with col1: st.write(s1, f'3) {opt[0]} 수량')
            if '수평재' in opt[0]:  Pa = Fca*A/1e3
            if '가새재' in opt[0]:  Pa = Fca*A/1e3*np.cos(np.pi/3)  # 가새재 최대 경사(60도) 고려
            EAx = In.Hx/Pa;  EAy = In.Hy/Pa
            if '수평재' in opt[0]:  txt1 = '';  txt2 = '';  txt3 = ''
            if '가새재' in opt[0]:  txt1 = '*';  txt2 = rf'\rm{{cos(60°)}} ×';  txt3 = '0.5 x '
            st.write(s2, f'➣ 허용압축하중{txt1} $\; : \;$', rf'$\small{{P_a = {txt2} F_{{ca}} × A}}$ = {txt3} {Fca:,.1f} MPa x {A:,.1f} mm² = {Pa:,.1f} kN')
            st.write(s2, f'➣ X방향 {opt[0]} 수량 $\; : \;$',  rf'$\bm{{\large\frac{{X방향 수평하중}}{{허용압축하중}} \normalsize = \large\frac{{ {In.Hx:,.1f} }}{{ {Pa:,.1f} }} \normalsize = \: }}$' + f'{EAx:.1f} EA 이상')
            st.write(s2, f'➣ Y방향 {opt[0]} 수량 $\; : \;$',  rf'$\bm{{\large\frac{{Y방향 수평하중}}{{허용압축하중}} \normalsize = \large\frac{{ {In.Hy:,.1f} }}{{ {Pa:,.1f} }} \normalsize = \: }}$' + f'{EAy:.1f} EA 이상')
            if '가새재' in opt[0]:  st.write('###### $\quad \qquad$', ':blue[*가새재의 최대 각도(60°)를 고려한 허용압축하중]')
            
    return Fca