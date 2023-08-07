import streamlit as st 
import plotly.graph_objects as go
import pandas as pd
import numpy as np

fn1 = 'Nanum Gothic';  fn2 = 'Gungsuhche';  fn3 = 'Lora';  fn4 = 'Noto Sans KR'
table_font = fn1
fs = 17;  lw = 2; width = 960

# # 공통 스타일 정의
# common_style = {
#     "align": ["center"],
#     "font": {"size": fs, "color": "black", "family": fn},
#     "fill_color": ["silver"],
#     "line": {"color": "black", "width": lw},
# }

# # 적용할 요소에 공통 스타일에 대한 참조 사용
# header=dict(
#     **common_style
# )

def Wood_Deformation(In):
    headers = [
        '<b>표면 등급</b>',
        '<b>상대변형 [mm]</b>',
        '<b>절대변형 [mm]</b>',
        '<b>표면 상태</b>',
        '<b>비고</b>',]
    data = [ f'<b>{In.level}', f'<b><i>L<sub>n</sub></i> / {In.d1}', f'<b>{In.d2}', f'<b>미관상 중요한 노출 콘크리트 면', '', ]    
    if 'B' in In.level: data[3] = f'<b>마감이 있는 콘크리트 면'
    if 'C' in In.level: data[3] = f'<b>미관상 중요하지 않은 노출콘크리트 면'

    data_dict = {header: [value] for header, value in zip(headers, data)}  # 행이 한개 일때
    df = pd.DataFrame(data_dict)
    
    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        columnwidth=[0.9, 1, 0.9, 2.2, 1],
        header=dict(
            values=list(df.columns),
            align=['center'],
            font=dict(size=fs, color='black', family=table_font, ),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            align=['center'],
            font=dict(size=fs, color='black', family=table_font, ),  # 글꼴 변경
            fill_color=['white'],  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            # format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ), )],
    )
    fig.update_layout(width=width, height=85, margin=dict(l=20, r=1, t=1, b=1))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)

