import streamlit as st
import numpy as np
from Sidebar import word_wrap_style
import Table

class Wood: pass
class Joist: pass
class Waling: pass
class Yoke: pass
class Vertical: pass
class Horizontal: pass
class Bracing: pass

h2 = '## ';  h3 = '### ';  h4 = '#### ';  h5 = '##### ';  h6 = '###### '
s1 = h5 + '$\quad$';  s2 = h5 + '$\qquad$';  s3 = h5 + '$\quad \qquad$'

def Info(In):
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.title(':green[Ⅰ. 일반 사항 ✍️]')  #!!!!!!!!!!!!!!!!!!!!!!
    st.markdown(In.border2, unsafe_allow_html=True) ########### border ##########

    st.write(h4, '1. 검토 개요 및 주의사항')
    tt = '비계' if '비계' in In.type else '동바리'
    txt_Common = [f'본 검토 보고서는 시스템 {tt}에 대한 구조 안전성 검토를 위한 것임.',
        f'시스템 {tt}의 하부구조는 :blue[충분한 지지력을 확보한 것으로 가정]하고 구조검토를 실시 하였음.',
        '① 시공사에서 제시한 시공조건 및 도면을 근거로 검토하였음. 따라서, :blue[현장 여건이 변경되는 경우에는 반드시 검토자와 협의 후 시공]한다.',
        '② 본 공사는 ":blue[5. 적용기준 및 참고문헌]"에 제시된 설계기준 및 시공기준을 따라 시공하며, 가시설물에 적용되는 각종 안전작업지침 및 설치지침에 따라 시공한다.',
        '③ 모든 재료적 성능은 검토서에 표기된 :blue[동등 이상의 제품을 확인]하고 설치한다.',]
    
    for i in ['A', 'B', 'C', 'D']:        
        if i in In.Kzr_txt: Kzr_txt = i

    if '비계' in In.type:
        txt_S = [
            '④ 구조물 전체 외부에 설치되는 비계 구조물 중에서 :blue[높이와 간격이 가장 불리한 일부 구간에 대하여 안정성 검토]를 수행함.',
            f'⑤ 풍하중 기본풍속 {In.V0:.0f}m/s, 지표면조도구분 {Kzr_txt}를 기준으로 검토하며, 산업안전보건기준에 관한 규칙 제383조에 의해 :blue[풍속 10m/s 이상일 경우 작업을 금지]한다.',
            f'⑥ 비계 외부 난간 설치구간의 보호망은 충실률 {In.phi:.1f}으로 검토함.',
            '⑦ :blue[벽 연결용 철물은 영구 구조물에 고정]되는 조건으로 검토함.',
            '⑧ 벽 연결용 철물은 수직재와 수평재의 교차부에서 비계면에 대하여 직각이 되도록 하여 수직재에 설치하고, 비계의 최상단과 가장자리 끝에도 벽 이음재를 설치한다.',
            '⑨ :blue[받침철물의 압축하중은 40kN 이상]으로 설치한다.',
            '⑩ 비계 기둥에는 미끄러지거나 침하하는 것을 방지하기 위하여 밑받침 철물을 사용하거나 깔판, 깔목 등을 사용하고, 밑둥잡이 등의 조치를 한다.',
            '⑪ 설치되는 바닥은 시방기준에 적합하도록 하여 기초에 안전하게 전달할 수 있는 조건으로 검토함.',
            '⑫ 적재는 집중적재를 하지 않고 분산하여 적재하고, 작업하중과 적재하중을 포함하여 허용이내로 적재한다.' ]
    else:    # 동바리
        txt_S = [
            '④ 경사지에 설치되는 구조용 :blue[동바리는 수직을 유지]하게 설치한다.',
            '⑤ 슬래브에 설치되는 합판은 주변의 벽체 및 기둥 등에 :blue[견고하게 밀착되도록 설치]한다.',
            '⑥ 구조용 동바리의 지지부 하부에는 :blue[침하가 발생하지 않도록] 지반을 다지고 버림 콘크리트를 시공하는 등 관련 조치를 하여 침하가 발생되지 않도록 한다. (특히, 지반 하부에 공동, 배수관 등에 대한 확인 및 조치 필요)',
            '⑦ 각각의 가설재(합판, 장선, 멍에, 수직재, 수평재, 가새재 등)는 서로 :blue[견고하게 결속하여 미끄러지거나 변형이 발생되지 않도록] 한다.',
            '⑧ 가설 구조물 양측에 강성이 큰 구조물이 존재할 경우에는 직접 이에 지지하여 수평변위를 최대한 방지하며, 특히 콘크리트 부분 타설 등 상부 편심하중에 의한 횡방향 쏠림 현상이 크게 발생할 우려가 있는 시공 조건일 경우 이를 미연에 방지할 수 있도록 경사 버팀대 등으로 충분히 보강한다.',
            '⑨ 본 검토에 적용된 시스템 동바리의 규격 및 물성치는 :blue[현장에 적용되는 제품과 반드시 일치되는지 확인]을 거쳐야 하며, 현장에서는 반입제품의 재사용 가설 기자재 성능저하 안전율을 확인하여 :blue[안정성이 검증된 제품을 설치]하도록 한다.' ]
        
    for txt_list in [txt_Common, txt_S]:
        for txt in txt_list:
            word_wrap_style(s1, txt, In.font_h5)

    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########    
    st.write(h4, '2. 사용부재 제원');  E = 210e3  #!!!!!!!!!!!!!!!!!!!!!!
    
    if '비계' in In.type:
        # 장선, 띠장, 수직재, 수평재, 가새재 (중공 원형)        
        st.write(s1, '1) 장선')
        d = In.joist_d;  t = In.joist_t;  d1 = d - 2*t;  Fy = In.joist_Fy
        A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(d/2);  r = np.sqrt(I/A);  Ib_Q = np.pi*d/2*t
        fba = 0.66*In.joist_Fy;  fsa = 0.40*In.joist_Fy
        Table.Info('장선', In.joist, A, Ib_Q, I, S, E, fba, fsa, 40)
        [Joist.A, Joist.Ib_Q, Joist.I, Joist.S, Joist.E, Joist.fba, Joist.fsa] = [A, Ib_Q, I, S, E, fba, fsa]

        st.write(s1, '2) 띠장')
        d = In.waling_d;  t = In.waling_t;  d1 = d - 2*t;  Fy = In.waling_Fy
        A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(d/2);  r = np.sqrt(I/A);  Ib_Q = np.pi*d/2*t
        fba = 0.66*In.waling_Fy;  fsa = 0.40*In.waling_Fy
        Table.Info('띠장', In.waling, A, Ib_Q, I, S, E, fba, fsa, 40)
        [Waling.A, Waling.Ib_Q, Waling.I, Waling.S, Waling.E, Waling.fba, Waling.fsa] = [A, Ib_Q, I, S, E, fba, fsa]

        st.write(s1, '3) 수직재')
        d = In.vertical_d;  t = In.vertical_t;  d1 = d - 2*t;  Fy = In.vertical_Fy
        A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(d/2);  r = np.sqrt(I/A);  Ib_Q = np.pi*d/2*t
        Table.Info('수직재', In.vertical, A, Ib_Q, I, S, E, r, Fy, 40)
        [Vertical.A, Vertical.Ib_Q, Vertical.I, Vertical.S, Vertical.E, Vertical.r, Vertical.Fy] = [A, Ib_Q, I, S, E, r, Fy]

        st.write(s1, '4) 수평재')
        d = In.horizontal_d;  t = In.horizontal_t;  d1 = d - 2*t;  Fy = In.horizontal_Fy
        A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(d/2);  r = np.sqrt(I/A);  Ib_Q = np.pi*d/2*t
        Table.Info('수평재', In.horizontal, A, Ib_Q, I, S, E, r, Fy, 40)    
        [Horizontal.A, Horizontal.Ib_Q, Horizontal.I, Horizontal.S, Horizontal.E, Horizontal.r, Horizontal.Fy] = [A, Ib_Q, I, S, E, r, Fy]

        st.write(s1, '5) 가새재')
        d = In.bracing_d;  t = In.bracing_t;  d1 = d - 2*t;  Fy = In.bracing_Fy
        A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(d/2);  r = np.sqrt(I/A);  Ib_Q = np.pi*d/2*t
        Table.Info('가새재', In.bracing, A, Ib_Q, I, S, E, r, Fy, 40)
        [Bracing.A, Bracing.Ib_Q, Bracing.I, Bracing.S, Bracing.E, Bracing.r, Bracing.Fy] = [A, Ib_Q, I, S, E, r, Fy]

    else:    # 동바리
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '1) 거푸집 널')
        with col2: st.write(h5, ':orange[<근거 : 2.2 거푸집 널 (KDS 21 50 00 : 2022)>]')        
        A = In.wood_t*1;  fba = 16.8;  fsa = 0.63
        if In.wood_t == 12:
            if In.wood_angle == 0:  I = 90;  S =13;  Ib_Q = 10
            if In.wood_angle ==90:  I = 20;  S = 6;  Ib_Q = 5.1
        if In.wood_t == 15:
            if In.wood_angle == 0:  I =160;  S =18;  Ib_Q = 11.5
            if In.wood_angle ==90:  I = 40;  S = 8;  Ib_Q = 6
        if In.wood_t == 18:
            if In.wood_angle == 0:  I =250;  S =23;  Ib_Q = 14.8
            if In.wood_angle ==90:  I =100;  S =13;  Ib_Q = 8    
        Table.Info('합판', In.wood, A, Ib_Q, I, S, 11e3, fba, fsa, 40)
        [Wood.A, Wood.Ib_Q, Wood.I, Wood.S, Wood.E, Wood.fba, Wood.fsa] = [A, Ib_Q, I, S, 11e3, fba, fsa]
        
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '2) 장선')
        with col2: st.write(h5, ':orange[<근거 : 2.3 장선 및 멍에 (KDS 21 50 00 : 2022)>]')
        
        # 장선, 멍에 공통 (중공 직사각형)
        def JoistYoke(b, h, t, b1, h1):
            A = b*h - b1*h1;  I = b*h**3/12 - b1*h1**3/12;  S = I/(h/2)
            A1 = b*t;  A2 = 2*t*(h/2 - t);  y1 = (h - t)/2;  y2 = (h/2 - t)/2     # 전단상수, 전단 단면적 계산
            y_bar = (A1*y1 + A2*y2)/(A1 + A2);  Q = A/2*y_bar;  Ib_Q = I*(2*t)/Q  # <== 정확한 계산, 간략 계산 ==> Ib_Q = 2*In.joist_b*In.joist_t
            return A, Ib_Q, I, S

        b = In.joist_b;  h = In.joist_h;  t = In.joist_t;  b1 = (b - 2*t);  h1 = (h - 2*t)        
        [A, Ib_Q, I, S] = JoistYoke(b, h, t, b1, h1)
        fba = 0.66*In.joist_Fy;  fsa = 0.40*In.joist_Fy
        Table.Info('장선', In.joist, A, Ib_Q, I, S, E, fba, fsa, 40)
        [Joist.A, Joist.Ib_Q, Joist.I, Joist.S, Joist.E, Joist.fba, Joist.fsa] = [A, Ib_Q, I, S, E, fba, fsa]
            
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '3) 멍에')
        with col2: st.write(h5, ':orange[<근거 : 2.3 장선 및 멍에 (KDS 21 50 00 : 2022)>]')    
        
        b = In.yoke_b;  h = In.yoke_h;  t = In.yoke_t;  b1 = (b - 2*t);  h1 = (h - 2*t)
        [A, Ib_Q, I, S] = JoistYoke(b, h, t, b1, h1)
        fba = 0.66*In.yoke_Fy;  fsa = 0.40*In.yoke_Fy
        Table.Info('멍에', In.yoke, A, Ib_Q, I, S, E, fba, fsa, 40)
        [Yoke.A, Yoke.Ib_Q, Yoke.I, Yoke.S, Yoke.E, Yoke.fba, Yoke.fsa] = [A, Ib_Q, I, S, E, fba, fsa]

        # 수직재, 수평재, 가새재 (중공 원형)
        st.write(s1, '4) 수직재')
        d = In.vertical_d;  t = In.vertical_t;  d1 = d - 2*t;  Fy = In.vertical_Fy
        A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(d/2);  r = np.sqrt(I/A);  Ib_Q = np.pi*d/2*t
        Table.Info('수직재', In.vertical, A, Ib_Q, I, S, E, r, Fy, 40)
        [Vertical.A, Vertical.Ib_Q, Vertical.I, Vertical.S, Vertical.E, Vertical.r, Vertical.Fy] = [A, Ib_Q, I, S, E, r, Fy]

        st.write(s1, '5) 수평재')
        d = In.horizontal_d;  t = In.horizontal_t;  d1 = d - 2*t;  Fy = In.horizontal_Fy
        A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(d/2);  r = np.sqrt(I/A);  Ib_Q = np.pi*d/2*t
        Table.Info('수평재', In.horizontal, A, Ib_Q, I, S, E, r, Fy, 40)    
        [Horizontal.A, Horizontal.Ib_Q, Horizontal.I, Horizontal.S, Horizontal.E, Horizontal.r, Horizontal.Fy] = [A, Ib_Q, I, S, E, r, Fy]

        st.write(s1, '6) 가새재')
        d = In.bracing_d;  t = In.bracing_t;  d1 = d - 2*t;  Fy = In.bracing_Fy
        A = np.pi*(d**2 - d1**2)/4;  I = np.pi*(d**4 - d1**4)/64;  S = I/(d/2);  r = np.sqrt(I/A);  Ib_Q = np.pi*d/2*t
        Table.Info('가새재', In.bracing, A, Ib_Q, I, S, E, r, Fy, 40)
        [Bracing.A, Bracing.Ib_Q, Bracing.I, Bracing.S, Bracing.E, Bracing.r, Bracing.Fy] = [A, Ib_Q, I, S, E, r, Fy]


    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '3. 설계 일반사항')  #!!!!!!!!!!!!!!!!!!!!!!

    if '비계' in In.type:
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '1) 일반사항')
        with col2: st.write(h5, ':orange[<근거 : 3.1 일반사항 (KDS 21 60 00 : 2022)>]')
        txts = [
            '￭ 비계 및 안전시설물의 설계는 KDS 14 30 00 (:blue[허용응력설계법])에 따른다.',
            '￭ 비계 및 안전시설물에 사용되는 부속품의 안전율(극한하중에 대한 허용하중의 비를 말하며, 극한하중은 인장 및 압축성능을 의미함)은 :blue[인장 2, 휨 2, 전단 3, 압축 3]을 적용한다.',
            '￭ 비계에 사용되는 :blue[와이어 로프 및 강선의 안전율은 10 이상]이어야 한다.',
            '￭ 비계 및 안전시설물의 설계는 시공 등을 고려하여 적정한 형식과 재료를 선택하고, 작용되는 :blue[하중을 안전하게 기초에 전달]하도록 하여야 한다.',
            '￭ 비계에 간이 크레인, 콘크리트 타설장비 등을 설치하는 경우는 :blue[운반하중으로 인한 전도 모멘트에 대하여 안전]하도록 하여야 한다.',
            '￭ 비계가 설치되는 :blue[하부 기초설계는 KDS 21 50 00(3.3)]에 따른다.' ]
        for txt in txts:
            word_wrap_style(s2, txt, In.font_h5)

    else:    # 동바리
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '1) 거푸집 설계')
        with col2: st.write(h5, ':orange[<근거 : 3.1 거푸집 설계 (KDS 21 50 00 : 2022)>]')
        txts = [
            '￭ 거푸집 설계는 :blue[허용응력설계법]을 적용한다.',
            '￭ 거푸집은 그 :blue[형상 및 위치가 정확히 유지]되도록 설계한다.',
            '￭ 규격품이나 성능이 확인된 제품을 제외한 거푸집의 경우는 :blue[공인시험기관의 시험값]을 기준으로 한 허용하중값을 적용한다.',
            '￭ 거푸집은 예상되는 하중조건에 대하여 모든 부속품이 :blue[허용응력을 초과하지 않아야 하며, 변형기준 이하]가 되도록 설계한다.',
            '￭ 거푸집은 부과되는 연직하중과 수평하중을 지반 또는 영구 구조체에 :blue[안전하게 전달]할 수 있도록 설계한다.',
            '￭ 목재 거푸집, 장선 및 멍에는 등분포 하중이 작용하는 :blue[단순보로 검토]한다. 다만, 강재나 알루미늄 등과 같은 재료가 사용되는 경우 지점조건에 맞게 설계한다.' ]
        for txt in txts:
            word_wrap_style(s2, txt, In.font_h5)
        
        st.write('')  ## 빈줄 공간
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '2) 동바리 설계')
        with col2: st.write(h5, ':orange[<근거 : 3.2 동바리 설계 (KDS 21 50 00 : 2022)>]') 
        txts = [
            '￭ 동바리 설계는 :blue[허용응력설계법]을 적용한다.',
            '￭ 동바리는 조립이나 해체가 편리한 구조로서, 그 이음이나 접속부에서 :blue[하중을 확실하게 전달]할 수 있도록 한다.',
            '￭ 동바리 기초는 상부하중에 대한 지반의 :blue[허용지지력 및 허용침하량을 초과하지 않도록 설계] 하며, 동바리의 모든 부품 및 부속품이 :blue[변형기준과 허용응력을 초과하지 않도록 설계]한다.',
            '￭ 동바리의 설계는 시공 중과 완성 후의 :blue[전체 연직방향 변위량에 충분한 안전성을 확보] 하며, 이때 전체 연직방향 변위량은 기초 침하량과 동바리 자체 변형량을 포함한다.',
            '￭ 양중이 필요한 동바리는 :blue[양중에 의한 영향을 고려]한다.',
            '￭ 동바리에 설치되는 수평재 및 가새재는 예상되는 :blue[모든 수평하중을 안전하게 지지]할 수 있도록 설치한다.',
            '￭ 동바리 시공 중 태풍 등과 같은 강풍이 작용하여 동바리가 붕괴될 우려가 있는 경우에는 수평방향 풍하중에 저항할 수 있도록 설계하며, 특히 콘크리트 부분 타설 등 상부 편심하중에 의해 횡방향 쏠림현상(sidesway)이 크게 발생할 우려가 있는 시공조건일 경우 이를 미연에 방지할 수 있는 :blue[경사버팀대 등으로 견고하게 보강]한다.',
            '￭ 건물의 층고 및 부재의 높이가 높아 단품지지 동바리를 사용할 수 없는 경우에는 :blue[현장 여건에 적합한 동바리로 설계]한다.'
            '￭ 콘크리트 타설 두께가 큰 구조물을 지지하는 동바리에 의해 하부의 지지 구조물에 전달되는 하중이 구조계산서에서 제시한 설계하중을 상회하는 경우에는 :blue[하부 지지구조물의 구조 안전성을 검토]한다. 이 때, 하부 지지구조물이 콘크리트 구조물인 경우 :blue[재령에 따른 콘크리트 압축강도를 고려]한다.'  ]
        for txt in txts:
            word_wrap_style(s2, txt, In.font_h5)

    if '비계' not in In.type:
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '4. 설계하중 및 하중조합')  #!!!!!!!!!!!!!!!!!!!!!!
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '1) 연직하중 (고정하중 + 작업하중)')
    if '비계' in In.type:
        with col2: st.write(h5, ':orange[<근거 : 1.6.2 연직하중 (KDS 21 60 00 : 2022)>]')    

        st.write(s2, '① 고정하중 (D)')
        st.write(s3, '➣ 수직재, 수평재, 가새재, 안전난간 등의 자중')
        st.write(s3, '➣ 작업발판의 고정하중 : :blue[0.2kN/m² 이상] 적용')

        st.write(s2, '② 작업하중 (L$_i$) (근로자와 근로자가 사용하는 자재, 공구 등을 포함)')
        st.write(s3, '➣ 통로의 역할을 하는 비계와 가벼운 공구만을 필요로 하는 :blue[경작업] : :blue[1.25kN/m² 이상]')
        st.write(s3, '➣ 공사용 자재의 적재를 필요로 하는 :blue[중작업] : :blue[2.5kN/m² 이상]')
        st.write(s3, '➣ :blue[돌 붙임 공사] 등과 같이 자재가 무거운 작업 : :blue[3.5kN/m² 이상]')

        st.write('')  ## 빈줄 공간
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '2) 수평하중')
        with col2: st.write(h5, ':orange[<근거 : 1.6.3 수평하중 (KDS 21 60 00 : 2022)>]')

        st.write(s2, '① 풍하중에 대한 영향과 연직하중의 :blue[5%] 적용')
        st.write(s3, '➣ 단, 수평하중과 풍하중의 동시 작용은 고려하지 않는다.')
        st.write(s2, '② 이동식 비계의 :blue[전도에 대한 안전성 검토]를 위해 최상단 작업발판에 :blue[0.3kN의 수평하중]을 적용한다.')
        st.write(s2, '③ 수평하중은 비계 설치면에 대하여 X방향 및 Y방향에 대하여 각각 적용한다.')

    else:    # 동바리
        with col2: st.write(h5, ':orange[<근거 : 1.6.2 연직하중 (KDS 21 50 00 : 2022)>]')

        st.write(s2, '① 고정하중 (D)')
        st.write(s3, '➣ 보통 콘크리트 자중 : :blue[24kN/m³ 이상] 적용')
        st.write(s3, '➣ 거푸집 자중 : :blue[0.4kN/m² 이상] 적용')

        st.write(s2, '② 작업하중 (작업원, 경량의 장비하중, 충격하중, 기타 콘크리트 타설에 필요한 자재 및 공구 등)')    
        txt = '➣ 콘크리트 타설 높이가 0.5m 미만인 경우 :blue[2.5kN/m²], 0.5m 이상 1m 미만인 경우 :blue[3.5kN/m²], 1m 이상인 경우 :blue[5kN/m² 이상] 적용'
        word_wrap_style(s3, txt, In.font_h5)

        st.write(s2, '③ 최소 연직하중')
        st.write(s3, '➣ 콘크리트 타설 높이와 관계없이 최소 :blue[5kN/m² 이상] 적용')

        st.write('')  ## 빈줄 공간
        [col1, col2] = st.columns(In.col_span_ref)
        with col1: st.write(s1, '2) 수평하중 [:blue[아래 두값 ①과 ②중 큰 값 적용]]')
        with col2: st.write(h5, ':orange[<근거 : 1.6.5 수평하중 (KDS 21 50 00 : 2022)>]')
        
        st.write(s2, '① 동바리 상단에 고정하중의 :blue[2% 이상]')
        st.write(s2, '② 동바리 상단에 수평방향으로 단위길이당 :blue[1.5kN/m 이상]')
        st.write(s3, '➣ 최소 수평하중은 동바리 설치면에 대하여 X방향 및 Y방향에 대하여 각각 적용한다.')

    st.write('')  ## 빈줄 공간
    [col1, col2] = st.columns(In.col_span_ref)
    with col1: st.write(s1, '3) 풍하중')
    n = 60 if '비계' in In.type else 50
    with col2: st.write(h5, f':orange[<근거 : 1.6.4 풍하중 (KDS 21 {n} 00 : 2022)>]')
    st.write(s2, '① 이 기준에서 규정한 사항 이외의 경우에는 KDS 41 12 00에 따른다.')
    st.write(s2, '② 가시설물의 재현기간에 따른 중요도계수($\small I_{w}$)는 KDS 21 50 00(1.6.4(2))에 따른다.')    
    if '비계' in In.type:
        st.write(s2, '③ 안전시설물의 풍력계수($\small C_{f}$)는 충실률에 따라 KDS 21 60 00(1.6.4(3))와 같이 산정한다.')

    if '비계' in In.type:
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.write('')  ## 빈줄 공간
    [col1, col2] = st.columns([1,2])
    with col1: st.write(s1, '4) 하중조합')
    with col2: st.write(h5, ':orange[<근거 : 3.3.1 거푸집 및 동바리, 비계 및 안전시설물 (KDS 21 10 00 : 2022)>]')
    st.write(s2, '➣ 거푸집 및 동바리, 비계 및 안전시설물 설계 시 하중조합 및 허용응력증가계수는 다음과 같이 적용한다.')
    Table.Load_Case()

    if '비계' not in In.type:
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################    
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '5. 적용기준 및 참고문헌')  #!!!!!!!!!!!!!!!!!!!!!!
    st.write(s1, '￭ 가시설물 설계 일반사항 (KDS 21 10 00 : 2022, 국토교통부)')    
    if '비계' not in In.type:  st.write(s1, '￭ 거푸집 및 동바리 설계기준 (KDS 21 50 00 : 2022, 국토교통부)')
    if '비계' in In.type:      st.write(s1, '￭ 비계 및 안전시설물 설계기준 (KDS 21 60 00 : 2022, 국토교통부)')
    st.write(s1, '￭ 강구조 설계 일반사항(허용응력설계법) (KDS 14 30 05 : 2019, 국토교통부)')
    st.write(s1, '￭ 강구조 부재 설계기준(허용응력설계법) (KDS 14 30 10 : 2019, 국토교통부)')
    st.write(s1, '￭ 건축물 설계하중 (KDS 41 12 00 : 2022, 국토교통부)')    

    st.write('')
    st.write(s1, '￭ 가설공사 일반사항 (KCS 21 10 00 : 2022, 국토교통부)')
    if '비계' in In.type:
        st.write(s1, '￭ 비계공사 일반사항 (KCS 21 60 05 : 2022, 국토교통부)')
        st.write(s1, '￭ 비계 (KCS 21 60 10 : 2022, 국토교통 부)')
    else:
        st.write(s1, '￭ 거푸집 및 동바리 (KCS 14 20 12 : 2022, 국토교통부)')    
        st.write(s1, '￭ 거푸집 및 동바리공사 일반사항 (KCS 21 50 05 : 2023, 국토교통부)')
        st.write(s1, '￭ 초고층 고주탑 공사용 거푸집 및 동바리 (KCS 21 50 10 : 2022, 국토교통부)')
        st.write(s1, '￭ 노출 콘크리트용 거푸집 및 동바리 (KCS 21 50 15 : 2022, 국토교통부)')
        st.write(s1, '￭ 기타 콘크리트용 거푸집 및 동바리 (KCS 21 50 20 : 2022, 국토교통부)')


    st.write('')
    st.write(s1, '￭ 시스템 동바리 안전작업 지침 (2020, 한국산업안전보건공단)')
    st.write(s1, '￭ 파이프 서포트 동바리 안전작업 지침 (2020, 한국산업안전보건공단)')
    st.write(s1, '￭ 거푸집 동바리 구조검토 및 설치 안전보건작업 지침 (2015, 한국산업안전보건공단)')
    st.write(s1, '￭ 산업안전보건기준에 관한 규칙 (2024, 고용노동부)')

    return Wood, Joist, Waling, Yoke, Vertical, Horizontal, Bracing
