from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets')

fs = [28, 24, 20, 16];  width_side = 500

style_sidebar = {
    "position": "fixed",                  # 요소의 위치를 상대적이 아닌 고정된 위치로 설정
    "top": "20px",                       # 상단에서의 위치를 100 픽셀로 설정
    "left": "10px",                       # 좌측에서의 위치를 10 픽셀로 설정
    "bottom": "10px",                      # 하단에서의 위치를 0 픽셀로 설정
    "width": f"{width_side}px",                     # 너비를 32rem으로 설정
    "padding": "10px",               #  padding, margin 속성은 top, right, bottom, left 값을 순서
    # "margin": "10px",                    # 바깥쪽 여백을 모든 방향에 100 픽셀로 설정
    "background-color": "#f8f9fa",        # 배경색을 설정
    "border": "2px solid #dee2e6",        # 2픽셀 두께의 실선 테두리 설정
    "border-radius": "0.25rem",           # 테두리 반경 (둥근 모서리)을 0.25rem으로 설정
    # "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",  # 박스 그림자 추가
    "font-family": "'Roboto', sans-serif",         # 글꼴 변경
    # "color": "red",                   # 글자색을 설정
    'font-weight':'bold',
    'font-size':f'{fs[3]}px',
    "overflow-y": "auto",  # 스크롤 기능 추가
}
style = {
    "color": 'black',
    'font-size':f'{fs[3]}px',
    "font-weight": "bold",
    'margin-top':'0px',
    'padding-left':'0px',
}
style_center = {
    "display": "flex",
    "justify-content": "center",
    "align-items": "center",
    "width": "100%",
}
style_input = {
    "width": "100%",
    'font-weight': 'bold',
    'background-color': 'linen',
    'color': 'black',
    "border": "1px solid gray",
    'padding': '5px'
}

class In:
    pass
In.title = {'id':'title'}
In.height = {'id':'height', 'v':9500}
In.slab_t = {'id':'slab_t', 'v':350}
In.beam_w = {'id':'beam_w', 'v':500}
In.beam_h = {'id':'beam_h', 'v':900}

header = html.P("[Information : 입력값]", style={**style, **style_center, **{'color':'blue', 'font-size':f'{fs[1]}px'}})    
Title = html.Div([
    dbc.Label("✤ 공사명", html_for=In.title['id'], style={'font-size':f'{fs[2]}px'}),
    dbc.Input(type="text", placeholder='공사명을 입력하세요', id=In.title['id'], style={**style_input, **{'margin-bottom':'20px'}},), ])

Type = html.Div([html.P('✤ 검토 유형', style={**style, **{'font-size':f'{fs[2]}px'}}),
    dbc.RadioItems(id="type",        
        options=[
            {"label": "슬래브", "value": 'slab',},
            {"label": "보하부", "value": 'beam',},
            {"label": "기타(?)", "value": 'etc', 'disabled':True}, ], 
        value='slab', inline=True,  # 가로 배치
        label_style={'color':'gray'}, label_checked_style={'color':'black'},
        input_style={'border':'5px solid gray'}, input_checked_style={'background-color':'blue', },
        style={**style_input, **{'display':'flex','justify-content':'space-between','align-items':'center', 'margin-bottom':'20px', 'padding-left': '20px', 'padding-right': '20px',}}, ), ])

def Type_fcn(value):
    if 'slab' in value:
        text = '슬래브';  id = In.slab_t['id'];  v = In.slab_t['v'];  t1 = '두께';  input2 = None
    else:
        text = '보하부';  id = In.beam_w['id'];  v = In.beam_w['v'];  t1 = '보의 폭'
        id2 = In.beam_h['id'];  v2 = In.beam_h['v'];  t2 = '보의 높이'
        input2 = dbc.Col([
            dbc.Label(f"{t2} [mm]", html_for=id2),
            dbc.Input(type="number", value=v2, step=10, id=id2, style=style_input,), ], width=4)
    
    input1 = dbc.Col([
        dbc.Label(f"{t1} [mm]", html_for=id),
        dbc.Input(type="number", value=v, step=10, id=id, style=style_input,), ], width=4)

    Typ = html.Div([html.P(f'✦ {text}', style={**style, **{'font-size':f'{fs[2]}px'}}),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Label("층고 [mm]", html_for=In.height['id']),
                dbc.Input(type="number", value=In.height['v'], step=10, id=In.height['id'], style=style_input,), ], width=4),
            input1,
            input2,
            ], style={'margin-left': '10px', 'margin-right': '10px'}),
        ], style={"border": "2px solid gray",'padding': '5px'}, )
    
    return Typ





# def Callback():
#     Sidebar()