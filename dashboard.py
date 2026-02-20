import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import date

st.set_page_config(
    page_title="BI Subscriptions",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Ivory / cream palette
# ─────────────────────────────────────────────────────────────────────────────
BG       = "#FFFDF7"
BG_SIDE  = "#F5F0E8"
CARD     = "#FFFFFF"
BORDER   = "rgba(0,0,0,0.06)"
TEXT     = "#2d2a26"
TEXT_SEC = "#8a8378"
ACCENT1  = "#6c5ce7"
ACCENT2  = "#00b894"
ACCENT3  = "#e17055"
ACCENT4  = "#0984e3"

PALETTE = [ACCENT1, ACCENT2, ACCENT3, ACCENT4,
           "#fdcb6e", "#e84393", "#74b9ff", "#55efc4",
           "#a29bfe", "#fab1a0"]

PLOTLY_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, SF Pro Display, -apple-system, sans-serif",
              size=13, color=TEXT_SEC),
    title_font=dict(family="Inter, SF Pro Display, -apple-system, sans-serif",
                    size=17, color=TEXT),
    coloraxis_showscale=False,
    margin=dict(t=52, b=36, l=16, r=16),
    xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.04)",
               zeroline=False, title_font_color=TEXT_SEC),
    yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.04)",
               zeroline=False, title_font_color=TEXT_SEC),
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {{
    --bg:       {BG};
    --card:     {CARD};
    --border:   {BORDER};
    --text:     {TEXT};
    --text-sec: {TEXT_SEC};
    --accent:   {ACCENT1};
    --radius:   16px;
}}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {{
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
}}

/* ── Sidebar ──────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: {BG_SIDE} !important;
    border-right: 1px solid rgba(0,0,0,0.05);
}}
section[data-testid="stSidebar"] * {{
    font-family: 'Inter', sans-serif !important;
}}
section[data-testid="stSidebar"] label {{
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em;
    color: {TEXT_SEC} !important;
    text-transform: uppercase;
    margin-bottom: 2px !important;
}}
section[data-testid="stSidebar"] .stDateInput input,
section[data-testid="stSidebar"] .stSelectbox > div > div {{
    background: {CARD} !important;
    border: 1px solid rgba(0,0,0,0.08) !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
    font-size: 0.9rem !important;
}}
section[data-testid="stSidebar"] .stButton > button {{
    background: {ACCENT1} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1rem !important;
    letter-spacing: 0.01em;
    transition: opacity 0.2s, transform 0.15s;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
    opacity: 0.88;
    transform: translateY(-1px);
}}
section[data-testid="stSidebar"] hr {{
    border-color: rgba(0,0,0,0.06) !important;
    margin: 1.4rem 0 !important;
}}
section[data-testid="stSidebar"] .sidebar-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {TEXT};
    letter-spacing: -0.01em;
    margin-bottom: 1rem;
}}
section[data-testid="stSidebar"] .sidebar-section {{
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {TEXT_SEC};
    margin: 1.2rem 0 0.6rem;
}}

/* ── Main container ───────────────────────────────────────────────────── */
.main .block-container {{
    padding: 2.5rem 3rem 3rem 3rem !important;
    max-width: 1400px;
}}

/* ── Typography ───────────────────────────────────────────────────────── */
h1 {{
    font-weight: 700 !important;
    font-size: 2.4rem !important;
    letter-spacing: -0.03em !important;
    color: {TEXT} !important;
    margin-bottom: 0.1rem !important;
    line-height: 1.1 !important;
}}
h3 {{
    font-weight: 600 !important;
    font-size: 1.15rem !important;
    letter-spacing: -0.01em !important;
    color: {TEXT} !important;
    margin-top: 0.4rem !important;
    margin-bottom: 0.8rem !important;
}}
.subtitle {{
    font-size: 1.02rem;
    font-weight: 400;
    color: {TEXT_SEC};
    line-height: 1.5;
    margin-bottom: 2rem;
}}

