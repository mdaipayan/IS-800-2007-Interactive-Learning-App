import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Materials | IS 800:2007", page_icon="🔩", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=IBM+Plex+Mono&display=swap');
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;}
.clause-box{background:#eff6ff;border-left:4px solid #2563eb;border-radius:0 8px 8px 0;padding:14px 18px;margin:10px 0;}
.formula-box{background:#1e293b;color:#e2e8f0;border-radius:10px;padding:18px 22px;font-family:'IBM Plex Mono',monospace;font-size:14px;margin:12px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔩 Materials & Section Properties")
st.markdown("**IS 800:2007 — Chapter 2 | IS 2062 | IS 808**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📖 Steel Grades", "📐 Section Properties", "📊 Stress-Strain Curve"])

# ─── TAB 1: Steel Grades ──────────────────────────────────────────────────────
with tab1:
    st.markdown("## Structural Steel Grades — IS 2062")
    st.markdown("""
    <div class="clause-box">
    <b>Clause 2.2</b> — Steel conforming to IS 2062 shall be used. The grade designation 
    includes the yield and tensile strength characteristics.
    </div>
    """, unsafe_allow_html=True)

    grades_df = pd.DataFrame({
        "Grade": ["E 250 (Fe 410)", "E 300 (Fe 440)", "E 350 (Fe 490)", "E 410 (Fe 540)", "E 450 (Fe 570/590)", "E 550 (Fe 650)"],
        "f_y (MPa) — t≤20mm": [250, 300, 350, 410, 450, 550],
        "f_y (MPa) — 20<t≤40mm": [240, 290, 330, 390, 430, 530],
        "f_y (MPa) — t>40mm": [230, 280, 320, 380, 420, 520],
        "f_u (MPa)": [410, 440, 490, 540, 570, 650],
        "Elongation (%)": [23, 22, 22, 20, 20, 18],
        "IS 2062 Grade": ["A/B/C", "A/B", "A/B/C", "A/B", "A/B", "A"],
    })

    st.dataframe(grades_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("## Material Constants — Cl. 2.2.4")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Young's Modulus (E)", "2×10⁵ MPa", "200 GPa")
    col2.metric("Shear Modulus (G)", "0.769×10⁵ MPa", "76.9 GPa")
    col3.metric("Poisson's Ratio (ν)", "0.3", "Elastic range")
    col4.metric("Thermal Coeff. (α)", "12×10⁻⁶ /°C", "")

    st.markdown("""
    <div class="formula-box">
    G = E / [2(1+ν)] = 2×10⁵ / [2(1+0.3)] = 0.769×10⁵ MPa<br>
    Unit weight of steel = 78.5 kN/m³  (Cl. 2.2.4)<br>
    Density             = 7850 kg/m³
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    grade_sel = st.selectbox("🔍 Grade Selector — Pick a grade for quick reference:", grades_df["Grade"].tolist())
    row = grades_df[grades_df["Grade"] == grade_sel].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric(f"f_y (t≤20mm)", f"{row['f_y (MPa) — t≤20mm']} MPa")
    col2.metric("f_u", f"{row['f_u (MPa)']} MPa")
    col3.metric("Elongation", f"{row['Elongation (%)']} %")

    fy = row['f_y (MPa) — t≤20mm']
    fu = row['f_u (MPa)']
    st.info(f"**Design yield stress** = f_y / γ_m0 = {fy}/{1.10:.2f} = **{fy/1.10:.1f} MPa**  \n"
            f"**Design rupture stress** = 0.9 f_u / γ_m1 = 0.9×{fu}/{1.25:.2f} = **{0.9*fu/1.25:.1f} MPa**")

# ─── TAB 2: Section Properties ────────────────────────────────────────────────
with tab2:
    st.markdown("## Standard I-Section Properties — IS 808")
    st.markdown("""
    <div class="clause-box">
    <b>IS 808 : 1989</b> — Dimensions and section properties of hot-rolled steel beams, 
    columns, channels, and angles.
    </div>
    """, unsafe_allow_html=True)

    sections = pd.DataFrame({
        "Section": ["ISMB 100", "ISMB 150", "ISMB 200", "ISMB 250", "ISMB 300",
                    "ISMB 350", "ISMB 400", "ISMB 450", "ISMB 500", "ISMB 600"],
        "h (mm)": [100, 150, 200, 250, 300, 350, 400, 450, 500, 600],
        "b_f (mm)": [75, 80, 100, 125, 140, 140, 140, 150, 180, 210],
        "t_w (mm)": [4.0, 4.8, 5.7, 6.9, 7.5, 8.1, 8.9, 9.4, 10.2, 12.0],
        "t_f (mm)": [7.2, 7.6, 10.8, 12.5, 12.4, 14.2, 16.0, 17.4, 17.2, 20.3],
        "A (cm²)": [14.6, 19.8, 32.3, 47.1, 58.0, 66.7, 78.5, 92.3, 110.0, 156.0],
        "I_zz (cm⁴)": [257, 726, 2235, 5131, 8603, 13630, 20458, 30390, 45218, 91813],
        "Z_p (cm³)": [57.5, 108, 252, 459, 683, 980, 1222, 1601, 2073, 3574],
        "r_zz (cm)": [4.19, 6.05, 8.32, 10.4, 12.2, 14.3, 16.2, 18.1, 20.2, 24.2],
    })

    st.dataframe(sections, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🔍 Section Quick-Check")
    sec_sel = st.selectbox("Select Section:", sections["Section"].tolist(), index=4)
    row = sections[sections["Section"] == sec_sel].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Depth h", f"{row['h (mm)']} mm")
    c2.metric("Flange Width b_f", f"{row['b_f (mm)']} mm")
    c3.metric("I_zz", f"{row['I_zz (cm⁴)']} cm⁴")
    c4.metric("Z_p (Plastic)", f"{row['Z_p (cm³)']} cm³")

    Iy = row['I_zz (cm⁴)']
    Zp = row['Z_p (cm³)']
    Ze = 2 * Iy / row['h (mm)'] * 10   # cm³
    beta_b = Zp / Ze
    st.info(f"**Elastic Modulus Z_e** = 2I_zz/h = {Ze:.1f} cm³  \n"
            f"**Shape Factor β_b** = Z_p/Z_e = {Zp}/{Ze:.1f} = **{beta_b:.3f}**  \n"
            f"*(Shape factor > 1.0 indicates plastic reserve capacity)*")

# ─── TAB 3: Stress-Strain ─────────────────────────────────────────────────────
with tab3:
    st.markdown("## Idealised Stress-Strain Curve for Structural Steel")

    fy_val = st.slider("Yield Strength f_y (MPa)", 200, 600, 250, 25)
    fu_val = st.slider("Ultimate Strength f_u (MPa)", 350, 700, 410, 25)

    # Build bilinear with strain hardening
    E = 200000  # MPa
    eps_y = fy_val / E
    eps_sh = 0.015
    eps_u = 0.20
    eps_frac = 0.23

    strain = [0, eps_y, eps_sh, eps_u, eps_frac]
    stress = [0, fy_val, fy_val, fu_val, 0.85 * fu_val]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[s*100 for s in strain], y=stress,
                             mode="lines+markers", name="Steel",
                             line=dict(color="#2563eb", width=3),
                             marker=dict(size=8)))

    # Annotations
    fig.add_annotation(x=eps_y*100, y=fy_val, text=f"f_y = {fy_val} MPa<br>(ε_y = {eps_y*100:.4f}%)",
                       showarrow=True, arrowhead=2, ax=40, ay=-40, font=dict(size=11))
    fig.add_annotation(x=eps_u*100, y=fu_val, text=f"f_u = {fu_val} MPa",
                       showarrow=True, arrowhead=2, ax=-40, ay=-40, font=dict(size=11))

    fig.add_vrect(x0=0, x1=eps_y*100, fillcolor="rgba(34,197,94,0.1)",
                  annotation_text="Elastic", annotation_position="top left")
    fig.add_vrect(x0=eps_y*100, x1=eps_sh*100, fillcolor="rgba(251,191,36,0.1)",
                  annotation_text="Yield Plateau")
    fig.add_vrect(x0=eps_sh*100, x1=eps_u*100, fillcolor="rgba(239,68,68,0.1)",
                  annotation_text="Strain Hardening")

    fig.update_layout(
        title=f"Stress-Strain Curve — Steel (f_y={fy_val} MPa, f_u={fu_val} MPa)",
        xaxis_title="Strain ε (%)",
        yaxis_title="Stress σ (MPa)",
        height=450, template="plotly_white",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    **Key observations for f_y = {fy_val} MPa:**
    - **Elastic range:** up to ε = {eps_y*100:.3f}% — Hooke's Law applies (E = {E//1000} GPa)
    - **Yield plateau:** constant stress at {fy_val} MPa — large plastic strains develop
    - **Strain hardening:** stress rises to f_u = {fu_val} MPa at ε ≈ {eps_u*100:.0f}%
    - **Fracture:** at ε ≈ {eps_frac*100:.0f}% — elongation meets IS 2062 requirement
    """)
