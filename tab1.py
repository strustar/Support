import streamlit as st
import numpy as np
import table

def Tab(In, color, fn, s1, s2, s3, h4, h5, Wood, Joist, Yoke):
    border1 = '<hr style="border-top: 5px double ' + color + '; margin-top: 0px; margin-bottom:30px; border-radius: 10px">'
    border2 = '<hr style="border-top: 2px solid ' + color + '; margin-top:30px; margin-bottom:30px; border-radius: 10px">'
    [s_weight, w_weight, w_s, w_t, w_angle, level, d1, d2, Ln] = [In.s_weight, In.w_weight, In.w_s, In.w_t, In.w_angle, In.level, In.d1, In.d2, In.Ln]

    st.markdown(border1, unsafe_allow_html=True)
    st.write(h4, '1. 설계하중 산정')
    st.write(s1, '1) 연직하중 (고정하중 + 작업하중)' + '$\qquad$ :orange[ <근거 : 1.6.2 연직하중 (KDS 21 50 00 : 2022)>]')
    t_load = table.Load(fn, In.thick_height, s_weight, w_weight)/1e3    
    st.write('###### $\quad \qquad$', '*콘크리트 타설 높이가 0.5m 미만인 경우 :blue[2.5kN/m²], 0.5m 이상 1m 미만인 경우 :blue[3.5kN/m²], 1m 이상인 경우 :blue[5kN/m² 이상] 적용')

    st.write(s1, '2) 수평하중' + '$\qquad$ :orange[ <근거 : 1.6.5 수평하중 (KDS 21 50 00 : 2022)>]')
    

    st.markdown(border2, unsafe_allow_html=True)
    opt = ['합판','장선', '2. '];  Lj = Check(In, opt, fn, s1, s2, s3, h4, h5, Wood, Joist, Yoke, t_load, level, d1, d2, Ln, 1)
    st.markdown(border2, unsafe_allow_html=True)
    opt = ['장선','멍에', '3. '];  Ly = Check(In, opt, fn, s1, s2, s3, h4, h5, Wood, Joist, Yoke, t_load, level, d1, d2, Ln, Lj)
    st.markdown(border2, unsafe_allow_html=True)
    opt = ['멍에','동바리', '4. '];  Ls = Check(In, opt, fn, s1, s2, s3, h4, h5, Wood, Joist, Yoke, t_load, level, d1, d2, Ln, Ly)
    st.markdown(border2, unsafe_allow_html=True)

    return t_load, Lj, Ly, Ls


