import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(page_title="Connections | IS 800:2007", page_icon="🔧", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=IBM+Plex+Mono&display=swap');
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;}
.clause-box{background:#eff6ff;border-left:4px solid #2563eb;border-radius:0 8px 8px 0;padding:14px 18px;margin:10px 0;}
.formula-box{background:#1e293b;color:#e2e8f0;border-radius:10px;padding:18px 22px;font-family:'IBM Plex Mono',monospace;font-size:14px;margin:12px 0;}
.result-box{background:#f0fdf4;border:2px solid #22c55e;border-radius:12px;padding:20px;margin:12px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔧 Bolted & Welded Connections")
st.markdown("**IS 800:2007 — Chapter 10**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🔩 Bolted Connections", "🔥 Welded Connections", "📊 Bolt Group Analysis"])

# ─── TAB 1: Bolts ─────────────────────────────────────────────────────────────
with tab1:
    st.markdown("## Bolt Design — IS 800:2007 Cl. 10.3")
    st.markdown("""
    <div class="clause-box">
    <b>Cl. 10.3.2</b> — Design capacity of a bolt = min(shear capacity, bearing capacity).  
    Slip-critical connections use friction-type design (HSFG bolts).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Bolt Grade Properties")
    bolt_grades = pd.DataFrame({
        "Grade": ["4.6", "5.6", "6.8", "8.8", "10.9"],
        "f_ub (MPa)": [400, 500, 600, 800, 1000],
        "f_yb (MPa)": [240, 300, 480, 640, 900],
        "Proof Stress (MPa)": [225, 280, 420, 560, 810],
    })
    st.dataframe(bolt_grades, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🧮 Bolt Capacity Calculator")

    col1, col2 = st.columns([1, 1])
    with col1:
        grade = st.selectbox("Bolt Grade", ["4.6", "8.8", "10.9"])
        fub_map = {"4.6": 400, "8.8": 800, "10.9": 1000}
        fub = fub_map[grade]

        dia = st.selectbox("Bolt Diameter (mm)", [12, 16, 20, 24, 27, 30], index=2)
        n_shear = st.radio("Number of shear planes", [1, 2])
        t_plate = st.number_input("Plate thickness t (mm, for bearing)", 6, 40, 12, 2)
        fy_plate = st.number_input("Plate f_y (MPa)", 200, 550, 250, 25)
        fu_plate = st.number_input("Plate f_u (MPa)", 350, 700, 410, 25)
        end_dist = st.number_input("End distance e (mm)", 20, 100, 40, 5)
        pitch_b = st.number_input("Pitch/spacing p (mm)", 30, 200, 60, 5)

    with col2:
        gm0 = 1.10; gm1 = 1.25; gmb = 1.25

        # Net shear area (0.78 × A_nominal for threads in shear)
        A_nom = np.pi * dia**2 / 4
        A_nb  = 0.78 * A_nom

        # Shear capacity
        f_nb = fub / (3**0.5)
        V_nsb = f_nb * A_nb * n_shear
        V_dsb = V_nsb / gmb / 1000  # kN

        # Bearing capacity
        kb = min(end_dist/(3*dia), pitch_b/(3*dia) - 0.25, fub/fu_plate, 1.0)
        V_dpb = 2.5 * kb * dia * t_plate * fu_plate / gmb / 1000  # kN

        V_db = min(V_dsb, V_dpb)

        st.markdown(f"""
        <div class="result-box">
        <h3 style="margin:0;">Design Bolt Capacity</h3>
        <h1 style="margin:8px 0;font-size:2.2rem;">V_db = {V_db:.2f} kN</h1>
        <p style="margin:0;">Governs: {"Shear" if V_dsb < V_dpb else "Bearing"}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        **Shear Capacity (Cl. 10.3.3):**  
        - A_nb = 0.78 × π×{dia}²/4 = {A_nb:.1f} mm²  
        - V_nsb = f_ub/(√3) × A_nb × {n_shear} = {V_nsb:.1f} N  
        - **V_dsb = {V_dsb:.2f} kN**

        **Bearing Capacity (Cl. 10.3.4):**  
        - k_b = min(e/3d, p/3d−0.25, f_ub/f_u, 1.0) = {kb:.3f}  
        - V_npb = 2.5 × k_b × d × t × f_u = {V_dpb*gmb*1000:.1f} N  
        - **V_dpb = {V_dpb:.2f} kN**
        """)

    st.markdown("---")
    st.markdown("### Bolt Spacing Rules — Cl. 10.2")
    spacing_df = pd.DataFrame({
        "Parameter": ["Min end distance", "Min edge distance", "Min pitch (spacing)",
                      "Max pitch (tension)", "Max pitch (compression)", "Max edge distance"],
        "Requirement": [
            "1.7 × hole diameter (sheared edge), 1.5d_h (rolled/sawn)",
            "1.7 × hole diameter (sheared edge), 1.5d_h (rolled/sawn)",
            "2.5 × nominal bolt diameter",
            "16t or 200 mm (whichever less)",
            "12t or 200 mm (whichever less)",
            "12t or 150 mm (whichever less), t = thinner plate",
        ],
        "Clause": ["10.2.2.1", "10.2.2.2", "10.2.3.1", "10.2.3.3", "10.2.3.3", "10.2.4.2"],
    })
    st.dataframe(spacing_df, use_container_width=True, hide_index=True)

# ─── TAB 2: Welds ─────────────────────────────────────────────────────────────
with tab2:
    st.markdown("## Weld Design — IS 800:2007 Cl. 10.5")

    st.markdown("""
    <div class="clause-box">
    <b>Cl. 10.5.7</b> — Design strength of fillet weld per unit length:<br>
    f_wd = f_u / (√3 × γ_mw)  where γ_mw = 1.25<br>
    Design capacity = f_wd × throat size × effective length
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### Weld Calculator")
        s_size = st.number_input("Fillet weld size s (mm)", 3, 25, 8, 1)
        weld_len = st.number_input("Effective weld length L_eff (mm)", 20, 2000, 200, 10)
        fu_w = st.number_input("f_u of weaker material (MPa)", 350, 700, 410, 25)
        weld_type = st.radio("Weld Type", ["Single Fillet", "Double Fillet (both sides)"])

        # Throat
        tt = 0.7 * s_size  # fillet throat
        gmw = 1.25
        fwd = fu_w / (3**0.5 * gmw)
        Vd_weld = fwd * tt * weld_len / 1000  # kN per weld
        n_welds = 2 if weld_type == "Double Fillet (both sides)" else 1

    with c2:
        st.markdown("### Weld Results")
        st.markdown(f"""
        <div class="result-box">
        <h3 style="margin:0;">Design Weld Capacity</h3>
        <h1 style="margin:8px 0;font-size:2.2rem;">{Vd_weld*n_welds:.1f} kN</h1>
        <p style="margin:0;">{n_welds} weld(s) × {Vd_weld:.1f} kN each</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        **Workings:**  
        - Throat thickness t_t = 0.7 × s = 0.7 × {s_size} = **{tt:.1f} mm**  
        - f_wd = f_u/(√3 × γ_mw) = {fu_w}/(1.732 × {gmw}) = **{fwd:.1f} MPa**  
        - Per-weld capacity = {fwd:.1f} × {tt:.1f} × {weld_len} / 1000 = **{Vd_weld:.1f} kN**  
        - Total = {n_welds} × {Vd_weld:.1f} = **{Vd_weld*n_welds:.1f} kN**
        """)

    st.markdown("---")
    st.markdown("### Weld Size Rules — Cl. 10.5.3")
    weld_rules = pd.DataFrame({
        "Rule": [
            "Minimum weld size",
            "Maximum weld size (along plate edge)",
            "Maximum weld size (for t_p > 6 mm)",
            "Effective length (min)",
        ],
        "Requirement": [
            "s_min as per Table 21 (e.g. 3mm for t<10mm, 5mm for t≤20mm)",
            "s ≤ t (plate thickness)",
            "s ≤ t_p − 1.5 mm",
            "≥ 4 × weld size (s)",
        ],
    })
    st.dataframe(weld_rules, use_container_width=True, hide_index=True)

# ─── TAB 3: Bolt Group ────────────────────────────────────────────────────────
with tab3:
    st.markdown("## Eccentrically Loaded Bolt Group")
    st.markdown("Determine critical bolt force in a bolt group with in-plane eccentric shear.")

    c1, c2 = st.columns([1, 1])
    with c1:
        P_eccen = st.number_input("Applied shear force P (kN)", 10.0, 500.0, 100.0, 10.0)
        e_dist  = st.number_input("Eccentricity e (mm)", 20, 500, 150, 10)
        n_rows  = st.number_input("Number of bolt rows", 1, 6, 3, 1)
        n_cols  = st.number_input("Number of bolt columns", 1, 4, 2, 1)
        sp_row  = st.number_input("Row spacing (vertical) s_v (mm)", 40, 200, 70, 10)
        sp_col  = st.number_input("Column spacing (horizontal) s_h (mm)", 40, 200, 70, 10)

    with c2:
        # Bolt positions (centred)
        bx = [(j - (n_cols-1)/2) * sp_col for j in range(n_cols) for i in range(n_rows)]
        by = [(i - (n_rows-1)/2) * sp_row for j in range(n_cols) for i in range(n_rows)]
        n_bolts = len(bx)

        # Direct shear
        Vx_direct = 0
        Vy_direct = P_eccen / n_bolts  # kN per bolt

        # Moment
        M = P_eccen * e_dist  # kN·mm
        Ip = sum(x**2 + y**2 for x, y in zip(bx, by))  # mm²

        # Torsional component
        Fx_t = [M * (-y) / Ip for y in by]    # kN
        Fy_t = [M * x / Ip for x in bx]

        # Resultant per bolt
        Fx_res = [Vx_direct + ft for ft in Fx_t]
        Fy_res = [Vy_direct + ft for ft in Fy_t]
        V_res  = [np.sqrt(fx**2 + fy**2) for fx, fy in zip(Fx_res, Fy_res)]
        V_max  = max(V_res)
        crit_idx = V_res.index(V_max)

        st.metric("Critical Bolt Force", f"{V_max:.2f} kN")
        st.markdown(f"""
        **Bolt group analysis:**  
        - Number of bolts = {n_bolts}  
        - Direct shear per bolt = {Vy_direct:.2f} kN  
        - Moment M = P × e = {P_eccen} × {e_dist} = **{M:.0f} kN·mm**  
        - Polar moment I_p = **{Ip:.0f} mm²**  
        - Critical bolt is at position ({bx[crit_idx]:.0f}, {by[crit_idx]:.0f}) mm
        """)

        # Plot
        fig = go.Figure()
        marker_colors = [V_res[i]/V_max for i in range(n_bolts)]
        fig.add_trace(go.Scatter(
            x=bx, y=by, mode="markers",
            marker=dict(size=22, color=V_res, colorscale="RdYlGn_r",
                        showscale=True, colorbar=dict(title="Force (kN)"),
                        line=dict(width=2, color="white")),
            text=[f"Bolt {i+1}<br>{V_res[i]:.2f} kN" for i in range(n_bolts)],
            hoverinfo="text",
        ))
        fig.add_annotation(x=bx[crit_idx], y=by[crit_idx],
                           text=f"Critical<br>{V_max:.1f} kN",
                           showarrow=True, arrowhead=2, font=dict(color="red", size=11))
        fig.update_layout(
            title="Bolt Group — Force Distribution",
            xaxis_title="x (mm)", yaxis_title="y (mm)",
            xaxis=dict(scaleanchor="y"), yaxis=dict(scaleratio=1),
            height=380, template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)
