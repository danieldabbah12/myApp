"""
🫁 בדיקת רנטגן ריאות — אפליקציה ידידותית למשתמש
ממשק פשוט, חם ומזמין לאנשים שאינם מכירים טכנולוגיה.
⚠️ לצורכי לימוד בלבד — אין להשתמש לאבחון רפואי אמיתי.
"""

import streamlit as st
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import io
import time
import hashlib

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="בדיקת רנטגן ריאות",
    page_icon="🫁",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Rubik', sans-serif;
    background-color: #f5f7fa;
    color: #2d3748;
    direction: rtl;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 24px;
    padding: 3rem 2.5rem 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(102,126,234,0.3);
}
.hero-icon { font-size: 4rem; margin-bottom: 0.5rem; }
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.6rem;
    line-height: 1.2;
}
.hero-sub {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.85);
    line-height: 1.7;
    max-width: 480px;
    margin: 0 auto;
}

/* ── Steps ── */
.steps-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    justify-content: center;
}
.step-card {
    background: white;
    border-radius: 16px;
    padding: 1.2rem 1rem;
    text-align: center;
    flex: 1;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #e8ecf4;
}
.step-icon { font-size: 1.8rem; margin-bottom: 0.4rem; }
.step-text { font-size: 0.82rem; color: #718096; font-weight: 500; line-height: 1.4; }

/* ── Upload area ── */
.upload-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #e8ecf4;
    margin-bottom: 1.5rem;
}
.upload-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 0.3rem;
}
.upload-hint { font-size: 0.85rem; color: #a0aec0; margin-bottom: 1rem; }

/* ── Result cards ── */
.result-good {
    background: linear-gradient(135deg, #d4f5e9 0%, #c6f0e0 100%);
    border: 2px solid #48bb78;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-top: 1.5rem;
    box-shadow: 0 8px 30px rgba(72,187,120,0.2);
}
.result-bad {
    background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
    border: 2px solid #fc8181;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-top: 1.5rem;
    box-shadow: 0 8px 30px rgba(252,129,129,0.2);
}
.result-emoji { font-size: 4rem; margin-bottom: 0.8rem; }
.result-title-good {
    font-size: 2rem;
    font-weight: 700;
    color: #276749;
    margin-bottom: 0.6rem;
}
.result-title-bad {
    font-size: 2rem;
    font-weight: 700;
    color: #c53030;
    margin-bottom: 0.6rem;
}
.result-msg {
    font-size: 1rem;
    line-height: 1.7;
    color: #4a5568;
    max-width: 380px;
    margin: 0 auto;
}

/* ── Confidence bar ── */
.conf-wrap {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #e8ecf4;
}
.conf-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #718096;
    margin-bottom: 1rem;
    text-align: center;
    letter-spacing: 0.5px;
}
.bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 0.3rem;
}
.bar-bg {
    height: 12px;
    background: #edf2f7;
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 0.8rem;
}
.bar-green { height:100%; background: linear-gradient(90deg,#48bb78,#68d391); border-radius:6px; }
.bar-red   { height:100%; background: linear-gradient(90deg,#fc8181,#feb2b2); border-radius:6px; }

/* ── Disclaimer ── */
.disclaimer {
    background: #fffbeb;
    border: 1px solid #f6e05e;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: #744210;
    margin-top: 1.5rem;
    text-align: center;
    line-height: 1.6;
}

/* ── Reset button ── */
.stButton > button {
    width: 100%;
    border-radius: 14px !important;
    font-family: 'Rubik', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: 0.75rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.35) !important;
}

[data-testid="stFileUploadDropzone"] {
    background: #f8faff !important;
    border: 2px dashed #c3d0f5 !important;
    border-radius: 14px !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: #667eea !important;
    background: #f0f3ff !important;
}

/* image preview round */
[data-testid="stImage"] img {
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)


# ─── Engine (unchanged logic) ──────────────────────────────────────────────────
def extract_features(img):
    img_gray = img.convert("L").resize((224, 224))
    arr = np.array(img_gray, dtype=np.float32) / 255.0
    density           = float(np.mean(arr))
    contrast          = float(np.std(arr))
    edges_arr         = np.array(img_gray.filter(ImageFilter.FIND_EDGES), dtype=np.float32) / 255.0
    edge_density      = float(np.mean(edges_arr))
    asymmetry         = float(np.abs(np.mean(arr[:, :112]) - np.mean(arr[:, 112:])))
    blocks            = arr.reshape(14, 16, 14, 16)
    texture_roughness = float(np.mean(blocks.var(axis=(1, 3))))
    bright_spots      = float(np.mean(arr > 0.85))
    return dict(density=density, contrast=contrast, edge_density=edge_density,
                asymmetry=asymmetry, texture_roughness=texture_roughness, bright_spots=bright_spots)

def get_probs(features, img_hash):
    rng = np.random.RandomState(img_hash % (2**31))
    mal = (features["edge_density"]*3.5 + features["asymmetry"]*4.0 +
           features["bright_spots"]*2.5 + features["texture_roughness"]*1.5)
    hlt = features["density"]*1.5 + (1 - features["contrast"])*1.0
    logits = np.array([
        hlt + rng.uniform(-0.3, 0.3),
        mal * 0.7 + rng.uniform(-0.2, 0.4),
        mal * 0.5 + rng.uniform(-0.5, 0.2),
    ])
    e = np.exp(logits - logits.max())
    return e / e.sum()   # [תקין, חשוד, ממאיר]


# ─── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-icon">🫁</div>
    <div class="hero-title">בדיקת רנטגן ריאות</div>
    <div class="hero-sub">
        העלו תמונת רנטגן וקבלו תוצאה מיידית —<br>
        פשוט, מהיר, וללא צורך בידע רפואי מוקדם.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── 3 steps ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="steps-row">
    <div class="step-card">
        <div class="step-icon">📤</div>
        <div class="step-text">העלו תמונת<br>רנטגן</div>
    </div>
    <div class="step-card">
        <div class="step-icon">🔍</div>
        <div class="step-text">המערכת<br>מנתחת</div>
    </div>
    <div class="step-card">
        <div class="step-icon">📋</div>
        <div class="step-text">קבלו תוצאה<br>ברורה</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Upload ────────────────────────────────────────────────────────────────────
if not st.session_state.get("analyzed"):
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.markdown('<div class="upload-title">📂 העלו את תמונת הרנטגן</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-hint">פורמטים נתמכים: JPG, PNG, BMP, WEBP</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("", type=["jpg","jpeg","png","bmp","webp"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded:
        img_bytes = uploaded.read()
        img_pil   = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        col_img, col_btn = st.columns([1.2, 1], gap="large")
        with col_img:
            st.image(img_pil, use_container_width=True, caption="התמונה שהועלתה")
        with col_btn:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(f"**📁 {uploaded.name}**")
            st.markdown(f"גודל: {len(img_bytes)/1024:.0f} KB")
            st.markdown("<br>", unsafe_allow_html=True)
            go = st.button("🔍  בדוק עכשיו", type="primary")

        if go:
            with st.spinner("המערכת מנתחת את התמונה..."):
                bar = st.progress(0)
                time.sleep(0.3); bar.progress(30)
                features = extract_features(img_pil)
                time.sleep(0.4); bar.progress(65)
                img_hash = int(hashlib.md5(img_bytes[:2048]).hexdigest(), 16)
                probs    = get_probs(features, img_hash)
                time.sleep(0.4); bar.progress(100)
                time.sleep(0.2); bar.empty()

            st.session_state["probs"]    = probs
            st.session_state["analyzed"] = True
            st.rerun()

# ─── Result ────────────────────────────────────────────────────────────────────
else:
    probs = st.session_state["probs"]

    # סיווג: אם הסתברות "תקין" > 55% → שפיר, אחרת → לא תקין
    prob_healthy = float(probs[0]) -10  # [תקין, חשוד, ממאיר]
    prob_concern = float(probs[1]) + float(probs[2]) +10 # חשוד + ממאיר

    is_healthy = prob_healthy > 0.45

    if is_healthy:
        st.markdown(f"""
        <div class="result-good">
            <div class="result-emoji">✅</div>
            <div class="result-title-good">תקין</div>
            <div class="result-msg">
                לא זוהו ממצאים חריגים בתמונת הרנטגן.<br>
                הריאות נראות תקינות.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-bad">
            <div class="result-emoji">⚠️</div>
            <div class="result-title-bad">מומלץ לבדוק</div>
            <div class="result-msg">
                זוהו ממצאים שכדאי לבדוק לעומק.<br>
                אנו ממליצים לפנות לרופא לבדיקה נוספת.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # אחוזי ביטחון
    pct_h = (prob_healthy  * 100) -10
    pct_c = (prob_concern  * 100) +10
    st.markdown(f"""
    <div class="conf-wrap">
        <div class="conf-title">רמת הביטחון של הניתוח</div>
        <div class="bar-label">
            <span>✅ תקין</span>
            <span>{pct_h:.0f}%</span>
        </div>
        <div class="bar-bg"><div class="bar-green" style="width:{pct_h:.0f}%"></div></div>
        <div class="bar-label">
            <span>⚠️ מומלץ לבדוק</span>
            <span>{pct_c:.0f}%</span>
        </div>
        <div class="bar-bg"><div class="bar-red" style="width:{pct_c:.0f}%"></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  בדוק תמונה אחרת"):
        for k in ["probs", "analyzed"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown("""
    <div class="disclaimer">
        ⚠️ <b>שימו לב:</b> תוצאה זו מיועדת לצורכי הדגמה בלבד ואינה מהווה אבחון רפואי.
        בכל מקרה של חשש יש לפנות לרופא מוסמך.
    </div>
    """, unsafe_allow_html=True)
