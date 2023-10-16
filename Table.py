import streamlit as st 
import plotly.graph_objects as go
import pandas as pd
import numpy as np

fn1 = 'Nanum Gothic';  fn2 = 'Gungsuhche';  fn3 = 'Lora';  fn4 = 'Noto Sans KR'
table_font = fn1;  fs = 17;  lw = 2;  width = 980

def common_table(headers, data, columnwidth, cells_align, cells_fill_color, height, left, **kargs):
    if np.ndim(data) == 1:
        data_dict = {header: [value] for header, value in zip(headers, data)}  # 행이 한개 일때
    else:
        data_dict = {header: values for header, values in zip(headers, zip(*data))}  # 행이 여러개(2개 이상) 일때
    df = pd.DataFrame(data_dict)
    
    fill_color = ['silver']
    if len(kargs) > 0:  fill_color = kargs['fill_color']
    fig = go.Figure(data = [go.Table(        
        columnwidth = columnwidth,
        header = dict(
            values = list(df.columns),
            align = ['center'],            
            fill_color = fill_color,  #'darkgray'
            font = dict(size = fs, color = 'black', family = table_font, ),  # 글꼴 변경
            line = dict(color = 'black', width = lw),   # 셀 경계색, 두께
        ),
        cells = dict(
            values = [df[col] for col in df.columns],
            align = cells_align,            
            fill_color = cells_fill_color,  # 셀 배경색 변경
            font = dict(size = fs, color = 'black', family = table_font, ),  # 글꼴 변경
            line = dict(color = 'black', width = lw),   # 셀 경계색, 두께
            # format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ), )],
    )
    fig.update_layout(width = width, height = height, margin = dict(l = left, r = 1, t = 1, b = 1))  # 테이블 여백 제거  # 표의 크기 지정    
    st.plotly_chart(fig)

def Summary(In):
    headers = [
        '<b><br>구 분</b>',
        '<b>보의 높이*<br>5,600 mm</b>',
        '<b>보의 높이*<br>3,550 mm</b>',
        '<b>보의 높이*<br>1,500 mm</b>',
        '<b><br>비 고</b>',]
    data = [
        ['<b>합판',       f'<b>{In.wood} (하중방향)', '<b>좌동', '<b>좌동', ''],
        ['<b><br>장선',   f'<b>{In.joist}<br>       @{In.Lj:,.0f}', f'<b>{In.joist}<br>       @130', f'<b>{In.joist}<br>       @170', ''],
        ['<b><br>멍에',   f'<b>{In.yoke}<br>        @{In.Ly:,.0f}', '<b><br>좌동', '<b><br>좌동', ''],
        ['<b><br>수직재', f'<b>{In.vertical}<br>       @{In.Lv:,.0f}', '<b><br>좌동', '<b><br>좌동', ''],
        ['<b><br>수평재', f'<b>{In.horizontal}<br>       @{In.Lh:,.0f}', '<b><br>좌동', '<b><br>좌동', ''],
        ['<b>가새재',     f'<b>{In.bracing}', '<b>좌동', '<b>좌동', ''],   ]
    
    columnwidth = [1, 1.5, 1.5, 1.5, 1];  height = 385;  left = 20
    cells_align = ['center', 'center', 'center', 'center', 'left'];  cells_fill_color = ['silver', 'white']    
    common_table(headers, data, columnwidth, cells_align, cells_fill_color, height, left)
    
def Section_Check(In, Axial, Moment, Shear, force, Support, txt):
    if '수직재' in txt:  index = 0
    if '수평재' in txt:  index = 2
    if '가새재' in txt:  index = 4
    height = 120
        
    if force == '':
        columnwidth = [1]
        headers = [        
            '<b>구 분</b>',
            '<b>축방향력 [kN]</b>',
            '<b>휨모멘트 [kN&#8226;m]</b>',
            '<b>전단력 [kN]</b>', 
            '<b>안전률</b>', ]
        data = [
            ['<b>LC1', f'<b>{Axial[index]:,.3f}', f'<b>{Moment[index]:,.3f}', f'<b>{Shear[index]:,.3f}', '<b>1.0'],
            ['<b>LC2', f'<b>{Axial[index+1]:,.3f}', f'<b>{Moment[index+1]:,.3f}', f'<b>{Shear[index+1]:,.3f}', '<b>1.0'],  ]
    elif '변위' in force:
        columnwidth = [1];  height = 159
        headers = [
            '<b>구 분</b>',
            f'<b>{force} [mm]</b>',
            '<b>허용변위 [mm]</b>',             
            '<b>변위 검토</b>',
            ]
        uz = Support;  Fy = txt
        check1 = 'OK (✅)' if uz[0] < In.d2 else 'NG (❌)'
        check2 = 'OK (✅)' if uz[1] < In.d2 else 'NG (❌)'        
        data = [
            ['<b>LC1', f'<b>{uz[0]:,.3f}', f'<b>{In.d2:,.1f} [{In.level}]', f'<b>{check1}'],
            ['<b>LC2', f'<b>{uz[1]:,.3f}', f'<b>{In.d2:,.1f} [{In.level}]', f'<b>{check2}'],
            ['<b>LC2*', f'<b>{uz[1]/1.25:,.3f}', f'<b>{In.d2:,.1f} [{In.level}]', f'<b>{check2}'], ]
    elif '응력' in force:
        columnwidth = [1];  height = 159
        headers = [
            '<b>구 분</b>',
            f'<b>{force} [MPa]</b>',
            '<b>허용응력 [MPa]</b>',             
            '<b>응력 검토</b>',
            ]
        seqv = Support;  Fy = Shear
        check1 = 'OK (✅)' if seqv[0] < Fy else 'NG (❌)'
        check2 = 'OK (✅)' if seqv[1] < Fy else 'NG (❌)'        
        data = [
            ['<b>LC1', f'<b>{seqv[0]:,.1f}', f'<b>{Fy:,.1f}', f'<b>{check1}'],
            ['<b>LC2', f'<b>{seqv[1]:,.1f}', f'<b>{Fy:,.1f}', f'<b>{check2}'],
            ['<b>LC2*', f'<b>{seqv[1]/1.25:,.1f}', f'<b>{Fy:,.1f}', f'<b>{check2}'], ]
    else:
        columnwidth = [0.8, 4.8, 1.4, 0.8, 0.9]        
        headers = [
            '<b>구 분</b>',
            '<b>응력계산 [MPa]</b>',
            '<b>허용응력 [MPa]</b>',
            '<b>응력비</b>', 
            '<b>검토</b>', ]
        
        if '축' in force:
            allowable = Support.Fca
            F1 = Axial[index];  F2 = Axial[index+1];  A = Support.A
            txt1 = '축방향력/단면적';  txt2 = 'kN';  txt3 = 'mm²'
            
        if '전단' in force:
            allowable = 125  # Check !!!
            F1 = Shear[index];  F2 = Shear[index+1];  A = Support.Ib_Q
            txt1 = '전단력/전단면적';  txt2 = 'kN';  txt3 = 'mm²'

        if '휨' in force:
            allowable = Support.Fy
            F1 = Moment[index];  F2 = Moment[index+1];  A = Support.S
            txt1 = '휨모멘트/단면계수';  txt2 = 'kN&#8226;m';  txt3 = 'mm³'
            
        f = 1e6 if '휨' in force else 1e3
        stress1 = f*F1/A;  ratio1 = stress1/allowable
        stress2 = f*F2/A;  ratio2 = stress2/allowable
        check1 = 'OK (✅)' if stress1 < allowable else 'NG (❌)'
        check2 = 'OK (✅)' if stress2 < allowable else 'NG (❌)'        
        data = [
            ['<b>LC1', f'<b>{txt1} = {F1:,.3f} {txt2} / {A:,.1f} {txt3} = {stress1:,.1f} MPa', f'<b>{allowable:,.1f}', f'<b>{ratio1:,.3f}', f'<b>{check1}'],
            ['<b>LC2', f'<b>{txt1} = {F2:,.3f} {txt2} / {A:,.1f} {txt3} = {stress2:,.1f} MPa', f'<b>{allowable:,.1f}', f'<b>{ratio2:,.3f}', f'<b>{check2}'], ]
            
    left = 40
    cells_align = 'center';  cells_fill_color = ['lightblue', 'white']
    common_table(headers, data, columnwidth, cells_align, cells_fill_color, height, left, fill_color = cells_fill_color[0])
        

def Section(In, Fx1, Fx2, My1, My2, Mz1, Mz2, SFz1, SFz2, SFy1, SFy2, opt):
    headers = [
        '<b>부 재<br>종 류</b>',
        '<b>축방향력<br>   [kN] </b>',
        '<b>축방향력<br>   [kN]</b>',
        '<b>휨모멘트<br> [kN&#8226;m] </b>',
        '<b>휨모멘트<br> [kN&#8226;m]</b>',
        '<b>전단력<br> [kN] </b>',
        '<b>전단력<br> [kN]</b>',
        '<b>비 고</b>', ]
    Axial = [];  Moment = [];  Shear = []
    for i in range(2, 7+1):
        Axial.append(np.max([np.abs(Fx1[i]), np.abs(Fx2[i])]))
        Moment.append(np.max([np.abs(My1[i]), np.abs(My2[i]), np.abs(Mz1[i]), np.abs(Mz2[i])]))
        Shear.append(np.max([np.abs(SFz1[i]), np.abs(SFz2[i]), np.abs(SFy1[i]), np.abs(SFy2[i])]))
    if opt == '':
        data = [
            ['<b>', '<b>LC1', '<b>LC2', '<b>LC1', '<b>LC2', '<b>LC1', '<b>LC2', '<b>'],
            ['<b>수직재', f'<b>{Axial[0]:,.3f}', f'<b>{Axial[1]:,.3f}', f'<b>{Moment[0]:,.3f}', f'<b>{Moment[1]:,.3f}', f'<b>{Shear[0]:,.3f}', f'<b>{Shear[1]:,.3f}', '<b>'],
            ['<b>수평재', f'<b>{Axial[2]:,.3f}', f'<b>{Axial[3]:,.3f}', f'<b>{Moment[2]:,.3f}', f'<b>{Moment[3]:,.3f}', f'<b>{Shear[2]:,.3f}', f'<b>{Shear[3]:,.3f}', '<b>'],
            ['<b>가새재', f'<b>{Axial[4]:,.3f}', f'<b>{Axial[5]:,.3f}', f'<b>{Moment[4]:,.3f}', f'<b>{Moment[5]:,.3f}', f'<b>{Shear[4]:,.3f}', f'<b>{Shear[5]:,.3f}', '<b>'],
        ]
    if opt == 1.25:
        for i in [1, 3, 5]:
            Axial[i] = Axial[i]/opt;  Moment[i] = Moment[i]/opt;  Shear[i] = Shear[i]/opt
        
        data = [
            ['<b>', '<b>LC1', '<b>LC2', '<b>LC1', '<b>LC2', '<b>LC1', '<b>LC2', '<b>'],
            ['<b>수직재', f'<b>{Axial[0]:,.3f}', f'<b>{Axial[1]:,.3f}', f'<b>{Moment[0]:,.3f}', f'<b>{Moment[1]:,.3f}', f'<b>{Shear[0]:,.3f}', f'<b>{Shear[1]:,.3f}', '<b>'],
            ['<b>수평재', f'<b>{Axial[2]:,.3f}', f'<b>{Axial[3]:,.3f}', f'<b>{Moment[2]:,.3f}', f'<b>{Moment[3]:,.3f}', f'<b>{Shear[2]:,.3f}', f'<b>{Shear[3]:,.3f}', '<b>'],
            ['<b>가새재', f'<b>{Axial[4]:,.3f}', f'<b>{Axial[5]:,.3f}', f'<b>{Moment[4]:,.3f}', f'<b>{Moment[5]:,.3f}', f'<b>{Shear[4]:,.3f}', f'<b>{Shear[5]:,.3f}', '<b>'],
        ]
    columnwidth = [1];  height = 220;  left = 40
    cells_align = 'center';  cells_fill_color = ['lightblue', 'white']
    common_table(headers, data, columnwidth, cells_align, cells_fill_color, height, left, fill_color = cells_fill_color[0])
    return Axial, Moment, Shear


def Wood_Deformation(In):
    headers = [
        '<b>표면 등급</b>',
        '<b>상대변형 [mm]</b>',
        '<b>절대변형 [mm]</b>',
        '<b>표면 상태</b>',
        '<b>비 고</b>',]
    data = [ f'<b>{In.level}', f'<b><i>L<sub>n</sub></i> / {In.d1}', f'<b>{In.d2}', f'<b>미관상 중요한 노출 콘크리트 면', '', ]    
    if 'B' in In.level: data[3] = f'<b>마감이 있는 콘크리트 면'
    if 'C' in In.level: data[3] = f'<b>미관상 중요하지 않은 노출콘크리트 면'

    columnwidth = [0.9, 1, 0.9, 2.2, 1];  height = 85;  left = 20
    cells_align = 'center';  cells_fill_color = 'white'
    common_table(headers, data, columnwidth, cells_align, cells_fill_color, height, left)


def Input(In):
    headers = [
        '<b>부재</b>',
        '<b>규격 [mm]</b>',
        '<b>재료</b>',
        '<b>설치간격 [mm]</b>',
        '<b>비 고</b>',]
    data = [
        ['<b>합판',   f'<b>{In.wood} (하중방향)', '<b>거푸집용', f'<b>-', ''],
        ['<b>장선',   f'<b>{In.joist}', '<b>SPSR400', f'<b><i>L<sub>j</sub></i> = {In.Lj:,.0f} mm', ''],
        ['<b>멍에',   f'<b>{In.yoke}', '<b>SPSR400', f'<b><i>L<sub>y</sub></i> = {In.Ly:,.0f} mm', ''], #f'<b>멍에의 간격은 수직재의 간격과 같다'],
        ['<b>수직재', f'<b>{In.vertical}', '<b>SKT500', f'<b><i>L<sub>v</sub></i> = {In.Lv:,.0f} mm', f'<b>수직재의 간격은 수평재 좌굴길이(KL<sub>h</sub>)와 같다'],
        ['<b>수평재', f'<b>{In.horizontal}', '<b>SKT400', f'<b><i>L<sub>h</sub></i> = <b>{In.Lh:,.0f} mm', f'<b>수평재의 간격은 수직재 좌굴길이(KL<sub>v</sub>)와 같다'],
        ['<b>가새재', f'<b>{In.bracing}', '<b>SKT400', f'<b>-', ''], ]    
    
    columnwidth = [0.8, 1.4, 1,1.2, 3];  height = 286;  left = 20
    cells_align = ['center', 'center', 'center', 'center', 'left'];  cells_fill_color = ['silver', 'white']    
    common_table(headers, data, columnwidth, cells_align, cells_fill_color, height, left)


def Load_Case():
    headers = [
        '<b>Load Case (LC)</b>',
        '<b>하중조합</b>',
        '<b>허용응력증가계수</b>', ]        
    data = [
        ['<b>LC1', '<b>D + L<sub>i</sub> + M (고정하중 + 작업하중 + 수평하중)', '<b>1.00',],
        ['<b>LC2', '<b>D + W (고정하중 + 풍하중)', '<b>1.25',],
        ['<b>LC3', '<b>D + L<sub>i</sub> + M + S (고정하중 + 작업하중 + 수평하중 + 특수하중)', '<b>1.50',],   ]    

    columnwidth = [1., 3.2, 1., 1];  height = 165;  left = 40
    cells_align = ['center', 'center', 'center', 'left'];  cells_fill_color = ['silver', 'white']    
    common_table(headers, data, columnwidth, cells_align, cells_fill_color, height, left)
    

def Load(In, verhor):
    headers = [
        '<b>구분</b>',
        '<b>하중 [N/mm²]</b>',
        '<b>하중 [kN/m²]</b>',
        '<b>하중 산정</b>', ]
        
    wood_load = In.wood_weight;  concrete_load = In.concrete_weight*In.thick_height/1e3;  live_load = 2.5   # kN/m²
    if In.thick_height/1e3 >= 0.5: live_load = 3.5
    if In.thick_height/1e3 >= 1.0: live_load = 5.0
    dead_load = concrete_load + wood_load;  design_load = dead_load + live_load
    [In.design_load, In.dead_load] = [design_load/1e3, dead_load/1e3]  # N/mm

    data = [
        ['<b>콘크리트 자중', f'<b>{concrete_load/1e3:.4f}', f'<b>{concrete_load:.2f}', f'<b>{In.concrete_weight:.1f}'+' kN/m³ × ' + f'<b>{In.thick_height/1e3:.3f}'+' m = ' + f'<b>{concrete_load:.2f}' + ' kN/m²'],
        ['<b>거푸집 자중', f'<b>{wood_load/1e3:.4f}', f'<b>{wood_load:.2f}', '<b>최소 0.4 kN/m²'],
        ['<b>작업하중*', f'<b>{live_load/1e3:.4f}', f'<b>{live_load:.2f}', '<b>최소 2.5 kN/m²'],
        ['<b>∑ (합계)', f'<b>{design_load/1e3:.4f}', f'<b>{design_load:.2f}', '<b>최소 5.0 kN/m²'], ]
        
    columnwidth = [1., 1., 1., 1.8];  height = 198    
    if 'hor' in verhor:
        H2 = dead_load*0.02;  Hx1 = H2*In.slab_Y;  Hy1 = H2*In.slab_X
        lgeqx = ' < ' if Hx1 <= 1.5 else ' > ';  lgeqy = ' < ' if Hy1 <= 1.5 else ' > '
        
        columnwidth = [1, 4.3];  height = 228
        headers = [
        '<b>구분</b>',
        '<b>max[고정하중의 2%, 단위길이당 1.5 kN/m]', ]

        txt1 = f'<b>X방향 : 고정하중의 2% × Y방향 길이 = {H2:.3f} kN/m² × {In.slab_Y:.1f} m = {Hx1:.3f} kN/m {lgeqx} 1.5 kN/m'+ f'<br><b>Y방향 : 고정하중의 2% × X방향 길이 = {H2:.3f} kN/m² × {In.slab_X:.1f} m = {Hy1:.3f} kN/m  {lgeqy} 1.5 kN/m'

        Hx1 = max(Hx1, 1.5);  Hx2 = Hx1/In.slab_X
        Hy1 = max(Hy1, 1.5);  Hy2 = Hy1/In.slab_Y
        txt2 = f'<b>X방향 : 위의 큰값 / X방향 길이 = {Hx1:.3f} kN/m / {In.slab_X:.1f} m = {Hx2:.3f} kN/m²'+ f'<br><b>Y방향 : 위의 큰값 / Y방향 길이 = {Hy1:.3f} kN/m / {In.slab_Y:.1f} m = {Hy2:.3f} kN/m²'
        In.Hx = Hx2*In.slab_X*In.slab_Y;  In.Hy = Hy2*In.slab_X*In.slab_Y
        In.Hx2 = Hx2;  In.Hy2 = Hy2

        txt3 = f'<b>X방향 : 위의 수평하중 × X방향 길이 × Y방향 길이 = {Hx2:.3f} kN/m² × {In.slab_X:.1f} m × {In.slab_Y:.1f} m = {In.Hx:.1f} kN'+ f'<br><b>Y방향 : 위의 수평하중 × X방향 길이 × Y방향 길이 = {Hy2:.3f} kN/m² × {In.slab_X:.1f} m × {In.slab_Y:.1f} m = {In.Hy:.1f} kN'

        data = [
            [f'<b>단위 길이당 수평하중<br><b>        [kN/m]', txt1],
            ['<b>단위 면적당 수평하중<br><b>         [kN/m²]', txt2],
            ['<b>수평하중 (P<sub>h</sub>)<br>      [kN]', txt3], ]
        
    left = 40
    cells_align = ['center', 'center', 'center', 'left'];  cells_fill_color = ['silver', 'white']    
    common_table(headers, data, columnwidth, cells_align, cells_fill_color, height, left)


def Info(opt, section, A, Ib_Q, I, S, E, fba, fsa, l_margin):
    headers = [
        '<b>부재<br>종류</b>',
        '<b>두께 / 하중방향<br>      [mm / °]</b>',
        '<b> 단면적<br>A [mm²]</b>',
        '<b>  전단상수<br>Ib/Q [mm²]</b>',        
        '<b>단면2차모멘트<br>    I [mm⁴]</b>',
        '<b>단면계수<br>S [mm³]</b>',        
        '<b>탄성계수<br> E [GPa]</b>',
        '<b>허용휨응력<br>  f<sub>ba</sub> [MPa]</b>',
        '<b>허용전단응력<br>   f<sub>sa</sub> [MPa]</b>', ]
    data = [
        '<b>' + opt,
        '<b>' + section,
        f'<b>{A:,.1f}</b>',
        f'<b>{Ib_Q:,.1f}</b>',
        f'<b>{I:,.1f}</b>',
        f'<b>{S:,.1f}</b>',        
        f'<b>{E/1e3:,.1f}</b>',
        f'<b>{fba:.1f}</b>',
        f'<b>{fsa:.2f}</b>', ]
    
    if '합판' in opt:
        data[2] = '<b>-'
    if '합판' not in opt:
        headers[1] = '<b>단면 규격<br>  [mm]</b>'
        data[4] = f'<b>{I/1e3:,.1f}×10³</b>'
        data[5] = f'<b>{S/1e3:,.1f}×10³</b>'
        data[8] = f'<b>{fsa:.1f}</b>'
    if '재' in opt:
        # data[3] = '<b>-'
        headers[7] = '<b>회전반경<br> r [mm]</b>'
        headers[8] = f'<b>항복강도<br><i>F<sub>y</sub></i> [MPa]</b>'        

    columnwidth = [0.7, 1.6, 0.9, 1.1, 1.2, 0.9, 0.9, 1,1.1];  height = 106;  left = l_margin
    cells_align = ['center'];  cells_fill_color = ['silver', 'white']    
    common_table(headers, data, columnwidth, cells_align, cells_fill_color, height, left)
