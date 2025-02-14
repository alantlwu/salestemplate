import streamlit as st
import datetime
import streamlit.components.v1 as components

# 定義公版選項與對應欄位
templates = {
    "Lead/PDC": ["Model", "現有車款", "用車習慣", "充電方式", "比較車款", "吸引及在乎之處", "客戶資料", "備註"],
    "Trade-in": ["廠牌車型", "年份", "里程", "所在地", "備註"],
    "Order": ["訂購人", "付款方式", "掛牌人", "充電座安裝", "車輛換購", "期望交付期間", "交車地點", "推薦碼", "備註"],
    "TD Note": ["目標 Model", "換購車動機", "考慮比較的競品", "疑慮(不購車的原因)", "購買時間", "決策者/ 使用人", "充電安裝", "平常開車的用途", "目前使用車輛", "是否Trade in"],
    "PDC SMS": []
}

st.title("🚗 Tesla 公版填寫工具")

# 選擇公版
selected_template = st.selectbox("📌 選擇公版:", list(templates.keys()))

# 初始化 session_state
if "data" not in st.session_state or "template" not in st.session_state or st.session_state.template != selected_template:
    st.session_state.template = selected_template
    st.session_state.data = {field: "" for field in templates[selected_template]}
    st.session_state.selected_date = datetime.date.today()  # 預設今天
    st.session_state.selected_time = "12:00"  # 預設時間

if selected_template == "PDC SMS":
    # 日期選擇器
    selected_date = st.date_input("📅 選擇試駕日期", st.session_state.selected_date)
    st.session_state.selected_date = selected_date

    # 時間選擇器（固定 11:00 - 20:00）
    time_options = [f"{hour}:00" for hour in range(11, 21)]
    selected_time = st.selectbox("🕒 選擇試駕時間", time_options, index=time_options.index(st.session_state.selected_time))
    st.session_state.selected_time = selected_time

    # 轉換星期格式
    weekday_map = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
    formatted_date = f"{selected_date.month}/{selected_date.day} ({weekday_map[selected_date.weekday()]}) {selected_time}"

    # PDC SMS 公版內容
    formatted_text = f"""【Tesla 試駕提醒】

親愛的貴賓您好，感謝您參與本次

以下為活動當天詳細資訊及注意事項：

| 試駕時間： {formatted_date}
| 報到地點：Tesla竹北體驗店
  (遠東百貨竹北店1F／莊敬二街與光明六路轉角處)

| 若開車前來可直接將您的愛車停至遠百停車場後再至1F展間報到
| 請您準時抵達並攜帶您的台灣駕照，預約將為您保留10分鐘
| 如需修改/取消試駕時間請您務必在一天前回撥告知

================================

| 客服: 0809-001-766
"""

else:
    # 建立輸入欄位
    for field in templates[selected_template]:
        st.session_state.data[field] = st.text_input(field, st.session_state.data.get(field, ""))

    # 整理輸出內容
    formatted_text = "\n".join([f"{key}: {value}" for key, value in st.session_state.data.items() if value])

# 顯示輸出區域
text_area = st.text_area("📋 整理好的文字:", formatted_text, height=200)

# **JavaScript 複製功能**
copy_script = """
<script>
function copyToClipboard() {
    var textArea = document.getElementById("copyTarget");
    navigator.clipboard.writeText(textArea.value).then(() => {
        alert("✅ 內容已成功複製到剪貼簿！");
    }).catch(err => {
        alert("❌ 複製失敗，請手動複製！");
    });
}
</script>
"""

# **插入 JavaScript 按鈕**
components.html(
    f"""
    {copy_script}
    <textarea id="copyTarget" style="display:none;">{formatted_text}</textarea>
    <button onclick="copyToClipboard()" style="padding:10px 20px; font-size:16px; border-radius:8px; background-color:#007bff; color:white; border:none; cursor:pointer;">
        📋 一鍵複製
    </button>
    """,
    height=50
)

# 清除所有輸入內容並重新渲染
if st.button("🗑️ 清除重填"):
    for key in st.session_state.data.keys():
        st.session_state.data[key] = ""  # 清空每個欄位
    st.session_state.selected_date = datetime.date.today()  # 重設日期
    st.session_state.selected_time = "12:00"  # 重設時間
    st.rerun()  # 重新渲染頁面
