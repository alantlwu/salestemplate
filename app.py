import streamlit as st
import pyperclip
import datetime

# 定義公版選項與對應欄位
templates = {
    "Lead/PDC": ["Model", "現有車款", "用車習慣", "充電方式", "比較車款", "吸引及在乎之處", "客戶資料", "備註"],
    "Trade-in": ["廠牌車型", "年份", "里程", "所在地", "備註"],
    "Order": ["訂購人", "付款方式", "掛牌人", "充電座安裝", "車輛換購", "期望交付期間", "交車地點", "推薦碼", "備註"],
    "TD Note": ["目標 Model", "換購車動機", "考慮比較的競品", "疑慮(不購車的原因)", "購買時間", "決策者/ 使用人",
                "充電安裝", "平常開車的用途", "目前使用車輛", "是否Trade in"],
    "PDC SMS": []  # 獨立選項，不需要輸入欄位
}

# 中文星期對應
day_mapping = {"Monday": "週一", "Tuesday": "週二", "Wednesday": "週三", "Thursday": "週四", "Friday": "週五",
               "Saturday": "週六", "Sunday": "週日"}

st.title("公版填寫工具")

# 選擇公版
selected_template = st.selectbox("選擇公版:", list(templates.keys()))

# 如果選擇 PDC SMS，顯示固定格式文字
if selected_template == "PDC SMS":
    today = datetime.date.today()
    selected_date = st.date_input("選擇試駕日期", today)
    selected_time = st.selectbox("選擇試駕時間", [f"{hour}:00" for hour in range(11, 21)])
    weekday_chinese = day_mapping[selected_date.strftime('%A')]

    sms_text = f"""
【Tesla 試駕提醒】

親愛的貴賓您好，感謝您參與本次
以下為活動當天詳細資訊及注意事項：

| 試駕時間： {selected_date.strftime('%m/%d')} ({weekday_chinese}) {selected_time}
| 報到地點：Tesla竹北體驗店
  (遠東百貨竹北店1F／莊敬二街與光明六路轉角處)
| 若開車前來可直接將您的愛車停至遠百停車場後再至1F展間報到
| 請您準時抵達並攜帶您的台灣駕照，預約將為您保留10分鐘
| 如需修改/取消試駕時間請您務必在一天前回撥告知

================================
| 客服: 0809-001-766
    """

    st.text_area("試駕提醒內容:", sms_text, height=200)
    if st.button("複製"):
        pyperclip.copy(sms_text)
        st.success("已複製到剪貼簿！")
else:
    # 初始化 session_state
    if "data" not in st.session_state or "selected_template" not in st.session_state:
        st.session_state.selected_template = selected_template  # 記錄當前選擇的公版
        st.session_state.data = {field: "" for field in templates[selected_template]}

    # 如果更換公版，則重新初始化輸入欄位
    if selected_template != st.session_state.selected_template:
        st.session_state.selected_template = selected_template
        st.session_state.data = {field: "" for field in templates[selected_template]}
        st.rerun()  # 立即刷新

    # 建立輸入欄位
    for field in templates[selected_template]:
        st.session_state.data[field] = st.text_input(field, st.session_state.data.get(field, ""))

    # 整理輸出內容
    formatted_text = "\n".join([f"{key}: {value}" for key, value in st.session_state.data.items() if value])
    st.text_area("整理好的文字:", formatted_text, height=150)

    # 一鍵複製
    if st.button("複製"):
        pyperclip.copy(formatted_text)
        st.success("已複製到剪貼簿！")

    # **完全清除所有輸入內容並重新載入**
    if st.button("清除重填"):
        del st.session_state.data  # 移除 `data` 鍵，讓它重新初始化
        st.rerun()  # 重新渲染頁面
