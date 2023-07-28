import streamlit as st

# 라디오 버튼 스타일 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def radio(color, width):    
    radio_style = f""" <style>
        div.row-widget.stRadio > div[role='radiogroup'] > label input[type=radio] {{
            display: none;   /*기본 스타일 옵션 제거, 없어도 될거 같은데?? */
        }}
        div.row-widget.stRadio > div[role='radiogroup'] {{
            display: flex;
            /* justify-content: space-between; */
            width: 100%;
            flex-direction: row;
            font-weight: bold !important;
        }}
        div.row-widget.stRadio > div[role='radiogroup'] > label {{
            display: inline-flex;
            justify-content: center;
            align-items: center;
            font-weight: bold !important;
            padding: 5px;
            padding-left: 10px;
            padding-right: 15px;
            margin-right: 3%;
            background-color: {color};
            border: 1px solid black;
            border-radius: 100px;    
            width: {width};       /* 추가: 라벨의 너비를 100px로 설정 */
            height: 100%;       /* 추가: 라벨의 높이를 50px로 설정 */
        }}
        div.row-widget.stRadio > div[role='radiogroup'] > label:hover {{
            font-weight: bold !important;
            background-color: lightblue;    
        }}
    </style> """
    st.markdown(radio_style, unsafe_allow_html=True)
# 라디오 버튼 스타일 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@