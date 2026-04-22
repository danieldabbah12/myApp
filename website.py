import streamlit as st

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="מדריך Streamlit",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700&family=Fira+Code:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Rubik', sans-serif;
    direction: rtl;
}

h1, h2, h3 {
    font-family: 'Rubik', sans-serif;
    font-weight: 700;
}

code, pre {
    font-family: 'Fira Code', monospace !important;
    direction: ltr;
    text-align: left;
}

.section-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin: 1.5rem 0 1rem 0;
    font-size: 1.3rem;
    font-weight: 700;
    border-left: 5px solid #e94560;
}

.tip-box {
    background: #e8f4fd;
    border-right: 4px solid #2196F3;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    color: #1a1a2e;
}

.output-label {
    font-size: 0.78rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.8rem;
    margin-bottom: 0.2rem;
}

.stCodeBlock {
    direction: ltr;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}

[data-testid="stSidebar"] * {
    color: #eee !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 מדריך Streamlit")
    st.markdown("---")
    section = st.radio(
        "בחר נושא:",
        [
            "🏠 מבוא",
            "📝 טקסט וכותרות",
            "📊 גרפים ונתונים",
            "🎛️ רכיבי קלט",
            "📐 פריסת עמוד",
            "🔄 מצב ולוגיקה",
            "📁 קבצים ומדיה",
            "🎨 עיצוב מתקדם",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**📌 טיפ:** כל דוגמה כאן היא קוד אמיתי שרץ עכשיו!")

# ─── Helper function ───────────────────────────────────────────────────────────
def show_code(code: str):
    """Renders a left-to-right code block."""
    st.code(code, language="python")


# ══════════════════════════════════════════════════════════════════════════════
# 🏠 מבוא
# ══════════════════════════════════════════════════════════════════════════════
if section == "🏠 מבוא":
    st.title("🚀 ברוכים הבאים למדריך Streamlit")
    st.subheader("בניית אפליקציות Web באמצעות Python בלבד!")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🤔 מה זה Streamlit?")
        st.markdown("""
        **Streamlit** היא ספריית Python שמאפשרת לבנות אפליקציות Web אינטראקטיביות
        בכמה שורות קוד — ללא HTML, CSS, או JavaScript.

        מתאים במיוחד ל:
        - 📊 דשבורדים ויזואליים
        - 🤖 הצגת מודלי AI / ML
        - 📈 ניתוח נתונים
        - 🛠️ כלים פנימיים
        """)
    with col2:
        st.markdown("### ⚡ התקנה והפעלה")
        show_code("""# התקנה (פעם אחת)
pip install streamlit

# יצירת קובץ
# app.py

# הפעלה
streamlit run app.py""")

    st.markdown("---")
    st.markdown("### 🗂️ מבנה קובץ בסיסי")
    show_code("""import streamlit as st

# כותרת ראשית
st.title("האפליקציה שלי")

# כותרת משנה
st.subheader("ברוכים הבאים!")

# פסקת טקסט
st.write("שלום עולם!")

# כל שינוי בקוד → הדפדפן מתעדכן אוטומטית ✨""")

    st.markdown('<div class="tip-box">💡 <b>טיפ:</b> כל פעם שמשתמש מקיש על כפתור או משנה ערך — Streamlit מריצה את הקובץ מחדש מלמעלה למטה.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 📝 טקסט וכותרות
# ══════════════════════════════════════════════════════════════════════════════
elif section == "📝 טקסט וכותרות":
    st.markdown('<div class="section-header">📝 טקסט וכותרות</div>', unsafe_allow_html=True)

    # st.title
    st.markdown("#### `st.title()` — כותרת ראשית")
    show_code('st.title("כותרת ראשית")')
    st.title("כותרת ראשית")

    st.markdown("---")

    # st.header / subheader
    st.markdown("#### `st.header()` / `st.subheader()`")
    show_code("""st.header("כותרת גדולה")
st.subheader("כותרת בינונית")""")
    st.header("כותרת גדולה")
    st.subheader("כותרת בינונית")

    st.markdown("---")

    # st.write
    st.markdown("#### `st.write()` — הכי גמיש!")
    show_code("""st.write("טקסט רגיל")
st.write("תומך **bold** ו-*italic* בסגנון Markdown")
st.write(42)          # מספרים
st.write([1, 2, 3])   # רשימות
st.write({"a": 1})    # מילונים""")
    st.write("טקסט רגיל")
    st.write("תומך **bold** ו-*italic* בסגנון Markdown")
    st.write(42)
    st.write([1, 2, 3])

    st.markdown("---")

    # st.markdown
    st.markdown("#### `st.markdown()` — Markdown מלא")
    show_code("""st.markdown(\"\"\"
## כותרת
- פריט 1
- פריט 2

> ציטוט מעניין

`קוד inline`
\"\"\")""")
    st.markdown("""
## כותרת
- פריט 1
- פריט 2

> ציטוט מעניין

`קוד inline`
""")

    st.markdown("---")

    # Alerts
    st.markdown("#### הודעות צבעוניות")
    show_code("""st.success("✅ הפעולה הצליחה!")
st.warning("⚠️ שים לב לנושא הזה")
st.error("❌ שגיאה! משהו השתבש")
st.info("ℹ️ מידע כללי")""")
    st.success("✅ הפעולה הצליחה!")
    st.warning("⚠️ שים לב לנושא הזה")
    st.error("❌ שגיאה! משהו השתבש")
    st.info("ℹ️ מידע כללי")

    st.markdown("---")

    # st.code
    st.markdown("#### `st.code()` — הצגת קוד")
    show_code("""st.code(\"\"\"
def hello(name):
    return f"שלום, {name}!"
\"\"\", language="python")""")


# ══════════════════════════════════════════════════════════════════════════════
# 📊 גרפים ונתונים
# ══════════════════════════════════════════════════════════════════════════════
elif section == "📊 גרפים ונתונים":
    import pandas as pd
    import numpy as np

    st.markdown('<div class="section-header">📊 גרפים ונתונים</div>', unsafe_allow_html=True)

    # DataFrame
    st.markdown("#### `st.dataframe()` — טבלה אינטראקטיבית")
    show_code("""import pandas as pd
import numpy as np

df = pd.DataFrame({
    "שם": ["אלי", "מיה", "דן", "נועה"],
    "ציון": [88, 95, 72, 91],
    "גיל":  [22, 24, 21, 23],
})
st.dataframe(df)""")
    df = pd.DataFrame({
        "שם": ["אלי", "מיה", "דן", "נועה"],
        "ציון": [88, 95, 72, 91],
        "גיל":  [22, 24, 21, 23],
    })
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # st.table
    st.markdown("#### `st.table()` — טבלה סטטית")
    show_code("st.table(df)")
    st.table(df)

    st.markdown("---")

    # Line chart
    st.markdown("#### `st.line_chart()` — גרף קו")
    show_code("""data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["קו א", "קו ב", "קו ג"]
)
st.line_chart(data)""")
    data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["קו א", "קו ב", "קו ג"]
    )
    st.line_chart(data)

    st.markdown("---")

    # Bar chart
    st.markdown("#### `st.bar_chart()` — גרף עמודות")
    show_code("""bar_data = pd.DataFrame(
    {"מכירות": [300, 450, 200, 600, 380]},
    index=["ינואר","פברואר","מרץ","אפריל","מאי"]
)
st.bar_chart(bar_data)""")
    bar_data = pd.DataFrame(
        {"מכירות": [300, 450, 200, 600, 380]},
        index=["ינואר","פברואר","מרץ","אפריל","מאי"]
    )
    st.bar_chart(bar_data)

    st.markdown("---")

    # Metrics
    st.markdown("#### `st.metric()` — כרטיסי מדד")
    show_code("""col1, col2, col3 = st.columns(3)
col1.metric("טמפרטורה", "25°C", "+2°C")
col2.metric("משתמשים", "1,284", "-38")
col3.metric("הכנסה", "₪12,400", "+8%")""")
    col1, col2, col3 = st.columns(3)
    col1.metric("טמפרטורה", "25°C", "+2°C")
    col2.metric("משתמשים", "1,284", "-38")
    col3.metric("הכנסה", "₪12,400", "+8%")


# ══════════════════════════════════════════════════════════════════════════════
# 🎛️ רכיבי קלט
# ══════════════════════════════════════════════════════════════════════════════
elif section == "🎛️ רכיבי קלט":
    st.markdown('<div class="section-header">🎛️ רכיבי קלט — אינטראקטיביות!</div>', unsafe_allow_html=True)
    st.info("כל רכיב כאן חי ופעיל! נסו לשנות את הערכים 👇")

    col1, col2 = st.columns(2)

    with col1:
        # text_input
        st.markdown("#### `st.text_input()`")
        show_code('name = st.text_input("מה שמך?")\nst.write(f"שלום, {name}!")')
        name = st.text_input("מה שמך?")
        st.write(f"שלום, {name}!" if name else "הכנס שם...")

        st.markdown("---")

        # number_input
        st.markdown("#### `st.number_input()`")
        show_code('num = st.number_input("הכנס מספר", min_value=0, max_value=100, value=50)')
        num = st.number_input("הכנס מספר", min_value=0, max_value=100, value=50)
        st.write(f"הכפול שלו: {num * 2}")

        st.markdown("---")

        # slider
        st.markdown("#### `st.slider()`")
        show_code('age = st.slider("גיל", 0, 100, 25)')
        age = st.slider("גיל", 0, 100, 25)
        st.write(f"גיל שנבחר: {age}")

        st.markdown("---")

        # button
        st.markdown("#### `st.button()`")
        show_code("""if st.button("לחץ עליי!"):
    st.balloons()
    st.success("כפתור נלחץ! 🎉")""")
        if st.button("לחץ עליי!"):
            st.balloons()
            st.success("כפתור נלחץ! 🎉")

    with col2:
        # selectbox
        st.markdown("#### `st.selectbox()`")
        show_code("""color = st.selectbox(
    "בחר צבע",
    ["אדום", "ירוק", "כחול"]
)""")
        color = st.selectbox("בחר צבע", ["אדום", "ירוק", "כחול"])
        st.write(f"בחרת: {color}")

        st.markdown("---")

        # multiselect
        st.markdown("#### `st.multiselect()`")
        show_code("""fruits = st.multiselect(
    "בחר פירות",
    ["תפוח", "בננה", "ענב", "מנגו"]
)""")
        fruits = st.multiselect("בחר פירות", ["תפוח", "בננה", "ענב", "מנגו"])
        st.write(f"נבחרו: {fruits}")

        st.markdown("---")

        # checkbox
        st.markdown("#### `st.checkbox()`")
        show_code("""agree = st.checkbox("קראתי את התנאים")
if agree:
    st.success("תודה!")""")
        agree = st.checkbox("קראתי את התנאים")
        if agree:
            st.success("תודה!")

        st.markdown("---")

        # radio
        st.markdown("#### `st.radio()`")
        show_code("""plan = st.radio(
    "בחר תוכנית",
    ["חינמי", "פרו", "עסקי"]
)""")
        plan = st.radio("בחר תוכנית", ["חינמי", "פרו", "עסקי"])
        st.write(f"תוכנית: {plan}")

    st.markdown("---")

    # text_area + date_input
    st.markdown("#### `st.text_area()` + `st.date_input()`")
    show_code("""import datetime
comment = st.text_area("הערות", height=100)
date = st.date_input("תאריך", datetime.date.today())
st.write(f"תאריך: {date}, תוכן: {len(comment)} תווים")""")
    import datetime
    comment = st.text_area("הערות", height=80)
    date = st.date_input("תאריך", datetime.date.today())
    st.write(f"תאריך: {date} | תוכן: {len(comment)} תווים")


# ══════════════════════════════════════════════════════════════════════════════
# 📐 פריסת עמוד
# ══════════════════════════════════════════════════════════════════════════════
elif section == "📐 פריסת עמוד":
    st.markdown('<div class="section-header">📐 פריסת עמוד — עמודות, טאבים ועוד</div>', unsafe_allow_html=True)

    # Columns
    st.markdown("#### `st.columns()` — עמודות")
    show_code("""col1, col2, col3 = st.columns(3)

with col1:
    st.header("עמודה 1")
    st.write("תוכן ראשון")

with col2:
    st.header("עמודה 2")
    st.write("תוכן שני")

with col3:
    st.header("עמודה 3")
    st.write("תוכן שלישי")""")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**עמודה 1**")
        st.write("תוכן ראשון")
    with col2:
        st.markdown("**עמודה 2**")
        st.write("תוכן שני")
    with col3:
        st.markdown("**עמודה 3**")
        st.write("תוכן שלישי")

    st.markdown("---")

    # יחסי רוחב
    st.markdown("#### עמודות עם יחסי רוחב שונים")
    show_code("""left, right = st.columns([1, 3])  # ימין רחב פי 3
with left:
    st.image("logo.png")
with right:
    st.write("תוכן רחב...")""")
    left, right = st.columns([1, 3])
    with left:
        st.metric("רוחב", "25%")
    with right:
        st.metric("רוחב", "75%")

    st.markdown("---")

    # Tabs
    st.markdown("#### `st.tabs()` — טאבים")
    show_code("""tab1, tab2, tab3 = st.tabs(["🏠 בית", "📊 נתונים", "⚙️ הגדרות"])

with tab1:
    st.write("ברוכים הבאים!")
with tab2:
    st.write("כאן יהיו גרפים")
with tab3:
    st.write("הגדרות המערכת")""")
    tab1, tab2, tab3 = st.tabs(["🏠 בית", "📊 נתונים", "⚙️ הגדרות"])
    with tab1:
        st.write("ברוכים הבאים!")
    with tab2:
        st.write("כאן יהיו גרפים")
    with tab3:
        st.write("הגדרות המערכת")

    st.markdown("---")

    # Expander
    st.markdown("#### `st.expander()` — אקורדיון")
    show_code("""with st.expander("לחץ לפרטים נוספים"):
    st.write("תוכן מוסתר שנחשף בלחיצה!")
    st.image("diagram.png")""")
    with st.expander("לחץ לפרטים נוספים ⬇️"):
        st.write("תוכן מוסתר שנחשף בלחיצה!")
        st.info("ניתן להכניס כאן כל רכיב Streamlit")

    st.markdown("---")

    # Sidebar
    st.markdown("#### `st.sidebar` — סרגל צד")
    show_code("""with st.sidebar:
    st.title("תפריט")
    option = st.selectbox("בחר עמוד", ["בית", "אודות"])

# גם כך:
st.sidebar.write("טקסט בסרגל")""")
    st.markdown('<div class="tip-box">💡 הסרגל הצדדי במדריך זה הוא דוגמה חיה ל-<code>st.sidebar</code>!</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Container
    st.markdown("#### `st.container()` — מיכל")
    show_code("""with st.container():
    st.write("הכל בתוך המיכל")
    st.button("כפתור")

st.write("זה כבר מחוץ למיכל")""")


# ══════════════════════════════════════════════════════════════════════════════
# 🔄 מצב ולוגיקה
# ══════════════════════════════════════════════════════════════════════════════
elif section == "🔄 מצב ולוגיקה":
    st.markdown('<div class="section-header">🔄 מצב ולוגיקה — Session State ו-Cache</div>', unsafe_allow_html=True)

    st.markdown("#### `st.session_state` — שמירת מצב בין ריצות")
    st.markdown("ב-Streamlit, הקוד רץ מחדש בכל אינטראקציה. `session_state` שומר ערכים:")

    show_code("""# אתחול (רק בפעם הראשונה)
if "count" not in st.session_state:
    st.session_state.count = 0

# כפתורים לשינוי המצב
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ הוסף"):
        st.session_state.count += 1
with col2:
    if st.button("➖ הפחת"):
        st.session_state.count -= 1

st.metric("ערך נוכחי", st.session_state.count)""")

    if "count" not in st.session_state:
        st.session_state.count = 0

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ הוסף"):
            st.session_state.count += 1
    with col2:
        if st.button("➖ הפחת"):
            st.session_state.count -= 1
    st.metric("ערך נוכחי", st.session_state.count)

    st.markdown("---")

    # Forms
    st.markdown("#### `st.form()` — טופס (שליחה אחת)")
    show_code("""with st.form("my_form"):
    name = st.text_input("שם")
    age  = st.number_input("גיל", 0, 120)
    submitted = st.form_submit_button("שלח")

if submitted:
    st.success(f"קיבלנו! {name}, גיל {age}")""")

    with st.form("demo_form"):
        fname = st.text_input("שם")
        fage  = st.number_input("גיל", 0, 120, value=20)
        submitted = st.form_submit_button("שלח")
    if submitted:
        st.success(f"קיבלנו! {fname}, גיל {fage}")

    st.markdown("---")

    # Cache
    st.markdown("#### `@st.cache_data` — מטמון לחישובים כבדים")
    show_code("""import time

@st.cache_data
def heavy_computation(n):
    time.sleep(2)          # מדמה חישוב כבד
    return n * n

result = heavy_computation(42)
# ← בפעם הראשונה לוקח 2 שניות
# ← בפעמים הבאות — מיידי! ⚡""")
    st.markdown('<div class="tip-box">💡 <code>@st.cache_data</code> שומר את תוצאת הפונקציה בזיכרון. אידיאלי לקריאות API, טעינת קבצים, וחישובים יקרים.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Progress / Spinner
    st.markdown("#### `st.progress()` + `st.spinner()`")
    show_code("""import time

with st.spinner("טוען..."):
    time.sleep(1)
st.success("נטען!")

# סרגל התקדמות:
bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1)
    time.sleep(0.01)""")


# ══════════════════════════════════════════════════════════════════════════════
# 📁 קבצים ומדיה
# ══════════════════════════════════════════════════════════════════════════════
elif section == "📁 קבצים ומדיה":
    st.markdown('<div class="section-header">📁 קבצים ומדיה</div>', unsafe_allow_html=True)

    # File uploader
    st.markdown("#### `st.file_uploader()` — העלאת קובץ")
    show_code("""uploaded = st.file_uploader(
    "העלה קובץ CSV",
    type=["csv", "xlsx"]
)

if uploaded:
    import pandas as pd
    df = pd.read_csv(uploaded)
    st.dataframe(df)
    st.success(f"הקובץ הועלה: {uploaded.name}")""")
    uploaded = st.file_uploader("העלה קובץ CSV לדוגמה", type=["csv", "txt"])
    if uploaded:
        st.success(f"✅ הועלה: {uploaded.name} ({uploaded.size} bytes)")

    st.markdown("---")

    # st.image
    st.markdown("#### `st.image()` — תמונות")
    show_code("""import numpy as np
from PIL import Image

# תמונה מ-URL
st.image("https://picsum.photos/400/200", caption="תמונה לדוגמה")

# תמונה מקובץ
img = Image.open("photo.jpg")
st.image(img, width=300)

# מ-numpy array
arr = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
st.image(arr, caption="רעש אקראי")""")
    import numpy as np
    arr = np.random.randint(0, 255, (80, 200, 3), dtype=np.uint8)
    st.image(arr, caption="מערך numpy אקראי — זו תמונה בפועל!")

    st.markdown("---")

    # Download button
    st.markdown("#### `st.download_button()` — הורדת קובץ")
    show_code("""import pandas as pd

df = pd.DataFrame({"א": [1,2,3], "ב": [4,5,6]})
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 הורד CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv"
)""")
    import pandas as pd
    sample_df = pd.DataFrame({"שם": ["אלי","מיה"], "ציון": [88, 95]})
    csv_data = sample_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 הורד קובץ דוגמה", data=csv_data, file_name="sample.csv", mime="text/csv")

    st.markdown("---")

    # Camera / video
    st.markdown("#### `st.camera_input()` + `st.video()`")
    show_code("""# צילום מהמצלמה
photo = st.camera_input("צלם תמונה")
if photo:
    st.image(photo)

# הצגת וידאו
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
st.video("local_video.mp4")""")


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 עיצוב מתקדם
# ══════════════════════════════════════════════════════════════════════════════
elif section == "🎨 עיצוב מתקדם":
    st.markdown('<div class="section-header">🎨 עיצוב מתקדם — CSS, HTML, ו-config</div>', unsafe_allow_html=True)

    # Custom CSS
    st.markdown("#### `st.markdown()` עם CSS")
    show_code("""st.markdown(\"\"\"
<style>
.my-box {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    font-size: 1.3rem;
    font-weight: bold;
}
</style>

<div class="my-box">
    📦 קופסה עם עיצוב מותאם אישית!
</div>
\"\"\", unsafe_allow_html=True)""")
    st.markdown("""
<style>
.my-box {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    font-size: 1.3rem;
    font-weight: bold;
}
</style>
<div class="my-box">📦 קופסה עם עיצוב מותאם אישית!</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # Page config
    st.markdown("#### `st.set_page_config()` — הגדרות עמוד")
    show_code("""st.set_page_config(
    page_title="שם האפליקציה",   # כותרת הטאב
    page_icon="🚀",               # אייקון
    layout="wide",               # "centered" / "wide"
    initial_sidebar_state="expanded"  # "auto"/"expanded"/"collapsed"
)
# ⚠️ חייב להיות השורה הראשונה בקוד!""")

    st.markdown("---")

    # Themes / config.toml
    st.markdown("#### `.streamlit/config.toml` — ערכת נושא")
    show_code("""# .streamlit/config.toml
[theme]
primaryColor       = "#e94560"
backgroundColor    = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor          = "#1a1a2e"
font               = "sans serif"   # "serif" / "monospace\"""")

    st.markdown("---")

    # st.columns with custom HTML
    st.markdown("#### כרטיסים עם HTML")
    show_code("""cols = st.columns(3)
items = [
    ("🚀", "מהיר",   "בניה בדקות"),
    ("🎨", "יפה",    "עיצוב קל"),
    ("🔌", "מחובר",  "API בשניות"),
]
for col, (icon, title, desc) in zip(cols, items):
    col.markdown(f\"\"\"
    <div style="border:1px solid #ddd; border-radius:10px;
                padding:1rem; text-align:center;">
        <h2>{icon}</h2>
        <b>{title}</b><br>{desc}
    </div>
    \"\"\", unsafe_allow_html=True)""")

    cols = st.columns(3)
    items = [("🚀", "מהיר", "בניה בדקות"), ("🎨", "יפה", "עיצוב קל"), ("🔌", "מחובר", "API בשניות")]
    for col, (icon, title, desc) in zip(cols, items):
        col.markdown(f"""
<div style="border:1px solid #ddd; border-radius:10px; padding:1rem; text-align:center; background:#fafafa;">
    <h2>{icon}</h2>
    <b>{title}</b><br><small>{desc}</small>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # Summary cheat sheet
    st.markdown("### 📋 דף-רמאות מהיר")
    show_code("""# ── טקסט ──────────────────────────────────
st.title()       st.header()      st.subheader()
st.write()       st.markdown()    st.code()
st.success()     st.warning()     st.error()     st.info()

# ── קלט ───────────────────────────────────
st.text_input()  st.number_input() st.text_area()
st.slider()      st.selectbox()   st.multiselect()
st.checkbox()    st.radio()       st.button()
st.date_input()  st.file_uploader()

# ── פריסה ─────────────────────────────────
st.columns()     st.tabs()        st.expander()
st.sidebar       st.container()   st.form()

# ── נתונים וגרפים ─────────────────────────
st.dataframe()   st.table()       st.metric()
st.line_chart()  st.bar_chart()   st.area_chart()

# ── מדיה ──────────────────────────────────
st.image()       st.video()       st.audio()
st.download_button()  st.camera_input()

# ── מצב ───────────────────────────────────
st.session_state    @st.cache_data
st.spinner()        st.progress()
st.balloons()       st.snow()""")
