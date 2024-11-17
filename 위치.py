import streamlit as st
import pandas as pd

data = pd.read_csv("역사좌표.csv")

st.title('1호선~9호선 역의 위치')

st.image('노선도.png')
st.divider()
st.text(" ")
st.write("아쉽게도, 확인할 수 있는 역의 범위가 서울에 한정되어 있습니다.")
st.write("수집한 데이터의 한계입니다...")

line_colors = {
    1: "#0032A0",
    2: "#00B140",
    3: "#FC4C02",
    4: "#00A9E0",
    5: "#A05EB5",
    6: "#A9431E",
    7: "#67823A",
    8: "#E31C79",
    9: "#8C8279",
}
data["color"] = data["호선"].map(line_colors)


st.map(data, latitude="위도",
       longitude="경도",
       size=10,
       color="color")
