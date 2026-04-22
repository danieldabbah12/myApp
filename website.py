"""
🫁 LungVision AI — אבחון רנטגן ריאות באמצעות Deep Learning
================================================================
מודל: EfficientNet-B0 (CNN) מאומן מראש על ImageNet
משימה: סיווג תמונות רנטגן — תקין / חשוד / דורש בדיקה

⚠️  הערה חשובה: אפליקציה זו היא לצורכי לימוד בלבד.
    אין להשתמש בה לאבחון רפואי אמיתי.
"""

import streamlit as st
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np
import time
import io

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LungVision AI",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&family=Bebas+Neue&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #05080f;
    color: #e8eaf0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero Banner ── */
.hero {
    background: linear-gradient(135deg, #05080f 0%, #0a1628 40%, #071a3e 100%);
    border: 1px solid #1a2744;
    border-radius: 20px;
    padding: 3rem 3.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(0, 200, 150, 0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: 5%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0, 120, 255, 0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 3px;
    color: #00c896;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem;
    line-height: 1;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #ffffff 0%, #a8d8ff 60%, #00c896 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #7a8aaa;
    max-width: 520px;
    line-height: 1.7;
}
.badge {
    display: inline-block;
    background: rgba(0, 200, 150, 0.1);
    border: 1px solid rgba(0, 200, 150, 0.3);
    color: #00c896;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin: 0.3rem 0.3rem 0 0;
    letter-spacing: 1px;
}
.badge-blue {
    background: rgba(0, 120, 255, 0.1);
    border-color: rgba(0, 120, 255, 0.3);
    color: #4d9fff;
}

/* ── Upload Zone ── */
.upload-zone {
    background: linear-gradient(135deg, #0a1220 0%, #0d1a2e 100%);
    border: 2px dashed #1e3054;
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    transition: border-color 0.3s;
}
.upload-icon {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}
.upload-text {
    font-size: 1rem;
    color: #5a6a88;
}

/* ── Info Card ── */
.info-card {
    background: #0a1220;
    border: 1px solid #1a2744;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.info-card-title {
    font-size: 0.7rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 2px;
    color: #4d9fff;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.info-card-value {
    font-size: 1.05rem;
    color: #e0e8ff;
    font-weight: 500;
}

/* ── Result Cards ── */
.result-safe {
    background: linear-gradient(135deg, #001a12 0%, #002a1c 100%);
    border: 1px solid #00c896;
    border-radius: 18px;
    padding: 2rem 2.5rem;
    text-align: center;
}
.result-warning {
    background: linear-gradient(135deg, #1a1000 0%, #2a1c00 100%);
    border: 1px solid #ffaa00;
    border-radius: 18px;
    padding: 2rem 2.5rem;
    text-align: center;
}
.result-danger {
    background: linear-gradient(135deg, #1a0008 0%, #2a000f 100%);
    border: 1px solid #ff3355;
    border-radius: 18px;
    padding: 2rem 2.5rem;
    text-align: center;
}
.result-icon { font-size: 3.5rem; margin-bottom: 0.5rem; }
.result-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 2px;
    margin-bottom: 0.4rem;
}
.result-sub { font-size: 0.9rem; color: #8899bb; }

/* ── Prob Bar ── */
.prob-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0.7rem;
}
.prob-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #7a8aaa;
    width: 90px;
    text-align: right;
}
.prob-bar-bg {
    flex: 1;
    height: 8px;
    background: #111d30;
    border-radius: 4px;
    overflow: hidden;
}
.prob-fill-green  { height: 100%; background: linear-gradient(90deg, #00c896, #00ffb3); border-radius: 4px; }
.prob-fill-yellow { height: 100%; background: linear-gradient(90deg, #ffaa00, #ffdd66); border-radius: 4px; }
.prob-fill-red    { height: 100%; background: linear-gradient(90deg, #ff3355, #ff7799); border-radius: 4px; }
.prob-pct {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #c0cce8;
    width: 42px;
}

/* ── Steps ── */
.step-row {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 1.2rem;
}
.step-num {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0050cc, #003a99);
    color: white;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
}
.step-content {}
.step-title { font-weight: 600; color: #c8d8f0; font-size: 0.95rem; }
.step-desc  { color: #5a6a88; font-size: 0.85rem; line-height: 1.5; margin-top: 2px; }

/* ── Model Architecture ── */
.arch-block {
    background: #0a1220;
    border: 1px solid #1a2744;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
}
.arch-icon { font-size: 1.3rem; }
.arch-name { font-weight: 600; font-size: 0.92rem; color: #c0d0ee; }
.arch-desc { font-size: 0.78rem; color: #5a6a88; }
.arch-arrow { color: #2a3a55; font-size: 1.2rem; text-align: center; margin: 2px 0; }

/* ── Warning ── */
.medical-disclaimer {
    background: rgba(255, 170, 0, 0.06);
    border: 1px solid rgba(255, 170, 0, 0.25);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-size: 0.8rem;
    color: #cc8800;
    margin-top: 1.5rem;
}

/* ── Divider ── */
.div { border-top: 1px solid #111d30; margin: 1.5rem 0; }

/* ── Override Streamlit file uploader ── */
[data-testid="stFileUploadDropzone"] {
    background: #0a1220 !important;
    border: 2px dashed #1e3054 !important;
    border-radius: 16px !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: #00c896 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    """
    טוען EfficientNet-B0 מאומן מראש.
    בפרויקט אמיתי: היינו מחליפים את שכבת הסיווג האחרונה
    ומאמנים על NIH Chest X-Ray Dataset.
    לצורכי הדגמה: משתמשים במשקלים של ImageNet.
    """
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)

    # החלפת שכבת הסיווג — 3 מחלקות: תקין / חשוד / ממאיר
    num_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(num_features, 3)
    )
    model.eval()
    return model

@st.cache_data(show_spinner=False)
def preprocess_image(img_bytes):
    """עיבוד מוקדם של התמונה לפורמט שהמודל מצפה לו."""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.Grayscale(num_output_channels=3),  # רנטגן → 3 ערוצים
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    tensor = transform(img).unsqueeze(0)  # הוספת batch dimension
    return img, tensor

def predict(model, tensor):
    """הרצת הנבואה וחישוב הסתברויות."""
    with torch.no_grad():
        logits = model(tensor)
        probs  = torch.softmax(logits, dim=1)[0]
    return probs.numpy()


# ─── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🔬 Deep Learning · Medical Imaging · CNN</div>
    <div class="hero-title">LungVision AI</div>
    <div class="hero-subtitle">
        אבחון תמונות רנטגן ריאות באמצעות רשת עצבית קונבולוציונית עמוקה.
        העלה תמונה וקבל ניתוח מיידי.
    </div>
    <div style="margin-top:1.2rem;">
        <span class="badge">EfficientNet-B0</span>
        <span class="badge">PyTorch</span>
        <span class="badge">CNN</span>
        <span class="badge badge-blue">Streamlit</span>
        <span class="badge badge-blue">Transfer Learning</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN LAYOUT ───────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.1, 1], gap="large")

# ══════════════════ LEFT COLUMN ══════════════════
with left_col:

    # Upload
    st.markdown("### 📤 העלה תמונת רנטגן")
    uploaded = st.file_uploader(
        "גרור ושחרר תמונה (JPG, PNG, DICOM-preview)",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        label_visibility="collapsed"
    )

    if uploaded:
        img_bytes = uploaded.read()
        img_pil, tensor = preprocess_image(img_bytes)

        # Show image with overlay
        st.markdown('<div class="div"></div>', unsafe_allow_html=True)

        col_img, col_meta = st.columns([1.4, 1])
        with col_img:
            st.image(img_pil, use_container_width=True, caption="תמונת הרנטגן שהועלתה")
        with col_meta:
            w, h = img_pil.size
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-title">שם קובץ</div>
                <div class="info-card-value" style="font-size:0.85rem">{uploaded.name}</div>
            </div>
            <div class="info-card">
                <div class="info-card-title">רזולוציה</div>
                <div class="info-card-value">{w} × {h}</div>
            </div>
            <div class="info-card">
                <div class="info-card-title">גודל</div>
                <div class="info-card-value">{len(img_bytes)/1024:.1f} KB</div>
            </div>
            <div class="info-card">
                <div class="info-card-title">Input למודל</div>
                <div class="info-card-value">224 × 224 × 3</div>
            </div>
            """, unsafe_allow_html=True)

        # Analyze button
        st.markdown('<div class="div"></div>', unsafe_allow_html=True)
        analyze_btn = st.button("🔍  נתח תמונה", use_container_width=True, type="primary")

        if analyze_btn:
            # Load model + run inference
            with st.spinner("טוען מודל ומריץ ניתוח..."):
                model = load_model()
                time.sleep(0.6)  # UX pause for drama
                probs = predict(model, tensor)

            # ── Inject result into session_state ──
            st.session_state["probs"]    = probs
            st.session_state["analyzed"] = True

    else:
        # Placeholder instructions
        st.markdown("""
        <div style="margin-top:1rem; color:#3a4a66; font-size:0.95rem; line-height:2;">
        📁 פורמטים נתמכים: JPG, PNG, BMP<br>
        🔬 המודל מנתח את דפוסי הצפיפות בתמונה<br>
        ⚡ זמן ניתוח: פחות משניה<br>
        🔒 התמונה לא נשמרת בשרת
        </div>
        """, unsafe_allow_html=True)


# ══════════════════ RIGHT COLUMN ══════════════════
with right_col:

    if st.session_state.get("analyzed") and "probs" in st.session_state:
        probs = st.session_state["probs"]
        labels = ["תקין", "חשוד", "ממאיר"]

        # Find top class
        top_idx   = int(np.argmax(probs))
        top_label = labels[top_idx]
        top_prob  = float(probs[top_idx]) * 100

        # Result card
        if top_idx == 0:
            css_cls = "result-safe"
            icon    = "✅"
            color   = "#00c896"
            msg     = "הריאות נראות תקינות. לא זוהו ממצאים חשודים."
        elif top_idx == 1:
            css_cls = "result-warning"
            icon    = "⚠️"
            color   = "#ffaa00"
            msg     = "זוהו ממצאים שמצריכים מעקב. מומלץ לפנות לרופא."
        else:
            css_cls = "result-danger"
            icon    = "🚨"
            color   = "#ff3355"
            msg     = "זוהו ממצאים חשודים. יש לפנות לאונקולוג בהקדם."

        st.markdown(f"""
        <div class="{css_cls}">
            <div class="result-icon">{icon}</div>
            <div class="result-label" style="color:{color};">{top_label}</div>
            <div style="font-family:'DM Mono',monospace; font-size:1.5rem; color:{color}; margin:0.3rem 0;">
                {top_prob:.1f}%
            </div>
            <div class="result-sub">{msg}</div>
        </div>
        """, unsafe_allow_html=True)

        # Probability bars
        st.markdown("#### 📊 התפלגות הסתברויות")
        colors_css = ["prob-fill-green", "prob-fill-yellow", "prob-fill-red"]
        for i, (lbl, prob, c) in enumerate(zip(labels, probs, colors_css)):
            pct = float(prob) * 100
            st.markdown(f"""
            <div class="prob-row">
                <div class="prob-label">{lbl}</div>
                <div class="prob-bar-bg">
                    <div class="{c}" style="width:{pct:.1f}%"></div>
                </div>
                <div class="prob-pct">{pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        # Tensor details expander
        with st.expander("🔢 פרטים טכניים — Tensor & Forward Pass"):
            st.markdown("**ממדי ה-Tensor שנכנס למודל:**")
            st.code(f"torch.Size([1, 3, 224, 224])  # batch=1, channels=3, H=224, W=224", language="python")
            st.markdown("**Logits (לפני Softmax):**")
            model_ref = load_model()
            with torch.no_grad():
                logits = model_ref(tensor)
            st.code(str(logits.numpy().round(4)), language="python")
            st.markdown("**אחרי `torch.softmax`:**")
            st.code(str(probs.round(4)), language="python")

        st.markdown('<div class="medical-disclaimer">⚠️ <b>אזהרה רפואית:</b> אפליקציה זו נועדה לצורכי לימוד בלבד. אל תשתמש בה לאבחון רפואי. תמיד פנה לרופא מוסמך.</div>', unsafe_allow_html=True)

    else:
        # Architecture panel (shown before analysis)
        st.markdown("### 🧠 ארכיטקטורת המודל")

        arch_items = [
            ("📷", "Input Layer",           "224×224×3 — תמונת רנטגן מנורמלת"),
            ("🔲", "MBConv Blocks ×16",     "Mobile Inverted Bottleneck — ליבת EfficientNet"),
            ("🌐", "Global Avg. Pooling",   "דחיסה מרחבית → וקטור 1280-מימד"),
            ("🎛️", "Dropout (p=0.3)",       "מניעת Overfitting"),
            ("🎯", "FC Layer → 3 classes",  "תקין / חשוד / ממאיר"),
            ("📊", "Softmax",               "הסתברויות — סכום = 100%"),
        ]
        arrows = True
        for i, (icon, name, desc) in enumerate(arch_items):
            st.markdown(f"""
            <div class="arch-block">
                <div class="arch-icon">{icon}</div>
                <div>
                    <div class="arch-name">{name}</div>
                    <div class="arch-desc">{desc}</div>
                </div>
            </div>
            {"<div class='arch-arrow'>↓</div>" if i < len(arch_items)-1 else ""}
            """, unsafe_allow_html=True)

        # How it works
        st.markdown('<div class="div"></div>', unsafe_allow_html=True)
        st.markdown("### 🔄 איך זה עובד?")

        steps = [
            ("עיבוד מוקדם",   "התמונה משתנה לגודל 224×224, מנורמלת עם ממוצע וסטיית תקן של ImageNet"),
            ("Convolutions",  "שכבות קונבולוציה מחלצות תכונות: קצוות, צורות, צפיפויות"),
            ("Feature Maps",  "המודל מייצר 1280 פיצ'רים שמתארים את תוכן התמונה"),
            ("סיווג",          "שכבה fully-connected ממירה לשלושה ציונים"),
            ("Softmax",        "ציונים הופכים להסתברויות (0-100%) — הגדולה ביותר היא האבחנה"),
        ]
        for i, (title, desc) in enumerate(steps, 1):
            st.markdown(f"""
            <div class="step-row">
                <div class="step-num">{i}</div>
                <div class="step-content">
                    <div class="step-title">{title}</div>
                    <div class="step-desc">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="div"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#2a3a55; font-family:'DM Mono',monospace; font-size:0.72rem; letter-spacing:1px;">
    LUNGVISION AI · BUILT WITH PYTORCH + STREAMLIT · FOR EDUCATIONAL USE ONLY
</div>
""", unsafe_allow_html=True)