/* ── KPI Cards ────────────────────────────────────────────────────────── */
.kpi-row {{
    display: flex;
    gap: 18px;
    margin-bottom: 2.2rem;
}}
.kpi {{
    flex: 1;
    background: {CARD};
    border: 1px solid rgba(0,0,0,0.05);
    border-radius: var(--radius);
    padding: 26px 24px 22px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 6px 24px rgba(0,0,0,0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.kpi:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
}}
.kpi-icon {{
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    margin-bottom: 14px;
}}
.kpi-label {{
    font-size: 0.74rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {TEXT_SEC};
    margin-bottom: 6px;
}}
.kpi-value {{
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1;
}}
.kpi-a1 .kpi-icon {{ background: rgba(108,92,231,0.1); }}
.kpi-a1 .kpi-value {{ color: {ACCENT1}; }}
.kpi-a2 .kpi-icon {{ background: rgba(0,184,148,0.1); }}
.kpi-a2 .kpi-value {{ color: {ACCENT2}; }}
.kpi-a3 .kpi-icon {{ background: rgba(225,112,85,0.1); }}
.kpi-a3 .kpi-value {{ color: {ACCENT3}; }}
.kpi-a4 .kpi-icon {{ background: rgba(9,132,227,0.1); }}
.kpi-a4 .kpi-value {{ color: {ACCENT4}; }}

/* ── Chart wrapper ────────────────────────────────────────────────────── */
.chart-wrap {{
    background: {CARD};
    border: 1px solid rgba(0,0,0,0.05);
    border-radius: var(--radius);
    padding: 20px 16px 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02), 0 4px 16px rgba(0,0,0,0.02);
    margin-bottom: 8px;
}}

/* ── Section divider ──────────────────────────────────────────────────── */
.section-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,0,0,0.06), transparent);
    margin: 2rem 0;
}}

