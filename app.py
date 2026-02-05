import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 앱 설정
import streamlit as st
from PIL import Image

# 이미지 파일 불러오기
icon_image = Image.open("images/main_icon.jpg")

# 앱 설정
st.set_page_config(
    page_title="나만의 부자 지수 측정기", # 웹 브라우저 탭(파비콘)에 뜨는 이름
    page_icon=icon_image,
    layout="centered"
)

# 로고 숨기기
hide_st_style = """
            <style>
            /* 1. 상단 헤더 영역 전체 삭제 (메뉴, 버튼 포함) */
            [data-testid="stHeader"] {display: none !important;}
            
            /* 2. 하단 푸터 (Made with Streamlit) 삭제 */
            footer {display: none !important;}
            
            /* 3. 오른쪽 하단 빨간색 Deploy 버튼 강제 삭제 */
            .stDeployButton {display: none !important;}
            
            /* 4. 상단 장식용 선 삭제 */
            [data-testid="stDecoration"] {display: none !important;}
            
            /* 5. 오른쪽 상단 메뉴 아이콘 삭제 */
            #MainMenu {display: none !important;}

            /* 6. 로고가 사라진 빈 공간만큼 위쪽 여백 줄이기 */
            .block-container {padding-top: 2rem !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 20가지 질문 리스트
questions = [
    {"cat": "현금흐름", "q": "매월 정해진 예산 안에서 지출을 통제하고 있는가?"},
    {"cat": "현금흐름", "q": "가계부(혹은 앱)를 통해 지출 내역을 매주 확인하는가?"},
    {"cat": "현금흐름", "q": "소득 대비 저축/투자 비중이 30% 이상인가?"},
    {"cat": "현금흐름", "q": "고정 지출(구독료 등)을 정기적으로 점검하고 줄이려 노력하는가?"},
    {"cat": "현금흐름", "q": "충동구매를 하는 횟수가 한 달에 1~2회 미만인가?"},
    {"cat": "자산저축", "q": "비상금(월 소득 3~6배)이 준비되어 있는가?"},
    {"cat": "자산저축", "q": "구체적인 재무 목표와 달성 기한이 있는가?"},
    {"cat": "자산저축", "q": "매달 저축액을 먼저 떼어놓고 남은 돈으로 생활하는가?"},
    {"cat": "자산저축", "q": "현재 내 순자산(자산-부채)이 얼마인지 정확히 알고 있는가?"},
    {"cat": "자산저축", "q": "주식, 채권, ISA 등 다양한 금융 상품에 관심을 갖는가?"},
    {"cat": "리스크관리", "q": "월 소득 대비 대출 원리금 상환액이 30% 이내인가?"},
    {"cat": "리스크관리", "q": "신용카드 할부나 현금서비스를 가급적 사용하지 않는가?"},
    {"cat": "리스크관리", "q": "예기치 못한 사고에 대비한 필수 보험이 있는가?"},
    {"cat": "리스크관리", "q": "나의 신용점수를 정기적으로 확인하고 관리하는가?"},
    {"cat": "리스크관리", "q": "대출 시 이율과 상환 조건을 꼼꼼히 비교하는가?"},
    {"cat": "금융지능", "q": "퇴직연금이나 개인연금 등 노후 준비를 시작했는가?"},
    {"cat": "금융지능", "q": "경제 뉴스나 금융 관련 서적을 정기적으로 접하는가?"},
    {"cat": "금융지능", "q": "연말정산이나 세액공제 혜택을 극대화하고 있는가?"},
    {"cat": "금융지능", "q": "사기성 투자나 고수익 유혹에 흔들리지 않는가?"},
    {"cat": "금융지능", "q": "주변과 비교하기보다 나의 재무 계획에 집중하는가?"}
]

# st.title("💰 나만의 부자 지수 측정기")

col1, col2 = st.columns([1, 5]) # 왼쪽(아이콘)과 오른쪽(제목) 비율

with col1:
    # 탭 아이콘과 똑같은 이미지를 본문에도 크게 넣습니다
    st.image(icon_image, width=80) 

with col2:
    st.title("나만의 부자 지수 측정기")

if st.session_state.step < len(questions):
    progress = (st.session_state.step + 1) / len(questions)
    st.progress(progress)
    st.subheader(f"질문 {st.session_state.step + 1} / 20")
    
    current_q = questions[st.session_state.step]
    st.info(f"[{current_q['cat']}] {current_q['q']}")
    
    score = st.radio(
        "본인의 상태를 선택하세요:",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {1:"전혀 아니다", 2:"아니다", 3:"보통이다", 4:"그렇다", 5:"매우 그렇다"}[x],
        horizontal=True,
        key=f"q_{st.session_state.step}"
    )
    
    if st.button("다음 질문으로"):
        st.session_state.answers.append(score)
        st.session_state.step += 1
        st.rerun()
else:
    total_score = sum(st.session_state.answers)
    
    # 영역별 점수 계산 (5문항씩)
    cat_scores = [
        sum(st.session_state.answers[0:5]),   # 현금흐름
        sum(st.session_state.answers[5:10]),  # 자산저축
        sum(st.session_state.answers[10:15]), # 리스크관리
        sum(st.session_state.answers[15:20])  # 금융지능
    ]
    categories = ["현금흐름", "자산저축", "리스크관리", "금융지능"]

    st.success("👍 모든 진단이 완료되었습니다!")
    
    # 등급 판정 로직
    if total_score >= 81:
        grade, color, msg = "재무 골드 등급", "green", "😄전문가 수준의 관리능력입니다! 현재를 유지하세요."
    elif total_score >= 61:
        grade, color, msg = "재무 실버 등급", "blue", "😳양호하지만 새는 돈이 있을 수 있습니다. 보완이 필요해요."
    elif total_score >= 41:
        grade, color, msg = "재무 주의 등급", "orange", "😢지출 통제가 시급합니다. 비상금부터 챙기세요!"
    else:
        grade, color, msg = "재무 위험 등급", "red", "😭즉각적인 재무 구조조정이 필요합니다!"

    # 결과 대시보드
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"### 결과: :{color}[{grade}]")
        st.metric("종합 점수", f"{total_score}점")
        st.info(msg)
    
    with col2:
        # 방사형 그래프 추가
        fig = go.Figure(data=go.Scatterpolar(
            r=cat_scores + [cat_scores[0]],
            theta=categories + [categories[0]],
            fill='toself',
            # --- 여기서부터 색상 설정 추가 ---
            line=dict(color='#FFD700', width=3), # 선 색상을 황금색(Gold)으로!
            fillcolor='rgba(255, 215, 0, 0.4)',  # 안쪽 채우기 색상을 투명한 황금색으로!
        # ------------------------------
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 25])), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    if st.button("다시 테스트하기"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.rerun()