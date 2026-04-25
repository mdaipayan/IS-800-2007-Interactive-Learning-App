import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Beams | IS 800:2007", page_icon="📐", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=IBM+Plex+Mono&display=swap');
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;}
.clause-box{background:#eff6ff;border-left:4px solid #2563eb;border-radius:0 8px 8px 0;padding:14px 18px;margin:10px 0;}
.formula-box{background:#1e293b;color:#e2e8f0;border-radius:10px;padding:18px 22px;font-family:'IBM Plex Mono',monospace;font-size:14px;margin:12px 0;}
.result-box{background:#f0fdf4;border:2px solid #22c55e;border-radius:12px;padding:20px;margin:12px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("# 📐 Beams — Flexural Members")
st.markdown("**IS 800:2007 — Chapter 8**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📖 Theory", "🧮 Beam Design Calculator", "📊 LTB Capacity Curve"])

# ─── TAB 1 ────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("## Limit States for Beams — Cl. 8.1")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        ### Bending (Flexure)
        **Cl. 8.2**
        - Plastic section: M_d = Z_p × f_y / γ_m0
        - Compact: limited to Z_p
        - Semi-compact: M_d = Z_e × f_y / γ_m0
        """)
    with c2:
        st.markdown("""
        ### Shear
        **Cl. 8.4**
        Design shear strength:  
        V_d = V_n / γ_m0  
        V_n = A_v × f_y / √3  
        A_v = shear area (web)
        """)
    with c3:
        st.markdown("""
        ### Lateral-Torsional Buckling
        **Cl. 8.2.2**
        When compression flange is laterally unrestrained, LTB reduces M_d below plastic moment.
        """)

    st.markdown("---")
    st.markdown("## Section Classification — Cl. 3.7.2 & Table 2")
    class_df = {
        "Class": ["Plastic (Class 1)", "Compact (Class 2)", "Semi-compact (Class 3)", "Slender (Class 4)"],
        "Flange b/t_f limit (ε=√250/f_y)": ["≤ 9.4ε", "≤ 10.5ε", "≤ 15.7ε", "> 15.7ε"],
        "Web d/t_w (pure bending)": ["≤ 84ε", "≤ 105ε", "≤ 126ε", "> 126ε"],
        "Design moment capacity": ["Z_p × f_y/γ_m0", "Z_p × f_y/γ_m0", "Z_e × f_y/γ_m0", "Reduced"],
    }
    import pandas as pd
    st.dataframe(pd.DataFrame(class_df), use_container_width=True, hide_index=True)

    st.markdown("## Lateral-Torsional Buckling (LTB) — Cl. 8.2.2")
    st.markdown("""
    <div class="formula-box">
    Elastic LTB moment:<br>
    M_cr = √[EI_y × GJ] × √[1 + (π²EI_w)/(GJL²)] × π/L<br><br>
    Non-dimensional slenderness:<br>
    λ_LT = √(β_b × Z_p × f_y / M_cr)<br><br>
    LTB reduction factor:<br>
    φ_LT = 0.5[1 + α_LT(λ_LT − 0.2) + λ_LT²]<br>
    χ_LT = 1 / [φ_LT + √(φ_LT² − λ_LT²)]  ≤ 1.0<br><br>
    Design bending strength:<br>
    M_d = χ_LT × β_b × Z_p × f_y / γ_m0<br><br>
    α_LT = 0.21 (rolled), 0.49 (welded)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="clause-box">
    <b>Cl. 8.2.2</b> — LTB need not be checked if the laterally unsupported length L_LT satisfies:<br>
    L_LT ≤ r_y × 1.76/√(f_y/E)  (for plastic or compact sections)
    </div>
    """, unsafe_allow_html=True)

# ─── TAB 2: Calculator ────────────────────────────────────────────────────────
with tab2:
    st.markdown("## 🧮 Beam Flexure & Shear Design — IS 800:2007")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Material & Section")
        fy = st.number_input("f_y (MPa)", 200, 600, 250, 25)
        E  = 200000; G = 76900

        sections_data = {
            "ISMB 200": {"A":3233,"h":200,"bf":100,"tf":10.8,"tw":5.7,"Izz":2235e4,"Iyy":150e4,"Zp":252e3,"Ze":224e3,"J":12.2e4,"Iw":3920e8},
            "ISMB 300": {"A":5813,"h":300,"bf":140,"tf":12.4,"tw":7.5,"Izz":8603e4,"Iyy":453e4,"Zp":683e3,"Ze":574e3,"J":35.5e4,"Iw":45200e8},
            "ISMB 400": {"A":7846,"h":400,"bf":140,"tf":16.0,"tw":8.9,"Izz":20458e4,"Iyy":622e4,"Zp":1222e3,"Ze":1022e3,"J":73.3e4,"Iw":175000e8},
            "ISMB 500": {"A":11074,"h":500,"bf":180,"tf":17.2,"tw":10.2,"Izz":45218e4,"Iyy":1369e4,"Zp":2073e3,"Ze":1808e3,"J":118e4,"Iw":737000e8},
        }
        sec = st.selectbox("Section", list(sections_data.keys()), index=1)
        d = sections_data[sec]

        st.markdown("### Beam Parameters")
        L_LT = st.number_input("Laterally Unsupported Length L_LT (m)", 0.5, 20.0, 3.0, 0.5) * 1000  # mm
        bc = st.radio("Support Conditions", ["Simply Supported", "Cantilever", "Fixed-Fixed"])
        sec_class = st.radio("Section Class", ["Plastic / Compact", "Semi-compact"])
        weld = st.checkbox("Welded section? (α_LT = 0.49)")

    with col2:
        st.markdown("### Results")
        gm0 = 1.10
        Zp = d["Zp"]; Ze = d["Ze"]; Iy = d["Iyy"]; J = d["J"]; Iw = d["Iw"]
        Av = d["h"] * d["tw"]

        beta_b = 1.0 if sec_class == "Plastic / Compact" else Ze/Zp
        alpha_lt = 0.49 if weld else 0.21

        # Full plastic moment (no LTB)
        M_pl = beta_b * Zp * fy / gm0 / 1e6  # kN·m

        # Mcr
        eff = 1.0 if bc == "Simply Supported" else (0.7 if bc == "Cantilever" else 0.5)
        L_eff = L_LT * eff
        Mcr_sq = (np.pi**2 * E * Iy / L_eff**2) * (G*J + np.pi**2 * E * Iw / L_eff**2)
        Mcr = Mcr_sq**0.5 / 1e6  # kN·m

        lam_LT = (beta_b * Zp * fy / (Mcr * 1e6))**0.5
        phi_LT = 0.5 * (1 + alpha_lt * (lam_LT - 0.2) + lam_LT**2)
        chi_LT = min(1.0, 1 / (phi_LT + max(phi_LT**2 - lam_LT**2, 1e-10)**0.5))

        Md_LTB = chi_LT * beta_b * Zp * fy / gm0 / 1e6  # kN·m
        Vd = Av * fy / (3**0.5 * gm0) / 1000  # kN

        st.markdown(f"""
        <div class="result-box">
        <h3 style="margin:0;">Design Bending Strength</h3>
        <h1 style="margin:8px 0;font-size:2.2rem;">M_d = {Md_LTB:.1f} kN·m</h1>
        <p style="margin:0;">Reduction due to LTB: χ_LT = {chi_LT:.3f} 
        {'(No LTB — full section capacity)' if chi_LT > 0.99 else ''}</p>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Plastic Moment (no LTB)", f"{M_pl:.1f} kN·m")
        st.metric("Design Shear Capacity V_d", f"{Vd:.1f} kN")
        st.metric("M_cr (Elastic LTB)", f"{Mcr:.1f} kN·m")

        st.markdown(f"""
        **Workings:**  
        - β_b = {beta_b:.3f}, α_LT = {alpha_lt}  
        - M_cr = {Mcr:.1f} kN·m  
        - λ_LT = √(β_b Z_p f_y / M_cr) = **{lam_LT:.3f}**  
        - φ_LT = **{phi_LT:.4f}**, χ_LT = **{chi_LT:.4f}**  
        - A_v = h × t_w = {d['h']} × {d['tw']} = {Av:.0f} mm²  
        """)

# ─── TAB 3: LTB Curve ─────────────────────────────────────────────────────────
with tab3:
    st.markdown("## LTB Capacity vs. Unsupported Length")
    fy3 = st.slider("f_y (MPa)", 200, 550, 250, 25)
    sec3 = st.selectbox("Section", list(sections_data.keys()), index=2, key="ltb_sec")
    d3 = sections_data[sec3]

    lengths = np.linspace(0.5, 12.0, 80) * 1000  # mm
    Md_vals, Mpl_val = [], d3["Zp"] * fy3 / 1.10 / 1e6

    for Lx in lengths:
        McS = (np.pi**2 * E * d3["Iyy"] / Lx**2) * (G*d3["J"] + np.pi**2 * E * d3["Iw"] / Lx**2)
        Mc = McS**0.5 / 1e6
        lam = (d3["Zp"] * fy3 / (Mc * 1e6))**0.5
        phi = 0.5 * (1 + 0.21*(lam-0.2) + lam**2)
        chi = min(1.0, 1/(phi + max(phi**2 - lam**2, 1e-10)**0.5))
        Md_vals.append(chi * d3["Zp"] * fy3 / 1.10 / 1e6)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=lengths/1000, y=Md_vals, name="M_d (with LTB)",
                             line=dict(color="#2563eb", width=3),
                             fill="tozeroy", fillcolor="rgba(37,99,235,0.08)"))
    fig.add_hline(y=Mpl_val, line_color="#22c55e", line_dash="dash",
                  annotation_text=f"M_pl = {Mpl_val:.1f} kN·m", annotation_position="right")
    fig.update_layout(
        title=f"LTB Capacity vs. Unsupported Length — {sec3}, f_y={fy3} MPa",
        xaxis_title="Laterally Unsupported Length L_LT (m)",
        yaxis_title="Design Bending Strength M_d (kN·m)",
        height=420, template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("> **Note:** At short lengths χ_LT ≈ 1.0 (no LTB). As length increases, LTB reduces M_d significantly. Provide intermediate lateral restraints to maintain plastic capacity.")
