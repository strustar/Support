import streamlit as st 
import plotly.graph_objects as go
import pandas as pd
import numpy as np

fs = 16;  lw = 2; width = 950

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

def Wood_Deformation(fn, In):
    headers = [
        '<b>표면 등급</b>',
        '<b>상대변형 [mm]</b>',
        '<b>절대변형 [mm]</b>',
        '<b>노출면 상태</b>',
        '<b>비고</b>',]
    data = [
    [f'<b>{In.level}', f'<b><i>L<sub>n</sub></i> / {In.d1}', f'<b>{In.d2}', f'<b>미관상 중요한 노출 콘크리트면', ''],    
    ]

    data_dict = {header: values for header, values in zip(headers, zip(*data))}  # 행이 여러개(2개 이상) 일때
    df = pd.DataFrame(data_dict)
    
    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        columnwidth=[1, 1, 1, 2, 1],
        header=dict(
            values=list(df.columns),
            align=['center'],
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            align=['center'],
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill_color=['white'],  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            # format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ), )],
    )
    fig.update_layout(width=width, height=80, margin=dict(l=20, r=0, t=1, b=0))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)

def Input(fn, In):
    headers = [
        '<b>부재</b>',
        '<b>규격 [mm]</b>',
        '<b>재료</b>',
        '<b>설치간격 [mm]</b>',
        '<b>비고</b>',]
    data = [
    ['<b>합판',   f'<b>{In.wood} (하중방향)', '<b>거푸집용', f'<b>-', ''],
    ['<b>장선',   f'<b>{In.joist}', '<b>SPSR400', f'<b><i>L<sub>j</sub></i> = {In.Lj:,.0f} mm', ''],
    ['<b>멍에',   f'<b>{In.yoke}', '<b>SPSR400', f'<b><i>L<sub>y</sub></i> = {In.Ly:,.0f} mm', f'<b>멍에의 간격은 수직재의 간격과 같다'],
    ['<b>수직재', f'<b>{In.vertical}', '<b>SKT500', f'<b><i>L<sub>v</sub></i> = {In.Ly:,.0f} mm', f'<b>수직재의 간격은 수평재 좌굴길이(KL<sub>h</sub>)와 같다'],
    ['<b>수평재', f'<b>{In.horizontal}', '<b>SKT400', f'<b><i>L<sub>h</sub></i> = <b>{In.Lh:,.0f} mm', f'<b>수평재의 간격은 수직재 좌굴길이(KL<sub>v</sub>)와 같다'],
    ['<b>가새재', f'<b>{In.bracing}', '<b>SKT400', f'<b>-', ''],
    ]

    data_dict = {header: values for header, values in zip(headers, zip(*data))}  # 행이 여러개(2개 이상) 일때
    df = pd.DataFrame(data_dict)
    
    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        columnwidth=[0.8, 1.3, 1,1,2.6],
        header=dict(
            values=list(df.columns),
            align=['center'],
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            # align=['center','center','center','center','left'],
            align=['center' if i != 4 else 'left' for i in range(len(df.columns))],
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill_color=['silver', 'white'],  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            # format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ), )],
    )
    fig.update_layout(width=width, height=275, margin=dict(l=20, r=0, t=1, b=0))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)


def Load(fn, thick_height, concrete_weight, wood_weight):
    headers = [
        '<b>구분</b>',
        '<b>하중 [N/mm²]</b>',
        '<b>하중 [kN/m²]</b>',
        '<b>하중 산정 [KDS 21 50 00 :2022]</b>', ]
    wood_load = wood_weight;  concrete_load = concrete_weight*thick_height/1e3;  live_load = 2.5   # kN/m²
    if thick_height/1e3 >= 0.5: live_load = 3.5
    if thick_height/1e3 >= 1.0: live_load = 5.0
    design_load = concrete_load + wood_load + live_load

    data = [
    ['<b>콘크리트 자중', f'<b>{concrete_load/1e3:.4f}', f'<b>{concrete_load:.2f}', f'<b>{concrete_weight:.1f}'+' kN/m³ × ' + f'<b>{thick_height/1e3:.3f}'+' m = ' + f'<b>{concrete_load:.2f}' + ' kN/m²'],
    ['<b>거푸집 자중', f'<b>{wood_load/1e3:.4f}', f'<b>{wood_load:.2f}', '<b>최소 0.4 kN/m² (1.6.2 연직하중)'],
    ['<b>작업하중 (활하중)', f'<b>{live_load/1e3:.4f}', f'<b>{live_load:.2f}', '<b>*최소 2.5 kN/m² (1.6.2 연직하중)'],
    ['<b>∑ (합계)', f'<b>{design_load/1e3:.4f}', f'<b>{design_load:.2f}', '<b>최소 5.0 kN/m² (1.6.2 연직하중)'], ]

    data_dict = {header: values for header, values in zip(headers, zip(*data))}  # 행이 여러개(2개 이상) 일때
    df = pd.DataFrame(data_dict)
    
    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        columnwidth=[1.6, 1., 1., 2.6],
        header=dict(
            values=list(df.columns),
            align=['center'],
            # height=10,
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            align=['center'],
            # align=['center', 'center', 'right', 'left'],
            # height=25,
            prefix=None,
            suffix=None,
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill=dict(color=['silver', 'white']),  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ), )],
    )
    fig.update_layout(width=width, height=190, margin=dict(l=40, r=0, t=1, b=0))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)
    return design_load


