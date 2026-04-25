import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Tension Members | IS 800:2007", page_icon="🔗", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=IBM+Plex+Mono&display=swap');
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;}
.clause-box{background:#eff6ff;border-left:4px solid #2563eb;border-radius:0 8px 8px 0;padding:14px 18px;margin:10px 0;}
.formula-box{background:#1e293b;color:#e2e8f0;border-radius:10px;padding:18px 22px;font-family:'IBM Plex Mono',monospace;font-size:14px;margin:12px 0;}
.result-box{background:#f0fdf4;border:2px solid #22c55e;border-radius:12px;padding:20px;margin:12px 0;}
.warn-box{background:#fff7ed;border-left:4px solid #f97316;border-radius:0 8px 8px 0;padding:12px 16px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔗 Tension Members")
st.markdown("**IS 800:2007 — Chapter 6**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📖 Theory & Clauses", "🧮 Design Calculator", "📊 Interaction Diagram"])

# ─── TAB 1: Theory ────────────────────────────────────────────────────────────
with tab1:
    st.markdown("## Modes of Failure")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        ### 1. Gross Yielding
        **Cl. 6.2**  
        Yielding of the gross cross-section away from the connection.
        
        **Governs:** Long members with small holes
        """)
        st.markdown("""
        <div class="formula-box">
        T_dg = f_y × A_g / γ_m0<br><br>
        A_g = Gross cross-sectional area<br>
        f_y = Yield strength (MPa)<br>
        γ_m0 = 1.10
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        ### 2. Net Section Rupture
        **Cl. 6.3**  
        Fracture of the net cross-section through bolt holes.
        
        **Governs:** Short members with large bolt holes
        """)
        st.markdown("""
        <div class="formula-box">
        T_dn = 0.9 × A_nc × f_u / γ_m1<br>
              + β × A_go × f_y / γ_m0<br><br>
        A_nc = Net area connected<br>
        A_go = Outstanding gross area<br>
        β    = 1.4 − 0.076(w/t)(f_y/f_u)(b_s/L_c)<br>
        γ_m1 = 1.25
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        ### 3. Block Shear
        **Cl. 6.4**  
        Simultaneous shear + tension failure block.
        
        **Governs:** Angle connected by one leg (gusset)
        """)
        st.markdown("""
        <div class="formula-box">
        T_db = min(T_db1, T_db2)<br><br>
        T_db1 = A_vg×f_y/(√3×γ_m0)<br>
                + 0.9×A_tn×f_u/γ_m1<br><br>
        T_db2 = 0.9×A_vn×f_u/(√3×γ_m1)<br>
                + A_tg×f_y/γ_m0
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## Design Tensile Strength")
    st.markdown("""
    <div class="clause-box">
    <b>Cl. 6.1</b> — The design strength of a tension member, <b>T_d = min(T_dg, T_dn, T_db)</b>.
    The applied factored tensile force T_u must not exceed T_d.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Shear Lag Factor β")
    st.markdown("""
    For angles connected by **one leg only**, the outstanding leg introduces shear lag.  
    The factor β reduces the effective net area:
    """)
    st.markdown("""
    <div class="formula-box">
    β = 1.4 − 0.076 × (w/t) × (f_y/f_u) × (b_s/L_c)<br><br>
    Where:<br>
    w   = width of outstanding leg<br>
    t   = thickness<br>
    b_s = shear lag width = w + w_c − t (w_c = connected leg width)<br>
    L_c = length of connection (centre-to-centre of end bolts)<br><br>
    Limits: 0.7 ≤ β ≤ (f_u × γ_m0) / (f_y × γ_m1)
    </div>
    """, unsafe_allow_html=True)

# ─── TAB 2: Calculator ────────────────────────────────────────────────────────
with tab2:
    st.markdown("## 🧮 Tension Member Design — IS 800:2007 Cl. 6")

    col_inp, col_out = st.columns([1, 1])
    with col_inp:
        st.markdown("### Member & Material")
        fy = st.number_input("Yield strength f_y (MPa)", 200, 600, 250, 25)
        fu = st.number_input("Ultimate strength f_u (MPa)", 350, 700, 410, 25)

        st.markdown("### Section Dimensions (ISA Angle)")
        wc = st.number_input("Connected leg width w_c (mm)", 40, 200, 90, 5)
        wo = st.number_input("Outstanding leg width w_o (mm)", 40, 200, 90, 5)
        t  = st.number_input("Thickness t (mm)", 4, 25, 8, 1)

        st.markdown("### Connection Details")
        n_bolt = st.number_input("Number of bolts in line", 1, 10, 3, 1)
        d_bolt = st.number_input("Bolt hole diameter d_h (mm)", 12, 30, 18, 1)
        pitch  = st.number_input("Pitch p (mm)", 40, 200, 60, 5)

    with col_out:
        st.markdown("### Step-by-Step Results")
        gm0 = 1.10; gm1 = 1.25

        # Gross area (angle)
        Ag = (wc + wo - t) * t
        # Net area of connected leg
        Anc = (wc - d_bolt/2 - t/2) * t  # approx net of connected leg
        Ago = wo * t  # outstanding leg gross

        # Lc
        Lc = (n_bolt - 1) * pitch if n_bolt > 1 else pitch

        # Beta
        w  = wo
        bs = wo + wc - t
        beta_raw = 1.4 - 0.076 * (w/t) * (fy/fu) * (bs/Lc)
        beta_max = (fu * gm0) / (fy * gm1)
        beta = max(0.7, min(beta_raw, beta_max))

        # Design strengths
        Tdg = fy * Ag / gm0 / 1000        # kN
        Tdn = (0.9 * Anc * fu / gm1 + beta * Ago * fy / gm0) / 1000   # kN

        # Block shear (simplified — connected leg)
        Avg = wc * t  # shear area gross
        Avn = (wc - (n_bolt * d_bolt / 2)) * t  # approx
        Atg = wo * t
        Atn = (wo - d_bolt/2) * t

        Tdb1 = (Avg * fy / (3**0.5 * gm0) + 0.9 * Atn * fu / gm1) / 1000
        Tdb2 = (0.9 * Avn * fu / (3**0.5 * gm1) + Atg * fy / gm0) / 1000
        Tdb  = min(Tdb1, Tdb2)

        Td = min(Tdg, Tdn, Tdb)
        governing = ["Gross Yielding", "Net Rupture", "Block Shear"][[Tdg, Tdn, Tdb].index(Td)]

        st.markdown(f"""
        | Check | Value (kN) |
        |---|---|
        | T_dg — Gross Yielding | **{Tdg:.2f}** |
        | T_dn — Net Rupture | **{Tdn:.2f}** |
        | T_db — Block Shear | **{Tdb:.2f}** |
        """)

        st.markdown(f"""
        <div class="result-box">
        <b>Design Tensile Strength T_d = {Td:.2f} kN</b><br>
        Governing failure mode: <b>{governing}</b><br>
        Shear Lag Factor β = {beta:.3f}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        **Key intermediate values:**  
        - Gross area A_g = {Ag:.0f} mm²  
        - Net connected area A_nc ≈ {Anc:.0f} mm²  
        - Outstanding gross A_go = {Ago:.0f} mm²  
        - Connection length L_c = {Lc:.0f} mm  
        - β_raw = {beta_raw:.3f} → β = {beta:.3f}
        """)

# ─── TAB 3: Interaction ───────────────────────────────────────────────────────
with tab3:
    st.markdown("## Effect of Number of Bolts on Design Strength")
    st.markdown("Watch how T_dg, T_dn, and T_db vary with number of bolts in line.")

    fy2, fu2, wc2, wo2, t2, dh2, p2 = 250, 410, 90, 90, 8, 18, 60
    bolts_range = range(1, 9)
    Tdg_list, Tdn_list, Tdb_list, Td_list = [], [], [], []

    for nb in bolts_range:
        Ag2 = (wc2 + wo2 - t2) * t2
        Anc2 = (wc2 - dh2/2 - t2/2) * t2
        Ago2 = wo2 * t2
        Lc2 = max((nb-1)*p2, p2)
        bs2 = wo2 + wc2 - t2
        b2 = max(0.7, min(1.4 - 0.076*(wo2/t2)*(fy2/fu2)*(bs2/Lc2),
                          (fu2*1.10)/(fy2*1.25)))
        tdg = fy2*Ag2/1.10/1000
        tdn = (0.9*Anc2*fu2/1.25 + b2*Ago2*fy2/1.10)/1000
        Avg2 = wc2*t2; Avn2 = max((wc2 - nb*dh2/2)*t2, 10)
        Atg2 = wo2*t2; Atn2 = (wo2 - dh2/2)*t2
        tdb1 = (Avg2*fy2/(3**0.5*1.10) + 0.9*Atn2*fu2/1.25)/1000
        tdb2 = (0.9*Avn2*fu2/(3**0.5*1.25) + Atg2*fy2/1.10)/1000
        tdb  = min(tdb1, tdb2)
        Tdg_list.append(tdg); Tdn_list.append(tdn)
        Tdb_list.append(tdb); Td_list.append(min(tdg, tdn, tdb))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(bolts_range), y=Tdg_list, name="T_dg (Gross Yielding)",
                             line=dict(color="#22c55e", width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=list(bolts_range), y=Tdn_list, name="T_dn (Net Rupture)",
                             line=dict(color="#f59e0b", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=list(bolts_range), y=Tdb_list, name="T_db (Block Shear)",
                             line=dict(color="#ef4444", width=2, dash="dashdot")))
    fig.add_trace(go.Scatter(x=list(bolts_range), y=Td_list, name="T_d (Design — Governing)",
                             line=dict(color="#2563eb", width=3),
                             fill="tozeroy", fillcolor="rgba(37,99,235,0.08)"))

    fig.update_layout(
        title="Design Tensile Strength vs Number of Bolts (ISA 90×90×8, Fe 250)",
        xaxis_title="Number of Bolts in Line",
        yaxis_title="Tensile Capacity T_d (kN)",
        height=420, template="plotly_white",
        legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(fig, use_container_width=True)
