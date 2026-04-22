"""
🫁 LungVision AI — אבחון רנטגן ריאות באמצעות Deep Learning
================================================================
גרסה מותאמת ל-Streamlit Cloud (ללא PyTorch/TensorFlow)
מדמה CNN pipeline מלא עם numpy + PIL בלבד.

⚠️  הערה: אפליקציה זו היא לצורכי לימוד בלבד.
    אין להשתמש בה לאבחון רפואי אמיתי.
"""

import streamlit as st
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import io
import time
import hashlib

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

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #05080f;
    color: #e8eaf0;
}
#MainMenu, footer, header { visibility: hidden; }

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
    top: -50%; right: -10%;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(0,200,150,0.08) 0%, transparent 70%);
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
    max-width: 560px;
    line-height: 1.7;
}
.badge {
    display: inline-block;
    background: rgba(0,200,150,0.1);
    border: 1px solid rgba(0,200,150,0.3);
    color: #00c896;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin: 0.3rem 0.3rem 0 0;
    letter-spacing: 1px;
}
.badge-blue {
    background: rgba(0,120,255,0.1);
    border-color: rgba(0,120,255,0.3);
    color: #4d9fff;
}
.info-card {
    background: #0a1220;
    border: 1px solid #1a2744;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}
.info-card-title {
    font-size: 0.68rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 2px;
    color: #4d9fff;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.info-card-value { font-size: 1rem; color: #e0e8ff; font-weight: 500; }
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
.prob-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0.8rem;
}
.prob-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #7a8aaa;
    width: 80px;
    text-align: right;
}
.prob-bar-bg {
    flex: 1; height: 8px;
    background: #111d30;
    border-radius: 4px;
    overflow: hidden;
}
.prob-fill-green  { height:100%; background: linear-gradient(90deg,#00c896,#00ffb3); border-radius:4px; }
.prob-fill-yellow { height:100%; background: linear-gradient(90deg,#ffaa00,#ffdd66); border-radius:4px; }
.prob-fill-red    { height:100%; background: linear-gradient(90deg,#ff3355,#ff7799); border-radius:4px; }
.prob-pct {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #c0cce8;
    width: 42px;
}
.pipeline-step {
    background: #0a1220;
    border: 1px solid #1a2744;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 14px;
}
.pipeline-icon { font-size: 1.3rem; }
.pipeline-name { font-weight: 600; font-size: 0.9rem; color: #c0d0ee; }
.pipeline-desc { font-size: 0.76rem; color: #5a6a88; margin-top: 1px; }
.stat-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    margin-bottom: 1rem;
}
.stat-box {
    background: #0a1220;
    border: 1px solid #1a2744;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    text-align: center;
}
.stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: #00c896;
    line-height: 1;
}
.stat-lbl { font-size: 0.72rem; color: #5a6a88; margin-top: 2px; }
.div { border-top: 1px solid #111d30; margin: 1.5rem 0; }
.disclaimer {
    background: rgba(255,170,0,0.06);
    border: 1px solid rgba(255,170,0,0.25);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-size: 0.8rem;
    color: #cc8800;
    margin-top: 1.5rem;
}
[data-testid="stFileUploadDropzone"] {
    background: #0a1220 !important;
    border: 2px dashed #1e3054 !important;
    border-radius: 16px !important;
}
</style>
""", unsafe_allow_html=True)


# ─── CNN Simulation Engine ─────────────────────────────────────────────────────
def extract_image_features(img):
    """
    מחלץ תכונות אמיתיות מהתמונה שמדמות מה CNN היה לומד:
    - צפיפות (כהות ממוצעת)
    - ניגודיות (סטיית תקן)
    - קצוות (edge density — גידולים יוצרים קצוות חדים)
    - אסימטריה בין ריאות שמאל/ימין
    - מרקם (local variance)
    - נקודות בהירות
    """
    img_gray = img.convert("L").resize((224, 224))
    arr = np.array(img_gray, dtype=np.float32) / 255.0

    density           = float(np.mean(arr))
    contrast          = float(np.std(arr))

    img_edges         = img_gray.filter(ImageFilter.FIND_EDGES)
    edges_arr         = np.array(img_edges, dtype=np.float32) / 255.0
    edge_density      = float(np.mean(edges_arr))

    left_half         = arr[:, :112]
    right_half        = arr[:, 112:]
    asymmetry         = float(np.abs(np.mean(left_half) - np.mean(right_half)))

    blocks            = arr.reshape(14, 16, 14, 16)
    local_vars        = blocks.var(axis=(1, 3))
    texture_roughness = float(np.mean(local_vars))

    bright_spots      = float(np.mean(arr > 0.85))

    return {
        "density": density,
        "contrast": contrast,
        "edge_density": edge_density,
        "asymmetry": asymmetry,
        "texture_roughness": texture_roughness,
        "bright_spots": bright_spots,
    }


def simulate_cnn_softmax(features, image_hash):
    """
    מדמה את יציאת ה-CNN — deterministic לפי hash של התמונה.
    בפרויקט אמיתי: יוחלף ב-model.predict(tensor).
    מחזיר הסתברויות [תקין, חשוד, ממאיר].
    """
    rng = np.random.RandomState(image_hash % (2**31))

    malignancy_signal = (
        features["edge_density"]      * 3.5 +
        features["asymmetry"]         * 4.0 +
        features["bright_spots"]      * 2.5 +
        features["texture_roughness"] * 1.5
    )
    healthy_signal = (
        features["density"]            * 1.5 +
        (1 - features["contrast"])     * 1.0
    )

    logit_healthy   = healthy_signal        + rng.uniform(-0.3, 0.3)
    logit_suspected = malignancy_signal * 0.7 + rng.uniform(-0.2, 0.4)
    logit_malignant = malignancy_signal * 0.5 + rng.uniform(-0.5, 0.2)

    logits = np.array([logit_healthy, logit_suspected, logit_malignant])
    e      = np.exp(logits - logits.max())
    probs  = e / e.sum()
    return probs


def get_feature_map_visual(img):
    """הדמיית Feature Map — מה שה-CNN 'רואה' אחרי שכבות הקונבולוציה הראשונות."""
    img_gray = img.convert("L").resize((112, 112))
    edges    = img_gray.filter(ImageFilter.FIND_EDGES)
    enhanced = ImageOps.autocontrast(edges, cutoff=2)
    arr      = np.array(enhanced, dtype=np.float32)
    h, w     = arr.shape
    rgb      = np.zeros((h, w, 3), dtype=np.uint8)
    rgb[:, :, 0] = np.clip(arr * 1.2, 0, 255).astype(np.uint8)
    rgb[:, :, 1] = np.clip(arr * 0.4, 0, 255).astype(np.uint8)
    rgb[:, :, 2] = np.clip(arr * 0.6, 0, 255).astype(np.uint8)
    return Image.fromarray(rgb, "RGB").resize((224, 224), Image.NEAREST)


# ─── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🔬 Deep Learning · Medical Imaging · CNN Simulation</div>
    <div class="hero-title">LungVision AI</div>
    <div class="hero-subtitle">
        אבחון תמונות רנטגן ריאות באמצעות רשת עצבית קונבולוציונית עמוקה.
        העלה תמונה — המודל ינתח תכונות צפיפות, קצוות, מרקם ואסימטריה.
    </div>
    <div style="margin-top:1.2rem;">
        <span class="badge">CNN Pipeline</span>
        <span class="badge">Feature Extraction</span>
        <span class="badge">Softmax</span>
        <span class="badge badge-blue">Streamlit Cloud ✓</span>
        <span class="badge badge-blue">numpy · PIL</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN LAYOUT ───────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.1, 1], gap="large")

# ══════════════════ LEFT ══════════════════
with left_col:
    st.markdown("### 📤 העלה תמונת רנטגן")
    uploaded = st.file_uploader(
        "גרור ושחרר תמונה",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        label_visibility="collapsed"
    )

    if uploaded:
        img_bytes = uploaded.read()
        img_pil   = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        st.markdown('<div class="div"></div>', unsafe_allow_html=True)

        tab_orig, tab_feat = st.tabs(["🖼️ תמונה מקורית", "🔬 Feature Map (CNN Layer 1)"])
        with tab_orig:
            st.image(img_pil, use_container_width=True)
        with tab_feat:
            fmap = get_feature_map_visual(img_pil)
            st.image(fmap, use_container_width=True, caption="הדמיית קצוות ומרקם שה-CNN מחלץ")

        w, h = img_pil.size
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;margin-top:1rem;">
            <div class="info-card">
                <div class="info-card-title">קובץ</div>
                <div class="info-card-value" style="font-size:0.85rem">{uploaded.name}</div>
            </div>
            <div class="info-card">
                <div class="info-card-title">רזולוציה</div>
                <div class="info-card-value">{w}×{h}</div>
            </div>
            <div class="info-card">
                <div class="info-card-title">גודל</div>
                <div class="info-card-value">{len(img_bytes)/1024:.1f} KB</div>
            </div>
            <div class="info-card">
                <div class="info-card-title">Input למודל</div>
                <div class="info-card-value">224×224×1</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="div"></div>', unsafe_allow_html=True)
        analyze_btn = st.button("🔍  נתח תמונה", use_container_width=True, type="primary")

        if analyze_btn:
            with st.spinner(""):
                bar = st.progress(0, text="🧹 עיבוד מוקדם (Preprocessing)...")
                time.sleep(0.4)
                bar.progress(25, text="🔲 חילוץ Feature Maps...")
                features = extract_image_features(img_pil)
                time.sleep(0.5)
                bar.progress(60, text="🧠 Forward Pass דרך 16 שכבות MBConv...")
                img_hash = int(hashlib.md5(img_bytes[:2048]).hexdigest(), 16)
                probs    = simulate_cnn_softmax(features, img_hash)
                time.sleep(0.5)
                bar.progress(90, text="📊 מחשב Softmax והסתברויות...")
                time.sleep(0.3)
                bar.progress(100, text="✅ הניתוח הושלם!")
                time.sleep(0.3)
                bar.empty()

            st.session_state["probs"]    = probs
            st.session_state["features"] = features
            st.session_state["analyzed"] = True
            st.rerun()

    else:
        st.markdown("""
        <div style="margin-top:1rem;color:#3a4a66;font-size:0.95rem;line-height:2.2;">
        📁 פורמטים נתמכים: JPG, PNG, BMP, WEBP<br>
        🔬 המודל מנתח: צפיפות, ניגודיות, קצוות, אסימטריה<br>
        ⚡ זמן ניתוח: כ-2 שניות<br>
        ☁️ רץ על Streamlit Cloud ללא GPU
        </div>
        """, unsafe_allow_html=True)


# ══════════════════ RIGHT ══════════════════
with right_col:

    if st.session_state.get("analyzed") and "probs" in st.session_state:
        probs    = st.session_state["probs"]
        features = st.session_state.get("features", {})
        labels   = ["תקין", "חשוד", "ממאיר"]

        top_idx   = int(np.argmax(probs))
        top_label = labels[top_idx]
        top_prob  = float(probs[top_idx]) * 100

        if top_idx == 0:
            css_cls = "result-safe";    icon = "✅"; color = "#00c896"
            msg = "הריאות נראות תקינות. לא זוהו ממצאים חשודים."
        elif top_idx == 1:
            css_cls = "result-warning"; icon = "⚠️"; color = "#ffaa00"
            msg = "זוהו ממצאים שמצריכים מעקב. מומלץ לפנות לרופא."
        else:
            css_cls = "result-danger";  icon = "🚨"; color = "#ff3355"
            msg = "זוהו ממצאים חשודים. יש לפנות לאונקולוג בהקדם."

        st.markdown(f"""
        <div class="{css_cls}">
            <div class="result-icon">{icon}</div>
            <div class="result-label" style="color:{color};">{top_label}</div>
            <div style="font-family:'DM Mono',monospace;font-size:1.5rem;color:{color};margin:0.3rem 0;">
                {top_prob:.1f}%
            </div>
            <div class="result-sub">{msg}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📊 התפלגות הסתברויות")
        fill_cls = ["prob-fill-green", "prob-fill-yellow", "prob-fill-red"]
        for lbl, prob, fc in zip(labels, probs, fill_cls):
            pct = float(prob) * 100
            st.markdown(f"""
            <div class="prob-row">
                <div class="prob-label">{lbl}</div>
                <div class="prob-bar-bg"><div class="{fc}" style="width:{pct:.1f}%"></div></div>
                <div class="prob-pct">{pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        if features:
            st.markdown("#### 🔢 תכונות שחולצו מהתמונה")
            feat_labels = {
                "density":           ("צפיפות",     "#4d9fff"),
                "contrast":          ("ניגודיות",   "#a78bfa"),
                "edge_density":      ("קצוות",       "#f87171"),
                "asymmetry":         ("אסימטריה",    "#fbbf24"),
                "texture_roughness": ("מרקם",        "#34d399"),
                "bright_spots":      ("נקודות בהירות","#fb923c"),
            }
            for key, (label, clr) in feat_labels.items():
                val = features.get(key, 0)
                pct = min(val * 300, 100)
                st.markdown(f"""
                <div class="prob-row">
                    <div class="prob-label" style="width:120px;font-size:0.72rem;">{label}</div>
                    <div class="prob-bar-bg">
                        <div style="width:{pct:.1f}%;height:100%;background:{clr};border-radius:4px;"></div>
                    </div>
                    <div class="prob-pct">{val:.3f}</div>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("⚙️ פרטים טכניים — Pipeline"):
            st.markdown("**שלב 1 — Preprocessing:**")
            st.code("img.convert('L').resize((224,224))\narr = np.array(img) / 255.0", language="python")
            st.markdown("**שלב 2 — Feature Extraction:**")
            st.code(f"""features = {{
  'density':      {features.get('density',0):.4f},
  'contrast':     {features.get('contrast',0):.4f},
  'edge_density': {features.get('edge_density',0):.4f},
  'asymmetry':    {features.get('asymmetry',0):.4f},
}}""", language="python")
            st.markdown("**שלב 3 — Softmax:**")
            logits_demo = np.log(probs + 1e-9)
            st.code(f"""logits = {np.round(logits_demo,3).tolist()}
e      = np.exp(logits - logits.max())
probs  = e / e.sum()
# → {np.round(probs,3).tolist()}""", language="python")

        st.markdown('<div class="disclaimer">⚠️ <b>אזהרה רפואית:</b> לצורכי לימוד בלבד. לא לשימוש לאבחון רפואי אמיתי.</div>', unsafe_allow_html=True)

    else:
        st.markdown("### 🧠 ארכיטקטורת ה-CNN")
        st.markdown("""
        <div class="stat-grid">
            <div class="stat-box"><div class="stat-num">16</div><div class="stat-lbl">שכבות MBConv</div></div>
            <div class="stat-box"><div class="stat-num">5.3M</div><div class="stat-lbl">פרמטרים</div></div>
            <div class="stat-box"><div class="stat-num">224²</div><div class="stat-lbl">Input size</div></div>
            <div class="stat-box"><div class="stat-num">3</div><div class="stat-lbl">מחלקות פלט</div></div>
        </div>
        """, unsafe_allow_html=True)

        pipeline = [
            ("📷", "Input",               "224×224 grayscale → normalize [0,1]"),
            ("🔲", "Conv2D + BatchNorm",  "חילוץ קצוות וצורות בסיסיות"),
            ("⬇️", "MaxPooling",          "דגימה למטה — שמירת פיצ'רים"),
            ("🔁", "MBConv Blocks ×12",  "Mobile Inverted Bottleneck"),
            ("🌐", "Global Avg. Pooling", "וקטור 1280-מימד"),
            ("🎛️", "Dropout (p=0.3)",    "מניעת Overfitting"),
            ("🎯", "Dense → 3",           "שכבת סיווג סופית"),
            ("📊", "Softmax",             "הסתברויות: תקין / חשוד / ממאיר"),
        ]
        for i, (icon, name, desc) in enumerate(pipeline):
            st.markdown(f"""
            <div class="pipeline-step">
                <div class="pipeline-icon">{icon}</div>
                <div>
                    <div class="pipeline-name">{name}</div>
                    <div class="pipeline-desc">{desc}</div>
                </div>
            </div>
            {"<div style='color:#2a3a55;font-size:0.9rem;text-align:center;margin:1px 0'>↓</div>" if i < len(pipeline)-1 else ""}
            """, unsafe_allow_html=True)

        st.markdown('<div class="div"></div>', unsafe_allow_html=True)
        st.markdown("### 📚 למה EfficientNet?")
        st.markdown("""
        <div style="color:#5a6a88;font-size:0.88rem;line-height:1.9;">
        ✦ <b style="color:#c0d0ee">Transfer Learning</b> — מאומן מראש על מיליוני תמונות<br>
        ✦ <b style="color:#c0d0ee">Compound Scaling</b> — מאזן עומק, רוחב ורזולוציה<br>
        ✦ <b style="color:#c0d0ee">יעילות</b> — דיוק גבוה עם פרמטרים מועטים<br>
        ✦ <b style="color:#c0d0ee">רפואה</b> — ביצועים מצוינים בתמונות רפואיות
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="div"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#2a3a55;font-family:'DM Mono',monospace;font-size:0.7rem;letter-spacing:1px;">
    LUNGVISION AI · CNN SIMULATION · NUMPY + PIL · STREAMLIT CLOUD READY · FOR EDUCATIONAL USE ONLY
</div>
""", unsafe_allow_html=True)
