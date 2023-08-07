import streamlit as st
import numpy as np
from Sidebar import word_wrap_style
import Table

class Wood: pass
class Joist: pass
class Yoke: pass
class Vertical: pass
class Horizontal: pass
class Bracing: pass

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'

def Tab(In, color):
    st.title(':green[Ⅰ. 일반 사항 ✍️]')
    st.markdown(In.border2, unsafe_allow_html=True) ########### border ##########

    st.write(h4, '1. 검토 개요 및 주의사항')    
    txt = ':red[ [공사명을 입력하세요 (좌측 사이드바에서 입력)] ]' if In.title == '' else f':blue[ {In.title} ]'
    txt = f'본 검토서는 {txt} 현장에서 의뢰한 시스템 동바리에 대한 구조 안전성 검토를 위한 것임.'
    word_wrap_style(s1, txt, In.font_h5)
    txt = '￭ 시스템 동바리의 하부구조는 :blue[충분한 지지력을 확보한 것으로 가정]하고 구조검토를 실시 하였음.'
    word_wrap_style(s1, txt, In.font_h5)    
    txt = '￭ 본 검토서는 시공사에서 제시한 시공조건 및 도면을 근거로 검토하였음. 따라서, :blue[현장 여건이 변경되는 경우에는 반드시 검토자와 협의 후 시공]하여야 함.'
    word_wrap_style(s1, txt, In.font_h5)
    txt = '￭ 본 공사는 ":blue[2. 적용기준 및 참고문헌]"에 제시된 설계기준 및 시공기준을 따라 시공하여야 하며, 거푸집 및 동바리에 적용되는 각종 안전작업지침 및 설치지침에 따라 시공하여야 함.'
    word_wrap_style(s1, txt, In.font_h5)
    txt = '￭ 모든 재료적 성능은 검토서에 표기된 :blue[동등 이상의 제품을 확인]하고 설치하여야 함.'
    word_wrap_style(s1, txt, In.font_h5)
    txt = '￭ 경사지에 설치되는 구조용 :blue[동바리는 수직을 유지]하게 설치하여야 함.'
    word_wrap_style(s1, txt, In.font_h5)    
    txt = '￭ 슬래브에 설치되는 합판은 주변의 벽체 및 기둥 등에 :blue[견고하게 밀착되도록 설치]하여야 함.'
    word_wrap_style(s1, txt, In.font_h5)
    txt = '￭ 구조용 동바리의 지지부 하부에는 :blue[침하가 발생하지 않도록] 지반을 다지고 버림 콘크리트를 시공하는 등 관련 조치를 하여 침하가 발생되지 않도록 하여야 함. (특히, 지반 하부에 공동, 배수관 등에 대한 확인 및 조치 필요)'
    word_wrap_style(s1, txt, In.font_h5)    
    txt = '￭ 각각의 가설재(합판, 장선, 멍에, 수직재, 수평재, 가새재 등)는 서로 :blue[견고하게 결속하여 미끄러지거나 변형이 발생되지 않도록] 하여야 함.'
    word_wrap_style(s1, txt, In.font_h5)    
    txt = '￭ 가설 구조물 양측에 강성이 큰 구조물이 존재할 경우에는 직접 이에 지지하여 수평변위를 최대한 방지하여야 함. 특히, 콘크리트 부분 타설 등 상부 편심하중에 의한 횡방향 쏠림 현상이 크게 발생할 우려가 있는 시공 조건일 경우 이를 미연에 방지할 수 있도록 경사 버팀대 등으로 충분히 보강하여야 함.'
    word_wrap_style(s1, txt, In.font_h5)    
    txt = '￭ 본 검토에 적용된 시스템 동바리의 규격 및 물성치는 :blue[현장에 적용되는 제품과 반드시 일치되는지 확인]을 거쳐야 하며, 현장에서는 반입제품의 재사용 가설 기자재 성능저하 안전율을 확인하여 :blue[안정성이 검증된 제품을 설치]하도록 하여야 함.'
    word_wrap_style(s1, txt, In.font_h5)
    

    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '2. 사용부재 제원')

    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '1) 거푸집 널')
    with col2: st.write(h5, ':orange[<근거 : 2.2 거푸집 널 (KDS 21 50 00 : 2022)>]')        
    A = In.wood_t*1;  E = 11e3;  fba = 16.8;  fsa = 0.63
    if In.wood_t == 12:
        if In.wood_angle == 0:  I = 90;  S =13;  Ib_Q = 10
        if In.wood_angle ==90:  I = 20;  S = 6;  Ib_Q = 5.1
    if In.wood_t == 15:
        if In.wood_angle == 0:  I =160;  S =18;  Ib_Q = 11.5
        if In.wood_angle ==90:  I = 40;  S = 8;  Ib_Q = 6
    if In.wood_t == 18:
        if In.wood_angle == 0:  I =250;  S =23;  Ib_Q = 14.8
        if In.wood_angle ==90:  I =100;  S =13;  Ib_Q = 8    
    Table.Info('합판', In.wood, A, Ib_Q, I, S, E, fba, fsa, 40)
    [Wood.A, Wood.I, Wood.S, Wood.E, Wood.fba, Wood.fsa, Wood.Ib_Q] = [A, I, S, E, fba, fsa, Ib_Q]

    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '2) 장선')
    with col2: st.write(h5, ':orange[<근거 : 2.3 장선 및 멍에 (KDS 21 50 00 : 2022)>]')    
    E = 210e3;  fba = 181.5;  fsa = 110  ### 장선, 멍에 공통
    
    b = In.joist_b;  h = In.joist_h;  t = In.joist_t;  b1 = (b - 2*t);  h1 = (h - 2*t)
    A = b*h - b1*h1
    I = b*h**3/12 - b1*h1**3/12
    S = I/(In.joist_h/2)
    A1 = b*t;  A2 = 2*t*(h/2 - t);  y1 = (h - t)/2;  y2 = (h/2 - t)/2    # 전단상수, 전단 단면적 계산
    y_bar = (A1*y1 + A2*y2)/(A1 + A2);  Q = A/2*y_bar;  Ib_Q = I*(2*t)/Q
    Table.Info('장선', In.joist, A, Ib_Q, I, S, E, fba, fsa, 40)
    [Joist.A, Joist.I, Joist.S, Joist.E, Joist.fba, Joist.fsa, Joist.Ib_Q] = [A, I, S, E, fba, fsa, Ib_Q]

    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '3) 멍에')
    with col2: st.write(h5, ':orange[<근거 : 2.3 장선 및 멍에 (KDS 21 50 00 : 2022)>]')    
    
    b = In.yoke_b;  h = In.yoke_h;  t = In.yoke_t;  b1 = (b - 2*t);  h1 = (h - 2*t)
    A = b*h - b1*h1
    I = b*h**3/12 - b1*h1**3/12
    S = I/(In.yoke_h/2)    
    A1 = b*t;  A2 = 2*t*(h/2 - t);  y1 = (h - t)/2;  y2 = (h/2 - t)/2    # 전단상수, 전단 단면적 계산
    y_bar = (A1*y1 + A2*y2)/(A1 + A2);  Q = A/2*y_bar;  Ib_Q = I*(2*t)/Q    
    Table.Info('멍에', In.yoke, A, Ib_Q, I, S, E, fba, fsa, 40)
    [Yoke.A, Yoke.I, Yoke.S, Yoke.E, Yoke.fba, Yoke.fsa, Yoke.Ib_Q] = [A, I, S, E, fba, fsa, Ib_Q]

    # 수직재, 수평재, 가새재 (중공 원형)
    st.write(s1, '4) 수직재')
    d = In.vertical_d;  t = In.vertical_t;  d1 = d - 2*t
    A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(In.vertical_d/2);  r = np.sqrt(I/A);  Fy = 355
    Table.Info('수직재', In.vertical, A, -1, I, S, E, r, Fy, 40)
    [Vertical.A, Vertical.I, Vertical.S, Vertical.E, Vertical.r, Vertical.Fy] = [A, I, S, 210e3, r, Fy]

    st.write(s1, '5) 수평재')
    d = In.horizontal_d;  t = In.horizontal_t;  d1 = d - 2*t
    A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(In.horizontal_d/2);  r = np.sqrt(I/A);  Fy = 235
    Table.Info('수평재', In.horizontal, A, -1, I, S, E, r, Fy, 40)
    [Horizontal.A, Horizontal.I, Horizontal.S, Horizontal.E, Horizontal.r, Horizontal.Fy] = [A, I, S, 210e3, r, Fy]

    st.write(s1, '6) 가새재')
    d = In.bracing_d;  t = In.bracing_t;  d1 = d - 2*t
    A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(In.bracing_d/2);  r = np.sqrt(I/A);  Fy = 235
    Table.Info('가새재', In.bracing, A, -1, I, S, E, r, Fy, 40)
    [Bracing.A, Bracing.I, Bracing.S, Bracing.E, Bracing.r, Bracing.Fy] = [A, I, S, 210e3, r, Fy]


    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '3. 설계조건')  # \enspace : 1/2 em space, \quad : 1 em space, \qquad : 2 em space

    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '1) 거푸집 설계')
    with col2: st.write(h5, ':orange[<근거 : 3.1 거푸집 설계 (KDS 21 50 00 : 2022)>]') 
    txt = '￭ 거푸집 설계는 :blue[허용응력설계법]을 적용한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 거푸집은 그 :blue[형상 및 위치가 정확히 유지]되도록 설계한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 규격품이나 성능이 확인된 제품을 제외한 거푸집의 경우는 :blue[공인시험기관의 시험값]을 기초로 한 허용하중값을 적용한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 거푸집은 예상되는 하중조건에 대하여 모든 부속품이 :blue[허용응력을 초과하지 않아야 하며, 변형기준 이하]가 되도록 설계되어야 한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 거푸집은 부과되는 연직하중과 수평하중을 지반 또는 영구 구조체에 :blue[안전하게 전달]할 수 있도록 설계되어야 한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 목재 거푸집 및 수평부재는 등분포 하중이 작용하는 :blue[단순보로 설계]하여야 한다. 다만, 강재나 알루미늄 등과 같은 재료가 사용되는 경우 지점조건에 맞게 설계하여야 한다.'
    word_wrap_style(s2, txt, In.font_h5)

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '2) 동바리 설계')
    with col2: st.write(h5, ':orange[<근거 : 3.2 동바리 설계 (KDS 21 50 00 : 2022)>]') 
    txt = '￭ 동바리 설계는 :blue[허용응력설계법]을 적용한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 동바리는 조립이나 해체가 편리한 구조로서, 그 이음이나 접속부에서 :blue[하중을 확실하게 전달]할 수 있도록 한다.'    
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 동바리 기초는 상부하중에 대한 지반의 :blue[허용지지력 및 허용침하량을 초과하지 않도록 설계]하여야 하며, 동바리의 모든 부속품이 :blue[변형기준과 허용응력을 초과하지 않도록 설계]되어야 한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 동바리의 설계는 시공 중과 완성 후의 :blue[전체 연직방향 변위량에 충분한 안전성을 확보]하여야 한다. 이때, 전체 연직방향 변위량 선정은 기초 침하량과 동바리 자체 변형량을 포함하여야 한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 양중이 필요한 동바리는 :blue[양중에 의한 영향을 고려]하여야 한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 동바리에 설치되는 수평연결재 및 가새재는 예상되는 :blue[모든 수평하중을 안전하게 지지]할 수 있도록 설치하여야 한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 동바리 시공 중 태풍 등과 같은 강풍이 작용하여 동바리가 붕괴될 우려가 있는 경우에는 수평방향 풍하중에 저항할 수 있도록 설계하여야 한다. 특히, 콘크리트 부분 타설 등 상부 편심하중에 의해 횡방향 쏠림현상(sidesway)이 크게 발생할 우려가 있는 시공조건일 경우 이를 미연에 방지할 수 있는 :blue[경사버팀대 등으로 견고하게 보강]하여야 한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 건물의 층고 및 부재의 높이가 높아 단품지지 동바리를 사용할 수 없는 경우에는 :blue[현장 여건에 적합한 동바리로 설계]하여야 한다.'
    word_wrap_style(s2, txt, In.font_h5)
    txt = '￭ 전이보(transfer girder) 등과 같이 콘크리트 타설 두께가 큰 구조물을 지지하는 동바리에 의해 하부의 구조물에 전달되는 하중이 구조계산서에서 제시한 그 부재의 설계하중을 상회하는 경우에는 :blue[하부 지지구조물의 구조 안전성을 검토]하여야 한다. 이 때, 하부 지지구조물이 콘크리트 구조물인 경우 :blue[재령에 따른 콘크리트 압축강도를 고려]하여야 한다.'
    word_wrap_style(s2, txt, In.font_h5)

    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '4. 설계하중 및 하중조합')
    [col1, col2] = st.columns(In.col_span_ref)  # \enspace : 1/2 em space, \quad : 1 em space, \qquad : 2 em space
    with col1: st.write(s1, '1) 연직하중 (고정하중 + 작업하중)')
    with col2: st.write(h5, ':orange[<근거 : 1.6.2 연직하중 (KDS 21 50 00 : 2022)>]')    

    st.write(s2, '① 고정하중')
    st.write(s3, '➣ 보통 콘크리트 자중 : :blue[24kN/m³ 이상] 적용')
    st.write(s3, '➣ 거푸집 자중 : :blue[0.4kN/m² 이상] 적용')

    st.write(s2, '② 작업하중 (작업원, 경량의 장비하중, 충격하중, 기타 콘크리트 타설에 필요한 자재 및 공구 등)')    
    txt = '➣ 콘크리트 타설 높이가 0.5m 미만인 경우 :blue[2.5kN/m²], 0.5m 이상 1m 미만인 경우 :blue[3.5kN/m²], 1m 이상인 경우 :blue[5kN/m² 이상] 적용'
    word_wrap_style(s3, txt, In.font_h5)

    st.write(s2, '③ 최소 연직하중')
    st.write(s3, '➣ 콘크리트 타설 높이와 관계없이 최소 :blue[5kN/m² 이상] 적용')

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '2) 수평하중 [:blue[아래 두값 ①과 ②중 큰 값 적용]]')
    with col2: st.write(h5, ':orange[<근거 : 1.6.5 수평하중 (KDS 21 50 00 : 2022)>]')
    
    st.write(s2, '① 동바리 상단에 고정하중의 :blue[2% 이상]')
    st.write(s2, '② 동바리 상단에 수평방향으로 단위길이당 :blue[1.5kN/m 이상]')
    st.write(s2, '➣ 최소 수평하중은 동바리 설치면에 대하여 X방향 및 Y방향에 대하여 각각 적용한다.')

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '3) 픙하중')
    with col2: st.write(h5, ':orange[<근거 : 1.6.4 풍하중 (KDS 21 50 00 : 2022)>]')
    st.write(s2, rf'➣ 기준 높이 $\small H$에서의 속도압($\small q_H$)은 다음과 같이 산정한다.')    
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s2, rf'➣ $\bm{{q_{{H}} \; = \; \Large{{\frac{{1}}{2}}} \small \, \rho \, V^2_H}}$ (N/m$^2$)')
    with col2: st.write(h5, ':orange[<근거 : 5.5 속도압 (KDS 41 12 00 : 2022)>]')
    st.write(s3, rf'￭ $\rho$ : 공기밀도로써 균일하게 1.225 kg/m$^3$으로 한다.')
    st.write(s3, rf'￭ $\small V_H$ : 설계풍속 (m/s) (5.5.1에 따른다)')

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    st.write(s2, rf'➣ $\bm{{\small{{V_{{H}} \; = \; V_0 \, K_D \, K_{{zr}} \, K_{{zt}} \, I_w(T)}} }}$ (m/s)')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s3, rf'￭ $\small V_0$ : 기본풍속 (m/s) (5.5.2에 따른다)')
    with col2: st.write(h5, ':green[[36m/s로 계산 : 제주도 제외 28 ~ 40m/s로 분포]]')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s3, rf'￭ $\small K_D$ : 풍향계수 (5.5.3에 따른다)')
    with col2: st.write(h5, ':green[[1.0으로 계산 : 최솟값 0.85]]')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s3, rf'￭ $\small K_{{zr}}$ : 풍속고도 분포계수 (5.5.4에 따른다)')
    with col2: st.write(h5, ':green[[1.0으로 계산 : 평탄한 지역에 0.58(A), 0.81(B), 1.0(C), 1.13(D) 적용]]')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s3, rf'￭ $\small K_{{zt}}$ : 지형계수 (5.5.5에 따른다)')
    with col2: st.write(h5, ':green[[1.0으로 계산 : 평탄한 지역에 대한 지형계수는 1.0이다]]')
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s3, rf'￭ $\small I_w (T)$ : 건축구조물의 중요도계수')
    with col2: st.write(h5, ':green[[0.6으로 계산 : 아래 계산의 0.60 적용]]')
    
    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s2, rf'➣ 가시설물의 재현기간에 따른 중요도계수 $\small I_w(T_w)$')
    with col2: st.write(h5, ':orange[<근거 : 1.6.4 풍하중 (KDS 21 50 00 : 2022)>]')    
    st.write(s3, rf'￭ 재현기간($\small I_w(T_w)$)이 1년 이하의 경우에는 0.60을 적용하고, 이 외 기간에 대해서는 다음 식에 의해 산정할 수 있다.')
    st.write(s3, rf'￭ $\small I_w = 0.56 + 0.1 ln(T_w)$')
    st.write(s3, rf'￭ $\bm{{\small T_{{w}} \; = \; \Large{{\frac{{1}}{{1 \,-\, (P)^\frac{{1}}{{N}}}} }} }} \; : \; $재현기간(년)')
    st.write(s3, rf'￭ $\small T_w$ : 재현기간(년), $\quad \small N$ : 가시실물의 존치기간(년), $\quad \small P$ : 비초과 확률(60%)')

    st.write(In.space, unsafe_allow_html=True)  ## 빈줄 공간
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '4) 하중조합')
    with col2: st.write(h5, ':orange[<근거 : 3.3.1 거푸집 및 동바리, 비계 및 안전시설물 (KDS 21 10 00 : 2022)>]')

    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '2. 적용기준 및 참고문헌')
    st.write(s1, '￭ 가시설물 설계 일반사항 (KDS 21 10 00 : 2022, 국토교통부)')
    st.write(s1, '￭ 거푸집 및 동바리 설계기준 (KDS 21 50 00 : 2022, 국토교통부)')
    st.write(s1, '￭ 강구조 설계 일반사항(허용응력설계법) (KDS 14 30 05 : 2019, 국토교통부)')
    st.write(s1, '￭ 강구조 부재 설계기준(허용응력설계법) (KDS 14 30 10 : 2019, 국토교통부)')
    st.write(s1, '￭ 건축물 설계하중 (KDS 41 12 00 : 2022, 국토교통부)')
    st.write(s1, '￭ 비계 및 안전시설물 설계기준 (KDS 21 60 00 : 2022, 국토교통부)')
    st.write('')

    st.write(s1, '￭ 거푸집 및 동바리 (KCS 14 20 12 : 2022, 국토교통부)')
    st.write(s1, '￭ 가설공사 일반사항 (KCS 21 10 00 : 2022, 국토교통부)')
    st.write(s1, '￭ 거푸집 및 동바리공사 일반사항 (KCS 21 50 05 : 2023, 국토교통부)')
    st.write(s1, '￭ 초고층 고주탑 공사용 거푸집 및 동바리 (KCS 21 50 10 : 2022, 국토교통부)')
    st.write(s1, '￭ 노출 콘크리트용 거푸집 및 동바리 (KCS 21 50 15 : 2022, 국토교통부)')
    st.write(s1, '￭ 기타 콘크리트용 거푸집 및 동바리 (KCS 21 50 20 : 2022, 국토교통부)')
    st.write(s1, '￭ 비계공사 일반사항 (KCS 21 60 05 : 2022, 국토교통부)')
    st.write(s1, '￭ 비계 (KCS 21 60 10 : 2022, 국토교통부)')
    st.write('')

    st.write(s1, '￭ 시스템 동바리 안전작업 지침 (2020, 한국산업안전보건공단)')
    st.write(s1, '￭ 파이프 서포트 동바리 안전작업 지침 (2020, 한국산업안전보건공단)')
    st.write(s1, '￭ 거푸집 동바리 구조검토 및 설치 안전보건작업 지침 (2015, 한국산업안전보건공단)')

    return Wood, Joist, Yoke, Vertical, Horizontal, Bracing
