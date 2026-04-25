import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(page_title="Compression Members | IS 800:2007", page_icon="🏛️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=IBM+Plex+Mono&display=swap');
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;}
.clause-box{background:#eff6ff;border-left:4px solid #2563eb;border-radius:0 8px 8px 0;padding:14px 18px;margin:10px 0;}
.formula-box{background:#1e293b;color:#e2e8f0;border-radius:10px;padding:18px 22px;font-family:'IBM Plex Mono',monospace;font-size:14px;margin:12px 0;}
.result-box{background:#f0fdf4;border:2px solid #22c55e;border-radius:12px;padding:20px;margin:12px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🏛️ Compression Members — Columns")
st.markdown("**IS 800:2007 — Chapter 7**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📖 Theory & Clauses", "🧮 Column Design Calculator", "📊 Buckling Curves"])

# ─── TAB 1 ────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("## Column Buckling Concept")
    st.markdown("""
    A slender column fails by **buckling** (elastic or inelastic) before reaching the material yield strength.  
    IS 800:2007 uses **multiple column curves** (a, b, c, d) based on section type and axis of buckling.
    """)

    st.markdown("## Key Formulae — Cl. 7.1")
    st.markdown("""
    <div class="formula-box">
    Step 1: Euler buckling load<br>
      P_e = π² E A / (KL/r)²<br><br>
    Step 2: Non-dimensional slenderness<br>
      λ = √(f_y / f_cc)   where f_cc = P_e/A<br><br>
    Step 3: Imperfection factor φ<br>
      φ = 0.5 [1 + α(λ − 0.2) + λ²]<br><br>
    Step 4: Reduction factor χ<br>
      χ = 1 / [φ + √(φ² − λ²)]  ≤ 1.0<br><br>
    Step 5: Design compressive stress<br>
      f_cd = χ × f_y / γ_m0<br><br>
    Step 6: Design compressive strength<br>
      P_d = A_e × f_cd
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Buckling Curves & Imperfection Factor α — Table 7")
    curve_df = pd.DataFrame({
        "Curve": ["a", "b", "c", "d"],
        "α (Imperfection factor)": [0.21, 0.34, 0.49, 0.76],
        "Typical Sections": [
            "Hot-rolled I (b/t>0.23h) — Z-Z axis",
            "Hot-rolled I (b/t<0.23h) — Z-Z; Hollow sections; Welded box",
            "Hot-rolled I — Y-Y axis; Channels, Tees",
            "Angles, Welded I (Y-Y), Built-up sections",
        ],
    })
    st.dataframe(curve_df, use_container_width=True, hide_index=True)

    st.markdown("## Effective Length Factors — Table 11")
    eff_df = pd.DataFrame({
        "Boundary Condition": [
            "Both ends pinned (Pin-Pin)",
            "Both ends fixed (Fixed-Fixed)",
            "One end fixed, other pinned (Fixed-Pin)",
            "One end fixed, other free (Cantilever)",
            "One end pinned, other fixed against rotation only",
        ],
        "Theoretical KL": ["L", "0.5L", "0.7L", "2.0L", "1.0L"],
        "IS 800 KL (recommended)": ["1.0L", "0.65L", "0.80L", "2.0L", "1.2L"],
    })
    st.dataframe(eff_df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="clause-box">
    <b>Cl. 7.3.2</b> — The slenderness ratio KL/r shall not exceed <b>180</b> for members 
    carrying compressive loads, and <b>250</b> for tension members acting as struts in secondary members.
    </div>
    """, unsafe_allow_html=True)

# ─── TAB 2: Calculator ────────────────────────────────────────────────────────
with tab2:
    st.markdown("## 🧮 Column Design — IS 800:2007 Cl. 7.1")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Material")
        fy = st.number_input("f_y (MPa)", 200, 600, 250, 25)
        E  = 200000

        st.markdown("### Section (from IS 808)")
        sections = {
            "ISMB 200": {"A": 3233, "r_z": 83.2, "r_y": 22.1, "h": 200, "bf": 100},
            "ISMB 250": {"A": 4755, "r_z": 104,  "r_y": 28.4, "h": 250, "bf": 125},
            "ISMB 300": {"A": 5813, "r_z": 122,  "r_y": 28.4, "h": 300, "bf": 140},
            "ISMB 350": {"A": 6671, "r_z": 143,  "r_y": 29.8, "h": 350, "bf": 140},
            "ISMB 400": {"A": 7846, "r_z": 162,  "r_y": 29.5, "h": 400, "bf": 140},
            "ISMB 450": {"A": 9227, "r_z": 181,  "r_y": 33.1, "h": 450, "bf": 150},
            "ISMB 500": {"A": 11074,"r_z": 202,  "r_y": 40.5, "h": 500, "bf": 180},
            "Custom": None,
        }
        sec = st.selectbox("Section", list(sections.keys()))

        if sec == "Custom":
            Ag = st.number_input("Gross area A (mm²)", 1000, 50000, 5000, 100)
            rz = st.number_input("Radius of gyration r (mm)", 10, 300, 100, 5)
        else:
            Ag = sections[sec]["A"]
            rz = sections[sec]["r_z"]
            st.info(f"A = {Ag} mm², r_z = {rz} mm")

        st.markdown("### Column Parameters")
        L  = st.number_input("Unsupported length L (m)", 1.0, 20.0, 4.0, 0.5)
        bc = st.selectbox("Boundary Condition",
                          ["Pin-Pin (K=1.0)", "Fixed-Fixed (K=0.65)",
                           "Fixed-Pin (K=0.80)", "Cantilever (K=2.0)"])
        K_map = {"Pin-Pin (K=1.0)": 1.0, "Fixed-Fixed (K=0.65)": 0.65,
                 "Fixed-Pin (K=0.80)": 0.80, "Cantilever (K=2.0)": 2.0}
        K = K_map[bc]

        curve = st.selectbox("Buckling Curve", ["a (α=0.21)", "b (α=0.34)", "c (α=0.49)", "d (α=0.76)"])
        alpha_map = {"a (α=0.21)": 0.21, "b (α=0.34)": 0.34, "c (α=0.49)": 0.49, "d (α=0.76)": 0.76}
        alpha = alpha_map[curve]

    with col2:
        st.markdown("### Results")
        KL = K * L * 1000  # mm
        KL_r = KL / rz
        gm0 = 1.10

        # Euler
        fcc = np.pi**2 * E / (KL_r)**2
        lam = np.sqrt(fy / fcc)

        # phi
        phi = 0.5 * (1 + alpha * (lam - 0.2) + lam**2)
        chi = min(1.0, 1 / (phi + np.sqrt(phi**2 - lam**2)))
        fcd = chi * fy / gm0
        Pd  = Ag * fcd / 1000  # kN

        slender_ok = KL_r <= 180
        color = "#f0fdf4" if slender_ok else "#fff7ed"
        border = "#22c55e" if slender_ok else "#f97316"

        st.markdown(f"""
        <div style="background:{color};border:2px solid {border};border-radius:12px;padding:20px;margin:8px 0;">
        <h3 style="margin:0;">Design Compressive Strength</h3>
        <h1 style="margin:8px 0;font-size:2.2rem;">P_d = {Pd:.1f} kN</h1>
        <p style="margin:0;">f_cd = χ × f_y / γ_m0 = {fcd:.1f} MPa</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Step-by-step workings:**")
        st.markdown(f"""
        - KL/r = {KL:.0f} / {rz} = **{KL_r:.1f}** {"✅ ≤ 180" if slender_ok else "⚠️ > 180 — exceeds limit!"}
        - f_cc = π²E/(KL/r)² = **{fcc:.1f} MPa**
        - λ = √(f_y/f_cc) = √({fy}/{fcc:.1f}) = **{lam:.3f}**
        - φ = 0.5[1 + α(λ−0.2) + λ²] = **{phi:.4f}**
        - χ = 1/(φ+√(φ²−λ²)) = **{chi:.4f}**
        - f_cd = {chi:.4f} × {fy} / {gm0} = **{fcd:.1f} MPa**
        - P_d = {Ag} × {fcd:.1f} / 1000 = **{Pd:.1f} kN**
        """)

# ─── TAB 3: Buckling Curves ───────────────────────────────────────────────────
with tab3:
    st.markdown("## IS 800:2007 Column Buckling Curves (a, b, c, d)")

    fy3 = st.slider("f_y (MPa)", 200, 550, 250, 25)
    gm0 = 1.10
    lam_range = np.linspace(0, 3.0, 200)

    fig = go.Figure()
    colors = {"a": "#22c55e", "b": "#3b82f6", "c": "#f59e0b", "d": "#ef4444"}
    alphas = {"a": 0.21, "b": 0.34, "c": 0.49, "d": 0.76}

    for curve_name, al in alphas.items():
        fcd_vals = []
        for lam in lam_range:
            phi = 0.5 * (1 + al * (lam - 0.2) + lam**2)
            chi = min(1.0, 1 / (phi + max(phi**2 - lam**2, 1e-10)**0.5))
            fcd_vals.append(chi * fy3 / gm0)
        fig.add_trace(go.Scatter(
            x=lam_range, y=fcd_vals,
            name=f"Curve {curve_name} (α={al})",
            line=dict(color=colors[curve_name], width=2.5),
        ))

    # Euler reference
    euler = [fy3 / (lam**2 * gm0) if lam > 0 else fy3/gm0 for lam in lam_range]
    fig.add_trace(go.Scatter(x=lam_range, y=euler, name="Euler (reference)",
                             line=dict(color="#94a3b8", width=1.5, dash="dot")))
    fig.add_hline(y=fy3/gm0, line_color="#1e293b", line_dash="dash",
                  annotation_text=f"f_y/γ_m0 = {fy3/gm0:.0f} MPa", annotation_position="right")

    fig.update_layout(
        title=f"IS 800:2007 Column Buckling Curves — f_y = {fy3} MPa",
        xaxis_title="Non-dimensional Slenderness λ",
        yaxis_title="Design Compressive Stress f_cd (MPa)",
        yaxis=dict(range=[0, fy3*1.1]),
        xaxis=dict(range=[0, 3]),
        height=460, template="plotly_white",
        legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Reading the chart:**  
    - **λ < 0.2** → No reduction (χ ≈ 1.0), full section capacity  
    - **λ ≈ 0.5–1.5** → Inelastic buckling — residual stresses and imperfections dominate  
    - **λ > 2.0** → Nearly elastic Euler buckling, very low capacity  
    - Curve **a** is least conservative (low imperfections), curve **d** is most conservative
    """)
