import streamlit as st

st.set_page_config(
    page_title="IS 800:2007 — Interactive Learning",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)
# ── State Management & Query Params ───────────────────────────────────────────
# Check if a module was clicked from the home page cards
params = st.query_params
if "module" in params:
    # Save the clicked module number (e.g., '01', '02') to session state
    st.session_state.current_module = params["module"]
    # Clear the parameter so it doesn't get stuck in the URL
    st.query_params.clear()
# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
h1, h2, h3 { font-weight: 700; letter-spacing: -0.02em; }
code, .stCode { font-family: 'IBM Plex Mono', monospace !important; }

.hero-banner {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    border-radius: 16px;
    padding: 48px 40px;
    margin-bottom: 32px;
    color: white;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "";
    position: absolute; top: -60px; right: -60px;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.module-card {
    background: #f8f9fc;
    border: 1.5px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
    cursor: pointer;
}
.module-card:hover { border-color: #2c5364; background: #eef2ff; }
.module-card h4 { margin: 0 0 6px; font-size: 16px; color: #1a202c; }
.module-card p  { margin: 0; font-size: 13px; color: #64748b; line-height: 1.5; }
.badge {
    display: inline-block;
    background: #dbeafe; color: #1e40af;
    border-radius: 6px; padding: 2px 10px;
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.05em; text-transform: uppercase;
    margin-bottom: 10px;
}
.stat-box {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}
.stat-box .num { font-size: 32px; font-weight: 700; color: #2c5364; }
.stat-box .lbl { font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-tag">Bureau of Indian Standards</div>
  <h1 style="font-size:2.6rem; margin:0 0 12px;">IS 800 : 2007</h1>
  <p style="font-size:1.15rem; margin:0 0 6px; opacity:0.9;">
      General Construction in Steel — Code of Practice
  </p>
  <p style="font-size:0.92rem; opacity:0.65; margin:0;">
      Third Revision · Limit State Design · Interactive Learning Platform
  </p>
</div>
""", unsafe_allow_html=True)

# ── Stats row ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
for col, num, lbl in [
    (c1, "17",   "Chapters"),
    (c2, "6",    "Interactive Calculators"),
    (c3, "50+",  "Clause References"),
    (c4, "40+",  "Quiz Questions"),
]:
    col.markdown(f"""
    <div class="stat-box">
        <div class="num">{num}</div>
        <div class="lbl">{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Module Directory ──────────────────────────────────────────────────────────
st.markdown("### 📚 Learning Modules")
st.caption("Use the **sidebar** to navigate between modules, or explore the directory below.")

modules = [
    ("01", "🎯", "LSD Philosophy & Load Combinations",
     "Limit State Design, partial safety factors (γ_f, γ_m), load combinations per Cl. 3.5 & IS 875.",
     "Foundational"),
    ("02", "🔩", "Materials & Section Properties",
     "Structural steel grades (Fe 250–Fe 550), ISA / I-section properties, Young's modulus, yield & ultimate strength.",
     "Foundational"),
    ("03", "🔗", "Tension Members",
     "Design strength by yielding, rupture & block shear (Cl. 6). Net area, shear lag factor β.",
     "Core"),
    ("04", "🏛️", "Compression Members",
     "Column buckling curves a/b/c/d, effective length, slenderness, design compressive stress fcd (Cl. 7).",
     "Core"),
    ("05", "📐", "Beams — Flexural Members",
     "Plastic & elastic section moduli, lateral-torsional buckling, shear capacity (Cl. 8).",
     "Core"),
    ("06", "⚡", "Members under Combined Forces",
     "Interaction equations for combined bending + axial + shear (Cl. 9).",
     "Advanced"),
    ("07", "🔧", "Bolted & Welded Connections",
     "Bolt capacities (bearing, shear), weld throat, fillet & butt welds, eccentrically loaded groups (Cl. 10).",
     "Core"),
    ("08", "📝", "Self-Assessment Quiz",
     "Test your understanding across all modules with 40+ MCQ and numerical questions.",
     "Assessment"),
]

cols = st.columns(2)
for i, (num, icon, title, desc, level) in enumerate(modules):
    badge_color = {"Foundational": "#dcfce7 ; color:#166534",
                   "Core": "#dbeafe ; color:#1e40af",
                   "Advanced": "#fde68a ; color:#92400e",
                   "Assessment": "#f3e8ff ; color:#6b21a8"}[level]
    with cols[i % 2]:
        # WRAPPED THE DIV IN AN <a> TAG POINTING TO /?module=...
        st.markdown(f"""
        <a href="/?module={num}" target="_self" style="text-decoration: none; color: inherit; display: block;">
            <div class="module-card">
              <div class="badge" style="background:{badge_color};">{level}</div>
              <h4>{icon} {num}. {title}</h4>
              <p>{desc}</p>
            </div>
        </a>""", unsafe_allow_html=True)

st.markdown("---")

# ── How to Use ────────────────────────────────────────────────────────────────
st.markdown("### 🚀 How to Use This App")
a, b, c = st.columns(3)
with a:
    st.info("**Step 1 — Learn**\nRead the theory, key clauses, and formulas in each module. Clause numbers are always cited.")
with b:
    st.success("**Step 2 — Calculate**\nUse the built-in interactive calculators. Change inputs and watch results update live with step-by-step workings.")
with c:
    st.warning("**Step 3 — Quiz**\nTest yourself in the Quiz module. Track your score and revisit weak areas.")

st.markdown("""
---
<p style="text-align:center; color:#94a3b8; font-size:13px;">
Built for IS 800 : 2007 (Third Revision) · BIS · 
<a href="https://github.com/" target="_blank">View on GitHub</a>
</p>
""", unsafe_allow_html=True)