def Info(fn, opt, section, A, I, S, E, fba, fsa, l_margin):
    headers = [
        '<b>부재<br>종류</b>',
        '<b>두께 / 하중방향<br>      [mm / °]</b>',
        '<b> 단면적<br>A [mm²]</b>',
        '<b>단면계수<br>S [mm³]</b>',
        '<b>단면2차모멘트<br>    I [mm⁴]</b>',
        '<b>탄성계수<br> E [GPa]</b>',
        '<b>허용휨응력<br>  f<sub>ba</sub> [MPa]</b>',
        '<b>허용전단응력<br>   f<sub>sa</sub> [MPa]</b>', ]
    data = [
        '<b>' + opt,
        '<b>' + section,
        f'<b>{A:,.1f}</b>',
        f'<b>{S:,.1f}</b>',
        f'<b>{I:,.1f}</b>',        
        f'<b>{E/1e3:,.1f}</b>',
        f'<b>{fba:.1f}</b>',
        f'<b>{fsa:.2f}</b>', ]
    
    if '합판' in opt:
        headers[2] = '<b>  전단상수<br>Ib/Q [mm²]</b>'
    if '합판' not in opt:
        headers[1] = '<b> 단면<br>[mm]</b>'
        data[3] = f'<b>{S/1e3:,.1f}×10³</b>'
        data[4] = f'<b>{I/1e3:,.1f}×10³</b>'
        data[7] = f'<b>{fsa:.1f}</b>'
    if '재' in opt:
        headers[6] = '<b>회전반경<br> r [mm]</b>'
        headers[7] = f'<b>항복강도<br><i>F<sub>y</sub></i> [MPa]</b>'        

    data_dict = {header: [value] for header, value in zip(headers, data)}  # 행이 한개 일때    
    df = pd.DataFrame(data_dict)

    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        columnwidth=[0.8, 1.4, 0.9, 0.9, 1.2, 0.9, 1, 1.1],
        header=dict(
            values=list(df.columns),
            align=['center'],
            # height=10,
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            align=['center']*1,
            # height=25,
            prefix=None,
            suffix=None,
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill=dict(color=['silver', 'white']),  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ), )],
    )    
    fig.update_layout(width=width, height=100, margin=dict(l=l_margin, r=0, t=1, b=0))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)
    

def Interval(fn, d, d1, d2):
    headers = [
        '<b>휨응력 검토</b>',
        '<b>상대변형 검토</b>',
        '<b>절대변형 검토</b>', ]
    data = [
        f'<b>{d:,.1f} mm</b>',
        f'<b>{d1:,.1f} mm</b>',
        f'<b>{d2:,.1f} mm</b>', ]
    data_dict = {header: [value] for header, value in zip(headers, data)}  # 행이 한개 일때    
    df = pd.DataFrame(data_dict)

    color = ['black','black','black']
    n = [d, d1, d2];  min_index = n.index(min(n));  color[min_index] = 'orange'    
    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        # columnwidth=[1, 1, 1, 1, 1.3, 1, 1, 1.3],
        header=dict(
            values=list(df.columns),
            align=['center'],
            font=dict(size=fs, color=['black','black','black'], family=fn),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            align=['center']*1,
            font=dict(size=fs, color=color, family=fn),  # 글꼴 변경
            fill=dict(color=['white']),  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ), )],
    )    
    fig.update_layout(width=600, height=80, margin=dict(l=65, r=0, t=1, b=0))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)

