import streamlit as st
from datetime import datetime

# 定義公版選項與對應欄位
templates = {
    "Lead/PDC": ["Model", "現有車款", "用車習慣", "充電方式", "比較車款", "吸引及在乎之處", "客戶資料", "備註"],
    "Trade-in": ["廠牌車型", "年份", "里程", "所在地", "備註"],
    "Order": ["訂購人", "付款方式", "掛牌人", "充電座安裝", "車輛換購", "期望交付期間", "交車地點", "推薦碼", "備註"],
    "TD Note": ["目標 Model", "換購車動機", "考慮比較的競品", "疑慮(不購車的原因)", "購買時間", "決策者/ 使用人",
                "充電安裝", "平常開車的用途", "目前使用車輛", "是否Trade in"],
    "PDC SMS": []  # PDC SMS 需要固定格式
}

st.title("公版填寫工具")

# 選擇公版
selected_template = st.selectbox("選擇公版:", list(templates.keys()))

if selected_template == "PDC SMS":
    # 讓用戶選擇日期與時間
    selected_date = st.date_input("選擇試駕日期", datetime.today())
    selected_time = st.selectbox("選擇試駕時間", [f"{hour}:00" for hour in range(11, 21)])

    # 轉換星期格式
    weekdays = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
    weekday_str = weekdays[selected_date.weekday()]

    # 固定公版文字
    formatted_text = f"""
    【Tesla 試駕提醒】

    親愛的貴賓您好，感謝您參與本次

    以下為活動當天詳細資訊及注意事項：

    | 試駕時間： {selected_date.strftime('%-m/%-d')} ({weekday_str}) {selected_time}
    | 報到地點：Tesla竹北體驗店
    | (遠東百貨竹北店1F／莊敬二街與光明六路轉角處)
    | 若開車前來可直接將您的愛車停至遠百停車場後再至1F展間報到
    | 請您準時抵達並攜帶您的台灣駕照，預約將為您保留10分鐘
    | 如需修改/取消試駕時間請您務必在一天前回撥告知

    =================================

    | 客服: 0809-001-766
    """
else:
    # 初始化 session_state
    if "data" not in st.session_state or st.session_state.selected_template != selected_template:
        st.session_state.data = {field: "" for field in templates[selected_template]}
        st.session_state.selected_template = selected_template

    # 建立輸入欄位
    for field in templates[selected_template]:
        st.session_state.data[field] = st.text_input(field, st.session_state.data.get(field, ""))

    # 整理輸出內容
    formatted_text = "\n".join([f"{key}: {value}" for key, value in st.session_state.data.items() if value])

# 顯示輸出內容
text_area = st.text_area("整理好的文字:", formatted_text, height=150)

# 一鍵複製 (使用 JavaScript)
st.markdown(
    f"""
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText(`{text_area}`).then(() => {{
            alert('已複製到剪貼簿！');
        }});
    }}
    </script>
    <button onclick="copyToClipboard()">複製</button>
    """,
    unsafe_allow_html=True
)

# 清除所有輸入內容並重新渲染
if st.button("清除重填"):
    if selected_template == "PDC SMS":
        st.rerun()
    else:
        for key in st.session_state.data.keys():
            st.session_state.data[key] = ""
        st.rerun()
