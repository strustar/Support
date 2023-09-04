from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import re
import pandas as pd
from dash_side import Type_fcn, header, Title, Type, fs, In, style_sidebar, width_side

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets')
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

style = {} #{"border": "1px solid black", 'width':'100%', 'backgroundColor':'yellow', "textDecoration": "underline", }
label_style = {
    "color": 'gray',
    'font-size':f'{fs[2]}px',
    "font-weight": "bold",    
    'textAlign':'center',
    # 'margin-top':'0px',
    # 'padding-left':'0px',
}
active_label_style={**label_style, **{'color':'blue', 'font-size':f'{fs[1]}px', "backgroundColor": "deepskyblue", "borderRadius": "50px"}}

tab_style={"backgroundColor": "lightgray", "border": "3px dashed lightblue", "borderRadius": "50px", 'width':'20%', 'marginRight':'50px'}
active_tab_style = {**tab_style, **{"border": "3px dashed blue"}}

common_style = {
    "label_style": label_style,
    "active_label_style": active_label_style,
    "tab_style": tab_style,
    "active_tab_style": active_tab_style,
    "labelClassName": "custom-tab",  # 마우스 올려놓았을때, 밑줄, 파란색
    }

blank = '\u2002' #빈칸
tabs = dbc.Tabs(children=[
        dbc.Tab([html.P('tttt'), html.Div(id='t1')], label=f"Ⅰ. 일반사항 📝", tab_id='tab1', **common_style),                 
        dbc.Tab(label="Ⅱ. 구조검토 💻", tab_id='tab2', **common_style), 
        dbc.Tab(label="Ⅲ. 요약 ⭕✔️", tab_id='tab3', **common_style), 
        dbc.Tab(label="[참고 사항] ✍️📊", tab_id='tab4', **common_style), 
        ], id='tabs', active_tab='tab1',  style=style, )


style_main = style_sidebar.copy()
style_main.update({'left':f'{width_side + 50}px', 'width':'1200px', 'background':'white'})
main_content = dbc.Container(id="main-content")

Typ = html.Div(id='dummy1')
@app.callback(
    Output("dummy1", "children"),
    [Input("type", "value")], )
def display_selected_value(value):    
    return Type_fcn(value)    

sidebar = dbc.Container( [header, Title, Type, Typ], style=style_sidebar,)
app.layout = dbc.Container([
    html.Div([
        dbc.Row([
            dbc.Col(sidebar),
            dbc.Col([main_content, tabs], style=style_main),
            ], align="top", ), 
        ],),
        html.Div(id='dummy12', style={'display': 'none'}),
    ], fluid=True, )

# @app.callback(
#     Output("t1", "children"),
#     [Input(In.height['id'], "value"), Input(In.slab_t['id'], "value")],
# )
# def update_output(h, t):
#     In.height['v'] = h
#     In.slab_t['v'] = t
#     print(In.height, In.slab_t)
#     return html.Div([f"Input 1: {h}, Input 2: {t}"])
#     # data = {In.s_h[0]:h, In.s_t[0]:t}    
#     # with open("In.json", "w") as f:
#     #     json.dump(data, f)
#     # return html.Div([]) #, print(height, thickness)


# @app.callback(
#     Output("main-content", "children"),
#     [Input("tabs", "active_tab")],
# )
# def update_output(tab):
#     print(tab)
#     if tab == "tab1":
#         return html.Div(id="t1", children="Tab 1 is selected.")
#     elif tab == "tab2":
#         return html.Div("Tab 2 is selected.")
#     elif tab == "tab3":
#         return html.Div("Tab 3 is selected.")
#     else:
#         return None

# # JSON 파일 읽기
# with open("data.json", "r") as f:
#     s = json.load(f)

# def flexible_function(a, b, *args, **kwargs):
#     print("a:", a)
#     print("b:", b)
#     print("args:", args[0])
#     for key, value in kwargs.items():
#         print(f"{key}: {value}")

# flexible_function(111, 2, s_h, 4, 5, s_t, y=20)

# print(fs)

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=True, dev_tools_hot_reload=True)


# hupper -m support{파일이름}  # 에러가 발생해도 자동 실행 !!! 


