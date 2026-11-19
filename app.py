import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="MOH Liberia | ANC Dashboard", page_icon="🏥", layout="wide")

st.markdown("""
<style>
    .denom-note { font-size: 0.80rem; color: #555555; font-style: italic; margin-top: -8px; margin-bottom: 12px; }
    .warning-banner { background-color: #fff3cd; border: 1px solid #ffeeba; color: #856404; padding: 12px; border-radius: 6px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

COUNTIES = [
    "Montserrado", "Nimba", "Bong", "Lofa", "Grand Bassa",
    "Margibi", "Grand Gedeh", "Maryland", "Sinoe", "Grand Cape Mount",
    "Bomi", "Rivercess", "Gbarpolu", "Grand Kru", "River Gee"
]
QUARTERS = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3", "2026 Q4 (Incomplete)"]

@st.cache_data
def load_shell_data():
    np.random.seed(42)
    rows = []
    for q in QUARTERS:
        inc = "Incomplete" in q
        sc = 0.35 if inc else 1.0
        for c in COUNTIES:
            exp = int(np.random.randint(800, 4500) * sc)
            anc1 = int(exp * np.random.uniform(1.03, 1.12)) if (c in ["Montserrado", "Margibi"] and not inc) else int(exp * np.random.uniform(0.62, 0.94))
            early = int(anc1 * np.random.uniform(0.28, 0.48))
            timely = int(anc1 * np.random.uniform(0.30, 0.42))
            late = max(0, anc1 - early - timely)
            anc2 = int(anc1 * np.random.uniform(0.82, 0.92))
            anc3 = int(anc2 * np.random.uniform(0.80, 0.90))
            anc4 = int(anc3 * np.random.uniform(0.75, 0.88))
            anc5 = int(anc4 * np.random.uniform(0.70, 0.85))
            anc6 = int(anc5 * np.random.uniform(0.68, 0.82))
            anc7 = int(anc6 * np.random.uniform(0.65, 0.80))
            anc8 = int(anc7 * np.random.uniform(0.60, 0.78))
            iptp3 = int(anc1 * np.random.uniform(0.45, 0.78))
            m_test = int(anc1 * np.random.uniform(0.70, 0.95))
            m_pos = int(m_test * np.random.uniform(0.12, 0.34))
            hiv = int(anc1 * np.random.uniform(0.80, 0.98))
            syph = int(anc1 * np.random.uniform(0.55, 0.88))
            hb = int(anc1 * np.random.uniform(0.40, 0.82))
            ifa = int(anc1 * np.random.uniform(0.75, 0.96))
            bp = int(anc1 * np.random.uniform(0.82, 0.99))
            pkg = int(anc1 * np.random.uniform(0.30, 0.62))
            hr_id = int(anc1 * np.random.uniform(0.08, 0.18))
            hr_ref = int(hr_id * np.random.uniform(0.65, 0.92))
            hr_comp = int(hr_ref * np.random.uniform(0.50, 0.85))
            exp_rep = np.random.randint(45, 180)
            sub_rep = int(exp_rep * (0.42 if inc else np.random.uniform(0.82, 1.0)))
            ot_rep = int(sub_rep * np.random.uniform(0.75, 0.96))
            rows.append({
                "Quarter": q, "Is_Incomplete": inc, "County": c, "Expected_ANC1_Pop": exp,
                "ANC1": anc1, "ANC2": anc2, "ANC3": anc3, "ANC4": anc4, "ANC5": anc5, "ANC6": anc6, "ANC7": anc7, "ANC8": anc8,
                "Early_ANC": early, "Timely_ANC": timely, "Late_ANC": late,
                "IPTp3": iptp3, "Malaria_Tested": m_test, "Malaria_Positive": m_pos,
                "HIV_Tested": hiv, "Syphilis_Tested": syph, "HB_Screened": hb, "Iron_Folate": ifa, "BP_Screened": bp, "Full_Package": pkg,
                "HR_Identified": hr_id, "HR_Referred": hr_ref, "HR_Completed": hr_comp,
                "Expected_Reports": exp_rep, "Submitted_Reports": sub_rep, "OnTime_Reports": ot_rep
            })
    return pd.DataFrame(rows)

@st.cache_data
def load_age_and_fac():
    np.random.seed(99)
    ages = [("10–14 yrs", 0.03, 0.22, 0.24), ("15–19 yrs", 0.22, 0.25, 0.27), ("20–24 yrs", 0.30, 0.41, 0.40), ("25–34 yrs", 0.33, 0.44, 0.43), ("35+ yrs", 0.12, 0.39, 0.38)]
    age_df = pd.DataFrame([{
        "Age_Group": a, "ANC1_Unique_Women": int(42000 * w),
        "Within_Group_Early_Pct": round(e * 100, 1), "Within_Group_ANC8_Retention_Pct": round(r * 100, 1)
    } for a, w, e, r in ages])

    fac_rows = []
    for c in COUNTIES:
        n = 55 if c == "Montserrado" else (38 if c in ["Nimba", "Bong", "Lofa"] else 22)
        for i in range(1, n + 1):
            ft = "County Hospital" if i == 1 else ("Health Center" if i <= 5 else "Clinic")
            bp, hiv, ifa = round(np.random.uniform(75, 100), 1), round(np.random.uniform(70, 99), 1), round(np.random.uniform(68, 98), 1)
            mal, syph, hb, iptp3 = round(np.random.uniform(60, 96), 1), round(np.random.uniform(35, 92), 1), round(np.random.uniform(25, 88), 1), round(np.random.uniform(38, 85), 1)
            bnd = round(min(bp, hiv, ifa, mal, syph, hb, iptp3) * np.random.uniform(0.75, 0.98), 1)
            tier = "1. High Performing (≥80%)" if bnd >= 80 else ("2. Moderate (60–79%)" if bnd >= 60 else ("3. Needs Support (40–59%)" if bnd >= 40 else "4. Critical Gap (<40%)"))
            fac_rows.append({"County": c, "Facility_Name": f"{c} {ft} #{i:02d}", "Facility_Type": ft, "ANC1_Cohort": np.random.randint(20, 350),
                             "Syphilis_Pct": syph, "Anemia_Hb_Pct": hb, "IPTp3_Pct": iptp3, "HIV_Pct": hiv, "Complete_Bundle_Pct": bnd, "Performance_Tier": tier})
    return age_df, pd.DataFrame(fac_rows)

df = load_shell_data()
df_age, df_fac = load_age_and_fac()

st.sidebar.header("Dashboard Controls")
selected_quarter = st.sidebar.selectbox("Reporting Period", QUARTERS, index=3)
selected_county = st.sidebar.selectbox("County Filter", ["All 15 Counties"] + COUNTIES)
st.sidebar.markdown("---")
TARGET_ANC1 = st.sidebar.slider("ANC1 Coverage Target (%)", 50, 100, 90)
TARGET_EARLY_ANC = st.sidebar.slider("Early ANC (<12 wks) Target (%)", 20, 80, 50)
TARGET_ANC8 = st.sidebar.slider("ANC8 Retention Target (%)", 20, 80, 45)
TARGET_IPTP3 = st.sidebar.slider("IPTp3+ Coverage Target (%)", 40, 100, 80)

df_q = df[df["Quarter"] == selected_quarter].copy()
if selected_county != "All 15 Counties":
    df_q = df_q[df_q["County"] == selected_county]
is_incomplete_period = bool(df_q["Is_Incomplete"].any())

st.title("Antenatal Care (ANC) Surveillance & Quality Dashboard")
st.caption("Ministry of Health (MOH) / NHIC — Shell Prototype with Simulated Data & Automated Quality Checks")

if is_incomplete_period:
    st.markdown(f"<div class='warning-banner'><strong>⚠️ INCOMPLETE REPORTING PERIOD ({selected_quarter}):</strong> Data is partial. Do not compare against completed quarters.</div>", unsafe_allow_html=True)

comp_pct = (df_q["Submitted_Reports"].sum() / df_q["Expected_Reports"].sum()) * 100
time_pct = (df_q["OnTime_Reports"].sum() / df_q["Expected_Reports"].sum()) * 100
conf_label, conf_color = ("HIGH CONFIDENCE", "green") if (comp_pct >= 90 and not is_incomplete_period) else (("MODERATE CONFIDENCE", "orange") if (comp_pct >= 75 and not is_incomplete_period) else ("LOW CONFIDENCE / INCOMPLETE", "red"))

c1, c2, c3, c4 = st.columns(4)
c1.metric("Facility Reporting Completeness", f"{comp_pct:.1f}%", f"{df_q['Submitted_Reports'].sum():,} / {df_q['Expected_Reports'].sum():,} reports")
c2.metric("Reporting Timeliness", f"{time_pct:.1f}%", "Submitted before deadline")
c3.markdown(f"**Data Confidence Status**<br><span style='color:{conf_color}; font-size:1.3rem; font-weight:bold;'>● {conf_label}</span>", unsafe_allow_html=True)
c4.info("**Unit of Analysis:** Unique pregnant women per cohort unless explicitly labeled as facility encounters.")

st.markdown("---")
st.subheader(f"1. Key ANC Performance Indicators ({selected_quarter})")
tot_anc1 = df_q["ANC1"].sum()
anc1_cov = (tot_anc1 / df_q["Expected_ANC1_Pop"].sum()) * 100
early_pct = (df_q["Early_ANC"].sum() / tot_anc1) * 100
anc4_ret = (df_q["ANC4"].sum() / tot_anc1) * 100
anc8_ret = (df_q["ANC8"].sum() / tot_anc1) * 100
full_pkg_pct = (df_q["Full_Package"].sum() / tot_anc1) * 100

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("ANC1 Coverage", f"{anc1_cov:.1f}%", f"Target: {TARGET_ANC1}% ({anc1_cov - TARGET_ANC1:+.1f}%)")
k1.markdown("<div class='denom-note'>Num: Unique ANC1 | Denom: Est. pregnancies</div>", unsafe_allow_html=True)
k2.metric("Early ANC (<12 Wks)", f"{early_pct:.1f}%", f"Target: {TARGET_EARLY_ANC}% ({early_pct - TARGET_EARLY_ANC:+.1f}%)")
k2.markdown("<div class='denom-note'>Num: ANC1 <12 wks | Denom: Total ANC1</div>", unsafe_allow_html=True)
k3.metric("ANC4+ Retention", f"{anc4_ret:.1f}%", f"{df_q['ANC4'].sum():,} unique women")
k3.markdown("<div class='denom-note'>Num: Reached ANC4 | Denom: ANC1 cohort</div>", unsafe_allow_html=True)
k4.metric("ANC8 Contact Rate", f"{anc8_ret:.1f}%", f"Target: {TARGET_ANC8}% ({anc8_ret - TARGET_ANC8:+.1f}%)")
k4.markdown("<div class='denom-note'>Num: Reached ANC8 | Denom: ANC1 cohort</div>", unsafe_allow_html=True)
k5.metric("Complete Service Package", f"{full_pkg_pct:.1f}%", f"{df_q['Full_Package'].sum():,} women")
k5.markdown("<div class='denom-note'>Num: All 7 core services | Denom: ANC1</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📉 Timing & ANC1–ANC8 Cascade",
    "🗺️ All 15 Counties & >100% Checks",
    "👩🏽 Age Group Dynamics",
    "💊 Service Package & Malaria",
    "🚨 High-Risk & Action Signals"
])

with tab1:
    col_a, col_b = st.columns([1, 1.4])
    with col_a:
        st.markdown("#### Timing of First ANC Entry (Gestational Age)")
        st.markdown("<div class='denom-note'>Distinguishes early entry from late presentation among all ANC1 women.</div>", unsafe_allow_html=True)
        t_df = pd.DataFrame({
            "Stage": ["Early (<12 wks)", "Timely (12–20 wks)", "Late (>20 wks)"],
            "Women": [df_q["Early_ANC"].sum(), df_q["Timely_ANC"].sum(), df_q["Late_ANC"].sum()]
        })
        t_df["Pct"] = (t_df["Women"] / t_df["Women"].sum()) * 100
        fig_t = px.bar(
            t_df, x="Stage", y="Pct",
            text=t_df.apply(lambda r: f"{r['Pct']:.1f}%<br>({r['Women']:,})", axis=1),
            color="Stage", color_discrete_sequence=["#2ca02c", "#1f77b4", "#d62728"]
        )
        fig_t.add_hline(y=TARGET_EARLY_ANC, line_dash="dash", line_color="green", annotation_text=f"Target ({TARGET_EARLY_ANC}%)")
        fig_t.update_layout(showlegend=False, yaxis_title="% of ANC1 Women", height=440)
        st.plotly_chart(fig_t, use_container_width=True)

    with col_b:
        st.markdown("#### Stage-Specific ANC Cascade Funnel (ANC1 to ANC8)")
        st.markdown("<div class='denom-note'>Shows unique women retained, % of initial ANC1 cohort, and step-by-step % retained from prior contact.</div>", unsafe_allow_html=True)
        stages = ["ANC1", "ANC2", "ANC3", "ANC4", "ANC5", "ANC6", "ANC7", "ANC8"]
        counts = [int(df_q[s].sum()) for s in stages]

        fig_funnel = go.Figure(go.Funnel(
            y=stages,
            x=counts,
            textposition="inside",
            textinfo="value+percent initial+percent previous",
            opacity=0.88,
            marker=dict(
                color=["#08519c", "#2171b5", "#4292c6", "#6baed6", "#fdae6b", "#fd8d3c", "#f16913", "#d94801"]
            ),
            connector=dict(line=dict(color="lightgray", dash="dot", width=1.5))
        ))
        fig_funnel.update_layout(
            height=440,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Unique Pregnant Women"
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

    st.markdown("#### Quarterly Trend vs. Target (Completed Periods Only)")
    comp_df = df[~df["Is_Incomplete"]].groupby("Quarter", as_index=False).agg(
        ANC1=("ANC1", "sum"), Early_ANC=("Early_ANC", "sum"), ANC8=("ANC8", "sum")
    )
    comp_df["Early_Pct"] = (comp_df["Early_ANC"] / comp_df["ANC1"]) * 100
    comp_df["ANC8_Pct"] = (comp_df["ANC8"] / comp_df["ANC1"]) * 100
    fig_tr = go.Figure()
    fig_tr.add_trace(go.Scatter(x=comp_df["Quarter"], y=comp_df["Early_Pct"], mode="lines+markers+text", name="Early ANC %", text=comp_df["Early_Pct"].round(1), textposition="top center"))
    fig_tr.add_trace(go.Scatter(x=comp_df["Quarter"], y=comp_df["ANC8_Pct"], mode="lines+markers+text", name="ANC8 Retention %", text=comp_df["ANC8_Pct"].round(1), textposition="bottom center"))
    fig_tr.add_hline(y=TARGET_EARLY_ANC, line_dash="dot", line_color="blue", annotation_text="Early Target")
    fig_tr.add_hline(y=TARGET_ANC8, line_dash="dot", line_color="red", annotation_text="ANC8 Target")
    fig_tr.update_layout(height=300, yaxis_title="%")
    st.plotly_chart(fig_tr, use_container_width=True)

with tab2:
    cdf = df[df["Quarter"] == selected_quarter].copy()
    cdf["ANC1_Cov"] = (cdf["ANC1"] / cdf["Expected_ANC1_Pop"]) * 100
    cdf["Early_Pct"] = (cdf["Early_ANC"] / cdf["ANC1"]) * 100
    cdf["ANC8_Pct"] = (cdf["ANC8"] / cdf["ANC1"]) * 100
    cdf["Comp_Pct"] = (cdf["Submitted_Reports"] / cdf["Expected_Reports"]) * 100

    over = cdf[cdf["ANC1_Cov"] > 100]
    if not over.empty:
        st.error("🚩 **DATA QUALITY WARNING (>100% Coverage):** " + ", ".join([f"{r['County']} ({r['ANC1_Cov']:.1f}%)" for _, r in over.iterrows()]) + ". Requires denominator/duplication verification.")

    col_c1, col_c2 = st.columns([1.5, 1])
    with col_c1:
        st.markdown("#### All 15 Counties Ranked by ANC1 Coverage")
        cs = cdf.sort_values("ANC1_Cov", ascending=True)
        cs["Flag"] = np.where(cs["ANC1_Cov"] > 100, "Exceeds 100% (Verify)", np.where(cs["ANC1_Cov"] < 70, "Below 70% (Attention)", "Expected Range"))
        fig_bar = px.bar(cs, x="ANC1_Cov", y="County", orientation="h", color="Flag",
                         color_discrete_map={"Exceeds 100% (Verify)": "#ff7f0e", "Below 70% (Attention)": "#d62728", "Expected Range": "#1f77b4"},
                         text=cs["ANC1_Cov"].apply(lambda x: f"{x:.1f}%"))
        fig_bar.add_vline(x=100, line_dash="dash", line_color="black")
        fig_bar.add_vline(x=TARGET_ANC1, line_dash="dot", line_color="green")
        fig_bar.update_layout(height=500, xaxis_title="ANC1 Coverage (%)", yaxis_title="")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_c2:
        st.markdown("#### Counties Requiring Attention")
        att = cdf[(cdf["ANC1_Cov"] < 72) | (cdf["ANC1_Cov"] > 100) | (cdf["ANC8_Pct"] < 30)][["County", "ANC1_Cov", "Early_Pct", "ANC8_Pct", "Comp_Pct"]].sort_values("ANC1_Cov")
        st.dataframe(att.style.format({"ANC1_Cov": "{:.1f}%", "Early_Pct": "{:.1f}%", "ANC8_Pct": "{:.1f}%", "Comp_Pct": "{:.1f}%"}), use_container_width=True, hide_index=True, height=440)

    st.markdown("---")
    st.markdown("#### Longitudinal 15-County Heatmap (Completed Quarters Only)")
    hm_ind = st.radio("Heatmap Indicator:", ["ANC1 Coverage (%)", "ANC4+ Retention (%)", "Early ANC (<12 wks) %"], horizontal=True)
    hm_df = df[~df["Is_Incomplete"]].copy()
    hm_df["Val"] = (hm_df["ANC1"] / hm_df["Expected_ANC1_Pop"] * 100) if "ANC1" in hm_ind else ((hm_df["ANC4"] / hm_df["ANC1"] * 100) if "ANC4" in hm_ind else (hm_df["Early_ANC"] / hm_df["ANC1"] * 100))
    piv = hm_df.pivot(index="County", columns="Quarter", values="Val").reindex(sorted(COUNTIES))
    txt_mat = piv.map(lambda v: f"{v:.1f}% ⚠️" if v > 100 else f"{v:.1f}%")
    fig_hm = go.Figure(data=go.Heatmap(z=piv.values, x=list(piv.columns), y=list(piv.index), text=txt_mat.values, texttemplate="%{text}", colorscale="YlGnBu", zmin=30, zmax=100))
    fig_hm.update_layout(height=520, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_hm, use_container_width=True)

with tab3:
    st.markdown("#### Within-Age-Group ANC Entry & Retention Analytics")
    ac1, ac2 = st.columns(2)
    with ac1:
        fig_av = px.bar(df_age, x="Age_Group", y="ANC1_Unique_Women", text="ANC1_Unique_Women", title="ANC1 Volume by Age Group", color_discrete_sequence=["#4c78a8"])
        fig_av.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_av.update_layout(height=380)
        fig_av.update_yaxes(range=list((0, df_age["ANC1_Unique_Women"].max() * 1.2)))
        st.plotly_chart(fig_av, use_container_width=True)
    with ac2:
        am = df_age.melt(id_vars="Age_Group", value_vars=["Within_Group_Early_Pct", "Within_Group_ANC8_Retention_Pct"], var_name="Metric", value_name="Pct")
        am["Metric"] = am["Metric"].replace({"Within_Group_Early_Pct": "Early Entry (%)", "Within_Group_ANC8_Retention_Pct": "ANC8 Retention (%)"})
        fig_ap = px.bar(am, x="Age_Group", y="Pct", color="Metric", barmode="group", text=am["Pct"].apply(lambda x: f"{x:.1f}%"), title="Within-Age-Group Proportions")
        fig_ap.update_traces(textposition="outside")
        fig_ap.update_layout(height=380, legend=dict(orientation="h", y=-0.25))
        fig_ap.update_yaxes(range=list((0, 60)))
        st.plotly_chart(fig_ap, use_container_width=True)

with tab4:
    col_s1, col_s2 = st.columns([1.3, 1])
    with col_s1:
        st.markdown("#### Essential ANC Service Package Coverage (% of ANC1)")
        pkg_df = pd.DataFrame({
            "Service": ["Blood Pressure", "HIV Testing", "Iron / Folate", "Malaria Testing", "Syphilis Testing", "Anemia (Hb)", "IPTp3+ Coverage", "Complete Bundle (All 7)"],
            "Pct": [round(df_q[col].sum() / tot_anc1 * 100, 1) for col in ["BP_Screened", "HIV_Tested", "Iron_Folate", "Malaria_Tested", "Syphilis_Tested", "HB_Screened", "IPTp3", "Full_Package"]]
        }).sort_values("Pct", ascending=True)
        fig_pkg = px.bar(pkg_df, x="Pct", y="Service", orientation="h", text="Pct", color="Pct", color_continuous_scale="Blues")
        fig_pkg.update_traces(texttemplate="%{text}%", textposition="outside")
        fig_pkg.update_layout(height=410, showlegend=False, coloraxis_showscale=False)
        fig_pkg.update_xaxes(range=list((0, 108)))
        st.plotly_chart(fig_pkg, use_container_width=True)

    with col_s2:
        st.markdown("#### Malaria in Pregnancy: Burden vs. Positivity")
        m_cov = (df_q["Malaria_Tested"].sum() / tot_anc1) * 100
        m_pos_r = (df_q["Malaria_Positive"].sum() / df_q["Malaria_Tested"].sum()) * 100
        m1, m2 = st.columns(2)
        m1.metric("Confirmed Cases (Burden)", f"{df_q['Malaria_Positive'].sum():,}")
        m2.metric("Test Positivity Rate", f"{m_pos_r:.1f}%", f"Testing Cov: {m_cov:.1f}%")
        mc = df[df["Quarter"] == selected_quarter].copy()
        mc["Pos_Rate"] = (mc["Malaria_Positive"] / mc["Malaria_Tested"]) * 100
        mc["Test_Cov"] = (mc["Malaria_Tested"] / mc["ANC1"]) * 100
        fig_m = px.scatter(mc, x="Test_Cov", y="Pos_Rate", size="Malaria_Positive", hover_name="County", text="County", title="Testing Coverage vs. Positivity")
        fig_m.update_traces(textposition="top center")
        fig_m.update_layout(height=310)
        st.plotly_chart(fig_m, use_container_width=True)

    st.markdown("---")
    st.markdown(f"#### County Stratification: Essential Service Package Matrix ({selected_quarter})")
    cs_df = df[df["Quarter"] == selected_quarter].copy()
    cs_df["BP"] = (cs_df["BP_Screened"] / cs_df["ANC1"]) * 100
    cs_df["HIV"] = (cs_df["HIV_Tested"] / cs_df["ANC1"]) * 100
    cs_df["Iron/Folate"] = (cs_df["Iron_Folate"] / cs_df["ANC1"]) * 100
    cs_df["Malaria Test"] = (cs_df["Malaria_Tested"] / cs_df["ANC1"]) * 100
    cs_df["Syphilis"] = (cs_df["Syphilis_Tested"] / cs_df["ANC1"]) * 100
    cs_df["Anemia (Hb)"] = (cs_df["HB_Screened"] / cs_df["ANC1"]) * 100
    cs_df["IPTp3+"] = (cs_df["IPTp3"] / cs_df["ANC1"]) * 100
    cs_df["Full Bundle"] = (cs_df["Full_Package"] / cs_df["ANC1"]) * 100

    s_cols = ["BP", "HIV", "Iron/Folate", "Malaria Test", "Syphilis", "Anemia (Hb)", "IPTp3+", "Full Bundle"]
    mat = cs_df.set_index("County")[s_cols].sort_values("Full Bundle", ascending=False)
    fig_shm = go.Figure(data=go.Heatmap(
        z=mat.values,
        x=s_cols,
        y=list(mat.index),
        text=np.round(mat.values, 1),
        texttemplate="%{text}%",
        colorscale="Blues",
        zmin=25,
        zmax=100
    ))
    fig_shm.update_layout(height=460, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_shm, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Facility-Level Service Quality Tiers & County Drill-Down")
    fv = df_fac if selected_county == "All 15 Counties" else df_fac[df_fac["County"] == selected_county]
    fc1, fc2 = st.columns([1, 1.8])
    with fc1:
        tc = fv["Performance_Tier"].value_counts().sort_index().reset_index()
        tc.columns = ["Tier", "Facilities"]
        fig_ft = px.bar(
            tc, x="Facilities", y="Tier", orientation="h", text="Facilities", color="Tier",
            color_discrete_map={
                "1. High Performing (≥80%)": "#2ca02c",
                "2. Moderate (60–79%)": "#1f77b4",
                "3. Needs Support (40–59%)": "#ff7f0e",
                "4. Critical Gap (<40%)": "#d62728"
            }
        )
        fig_ft.update_traces(textposition="outside")
        fig_ft.update_layout(showlegend=False, height=320, yaxis=dict(autorange="reversed"))
        fig_ft.update_xaxes(range=list((0, tc["Facilities"].max() * 1.25)))
        st.plotly_chart(fig_ft, use_container_width=True)
    with fc2:
        d1, d2 = st.columns([1.2, 1])
        dc = d1.selectbox("Inspect Facilities in County:", COUNTIES, index=COUNTIES.index(selected_county) if selected_county != "All 15 Counties" else 0)
        low_only = d2.checkbox("Only Facilities < 50% Bundle", value=True)
        ftab = df_fac[df_fac["County"] == dc].sort_values("Complete_Bundle_Pct")
        if low_only:
            ftab = ftab[ftab["Complete_Bundle_Pct"] < 50]
        st.dataframe(
            ftab[["Facility_Name", "Facility_Type", "ANC1_Cohort", "Complete_Bundle_Pct", "Syphilis_Pct", "Anemia_Hb_Pct", "IPTp3_Pct"]].style.format({
                "Complete_Bundle_Pct": "{:.1f}%",
                "Syphilis_Pct": "{:.1f}%",
                "Anemia_Hb_Pct": "{:.1f}%",
                "IPTp3_Pct": "{:.1f}%"
            }),
            use_container_width=True,
            hide_index=True,
            height=280
        )
with tab5:
    st.markdown("#### 1. High-Risk Pregnancy Assessment & Referral Completion Cascade")
    hr_id, hr_ref, hr_comp = df_q["HR_Identified"].sum(), df_q["HR_Referred"].sum(), df_q["HR_Completed"].sum()
    h1, h2, h3 = st.columns(3)
    h1.metric("1. High-Risk Identified", f"{hr_id:,}", f"{(hr_id / tot_anc1) * 100:.1f}% of ANC1")
    h2.metric("2. High-Risk Referred", f"{hr_ref:,}", f"{(hr_ref / hr_id) * 100:.1f}% of identified")
    h3.metric("3. Referral Completed", f"{hr_comp:,}", f"{(hr_comp / hr_ref) * 100:.1f}% reached care (Target ≥80%)")

    st.markdown("---")
    st.markdown(f"#### 2. Automated ANC Signals Requiring Action ({selected_quarter})")
    ev = df[df["Quarter"] == selected_quarter].copy()
    if selected_county != "All 15 Counties":
        ev = ev[ev["County"] == selected_county]
    ev["ANC1_Cov"] = (ev["ANC1"] / ev["Expected_ANC1_Pop"]) * 100
    ev["Early_Pct"] = (ev["Early_ANC"] / ev["ANC1"]) * 100
    ev["ANC8_Pct"] = (ev["ANC8"] / ev["ANC1"]) * 100
    ev["Comp_Pct"] = (ev["Submitted_Reports"] / ev["Expected_Reports"]) * 100
    ev["Mal_Pos"] = (ev["Malaria_Positive"] / ev["Malaria_Tested"]) * 100
    ev["HR_Comp"] = (ev["HR_Completed"] / ev["HR_Referred"]) * 100

    sigs = []
    for _, r in ev[ev["ANC1_Cov"] > 100].iterrows():
        sigs.append(("🟠 Data Anomaly", "Data Quality", f"{r['County']}: ANC1 Coverage {r['ANC1_Cov']:.1f}% (>100%)", "Denominator mismatch or duplicate visits.", "Audit DHIS2 duplicates & denominators.", "NHIC HMIS Team", "Verify"))
    for _, r in ev[ev["ANC1_Cov"] < 70].sort_values("ANC1_Cov").iterrows():
        sigs.append(("🔴 Critical", "Access & Coverage", f"{r['County']}: Low ANC1 Coverage ({r['ANC1_Cov']:.1f}% < 70%)", "Low initial ANC uptake.", "Deploy CHAs for pregnancy mapping.", f"{r['County']} CHT", "Action Required"))
    for _, r in ev[ev["Comp_Pct"] < 85].sort_values("Comp_Pct").iterrows():
        sigs.append(("🟠 Data Warning", "Completeness", f"{r['County']}: Completeness {r['Comp_Pct']:.1f}% (<85%)", "Missing facility reports.", "Follow up with silent facilities.", f"{r['County']} M&E", "Pending"))
    for _, r in ev[ev["Early_Pct"] < 32].sort_values("Early_Pct").iterrows():
        sigs.append(("🟡 Moderate", "Early Entry", f"{r['County']}: Early ANC {r['Early_Pct']:.1f}% (<32%)", "Late 1st trimester booking.", "Strengthen community referral messaging.", f"{r['County']} RH Sup.", "Action Required"))
    for _, r in ev[ev["ANC8_Pct"] < 22].sort_values("ANC8_Pct").iterrows():
        sigs.append(("🔴 Critical", "Continuity (ANC8)", f"{r['County']}: ANC8 Completion {r['ANC8_Pct']:.1f}% (<22%)", "High late-pregnancy dropout.", "Enforce midwife appointment tracking.", f"{r['County']} CHT", "Action Required"))
    for _, r in ev[ev["Mal_Pos"] >= 25].sort_values("Mal_Pos", ascending=False).iterrows():
        sigs.append(("🔴 Clinical Alert", "Malaria", f"{r['County']}: Malaria Positivity {r['Mal_Pos']:.1f}% (≥25%)", "Elevated malaria burden in pregnancy.", "Verify ITN & IPTp3+ clinic stock.", "NMCP / County", "Escalated"))
    for _, r in ev[ev["HR_Comp"] < 75].sort_values("HR_Comp").iterrows():
        sigs.append(("🔴 Clinical Alert", "High-Risk Referral", f"{r['County']}: Referral Completion {r['HR_Comp']:.1f}% (<75%)", "High-risk mothers missing hospital care.", "Audit referral transport & feedback.", f"{r['County']} Hospital", "Action Required"))
    for _, ar in df_age.iterrows():
        if ar["Within_Group_Early_Pct"] < 30:
            sigs.append(("🟡 Equity Alert", "Age Equity", f"Age {ar['Age_Group']}: Early Entry {ar['Within_Group_Early_Pct']}% (<30%)", "Adolescents enter ANC significantly later.", "Expand youth-friendly ANC & CHA outreach.", "FHD Adolescent Unit", "Action Required"))

    sig_df = pd.DataFrame(sigs, columns=["Severity", "Domain", "Signal / Finding", "Interpretation", "Recommended Action", "Assigned Owner", "Status"])
    if not sig_df.empty:
        st.info(f"**{len(sig_df)} active rule violations detected** across all counties and ANC domains for {selected_quarter}.")
        st.dataframe(sig_df, use_container_width=True, hide_index=True, height=450)
    else:
        st.success("✅ All ANC indicators meet acceptable MOH/NHIC thresholds.")
