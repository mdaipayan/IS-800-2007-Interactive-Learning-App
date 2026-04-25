import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="LSD Philosophy | IS 800:2007", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=IBM+Plex+Mono&display=swap');
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;}
.clause-box{background:#eff6ff;border-left:4px solid #2563eb;border-radius:0 8px 8px 0;padding:14px 18px;margin:10px 0;}
.formula-box{background:#1e293b;color:#e2e8f0;border-radius:10px;padding:18px 22px;font-family:'IBM Plex Mono',monospace;font-size:14px;margin:12px 0;}
.note-box{background:#fef9c3;border-left:4px solid #eab308;border-radius:0 8px 8px 0;padding:12px 16px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🎯 Limit State Design Philosophy")
st.markdown("**IS 800:2007 — Chapter 3 & 5**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📖 Theory", "🧮 Load Combination Calculator", "📊 Visualization"])

# ─── TAB 1: Theory ────────────────────────────────────────────────────────────
with tab1:
    st.markdown("## What is Limit State Design?")
    st.markdown("""
    IS 800:2007 adopts the **Limit State Method (LSM)** — a shift from the older Working Stress Method (WSM).
    The structure must satisfy two fundamental criteria:
    """)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        #### 🔴 Ultimate Limit States (ULS)
        Concern **collapse or structural failure**:
        - Loss of static equilibrium
        - Failure by excessive deformation
        - Fracture due to fatigue
        - Brittle fracture
        
        > *Design against improbable but catastrophic events.*
        """)
    with c2:
        st.markdown("""
        #### 🟡 Serviceability Limit States (SLS)
        Concern **loss of functionality**:
        - Excessive deflection (span/300 for beams)
        - Excessive vibration
        - Corrosion and durability
        - Fire resistance
        
        > *Design to maintain normal use conditions.*
        """)

    st.markdown("---")
    st.markdown("## Partial Safety Factors")

    st.markdown("""
    <div class="clause-box">
    <b>Clause 5.3.3</b> — Partial safety factor for material (γ<sub>m</sub>) accounts for 
    variability in material strength and manufacturing imperfections.
    </div>
    """, unsafe_allow_html=True)

    data = {
        "Resistance": ["Yielding (γ_m0)", "Rupture (γ_m1)", "Bolt Bearing (γ_mb)", "Weld (γ_mw)"],
        "Symbol": ["γ_m0", "γ_m1", "γ_mb", "γ_mw"],
        "Value": [1.10, 1.25, 1.25, 1.25],
        "Clause": ["Cl. 5.4.1", "Cl. 5.4.1", "Cl. 10.3.2", "Cl. 10.5.7"],
    }
    import pandas as pd
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("## Partial Safety Factors for Loads (γ_f)")

    st.markdown("""
    <div class="clause-box">
    <b>Clause 5.3.1 & Table 4</b> — Load factors for Ultimate Limit State design combinations.
    </div>
    """, unsafe_allow_html=True)

    load_data = {
        "Combination": [
            "DL + IL",
            "DL + WL/EL",
            "DL + IL + WL/EL",
            "DL + IL + Erection",
        ],
        "Dead Load (γ_DL)": [1.5, 1.5, 1.2, 1.5],
        "Imposed Load (γ_IL)": [1.5, "–", 1.2, 1.05],
        "Wind/EQ (γ_WL)": ["–", 1.5, 1.2, "–"],
    }
    st.dataframe(pd.DataFrame(load_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("## Key Design Equation")
    st.markdown("""
    <div class="formula-box">
    Design Action ≤ Design Resistance<br><br>
    γ_f × Q_k  ≤  f_y / γ_m0  (for yielding)<br>
    γ_f × Q_k  ≤  f_u / γ_m1  (for rupture)<br><br>
    Where:<br>
    Q_k = Characteristic load<br>
    f_y  = Yield strength of steel<br>
    f_u  = Ultimate tensile strength<br>
    γ_f  = Partial safety factor for load<br>
    γ_m0 = 1.10  (Cl. 5.4.1)<br>
    γ_m1 = 1.25  (Cl. 5.4.1)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="note-box">
    ⚠️ <b>Important:</b> IS 800:2007 uses characteristic values at 5% probability of not being exceeded 
    for material strengths, and 95% probability for load effects.
    </div>
    """, unsafe_allow_html=True)

# ─── TAB 2: Calculator ────────────────────────────────────────────────────────
with tab2:
    st.markdown("## 🧮 Factored Load Combination Calculator")
    st.markdown("Compute the factored design load per **IS 800:2007 Table 4** (Cl. 5.3.3)")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Input Characteristic Loads")
        DL = st.number_input("Dead Load, G_k (kN or kN/m)", value=50.0, step=5.0)
        IL = st.number_input("Imposed Live Load, Q_k (kN or kN/m)", value=30.0, step=5.0)
        WL = st.number_input("Wind Load, W_k (kN or kN/m)", value=15.0, step=5.0)
        EL = st.number_input("Seismic/EQ Load, E_k (kN or kN/m)", value=0.0, step=5.0)

        combo = st.selectbox("Load Combination", [
            "DL + IL  (γ_DL=1.5, γ_IL=1.5)",
            "DL + WL  (γ_DL=1.5, γ_WL=1.5)",
            "DL + EL  (γ_DL=1.5, γ_EL=1.5)",
            "DL + IL + WL  (γ_DL=1.2, γ_IL=1.2, γ_WL=1.2)",
            "DL + IL + EL  (γ_DL=1.2, γ_IL=1.2, γ_EL=1.2)",
        ])

    with col2:
        st.markdown("### Results")
        combos_map = {
            "DL + IL  (γ_DL=1.5, γ_IL=1.5)":             (1.5, 1.5, 0.0, 0.0),
            "DL + WL  (γ_DL=1.5, γ_WL=1.5)":             (1.5, 0.0, 1.5, 0.0),
            "DL + EL  (γ_DL=1.5, γ_EL=1.5)":             (1.5, 0.0, 0.0, 1.5),
            "DL + IL + WL  (γ_DL=1.2, γ_IL=1.2, γ_WL=1.2)": (1.2, 1.2, 1.2, 0.0),
            "DL + IL + EL  (γ_DL=1.2, γ_IL=1.2, γ_EL=1.2)": (1.2, 1.2, 0.0, 1.2),
        }
        gDL, gIL, gWL, gEL = combos_map[combo]
        factored = gDL*DL + gIL*IL + gWL*WL + gEL*EL

        st.markdown(f"""
        <div style="background:#f0fdf4;border:2px solid #22c55e;border-radius:12px;padding:24px;margin-top:8px;">
        <h3 style="margin:0;color:#15803d;">Factored Design Load</h3>
        <h1 style="margin:8px 0;color:#166534;font-size:2.4rem;">{factored:.2f} <span style="font-size:1.2rem;">kN or kN/m</span></h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Step-by-step workings:**")
        steps = []
        if gDL: steps.append(f"  γ_DL × G_k = {gDL} × {DL} = **{gDL*DL:.2f}**")
        if gIL: steps.append(f"  γ_IL × Q_k = {gIL} × {IL} = **{gIL*IL:.2f}**")
        if gWL: steps.append(f"  γ_WL × W_k = {gWL} × {WL} = **{gWL*WL:.2f}**")
        if gEL: steps.append(f"  γ_EL × E_k = {gEL} × {EL} = **{gEL*EL:.2f}**")
        for s in steps:
            st.markdown(s)
        st.markdown(f"  **Total Factored Load = {factored:.2f}**")

# ─── TAB 3: Visualization ─────────────────────────────────────────────────────
with tab3:
    st.markdown("## 📊 Reliability Concept — WSM vs LSM")

    x = np.linspace(0, 1, 300)
    load_pdf = np.exp(-((x - 0.4)**2) / (2 * 0.07**2))
    resist_pdf = np.exp(-((x - 0.65)**2) / (2 * 0.07**2))
    load_pdf /= load_pdf.max()
    resist_pdf /= resist_pdf.max()
    overlap = np.minimum(load_pdf, resist_pdf)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=load_pdf, name="Load Effect (S)", fill="tozeroy",
                             fillcolor="rgba(239,68,68,0.2)", line=dict(color="#ef4444", width=2)))
    fig.add_trace(go.Scatter(x=x, y=resist_pdf, name="Resistance (R)", fill="tozeroy",
                             fillcolor="rgba(34,197,94,0.2)", line=dict(color="#22c55e", width=2)))
    fig.add_trace(go.Scatter(x=x, y=overlap, name="Failure Zone (R < S)", fill="tozeroy",
                             fillcolor="rgba(239,68,68,0.5)", line=dict(color="rgba(0,0,0,0)")))
    fig.update_layout(
        title="Probability Distributions of Load Effect vs Resistance",
        xaxis_title="Magnitude (normalized)",
        yaxis_title="Probability Density",
        legend=dict(orientation="h", y=1.1),
        height=400, template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    > **Interpretation:** The shaded red overlap zone represents the probability of failure (R < S).  
    > LSD explicitly quantifies and minimises this zone using partial safety factors γ_f and γ_m,  
    > unlike the old WSM which used a single global factor of safety.
    """)

    # Sensitivity bar chart
    st.markdown("### Load Factor Contribution — Selected Combination")
    DLv, ILv, WLv, ELv = 50.0, 30.0, 15.0, 0.0
    gDL2, gIL2, gWL2, gEL2 = 1.2, 1.2, 1.2, 0.0
    labels = ["Dead Load", "Live Load", "Wind Load"]
    values = [gDL2*DLv, gIL2*ILv, gWL2*WLv]
    fig2 = go.Figure(go.Bar(x=labels, y=values,
                            marker_color=["#2563eb","#f59e0b","#10b981"],
                            text=[f"{v:.1f}" for v in values], textposition="outside"))
    fig2.update_layout(title="Factored Load Contributions (DL+IL+WL, γ=1.2)",
                       yaxis_title="Factored Value (kN)", height=350, template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)