def Input(In):
    headers = [
        '<b>부재</b>',
        '<b>규격 [mm]</b>',
        '<b>재료</b>',
        '<b>설치간격 [mm]</b>',
        '<b>비고</b>',]
    data = [
    ['<b>합판',   f'<b>{In.wood} (하중방향)', '<b>거푸집용', f'<b>-', ''],
    ['<b>장선',   f'<b>{In.joist}', '<b>SPSR400', f'<b><i>L<sub>j</sub></i> = {In.Lj:,.0f} mm', ''],
    ['<b>멍에',   f'<b>{In.yoke}', '<b>SPSR400', f'<b><i>L<sub>y</sub></i> = {In.Ly:,.0f} mm', ''], #f'<b>멍에의 간격은 수직재의 간격과 같다'],
    ['<b>수직재', f'<b>{In.vertical}', '<b>SKT500', f'<b><i>L<sub>v</sub></i> = {In.Lv:,.0f} mm', f'<b>수직재의 간격은 수평재 좌굴길이(KL<sub>h</sub>)와 같다'],
    ['<b>수평재', f'<b>{In.horizontal}', '<b>SKT400', f'<b><i>L<sub>h</sub></i> = <b>{In.Lh:,.0f} mm', f'<b>수평재의 간격은 수직재 좌굴길이(KL<sub>v</sub>)와 같다'],
    ['<b>가새재', f'<b>{In.bracing}', '<b>SKT400', f'<b>-', ''],
    ]

    data_dict = {header: values for header, values in zip(headers, zip(*data))}  # 행이 여러개(2개 이상) 일때
    df = pd.DataFrame(data_dict)
    
    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        columnwidth=[0.8, 1.4, 1,1.2, 3],
        header=dict(
            values=list(df.columns),
            align=['center'],
            font=dict(size=fs, color='black', family=table_font, ),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            # align=['center','center','center','center','left'],
            align=['center' if i != 4 else 'left' for i in range(len(df.columns))],
            font=dict(size=fs, color='black', family=table_font, ),  # 글꼴 변경
            fill_color=['silver', 'white'],  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            # format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ), )],
    )
    fig.update_layout(width=width, height=285, margin=dict(l=20, r=1, t=1, b=1))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)


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
        
        columnwidth = [1, 4.3];  height = 220
        headers = [
        '<b>구분</b>',
        '<b>max[고정하중의 2%, 단위길이당 1.5 kN/m]', ]

        txt1 = f'<b>X방향 : 고정하중의 2% × Y방향 길이 = {H2:.3f} kN/m² × {In.slab_Y:.1f} m = {Hx1:.3f} kN/m {lgeqx} 1.5 kN/m'+ f'<br><b>Y방향 : 고정하중의 2% × X방향 길이 = {H2:.3f} kN/m² × {In.slab_X:.1f} m = {Hy1:.3f} kN/m  {lgeqy} 1.5 kN/m'

        Hx1 = max(Hx1, 1.5);  Hx2 = Hx1/In.slab_X
        Hy1 = max(Hy1, 1.5);  Hy2 = Hy1/In.slab_Y
        txt2 = f'<b>X방향 : 위의 큰값 / X방향 길이 = {Hx1:.3f} kN/m / {In.slab_X:.1f} m = {Hx2:.3f} kN/m²'+ f'<br><b>Y방향 : 위의 큰값 / Y방향 길이 = {Hy1:.3f} kN/m / {In.slab_Y:.1f} m = {Hy2:.3f} kN/m²'
        In.Hx = Hx2*In.slab_X*In.slab_Y;  In.Hy = Hy2*In.slab_X*In.slab_Y

        txt3 = f'<b>X방향 : 위의 수평하중 × X방향 길이 × Y방향 길이 = {Hx2:.3f} kN/m² × {In.slab_X:.1f} m × {In.slab_Y:.1f} m = {In.Hx:.1f} kN'+ f'<br><b>Y방향 : 위의 수평하중 × X방향 길이 × Y방향 길이 = {Hy2:.3f} kN/m² × {In.slab_X:.1f} m × {In.slab_Y:.1f} m = {In.Hy:.1f} kN'

        data = [
        [f'<b>단위 길이당 수평하중<br><b>        [kN/m]', txt1],
        ['<b>단위 면적당 수평하중<br><b>         [kN/m²]', txt2],
        ['<b>수평하중 (P<sub>h</sub>)<br>      [kN]', txt3], ]
        
    data_dict = {header: values for header, values in zip(headers, zip(*data))}  # 행이 여러개(2개 이상) 일때
    df = pd.DataFrame(data_dict)
    
    fs_verhor = 16 if 'hor' in verhor else 17
    fig = go.Figure(data=[go.Table(
        columnwidth = columnwidth,
        header=dict(
            values=list(df.columns),
            align=['center'],
            # height=10,
            font=dict(size=fs, color='black', family=table_font, ),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],            
            align=['center', 'center', 'center', 'left'],
            # height=25,            
            prefix=None,
            suffix=None,
            font=dict(size=fs_verhor, color='black', family=table_font, ),  # 글꼴 변경
            fill=dict(color=['silver', 'white']),  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ), )],
    )
    fig.update_layout(width=width, height=height, margin=dict(l=40, r=1, t=1, b=1))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)    


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
        data[3] = '<b>-'
        headers[7] = '<b>회전반경<br> r [mm]</b>'
        headers[8] = f'<b>항복강도<br><i>F<sub>y</sub></i> [MPa]</b>'        

    data_dict = {header: [value] for header, value in zip(headers, data)}  # 행이 한개 일때
    df = pd.DataFrame(data_dict)

    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        columnwidth=[0.7, 1.6, 0.9, 1.1, 1.2, 0.9, 0.9, 1,1.1],
        header=dict(
            values=list(df.columns),
            align=['center'],
            # height=10,
            font=dict(size=fs, color='black', family=table_font),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            align=['center']*1,
            # height=25,
            prefix=None,
            suffix=None,
            font=dict(size=fs, color='black', family=table_font),  # 글꼴 변경
            fill=dict(color=['silver', 'white']),  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ), )],
    )    
    fig.update_layout(width=width, height=106, margin=dict(l=l_margin, r=1, t=1, b=1))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)
    