def Check(In, opt, fn, s1, s2, s3, h4, h5, Wood, Joist, Yoke, t_load, level, d1, d2, Ln, L):
    title = opt[2] + opt[0] + ' 검토 및 ' + opt[1] + ' 간격'
    interval_str = opt[1] + ' 간격'
    width_str = '단위폭 1mm' if '합판' in opt[0] else opt[0] + ' 간격'
    w = t_load*L

    if '합판' in opt[0]:
        [A, I, S, E, fba, fsa, Ib_Q, section] = [Wood.A, Wood.I, Wood.S, Wood.E, Wood.fba, Wood.fsa, Wood.Ib_Q, Wood.section]
        color = 'magenta';  txt = '{L_j}'  # L_str        
        w_str = 'ω_w'
        img = 'wood.png';  margin = In.j_margin;  AIb_Q = Ib_Q;  shape = In.w_s
        
    if '장선' in opt[0]:
        [A, I, S, E, fba, fsa, section] = [Joist.A, Joist.I, Joist.S, Joist.E, Joist.fba, Joist.fsa, Joist.section]
        color = 'green';  txt = '{L_y}'  # L_str        
        w_str = 'ω_j'
        img = 'joist.png';  margin = In.y_margin;  AIb_Q = A;  shape = In.j_s[0]

    if '멍에' in opt[0]:
        [A, I, S, E, fba, fsa, section] = [Yoke.A, Yoke.I, Yoke.S, Yoke.E, Yoke.fba, Yoke.fsa, Yoke.section]
        color = 'blue';  txt = '{L_s}'  # L_str        
        w_str = 'ω_y'
        img = 'yoke.png';  margin = In.s_margin;  AIb_Q = A;  shape = In.j_s[1]

    load_str = opt[0] + rf'에 재하되는 하중 ($\bm{{{w_str}}}$) [폭 : {width_str}]'  #이, 가 로 안됨 ㅠㅠㅠ    
    L_str = rf'\textcolor{{{color}}}' + txt
    st.write(h4, title + rf'($\small\bm{{{L_str}}}$) 결정')
    table.Info(fn, shape, section, AIb_Q, I, S, E, fba, fsa, 20)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(s1, '1) 개요')
        st.write(s2, '➣ 등분포 하중을 받는 단순보로 계산한다.')
        st.write(s1, '2) ' + load_str)
        st.write(s2, rf'➣ $\bm{{{w_str}}}$ = 설계 하중 x ' + width_str)
        precision = 4 if '합판' in opt[0] else 2
        st.write(s2, rf'➣ $\bm{{\small{{{w_str} = {t_load:0.4f}}} }}$ N/mm² x  {L:0.1f} mm = {w:.{precision}f} N/mm')
    with col2:
        st.image(img, width=500)

    st.write(s1, '3) ' + interval_str)
    st.write(s2, '① 휨응력에 의한 간격 검토')  #\color{red}, \textcolor{blue}{}(범위 지정), \bm, \textbf, \boldsymbol [\pmb], \small, \normalize, \large, \Large    
    st.write(s3, rf'$\bm{{\quad M = \Large{{\frac{{{w_str}\textcolor{{red}}{{{L_str}}}^2}}{{8}}}} \normalsize \leq f_{{ba}}\,S}} $')    
    Lm = (8*fba*S/w)**(1/2)
    num_str = rf"$\bm{{\Large{{\sqrt{{\frac{{8 \times {fba:.1f} \times {S:,.1f}}}{{{w:.4f}}} }} }} \normalsize = \:}}$"
    st.write(s3, rf'$\bm{{\quad\textcolor{{red}}{{{L_str}}}\leq \Large\sqrt{{\frac{{8\,f_{{ba}}\,S}}{{{w_str}}}}} \normalsize = \:}} $', num_str + f'{Lm:,.1f} mm')
        
    st.write(s2, '② 변위에 의한 간격 검토 (:red[', level, '] )' + '$\qquad$ :orange[ <근거 : 1.9 변형기준 (KDS 21 50 00 : 2022)>]')
    import re
    pattern = r'\d+'
    j1 = re.findall(pattern, d1);  j1 = float(j1[0]);  Ld1 = (384*E*I*Ln/(5*w*j1))**(1/4)
    j2 = re.findall(pattern, d2);  j2 = float(j2[0]);  Ld2 = (384*E*I*j2/(5*w))**(1/4)
    st.write(s3, 'a. 상대변형 기준')
    st.write(s3, rf'$\bm{{\quad \delta = \Large{{\frac{{5\,{{{w_str}}} \textcolor{{red}}{{{L_str}}}^4}}{{384\,E\,I}}}} \normalsize \leq}} $', d1)
    num_str = rf"$\bm{{\Large{{\sqrt[4]{{\frac{{384 \times {E:,.1f} \times {I:,.1f} \times {Ln:,.1f}}}{{5 \times {w:,.4f} \times 360 }}}} }} \normalsize = \:}}$"
    st.write(s3, rf'$\bm{{\quad\textcolor{{red}}{{{L_str}}} \leq \Large\sqrt[4]{{\frac{{384\,E\,I\,L_n}}{{{{5\,{{{w_str}}}}}\,{{{j1:.0f}}} }}}} \normalsize = \:}} $', num_str + f'{Ld1:,.1f} mm')

    st.write(s3, 'b. 절대변형 기준')
    st.write(s3, rf'$\bm{{\quad \delta = \Large{{\frac{{5\,{{{w_str}}} \textcolor{{red}}{{{L_str}}}^4}}{{384\,E\,I}}}} \normalsize \leq}} $', d2)
    num_str = rf'$\bm{{\Large{{\sqrt[4]{{\frac{{384 \times {E:,.1f} \times {I:,.1f} \times 3}}{{5 \times {w:,.4f} }}}} }} \normalsize = \:}}$'
    st.write(s3, rf'$\bm{{\quad\textcolor{{red}}{{{L_str}}} \leq \Large\sqrt[4]{{\frac{{384\,E\,I\,{{{j2:.0f}}}}}{{5\,{{{w_str}}} }}}} \normalsize = \:}} $', num_str + rf'{Ld2:,.1f} mm')

    st.write(s2, '③ '+opt[1]+' 간격 검토결과')
    table.Interval(fn, Lm, Ld1, Ld2)
    L = round(min(Lm, Ld1, Ld2)*margin/100, -1)
    st.write(s3, '➣ 검토 항목 중 최솟값 이하 간격으로 설치한다.')    
    st.write(s3, '➣ '+opt[1]+' 간격을', rf'$\bm{{\small \: \textcolor{{blue}}{{{L_str}}} = }}$ :orange['+f'{L:,.0f}', 'mm] 간격으로 설치한다. (:orange[최솟값의]', rf'$\bm{{\small \textcolor{{orange}}{{{margin:.0f}}} }}$'+':orange[%] 정도로 설정)')
    
    st.write(s2, '④ 전단 검토')
    Vmax = w*L/2;  fs = Vmax/AIb_Q
    fs_str = 'Ib/Q' if '합판' in opt[0] else 'A'
    num_str = rf'$\boldsymbol{{\Large{{\frac{{ {w:,.4f} \times {L:,.1f}}}{{2}} }} \normalsize = \:}} $'    
    st.write(s3, rf'$\bm{{\quad V_{{max}} = \Large{{\frac{{ {{{w_str}}} \textcolor{{red}}{{{L_str}}}}}{{2}}}} \normalsize = \:}} $', num_str, rf'{Vmax:,.2f} N')
    num_str = rf'$\bm{{\Large{{\frac{{ {Vmax:,.1f}}}{{{AIb_Q:,.1f}}} }} \normalsize = \:}} $'    
    okng = ':blue[OK]' if fs <= fsa else ':red[NG]'
    st.write(s3, rf'$\boldsymbol{{\quad f_s = \Large{{\frac{{V_{{max}}}}{{{fs_str}}} }} \normalsize =}}$', num_str, f'{fs:.2f} MPa', rf'$\: \bm{{\leq}} \:$', f'{fsa:.2f} MPa', r'$\bm {( = f_{sa})} \qquad$', okng)

    return L

