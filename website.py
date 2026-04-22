import streamlit as st
import pandas as pd
import numpy as np

# הגדרת כותרת לדף
st.set_page_config(page_title="מדריך Streamlit לתלמידים", layout="wide")

st.title("🚀 מדריך Streamlit מהיר למפתחים צעירים")
st.write("ברוכים הבאים! במדריך הזה תלמדו איך ליצור ממשקים גרפיים בקלות בעזרת פייתון.")

st.divider()

# --- חלק 1: טקסט וכותרות ---
st.header("1. הצגת טקסט")
col1, col2 = st.columns(2)

with col1:
    st.subheader("איך זה נראה?")
    st.title("זו כותרת ראשית (Title)")
    st.header("זו כותרת משנה (Header)")
    st.write("זה טקסט רגיל. אפשר להשתמש ב-write להצגת כמעט כל דבר.")
    st.success("הצלחנו! (הודעת הצלחה)")

with col2:
    st.subheader("הקוד:")
    st.code('''
st.title("זו כותרת ראשית")
st.header("זו כותרת משנה")
st.write("זה טקסט רגיל")
st.success("הודעת הצלחה בירוק")
    ''')

st.divider()

# --- חלק 2: רכיבי קלט (Widgets) ---
st.header("2. קבלת קלט מהמשתמש")

col3, col4 = st.columns(2)

with col3:
    st.subheader("איך זה נראה?")
    
    # כפתור
    if st.button('לחצו עלי!'):
        st.write('הכפתור נלחץ!')
    
    # תיבת טקסט
    name = st.text_input("מה שמך?", "הקלידו כאן...")
    
    # בחירה מרשימה
    color = st.selectbox("מה הצבע האהוב עליך?", ["כחול", "אדום", "ירוק"])
    
    # סליידר (מדד)
    age = st.slider("בן כמה אתה?", 0, 120, 25)

with col4:
    st.subheader("הקוד:")
    st.code('''
# כפתור
if st.button('לחצו עלי!'):
    st.write('הכפתור נלחץ!')

# תיבת טקסט
name = st.text_input("מה שמך?")

# בחירה מרשימה
color = st.selectbox("צבע אהוב", ["כחול", "אדום"])

# סליידר
age = st.slider("גיל", 0, 120, 25)
    ''')

st.divider()

# --- חלק 3: נתונים וגרפים ---
st.header("3. הצגת נתונים וגרפים")

# יצירת נתונים לדוגמה
data = pd.DataFrame(
    np.random.randn(10, 2),
    columns=['מדד א', 'מדד ב']
)

col5, col6 = st.columns(2)

with col5:
    st.subheader("טבלה וגרף:")
    st.dataframe(data)  # הצגת טבלה
    st.line_chart(data) # הצגת גרף קווים

with col6:
    st.subheader("הקוד:")
    st.code('''
import pandas as pd
import numpy as np

# יצירת נתונים
data = pd.DataFrame(
    np.random.randn(10, 2),
    columns=['א', 'ב']
)

# הצגת טבלה
st.dataframe(data)

# הצגת גרף קווים
st.line_chart(data)
    ''')

st.divider()

# --- חלק 4: סידורי דף (Layout) ---
st.header("4. ארגון הדף")
st.info("שימו לב לתפריט הצידי (Sidebar) שנפתח בצד שמאל!")

with st.sidebar:
    st.header("תפריט צידי")
    st.write("כאן אפשר לשים הגדרות כלליות לאתר.")
    st.radio("בחר רמה:", ["מתחיל", "בינוני", "מתקדם"])

st.code('''
# יצירת תפריט צידי
with st.sidebar:
    st.header("תפריט צידי")
    st.radio("בחר רמה:", ["מתחיל", "מתקדם"])
''')

st.success("זהו! אתם מוכנים להתחיל לבנות אתר משלכם.")
