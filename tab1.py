import streamlit as st
import numpy as np
import table

def Tab(In, color, fn, s1, s2, s3, h4, h5, Wood, Joist, Yoke):
    border1 = '<hr style="border-top: 5px double ' + color + '; margin-top: 0px; margin-bottom:30px; border-radius: 10px">'
    border2 = '<hr style="border-top: 2px solid ' + color + '; margin-top:30px; margin-bottom:30px; border-radius: 10px">'
    [s_h, s_t, s_weight, w_weight, w_s, w_t, w_angle, level, d1, d2, Ln] = [In.s_h, In.s_t, In.s_weight, In.w_weight, In.w_s, In.w_t, In.w_angle, In.level, In.d1, In.d2, In.Ln]

    st.markdown(border1, unsafe_allow_html=True)
    st.write(h4, '1. 설계하중 산정')
    st.write(s1, '1) 연직하중 (고정하중 + 작업하중)')
    t_load = table.Load(fn, s_t, s_weight, w_weight)/1e3        
    st.write(s3, '*콘크리트 타설 높이가 0.5m 미만인 경우 :blue[2.5kN/m²], 0.5m 이상 1m 미만인 경우 :blue[3.5kN/m²], 1m 이상인 경우 :blue[5kN/m² 이상] 적용')

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
        w_str = 'ω_w';  load_str = '합판이 받는 하중 ($\pmb{{{}}}$) [폭 : 단위폭 1mm]'.format(w_str)        
        img = 'wood.png'
        margin = In.j_margin
        AIb_Q = Ib_Q        
        style = In.w_s
        
    if '장선' in opt[0]:
        [A, I, S, E, fba, fsa, section] = [Joist.A, Joist.I, Joist.S, Joist.E, Joist.fba, Joist.fsa, Joist.section]
        color = 'green';  txt = '{L_y}'  # L_str        
        w_str = 'ω_j';  load_str = '장선이 받는 하중 ($\pmb{{{}}}$) [폭 : 장선 간격]'.format(w_str)        
        img = 'joist.png'
        margin = In.y_margin
        AIb_Q = A        
        style = In.j_s[0]

    if '멍에' in opt[0]:
        [A, I, S, E, fba, fsa, section] = [Yoke.A, Yoke.I, Yoke.S, Yoke.E, Yoke.fba, Yoke.fsa, Yoke.section]
        color = 'blue';  txt = '{L_s}'  # L_str        
        w_str = 'ω_y';  load_str = '멍에가 받는 하중 ($\pmb{{{}}}$) [폭 : 멍에 간격]'.format(w_str)        
        img = 'yoke.png'
        margin = In.s_margin
        AIb_Q = A        
        style = In.j_s[1]

    # load_str = opt[0] + '이(가) 받는 하중 ($\pmb{{{0}}}$) [폭 : {{{1}}}]'.format(w_str, width_str)  #이, 가 로 안됨 ㅠㅠㅠ
    
    L_str = r'\textcolor{'+color+'}'+txt
    st.write(h4, title + r'(${\small\pmb{%s}}$) 결정' %L_str)
    table.Info(fn, style, section, AIb_Q, I, S, E, fba, fsa, 20)    
    col1, col2 = st.columns([1.7, 1])
    with col1:
        st.write(s1, '1) 개요')
        st.write(s2, '➣ 등분포 하중을 받는 단순보로 계산한다.')
        st.write(s1, '2) ' + load_str)
        st.write(s2, '➣ $\pmb{{{}}}$ = '.format(w_str) + '설계 하중 x ' + width_str)
        st.write(s2, '➣ $\pmb{{{}}}$ = {:0.4f}'.format(w_str, t_load) + ' N/mm² x '+str(round(L))+' mm = {:.4f}'.format(w) + ' N/mm')
    with col2:
        st.image(img, width=550)

    st.write(s1, '3) ' + interval_str)
    st.write(s2, '① 휨응력에 의한 간격 검토')  #\color{red}, \textcolor{blue}{}(범위 지정), \boldsymbol [\pmb or \pmb], \small, \normalize, \large, \Large    
    st.write(s3, r'$\pmb{{\quad M = \Large{{\frac{{{0}\textcolor{{red}}{{{1}}}^2}}{{8}}}} \normalsize \leq f_{{ba}}\,S}} $'.format(w_str, L_str))
    Lm = (8*fba*S/w)**(1/2)
    num_str = rf"$$\pmb{{\Large{{\sqrt{{\frac{{8 \times {fba} \times {S}}}{{{round(w,4)}}} }} }} \normalsize = \:}}$$"    
    st.write(s3, r'$\pmb{{\quad\textcolor{{red}}{{{0}}}\leq \Large\sqrt{{\frac{{8\,f_{{ba}}\,S}}{{{1}}}}} \normalsize = \:}} $'.format(L_str, w_str), num_str + '{:.1f}'.format(Lm) + ' mm')
    
    st.write(s2, '② 변위에 의한 간격 검토 (:red[', level, '] )' + ':orange[  <근거 : 1.9 변형기준 (KDS 21 50 00 : 2022)>]')    
    import re
    pattern = r'\d+'
    j1 = re.findall(pattern, d1);  j1 = float(j1[0]);  Ld1 = (384*E*I*Ln/(5*w*j1))**(1/4)
    j2 = re.findall(pattern, d2);  j2 = float(j2[0]);  Ld2 = (384*E*I*j2/(5*w))**(1/4)
    st.write(s3, 'a. 상대변형 기준')
    st.write(s3, r'$\pmb{{\quad \delta = \Large{{\frac{{5\,{{{0}}} \textcolor{{red}}{{{1}}}^4}}{{384\,E\,I}}}} \normalsize \leq}} $'.format(w_str, L_str), d1)
    st.write(s3, r'$\pmb{{\quad\textcolor{{red}}{{{0}}} \leq \Large\sqrt[4]{{\frac{{384\,E\,I\,L_n}}{{{{5\,{{{1}}}}}\,{{{2}}} }}}} \normalsize = \:}} $'.format(L_str, w_str, round(j1)) + '{:.1f}'.format(Ld1) + ' mm')

    st.write(s3, 'b. 절대변형 기준')
    st.write(s3, r'$\pmb{{\quad \delta = \Large{{\frac{{5\,{{{0}}} \textcolor{{red}}{{{1}}}^4}}{{384\,E\,I}}}} \normalsize \leq}} $'.format(w_str, L_str), d2)
    st.write(s3, r'$\pmb{{\quad\textcolor{{red}}{{{0}}} \leq \Large\sqrt[4]{{\frac{{384\,E\,I\,{{{2}}}}}{{5\,{{{1}}} }}}} \normalsize = \:}} $'.format(L_str, w_str, round(j2)) + '{:.1f}'.format(Ld2) + ' mm')

    st.write(s2, '③ '+opt[1]+' 간격 검토결과')
    table.Interval(fn, Lm, Ld1, Ld2)
    L = round(min(Lm, Ld1, Ld2)*margin/100, -1)
    st.write(s3, '➣ 검토 항목 중 최솟값 이하 간격으로 설치한다.')
    # margin = r'\textcolor{orange}{'+str(round(margin))+'}'
    st.write(s3, '➣ '+opt[1]+' 간격을', r'$\pmb{{\small \: \textcolor{{blue}}{{{0}}} = }}$'.format(L_str) + ':orange['+str(round(L)), 'mm] 간격으로 설치한다. (:orange[최솟값의]', r'$\pmb{{\small \textcolor{{orange}}{{{0}}} }}$'.format(round(margin))+':orange[%] 정도로 설정)')
    
    st.write(s2, '④ 전단 검토')
    Vmax = w*L/2 #max(Ljm, Lj1, Lj2)/2
    if '합판' in opt[0]:
        fs = Vmax/Ib_Q;  fs_str = 'Ib/Q'
    else:
        fs = Vmax/A;  fs_str = 'A'
    st.write(s3, r'$\pmb{{\quad V_{{max}} = \Large{{\frac{{ {{{0}}}\,\textcolor{{red}}{{{1}}}}} {{2}}}} \normalsize =}}$'.format(w_str, L_str), '{:.2f}'.format(Vmax) + ' N')
    if fs <= fsa:
        st.write(s3, r"$\pmb{{\quad f_s = \Large{{\frac{{V_{{max}}}}{{{0}}} }} \normalsize =}}$".format(fs_str) + " {:.2f}".format(fs) + ' MPa', r'$\pmb \leq$', '{:.2f}'.format(fsa) + ' MPa', r'$\pmb {( = f_{sa})} \qquad$', ':blue[OK]')
    else:
        st.write(s3, r"$\pmb{{\quad f_s = \Large{{\frac{{V_{{max}}}}{{{0}}} }} \normalsize =}}$".format(fs_str) + " {:.2f}".format(fs) + ' MPa', r'$\pmb \leq$', '{:.2f}'.format(fsa) + ' MPa', r'$\pmb {( = f_{sa})} \qquad$', ':red[NG]')

    return L


