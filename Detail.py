import streamlit as st
import numpy as np
import Table, os, json

def Result(In, Vertical, Horizontal, Bracing):
    h4 = In.h4;  h5 = In.h5
    s1 = In.s1;  s2 = In.s2

    # Input file
    if '비계' in In.type:
        inputs = {
            'type':In.type,
            'Lj':round(In.Lj, 1), 'Lw':round(In.Lw, 1), 'bracing_N':In.bracing_N,
            'Lbottom':round(In.Lbottom, 1), 'Lh':round(In.Lh, 1),
            'nX':In.nX, 'nY':In.nY, 'nZ':In.nZ, 
            'vertical_d':round(In.vertical_d, 1), 'vertical_t':round(In.vertical_t, 1),
            'horizontal_d':round(In.horizontal_d, 1), 'horizontal_t':round(In.horizontal_t, 1),
            'bracing_d':round(In.bracing_d, 1), 'bracing_t':round(In.bracing_t, 1), 
            'dead_load':round(In.working_weight1/1e3, 4), 'design_load':round(In.design_load, 4),   # N/mm2
            'Hx':round(In.Hx, 4), 'Hy':round(In.Hy, 4), 'wind2':round(In.wind2, 4),  # Hx, Hy : kN, wind2 : kN/m2
            'fastener_Ly':In.fastener_Ly, 'fastener_Lz':In.fastener_Lz, 'fastener_Lz1':In.fastener_Lz1, }
    else:
        inputs = {
            'type':In.type,
            'Ly':round(In.Ly, 1), 'Lv':round(In.Lv, 1), 'Lh':round(In.Lh, 1),
            'X':round(In.X, 2), 'Y':round(In.Y, 2), 'Z':round(In.Z, 2),
            'vertical_d':round(In.vertical_d, 1), 'vertical_t':round(In.vertical_t, 1),
            'horizontal_d':round(In.horizontal_d, 1), 'horizontal_t':round(In.horizontal_t, 1),
            'bracing_d':round(In.bracing_d, 1), 'bracing_t':round(In.bracing_t, 1),            
            'dead_load':round(In.dead_load, 4), 'design_load':round(In.design_load, 4),   # N/mm2
            'Hx2':round(In.Hx2, 4), 'Hy2':round(In.Hy2, 4), 'wind2':round(In.wind2, 4) }  # kN/m2
        
    with open('Input.json', 'w', encoding='utf-8') as f:   # 한글 쓸때 (encoding-'utf-8', ensure_ascii=False)
        json.dump(inputs, f, indent = 4, ensure_ascii=False)
    # Input file
    
    # Output file
    with open('Result.json', 'r') as f:
        result = json.load(f)
    with open('Vertical.json', 'r') as f:
        vertical = json.load(f)
    with open('Horizontal.json', 'r') as f:
        horizontal = json.load(f)
    with open('Bracing.json', 'r') as f:
        bracing = json.load(f)

    uz = [];  seqv = [];  Fx1 = [];  Fx2 = []
    My1 = [];  My2 = [];  Mz1 = [];  Mz2 = []
    SFz1 = [];  SFz2 = [];  SFy1 = [];  SFy2 = []
    for item in result:
        uz.append(np.abs(item['uz']));  seqv.append(np.abs(item['seqv']))
        Fx1.append(item['Fx1']/1e3);    Fx2.append(item['Fx2']/1e3)
        My1.append(item['My1']/1e6);    My2.append(item['My2']/1e6)
        Mz1.append(item['Mz1']/1e6);    Mz2.append(item['Mz2']/1e6)
        SFz1.append(item['SFz1']/1e3);  SFz2.append(item['SFz2']/1e3)
        SFy1.append(item['SFy1']/1e3);  SFy2.append(item['SFy2']/1e3)
    for item in vertical:
        Fx1.append(item['Fx1']/1e3);    Fx2.append(item['Fx2']/1e3)
        My1.append(item['My1']/1e6);    My2.append(item['My2']/1e6)
        Mz1.append(item['Mz1']/1e6);    Mz2.append(item['Mz2']/1e6)
        SFz1.append(item['SFz1']/1e3);  SFz2.append(item['SFz2']/1e3)
        SFy1.append(item['SFy1']/1e3);  SFy2.append(item['SFy2']/1e3)
    for item in horizontal:
        Fx1.append(item['Fx1']/1e3);    Fx2.append(item['Fx2']/1e3)
        My1.append(item['My1']/1e6);    My2.append(item['My2']/1e6)
        Mz1.append(item['Mz1']/1e6);    Mz2.append(item['Mz2']/1e6)
        SFz1.append(item['SFz1']/1e3);  SFz2.append(item['SFz2']/1e3)
        SFy1.append(item['SFy1']/1e3);  SFy2.append(item['SFy2']/1e3)
    for item in bracing:
        Fx1.append(item['Fx1']/1e3);    Fx2.append(item['Fx2']/1e3)
        My1.append(item['My1']/1e6);    My2.append(item['My2']/1e6)
        Mz1.append(item['Mz1']/1e6);    Mz2.append(item['Mz2']/1e6)
        SFz1.append(item['SFz1']/1e3);  SFz2.append(item['SFz2']/1e3)
        SFy1.append(item['SFy1']/1e3);  SFy2.append(item['SFy2']/1e3)
        
    st.write(h4, '1. 하중 조합 (Load Case)')    
    st.write(s1, '✦ LC1 : 고정하중 + 작업하중 + 수평하중')
    st.write(s1, '✦ LC2 : 고정하중 + 풍하중 &nbsp;&nbsp;&nbsp; (허용응력 증가계수 : 1.25)')
    
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '2. 변위 및 응력 검토')
    st.write(s1, '1) 수직변위 검토 (절대 최댓값)')
    Fy = min(Vertical.Fy, Horizontal.Fy, Bracing.Fy)
    Table.Section_Check(In, '', '', '', '수직변위', uz, '')
    st.write('###### $\,\,\,\,\,\,\,\,\,\,$', rf':blue[*LC2의 경우 허용응력 증가계수 1.25를 고려한다. (변위값/1.25)]')
    
    st.write(s1, '2) 등가응력 검토 (절대 최댓값)')
    Table.Section_Check(In, '', '', Fy, '등가응력', seqv, '')
    st.write('###### $\,\,\,\,\,\,\,\,\,\,$', rf':blue[*LC2의 경우 허용응력 증가계수 1.25를 고려한다. (응력값/1.25)]')


    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '3. 단면력 집계')
    st.write(s1, '1) 단면력 (절대 최댓값)')
    Table.Section(In, Fx1, Fx2, My1, My2, Mz1, Mz2, SFz1, SFz2, SFy1, SFy2, '')
    
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.write(s1, '2) 허용응력 증가계수를 고려한 단면력')
    st.write(s2, '➣ LC2(하중조합 2)의 경우 허용응력 증가계수 1.25를 고려한다.')
    st.write(s2, '➣ 허용응력 증가는 단면력을 1.25로 나눈 것과 같다.')
    [Axial, Moment, Shear] = Table.Section(In, Fx1, Fx2, My1, My2, Mz1, Mz2, SFz1, SFz2, SFy1, SFy2, 1.25)    
    
    for i in [1, 2, 3]:
        if i != 1:
            st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
        txt = ['4. ', '수직재'];  opt = ['축방향력', '휨모멘트', '전단력', Vertical]
        if i == 2:  txt = ['5. ', '수평재'];  opt[3] = Horizontal
        if i == 3:  txt = ['6. ', '가새재'];  opt[3] = Bracing
        
        st.write(h4, f'{txt[0]} {txt[1]} 검토')
        st.write(s1, f'1) {txt[1]}에 발생하는 절대 최대 단면력')
        Table.Section_Check(In, Axial, Moment, Shear, '', '', txt[1])    
        st.write(s1, f'2) {opt[0]}에 대한 검토')
        Table.Section_Check(In, Axial, Moment, Shear, opt[0], opt[3], txt[1])
        st.write(s1, f'3) {opt[1]}에 대한 검토')
        Table.Section_Check(In, Axial, Moment, Shear, opt[1], opt[3], txt[1])
        st.write(s1, f'4) {opt[2]}에 대한 검토')
        Table.Section_Check(In, Axial, Moment, Shear, opt[2], opt[3], txt[1])
    
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, '7. 상세 구조해석 결과')    
    working_dir = 'pyAPDL';  jobname = 'file';  png = []
    for i in range(0, 18):
        if i < 10:  name = os.path.join(working_dir, jobname + '00' + str(i) + '.png')
        if i >= 10: name = os.path.join(working_dir, jobname + '0'  + str(i) + '.png')
        png.append(name)
    
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h4, '[해석 모델]')
        st.image(png[0], width=800)
        
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h4, '[경계조건 및 하중조건]')    
        st.image(png[1], width=800)
    
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, f':blue[<Displacement [u$_z$, 변위 (mm)]>]')
    col = st.columns([1,8,1])
    with col[1]:        
        st.write(h5, f'➣ 최대 변위 : {uz[0]:,.3f} mm [LC1]')
        st.image(png[2], width=800)
        
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 변위 : {uz[1]:,.3f} mm [LC2 : 풍하중 고려]')
        st.image(png[2+9], width=800)

    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, f':blue[<von Mises Stress [$\sigma_{{eqv}}$, 등가응력 (MPa)]>]')
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 등가응력 : {seqv[0]:,.1f} MPa [LC1]')
        st.image(png[3], width=800)
    
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 등가응력 : {seqv[1]:,.1f} MPa [LC2 : 풍하중 고려]')
        st.image(png[3+9], width=800)

    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########    
    st.write(h4, f':blue[<Axial Force [F$_x$, 축방향력 (N)]>]')
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 축방향력 : {Fx1[0]:,.3f} kN [LC1]')
        st.write(h5, f'➣ 최소 축방향력 : {Fx2[0]:,.3f} kN [LC1]')
        st.image(png[4], width=800)
        
    col = st.columns([1,8,1])
    with col[1]:        
        st.write(h5, f'➣ 최대 축방향력 : {Fx1[1]:,.3f} kN [LC2 : 풍하중 고려]')
        st.write(h5, f'➣ 최소 축방향력 : {Fx2[1]:,.3f} kN [LC2 : 풍하중 고려]')
        st.image(png[4+9], width=800)

    
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, f':blue[<Moment [M$_y$, 모멘트 (N·mm)]>]')
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 모멘트 : {My1[0]:,.3f} kN·m [LC1]')
        st.write(h5, f'➣ 최소 모멘트 : {My2[0]:,.3f} kN·m [LC1]')
        st.image(png[5], width=800)

    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 모멘트 : {My1[1]:,.3f} kN·m [LC2 : 풍하중 고려]')
        st.write(h5, f'➣ 최소 모멘트 : {My2[1]:,.3f} kN·m [LC2 : 풍하중 고려]')
        st.image(png[5+9], width=800)

    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, f':blue[<Moment [M$_z$, 모멘트 (N·mm)]>]')
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 모멘트 : {Mz1[0]:,.3f} kN·m [LC1]')
        st.write(h5, f'➣ 최소 모멘트 : {Mz2[0]:,.3f} kN·m [LC1]')
        st.image(png[6], width=800)

    col = st.columns([1,8,1])
    with col[1]:    
        st.write(h5, f'➣ 최대 모멘트 : {Mz1[1]:,.3f} kN·m [LC2 : 풍하중 고려]')
        st.write(h5, f'➣ 최소 모멘트 : {Mz2[1]:,.3f} kN·m [LC2 : 풍하중 고려]')
        st.image(png[6+9], width=800)    
    
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, f':blue[<Shear Force [S$_z$, 전단력 (N)]>]')
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 전단력 : {SFz1[0]:,.3f} kN [LC1]')
        st.write(h5, f'➣ 최소 전단력 : {SFz2[0]:,.3f} kN [LC1]')
        st.image(png[7], width=800)

    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 전단력 : {SFz1[1]:,.3f} kN [LC2 : 풍하중 고려]')
        st.write(h5, f'➣ 최소 전단력 : {SFz2[1]:,.3f} kN [LC2 : 풍하중 고려]')
        st.image(png[7+9], width=800)
    
        
    st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
    st.markdown(In.border1, unsafe_allow_html=True) ########### border ##########
    st.write(h4, f':blue[<Shear Force [S$_y$, 전단력 (N)]>]')
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 전단력 : {SFy1[0]:,.3f} kN [LC1]')
        st.write(h5, f'➣ 최소 전단력 : {SFy2[0]:,.3f} kN [LC1]')
        st.image(png[8], width=800)
    
    col = st.columns([1,8,1])
    with col[1]:
        st.write(h5, f'➣ 최대 전단력 : {SFy1[1]:,.3f} kN [LC2 : 풍하중 고려]')
        st.write(h5, f'➣ 최소 전단력 : {SFy2[1]:,.3f} kN [LC2 : 풍하중 고려]')
        st.image(png[8+9], width=800)

def Code():
    file_path = 'pyAPDL.py';  encoding = 'utf-8'    
    with open(file_path, 'r', encoding = encoding) as f:
        lines = f.readlines()
    code_string = ''.join(lines)
    st.code(code_string, line_numbers=True)

def Analysis(In, opt, Vertical, Horizontal, Bracing):
    if 'code' in opt:
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.title(':orange[부 록 🎯] (ANSYS 3차원 상세 구조해석 코드)')
    else:
        st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)    ############ 인쇄할 때, 페이지 나누기 ###################
        st.title(':orange[Ⅲ. 3차원 상세 구조해석 🎯]')
    st.markdown(In.border2, unsafe_allow_html=True) ########### border ##########  #st.markdown('\n')
    
    if 'result' in opt:  Result(In, Vertical, Horizontal, Bracing)
    if 'code' in opt:    Code()
    
    if 'both' in opt:
        tabtab = st.tabs([In.h4+':orange[해석 결과]', In.h4+':blue[해석 코드]'])
        with tabtab[0]:
            Result(In, Vertical, Horizontal, Bracing)

        with tabtab[1]:
            Code()
