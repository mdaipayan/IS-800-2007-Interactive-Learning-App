import streamlit as st
import random

st.set_page_config(page_title="Quiz | IS 800:2007", page_icon="📝", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=IBM+Plex+Mono&display=swap');
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;}
.q-card{background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:12px;padding:22px;margin-bottom:18px;}
.correct{background:#f0fdf4;border:2px solid #22c55e;border-radius:8px;padding:12px;margin-top:8px;}
.wrong{background:#fef2f2;border:2px solid #ef4444;border-radius:8px;padding:12px;margin-top:8px;}
.score-banner{background:linear-gradient(135deg,#0f2027,#2c5364);color:white;border-radius:14px;padding:30px;text-align:center;}
</style>
""", unsafe_allow_html=True)

st.markdown("# 📝 Self-Assessment Quiz")
st.markdown("**IS 800:2007 — All Chapters**")
st.markdown("---")

# ─── Question Bank ─────────────────────────────────────────────────────────────
ALL_QUESTIONS = [
    # LSD Philosophy
    {
        "topic": "LSD Philosophy",
        "clause": "Cl. 5.4.1",
        "q": "What is the partial safety factor for material γ_m0 used in IS 800:2007 for yielding?",
        "options": ["1.00", "1.10", "1.25", "1.50"],
        "ans": "1.10",
        "explanation": "γ_m0 = 1.10 is used for the limit state of yielding and buckling (Cl. 5.4.1). γ_m1 = 1.25 is used for fracture/rupture.",
    },
    {
        "topic": "LSD Philosophy",
        "clause": "Cl. 5.4.1",
        "q": "What is γ_m1 in IS 800:2007?",
        "options": ["1.00", "1.10", "1.25", "1.50"],
        "ans": "1.25",
        "explanation": "γ_m1 = 1.25 is the partial safety factor for the limit state of rupture (fracture) at net section (Cl. 5.4.1).",
    },
    {
        "topic": "LSD Philosophy",
        "clause": "Cl. 5.3.3 Table 4",
        "q": "For the load combination DL + IL, what is the load factor for Imposed Load (γ_IL)?",
        "options": ["1.0", "1.2", "1.5", "2.0"],
        "ans": "1.5",
        "explanation": "For DL + IL combination, γ_DL = 1.5 and γ_IL = 1.5 per IS 800:2007 Table 4.",
    },
    {
        "topic": "LSD Philosophy",
        "clause": "Cl. 5.3.3",
        "q": "For DL + IL + WL combination, the partial safety factor applied to each load is:",
        "options": ["1.5 for all", "1.2 for all", "1.0 for all", "1.5 DL, 1.2 IL, 1.0 WL"],
        "ans": "1.2 for all",
        "explanation": "When all three loads (DL+IL+WL) act together, γ_f = 1.2 for each, as the probability of all maxima occurring simultaneously is lower (IS 800 Table 4).",
    },
    # Materials
    {
        "topic": "Materials",
        "clause": "Cl. 2.2.4",
        "q": "What is the modulus of elasticity E for structural steel per IS 800:2007?",
        "options": ["1×10⁵ MPa", "2×10⁵ MPa", "2.5×10⁵ MPa", "1.5×10⁵ MPa"],
        "ans": "2×10⁵ MPa",
        "explanation": "E = 2×10⁵ MPa (200 GPa) for structural steel per Cl. 2.2.4 of IS 800:2007.",
    },
    {
        "topic": "Materials",
        "clause": "IS 2062",
        "q": "The yield strength of E 250 grade steel (t ≤ 20mm) is:",
        "options": ["200 MPa", "230 MPa", "250 MPa", "300 MPa"],
        "ans": "250 MPa",
        "explanation": "E 250 (Fe 410) grade steel has f_y = 250 MPa for thickness ≤ 20mm per IS 2062.",
    },
    {
        "topic": "Materials",
        "clause": "Cl. 2.2.4",
        "q": "Poisson's ratio for structural steel (elastic range) is:",
        "options": ["0.2", "0.25", "0.3", "0.35"],
        "ans": "0.3",
        "explanation": "Poisson's ratio ν = 0.3 for structural steel in the elastic range (Cl. 2.2.4).",
    },
    # Tension Members
    {
        "topic": "Tension Members",
        "clause": "Cl. 6.2",
        "q": "The design strength of a tension member by gross section yielding (T_dg) is:",
        "options": [
            "A_g × f_y / γ_m1",
            "A_g × f_y / γ_m0",
            "0.9 × A_net × f_u / γ_m1",
            "A_g × f_u / γ_m0",
        ],
        "ans": "A_g × f_y / γ_m0",
        "explanation": "T_dg = A_g × f_y / γ_m0 (Cl. 6.2). Gross section yielding uses γ_m0 = 1.10.",
    },
    {
        "topic": "Tension Members",
        "clause": "Cl. 6.3",
        "q": "In the net section rupture formula, the factor 0.9 accounts for:",
        "options": [
            "Stress concentration at holes",
            "Non-uniform stress over net section",
            "Both stress concentration and non-uniform distribution",
            "Partial safety factor",
        ],
        "ans": "Both stress concentration and non-uniform distribution",
        "explanation": "The 0.9 factor in T_dn = 0.9 A_nc f_u / γ_m1 + β A_go f_y / γ_m0 accounts for both stress concentration at holes and non-uniform stress distribution over the net cross-section.",
    },
    {
        "topic": "Tension Members",
        "clause": "Cl. 6.4",
        "q": "Block shear failure involves:",
        "options": [
            "Shear failure along bolt line only",
            "Tension failure on net section only",
            "Simultaneous shear along bolt line and tension perpendicular to it",
            "Yielding of full gross section",
        ],
        "ans": "Simultaneous shear along bolt line and tension perpendicular to it",
        "explanation": "Block shear (Cl. 6.4) is a failure mode involving simultaneous shear yielding/fracture along the bolt line and tension fracture/yielding on the perpendicular section.",
    },
    # Compression
    {
        "topic": "Compression Members",
        "clause": "Cl. 7.3.2",
        "q": "The maximum slenderness ratio KL/r for a compression member in IS 800:2007 is:",
        "options": ["120", "150", "180", "250"],
        "ans": "180",
        "explanation": "Cl. 7.3.2 limits KL/r ≤ 180 for members under compressive loads. For tension members, the limit is 250.",
    },
    {
        "topic": "Compression Members",
        "clause": "Cl. 7.1",
        "q": "Which buckling curve in IS 800:2007 has the highest imperfection factor α?",
        "options": ["Curve a (α=0.21)", "Curve b (α=0.34)", "Curve c (α=0.49)", "Curve d (α=0.76)"],
        "ans": "Curve d (α=0.76)",
        "explanation": "Curve d (α=0.76) is the most conservative curve, used for angles and welded I-sections buckling about the minor axis.",
    },
    {
        "topic": "Compression Members",
        "clause": "Cl. 7.1 Table 11",
        "q": "The effective length KL for a column with BOTH ends FIXED is:",
        "options": ["0.5L (theoretical) / 0.65L (IS 800)", "0.7L / 0.80L", "L / 1.0L", "2L / 2L"],
        "ans": "0.5L (theoretical) / 0.65L (IS 800)",
        "explanation": "Both-ends-fixed column: theoretical KL = 0.5L. IS 800:2007 Table 11 recommends KL = 0.65L to account for practical end conditions.",
    },
    # Beams
    {
        "topic": "Beams",
        "clause": "Cl. 3.7.2",
        "q": "The shape factor (Z_p / Z_e) for a rectangular section is approximately:",
        "options": ["1.0", "1.12", "1.5", "2.0"],
        "ans": "1.5",
        "explanation": "For a rectangular section, Z_p = bh²/4 and Z_e = bh²/6, so shape factor = 1.5. For I-sections it is ~1.14.",
    },
    {
        "topic": "Beams",
        "clause": "Cl. 8.4",
        "q": "The design shear strength of a beam web per IS 800:2007 is:",
        "options": [
            "A_v × f_y / γ_m0",
            "A_v × f_y / (√3 × γ_m0)",
            "A_v × f_u / γ_m1",
            "A_g × f_y / (√3 × γ_m0)",
        ],
        "ans": "A_v × f_y / (√3 × γ_m0)",
        "explanation": "V_d = V_n / γ_m0 where V_n = A_v f_y / √3 per Von Mises yield criterion (Cl. 8.4.1). A_v = shear area (web).",
    },
    {
        "topic": "Beams",
        "clause": "Cl. 8.2.2",
        "q": "Lateral-Torsional Buckling (LTB) in beams is caused by:",
        "options": [
            "Excessive vertical deflection",
            "Buckling of the compression flange laterally with section twisting",
            "Shear yielding of the web",
            "Fatigue under cyclic loading",
        ],
        "ans": "Buckling of the compression flange laterally with section twisting",
        "explanation": "LTB occurs when the compression flange buckles laterally while the section twists. It reduces the bending capacity below the plastic moment (Cl. 8.2.2).",
    },
    # Connections
    {
        "topic": "Connections",
        "clause": "Cl. 10.3.3",
        "q": "In IS 800:2007, the nominal capacity of a bolt in shear uses:",
        "options": [
            "f_ub × A_gross",
            "f_ub / √3 × A_net (shear area)",
            "f_yb × A_gross",
            "f_ub × A_gross / √2",
        ],
        "ans": "f_ub / √3 × A_net (shear area)",
        "explanation": "V_nsb = f_ub / √3 × A_nb (net shear area), based on Von Mises criterion. A_nb = 0.78 × A_gross when threads are in the shear plane (Cl. 10.3.3).",
    },
    {
        "topic": "Connections",
        "clause": "Cl. 10.5.7",
        "q": "The effective throat thickness of a fillet weld (weld size s) is:",
        "options": ["0.5s", "0.6s", "0.7s", "s"],
        "ans": "0.7s",
        "explanation": "For a fillet weld, the effective throat thickness = 0.7 × s (weld leg size) for a 45° fillet (Cl. 10.5.3.2).",
    },
    {
        "topic": "Connections",
        "clause": "Cl. 10.2.3.1",
        "q": "Minimum pitch (spacing) of bolts in IS 800:2007 is:",
        "options": [
            "2.0 × bolt diameter",
            "2.5 × bolt diameter",
            "3.0 × bolt diameter",
            "4.0 × bolt diameter",
        ],
        "ans": "2.5 × bolt diameter",
        "explanation": "Minimum pitch = 2.5 × nominal diameter of bolt (Cl. 10.2.3.1). This allows sufficient space for bolt installation and prevents overlap failure.",
    },
    {
        "topic": "Connections",
        "clause": "Cl. 10.5.7",
        "q": "The partial safety factor γ_mw for welds in IS 800:2007 is:",
        "options": ["1.00", "1.10", "1.25", "1.50"],
        "ans": "1.25",
        "explanation": "γ_mw = 1.25 for weld capacity calculations (Cl. 10.5.7). Same as γ_m1 for rupture.",
    },
]

# ─── Quiz Logic ────────────────────────────────────────────────────────────────
if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = "start"
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "q_order" not in st.session_state:
    st.session_state.q_order = list(range(len(ALL_QUESTIONS)))

topics = sorted(set(q["topic"] for q in ALL_QUESTIONS))
sel_topics = st.multiselect("Filter by topic", topics, default=topics)
n_q = st.slider("Number of questions", 5, len(ALL_QUESTIONS), 10)

filtered_qs = [q for q in ALL_QUESTIONS if q["topic"] in sel_topics]

col_a, col_b, col_c = st.columns([1,1,4])
if col_a.button("🎲 Start / New Quiz", type="primary"):
    pool = filtered_qs.copy()
    random.shuffle(pool)
    st.session_state.quiz_qs = pool[:n_q]
    st.session_state.answers = {}
    st.session_state.quiz_state = "active"
    st.session_state.submitted = False

if col_b.button("🔄 Reset"):
    st.session_state.quiz_state = "start"
    st.session_state.answers = {}

st.markdown("---")

if st.session_state.quiz_state == "start":
    st.info("👆 Click **Start / New Quiz** to begin. Select topics and number of questions above.")

elif st.session_state.quiz_state == "active":
    qs = st.session_state.quiz_qs
    submitted = st.session_state.get("submitted", False)

    for i, q in enumerate(qs):
        st.markdown(f"""
        <div class="q-card">
        <span style="font-size:12px;font-weight:700;color:#64748b;text-transform:uppercase;
              letter-spacing:.08em;">{q['topic']} · {q['clause']}</span>
        <h4 style="margin:8px 0 0;">Q{i+1}. {q['q']}</h4>
        </div>
        """, unsafe_allow_html=True)

        if submitted:
            user_ans = st.session_state.answers.get(i, None)
            for opt in q["options"]:
                if opt == q["ans"]:
                    st.markdown(f"✅ **{opt}** ← Correct")
                elif opt == user_ans:
                    st.markdown(f"❌ ~~{opt}~~")
                else:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;{opt}")
            exp_color = "#f0fdf4" if user_ans == q["ans"] else "#fef2f2"
            st.markdown(f"""
            <div style="background:{exp_color};border-radius:8px;padding:12px;margin-top:4px;">
            📖 <b>Explanation ({q['clause']}):</b> {q['explanation']}
            </div>
            """, unsafe_allow_html=True)
        else:
            ans = st.radio(f"Q{i+1}", q["options"], index=None,
                           key=f"q_{i}", label_visibility="collapsed")
            if ans:
                st.session_state.answers[i] = ans

        st.markdown("")

    if not submitted:
        if st.button("✅ Submit Quiz", type="primary", use_container_width=True):
            st.session_state.submitted = True
            st.rerun()
    else:
        # Score
        score = sum(1 for i, q in enumerate(qs)
                    if st.session_state.answers.get(i) == q["ans"])
        pct = score / len(qs) * 100
        grade = "🏆 Excellent" if pct >= 80 else ("👍 Good" if pct >= 60 else "📚 Keep Studying")
        st.markdown(f"""
        <div class="score-banner">
        <h2 style="margin:0;">{grade}</h2>
        <h1 style="font-size:3rem;margin:12px 0;">{score} / {len(qs)}</h1>
        <p style="font-size:1.2rem;opacity:0.85;">{pct:.0f}% — IS 800:2007 Quiz</p>
        </div>
        """, unsafe_allow_html=True)

        # Per-topic breakdown
        st.markdown("### Topic Breakdown")
        topic_scores = {}
        for i, q in enumerate(qs):
            t = q["topic"]
            correct = st.session_state.answers.get(i) == q["ans"]
            if t not in topic_scores:
                topic_scores[t] = [0, 0]
            topic_scores[t][1] += 1
            if correct:
                topic_scores[t][0] += 1

        for t, (c, tot) in topic_scores.items():
            pct_t = c/tot*100
            bar_col = "#22c55e" if pct_t >= 70 else ("#f59e0b" if pct_t >= 50 else "#ef4444")
            st.markdown(f"""
            <div style="margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span style="font-weight:600;">{t}</span>
                <span>{c}/{tot} ({pct_t:.0f}%)</span>
            </div>
            <div style="background:#e2e8f0;border-radius:4px;height:10px;">
            <div style="background:{bar_col};width:{pct_t}%;height:10px;border-radius:4px;"></div>
            </div>
            </div>
            """, unsafe_allow_html=True)
