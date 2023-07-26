import streamlit as st 
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def Load(fn, thick_height, s_weight, w_weight):
    headers = [
        '<b>구분</b>',
        '<b>하중 [N/mm²]</b>',
        '<b>하중 [kN/m²]</b>',
        '<b>하중 산정 [KDS 21 50 00 :2022]</b>',
    ]
    w_load = w_weight;  s_load = s_weight*thick_height/1e3;  live_load = 2.5   # kN/m²
    if thick_height/1e3 >= 0.5: live_load = 3.5
    if thick_height/1e3 >= 1.0: live_load = 5.0
    t_load = s_load + w_load + live_load

    data = [
    ['<b>콘크리트 자중', f'<b>{s_load/1e3:.4f}', f'<b>{s_load:.2f}', f'<b>{s_weight:.1f}'+' kN/m³ × ' + f'<b>{thick_height/1e3:.3f}'+' m = ' + f'<b>{s_load:.2f}' + ' kN/m²'],
    ['<b>거푸집 자중', f'<b>{w_load/1e3:.4f}', f'<b>{w_load:.2f}', '<b>최소 0.4 kN/m² (1.6.2 연직하중)'],
    ['<b>작업하중 (활하중)', f'<b>{live_load/1e3:.4f}', f'<b>{live_load:.2f}', '<b>*최소 2.5 kN/m² (1.6.2 연직하중)'],
    ['<b>∑ (합계)', f'<b>{t_load/1e3:.4f}', f'<b>{t_load:.2f}', '<b>최소 5.0 kN/m² (1.6.2 연직하중)'],
    ]

    data_dict = {header: values for header, values in zip(headers, zip(*data))}  # 행이 여러개(2개 이상) 일때
    df = pd.DataFrame(data_dict)

    fs = 16;  lw = 2
    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        columnwidth=[1.6, 1., 1., 2.6],
        header=dict(
            values=list(df.columns),
            align=['center'],
            height=10,
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            align=['center'],
            # align=['center', 'center', 'right', 'left'],
            height=25,
            prefix=None,
            suffix=None,
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill=dict(color=['silver', 'white']),  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ),
    )],
    )    
    fig.update_layout(width=900, height=190, margin=dict(l=40, r=0, t=1, b=0))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)
    return t_load


def Info(fn, shape, section, A, I, S, E, fba, fsa, l_margin):
    headers = [
        '<b>부재<br>형상</b>',
        '<b>두께 / 하중방향<br>      [mm / °]</b>',
        '<b> 단면적<br>A [mm²]</b>',
        '<b>단면계수<br>S [mm³]</b>',
        '<b>단면2차모멘트<br>    I [mm⁴]</b>',
        '<b>탄성계수<br> E [GPa]</b>',
        '<b>허용휨응력<br>  <i>f<sub>ba</sub></i> [MPa]</b>',        
        '<b>허용전단응력<br>   <i>f<sub>sa</sub></i> [MPa]</b>',
        ]
    data = [
        '<b>' + shape,
        '<b>' + section,
        f'<b>{A:,.1f}</b>',
        f'<b>{S:,.1f}</b>',
        f'<b>{I:,.1f}</b>',        
        f'<b>{E/1e3:,.1f}</b>',
        f'<b>{fba:.1f}</b>',
        f'<b>{fsa:.2f}</b>',
        ]
    if '합판' in shape:
        headers[2] = '<b>  전단상수<br>Ib/Q [mm²]</b>'
    if '합판' not in shape:
        headers[1] = '<b> 단면<br>[mm]</b>'
        data[3] = f'<b>{S/1e3:,.1f}×10³</b>'
        data[4] = f'<b>{I/1e3:,.1f}×10³</b>'
        data[7] = f'<b>{fsa:.1f}</b>'

    if '동바리' in shape:
        headers = np.delete(headers, -1)
        data[0] = '<b>원형강관'
        headers[3] = '<b>회전반경<br> r [mm]</b>'
        data[3] = f'<b>{S:,.1f}</b>'
        headers[6] = '<b>항복강도<br><i>F<sub>y</sub></i> [MPa]</b>'
        pass

    data_dict = {header: [value] for header, value in zip(headers, data)}  # 행이 한개 일때    
    df = pd.DataFrame(data_dict)

    fs = 16;  lw = 2
    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        columnwidth=[0.8, 1.2, 1, 0.8, 1.2, 0.8, 1, 1.2],
        header=dict(
            values=list(df.columns),
            align=['center'],
            height=10,
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            align=['center']*1,
            height=25,
            prefix=None,
            suffix=None,
            font=dict(size=fs, color='black', family=fn),  # 글꼴 변경
            fill=dict(color=['silver', 'white']),  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ),
    )],
    )    
    fig.update_layout(width=900, height=100, margin=dict(l=l_margin, r=0, t=1, b=0))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)
    

def Interval(fn, d, d1, d2):
    headers = [
        '<b>휨응력 검토</b>',
        '<b>상대변형 검토</b>',
        '<b>절대변형 검토</b>',
        ]
    data = [
        f'<b>{d:,.1f} mm</b>',
        f'<b>{d1:,.1f} mm</b>',
        f'<b>{d2:,.1f} mm</b>',
        ]
    data_dict = {header: [value] for header, value in zip(headers, data)}  # 행이 한개 일때    
    df = pd.DataFrame(data_dict)

    color = ['black','black','black']
    n = [d, d1, d2];  min_index = n.index(min(n));  color[min_index] = 'orange'
    fs = 16;  lw = 2
    fig = go.Figure(data=[go.Table(
        # columnorder=[1,2,3],
        # columnwidth=[1, 1, 1, 1, 1.3, 1, 1, 1.3],
        header=dict(
            values=list(df.columns),
            align=['center'],
            height=10,
            font=dict(size=fs, color=['black','black','black'], family=fn),  # 글꼴 변경
            fill_color=['silver'],  #'darkgray'
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            align=['center']*1,
            height=25,
            prefix=None,
            suffix=None,
            font=dict(size=fs, color=color, family=fn),  # 글꼴 변경
            fill=dict(color=['white']),  # 셀 배경색 변경
            line=dict(color='black', width=lw),   # 셀 경계색, 두께
            format=[None, None]  # '나이' 열의 데이터를 실수 형태로 변환하여 출력  '.2f'
        ),
    )],
    )    
    fig.update_layout(width=600, height=80, margin=dict(l=65, r=0, t=1, b=0))  # 테이블 여백 제거  # 표의 크기 지정
    st.plotly_chart(fig)