/* ── Dataframe ────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {{
    border-radius: var(--radius) !important;
    overflow: hidden;
    border: 1px solid rgba(0,0,0,0.06) !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}}

/* ── Scrollbar ────────────────────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: rgba(0,0,0,0.12); border-radius: 3px; }}

#MainMenu, footer, header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data(date_from: str, date_to: str) -> pd.DataFrame:
    url = "https://1c-lk.uztelecom.uz/a/adm/hs/BI/subscriptions"
    resp = requests.get(
        url, params={"from": date_from, "to": date_to},
        auth=("BI", "Syxukogepe96"), verify=False,
    )
    resp.encoding = "utf-8"
    df = pd.DataFrame(resp.json())
    for c in ["subscription_conection_time", "connection_date", "disconnection_date"]:
        df[c] = pd.to_datetime(df[c], errors="coerce")
    for c in ["quantity", "amount", "procent_bonus_id", "amount_of_remuneration_id"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    df["subscriber_id"] = df["subscriber_id"].astype(str)
    df["month"] = df["connection_date"].dt.to_period("M").astype(str)
    df["day_of_week"] = df["connection_date"].dt.day_name()
    return df


def styled(fig, **kw):
    fig.update_layout(**{**PLOTLY_LAYOUT, **kw})
    return fig


ALL = "Все"

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">BI Subscriptions</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Период</div>',
                unsafe_allow_html=True)
    d_from = st.date_input("С", value=date(2025, 4, 25))
    d_to   = st.date_input("По", value=date(2025, 12, 23))

    if st.button("Обновить", use_container_width=True):
        st.cache_data.clear()

    st.markdown("---")
    st.markdown('<div class="sidebar-section">Фильтры</div>',
                unsafe_allow_html=True)

with st.spinner(""):
    df = load_data(f"{d_from}T00:00:00", f"{d_to}T23:59:59")

if df.empty:
    st.warning("Нет данных за выбранный период.")
    st.stop()

with st.sidebar:
    cities = sorted([c for c in df["city_id"].dropna().unique() if str(c).strip()])
    sel_city = st.selectbox("Город", [ALL] + cities)

    tariffs = sorted(df["provaider_tariff_name"].dropna().unique().tolist())
    sel_tariff = st.selectbox("Тариф", [ALL] + tariffs)

    sub_types = sorted(df["subscription_type"].dropna().unique().tolist())
    sel_type = st.selectbox("Тип подписки", [ALL] + sub_types)

    managers = sorted([m for m in df["manager_id"].dropna().unique() if str(m).strip()])
    sel_manager = st.selectbox("Менеджер", [ALL] + managers) if managers else ALL

    billing_periods = sorted(df["billing_period"].dropna().unique().tolist())
    sel_billing = st.selectbox("Биллинг", [ALL] + billing_periods)

# ─────────────────────────────────────────────────────────────────────────────
# Apply filters
# ─────────────────────────────────────────────────────────────────────────────
mask = pd.Series(True, index=df.index)
if sel_city != ALL:
    mask &= df["city_id"] == sel_city
if sel_tariff != ALL:
    mask &= df["provaider_tariff_name"] == sel_tariff
if sel_type != ALL:
    mask &= df["subscription_type"] == sel_type
if sel_manager != ALL:
    mask &= df["manager_id"] == sel_manager
if sel_billing != ALL:
    mask &= df["billing_period"] == sel_billing

filtered = df[mask].copy()

# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("# Subscriptions")
st.markdown(
    f'<p class="subtitle">{d_from.strftime("%d.%m.%Y")} &mdash; '
    f'{d_to.strftime("%d.%m.%Y")}'
    f'&nbsp;&nbsp;&middot;&nbsp;&nbsp;'
    f'{len(filtered)} из {len(df)} записей</p>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────────────────────────────────────
unique_subs  = filtered["subscriber_id"].nunique()
total_amount = filtered["amount"].sum()
avg_bonus    = filtered["procent_bonus_id"].mean()

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi kpi-a1">
    <div class="kpi-icon">&#9632;</div>
    <div class="kpi-label">Всего подписок</div>
    <div class="kpi-value">{len(filtered)}</div>
  </div>
  <div class="kpi kpi-a2">
    <div class="kpi-icon">&#9679;</div>
    <div class="kpi-label">Уникальных абонентов</div>
    <div class="kpi-value">{unique_subs}</div>
  </div>
  <div class="kpi kpi-a3">
    <div class="kpi-icon">&#9650;</div>
    <div class="kpi-label">Общая сумма</div>
    <div class="kpi-value">{total_amount:,.0f}</div>
  </div>
  <div class="kpi kpi-a4">
    <div class="kpi-icon">&#9733;</div>
    <div class="kpi-label">Средний бонус</div>
    <div class="kpi-value">{avg_bonus:.1f}%</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Row 1
# ─────────────────────────────────────────────────────────────────────────────
r1a, r1b = st.columns(2, gap="large")

with r1a:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    monthly = filtered.groupby("month").size().reset_index(name="count")
    fig = px.bar(monthly, x="month", y="count", text="count",
                 color_discrete_sequence=[ACCENT1])
    fig.update_traces(textposition="outside", marker_line_width=0,
                      marker_cornerradius=8)
    styled(fig, title_text="Подписки по месяцам", xaxis_title="", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r1b:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    tc = filtered["provaider_tariff_name"].value_counts().reset_index()
    tc.columns = ["tariff", "count"]
    fig2 = px.pie(tc, names="tariff", values="count", hole=0.55,
                  color_discrete_sequence=PALETTE)
    fig2.update_traces(textposition="inside", textinfo="percent+label",
                       textfont_size=12)
    styled(fig2, title_text="По тарифам", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Row 2
# ─────────────────────────────────────────────────────────────────────────────
r2a, r2b = st.columns(2, gap="large")

with r2a:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    cc = (filtered[filtered["city_id"].str.strip() != ""]["city_id"]
          .value_counts().reset_index())
    cc.columns = ["city", "count"]
    fig3 = px.bar(cc.head(15), x="count", y="city", orientation="h",
                  text="count", color_discrete_sequence=[ACCENT2])
    fig3.update_traces(textposition="outside", marker_line_width=0,
                       marker_cornerradius=8)
    styled(fig3, title_text="По городам",
           yaxis=dict(autorange="reversed", showgrid=False),
           xaxis_title="", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r2b:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    tyc = filtered["subscription_type"].value_counts().reset_index()
    tyc.columns = ["type", "count"]
    fig4 = px.pie(tyc, names="type", values="count", hole=0.55,
                  color_discrete_sequence=[ACCENT2, ACCENT3, ACCENT1, ACCENT4])
    fig4.update_traces(textposition="inside", textinfo="percent+label",
                       textfont_size=12)
    styled(fig4, title_text="Тип подписки", showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Row 3
# ─────────────────────────────────────────────────────────────────────────────
r3a, r3b = st.columns(2, gap="large")

with r3a:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    daily = (filtered.groupby(filtered["connection_date"].dt.date)
             .size().reset_index(name="count"))
    daily.columns = ["date", "count"]
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=daily["date"], y=daily["count"],
        mode="lines+markers", fill="tozeroy",
        line=dict(color=ACCENT1, width=2.5, shape="spline"),
        marker=dict(size=5, color=ACCENT1),
        fillcolor="rgba(108,92,231,0.07)",
    ))
    styled(fig5, title_text="Динамика подключений",
           xaxis_title="", yaxis_title="")
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r3b:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    if filtered["amount"].sum() > 0:
        ma = filtered.groupby("month")["amount"].sum().reset_index()
        fig6 = px.bar(ma, x="month", y="amount", text="amount",
                      color_discrete_sequence=[ACCENT3])
        fig6.update_traces(textposition="outside", texttemplate="%{text:,.0f}",
                           marker_line_width=0, marker_cornerradius=8)
        styled(fig6, title_text="Сумма по месяцам",
               xaxis_title="", yaxis_title="")
    else:
        bc = filtered["billing_period"].value_counts().reset_index()
        bc.columns = ["period", "count"]
        fig6 = px.bar(bc, x="period", y="count", text="count",
                      color_discrete_sequence=[ACCENT3])
        fig6.update_traces(textposition="outside", marker_line_width=0,
                           marker_cornerradius=8)
        styled(fig6, title_text="Период биллинга",
               xaxis_title="", yaxis_title="", showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Row 4
# ─────────────────────────────────────────────────────────────────────────────
r4a, r4b = st.columns(2, gap="large")

with r4a:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    mgr = filtered[filtered["manager_id"].str.strip() != ""]
    if not mgr.empty:
        mc = mgr["manager_id"].value_counts().reset_index()
        mc.columns = ["manager", "count"]
        fig7 = px.bar(mc.head(10), x="count", y="manager", orientation="h",
                      text="count", color_discrete_sequence=[ACCENT4])
        fig7.update_traces(textposition="outside", marker_line_width=0,
                           marker_cornerradius=8)
        styled(fig7, title_text="По менеджерам",
               yaxis=dict(autorange="reversed", showgrid=False),
               xaxis_title="", yaxis_title="")
        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.markdown(f'<div style="padding:48px;text-align:center;'
                    f'color:{TEXT_SEC};font-size:0.92rem">'
                    f'Нет данных по менеджерам</div>',
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r4b:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    bonus = filtered[filtered["procent_bonus_id"] > 0]
    if not bonus.empty:
        bd = bonus["procent_bonus_id"].value_counts().sort_index().reset_index()
        bd.columns = ["pct", "count"]
        fig8 = px.bar(bd, x="pct", y="count", text="count",
                      color_discrete_sequence=[ACCENT4])
        fig8.update_traces(textposition="outside", marker_line_width=0,
                           marker_cornerradius=8)
        styled(fig8, title_text="Бонусы (%)", xaxis_title="", yaxis_title="")
    else:
        day_order = ["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "Sunday"]
        day_labels = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        dow = (filtered["day_of_week"].value_counts()
               .reindex(day_order).fillna(0).reset_index())
        dow.columns = ["day", "count"]
        dow["label"] = day_labels
        fig8 = px.bar(dow, x="label", y="count", text="count",
                      color_discrete_sequence=[ACCENT1])
        fig8.update_traces(textposition="outside", marker_line_width=0,
                           marker_cornerradius=8)
        styled(fig8, title_text="По дням недели",
               xaxis_title="", yaxis_title="", showlegend=False)
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Top subscribers
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### Топ-10 абонентов")
st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
top = (filtered.groupby(["subscriber_id", "subscriber_name"])
       .size().reset_index(name="subs")
       .sort_values("subs", ascending=False).head(10))
fig9 = px.bar(top, x="subs", y="subscriber_name", orientation="h",
              text="subs", color_discrete_sequence=[ACCENT1])
fig9.update_traces(textposition="outside", marker_line_width=0,
                   marker_cornerradius=8)
styled(fig9, yaxis=dict(autorange="reversed", showgrid=False),
       xaxis_title="", yaxis_title="", height=400)
st.plotly_chart(fig9, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Table
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### Данные")
st.dataframe(
    filtered.drop(columns=["month", "day_of_week"], errors="ignore"),
    use_container_width=True,
    height=420,
)
