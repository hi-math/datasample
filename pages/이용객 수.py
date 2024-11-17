import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib import font_manager, rc

# 폰트 설정
#font_path = "NanumGothic.ttf"  # Windows의 일반적인 경로
#font_manager.fontManager.addfont(font_path)
#rc('font', family='NanumGothic')

# 1. CSV 파일 불러오기
data = pd.read_csv("승객종합데이터.csv")

# 2. '사용일자' 열을 날짜 형식으로 변환
data['사용일자'] = pd.to_datetime(data['사용일자'], format='%Y%m%d')

# 3. '노선명' 열에서 특정 노선만 남기고 나머지 삭제
valid_lines = ['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선', '9호선 2~3단계']
data = data[data['노선명'].isin(valid_lines)]

# 4. '노선명'에서 '9호선 2~3단계'를 '9호선'으로 변경
data['노선명'] = data['노선명'].replace('9호선 2~3단계', '9호선')

# 세션 상태 초기화
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False  # 그래프 조회 상태
if "sogam" not in st.session_state:
    st.session_state["sogam"] = ""  # 소감 내용 초기화
if "selected_lines" not in st.session_state:
    st.session_state["selected_lines"] = []  # 선택된 노선 초기화
if "selected_updown" not in st.session_state:
    st.session_state["selected_updown"] = []  # 선택된 승차/하차 옵션 초기화

# 타이틀
st.title("지하철 이용 승객 수 알아보기")

# 1. 그래프 조회 폼
with st.form("input"):
    number = st.multiselect("노선명", ['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선'])
    updown = st.multiselect("승차/하차 승객", ['승차총승객수', '하차총승객수'])
    submitted = st.form_submit_button("조회")

    if submitted:
        if number and updown:
            st.session_state["submitted"] = True
            st.session_state["selected_lines"] = number  # 선택된 노선 저장
            st.session_state["selected_updown"] = updown  # 선택된 승차/하차 옵션 저장
        else:
            st.warning("노선명과 승차/하차 승객 옵션을 선택해주세요.")

# 2. 그래프 표시
if st.session_state["submitted"]:
    number = st.session_state["selected_lines"]
    updown = st.session_state["selected_updown"]

    for line in number:
        line_data = data[data['노선명'] == line]  # 특정 호선 필터링
        aggregated_data = line_data.groupby('사용일자')[updown].sum().reset_index()  # 날짜별 승객 수 합산

        # 그래프 생성
        plt.figure(figsize=(14, 7))
        for col in updown:
            plt.plot(aggregated_data['사용일자'], aggregated_data[col], label=f'{line} - {col}')

        # 그래프 설정
        plt.title(f"{line}에서의 총 이용 승객 정보")
        plt.xlabel('날짜')
        plt.ylabel('승객 수')
        plt.xticks(aggregated_data['사용일자'][::15], rotation=45)
        plt.legend()
        plt.tight_layout()
        st.pyplot(plt.gcf())

# 3. 소감 입력 폼
if st.session_state["submitted"]:
    with st.form(key="sogam_form"):
        sogam_input = st.text_input(
            "그래프를 보고 느낀 점을 간단히 작성해보세요.",
            value=st.session_state["sogam"]
        )
        submitted2 = st.form_submit_button("제출")

        if submitted2:
            if not sogam_input.strip():  # 공백 입력 방지
                st.warning("소감을 입력해주세요.")
            else:
                st.session_state["sogam"] = sogam_input  # 세션 상태 업데이트
                st.success("제출되었습니다!")
