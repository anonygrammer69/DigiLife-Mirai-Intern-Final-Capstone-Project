import os
import streamlit as st
import pandas as pd
from google import genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="DigiLife",
    page_icon="\U0001f4f1",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Palette ─────────────────────────────────────── */
    /*  bg:       #0d1117  #151d2e  #1c2537             */
    /*  accent:   #7c5cfc  #a78bfa                      */
    /*  green:    #34d399   amber: #fbbf24   red: #f87171 */

    * { box-sizing: border-box; }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background: #0d1117 !important;
        color: #e2e8f0 !important;
    }
    .stApp > header { background: transparent !important; }

    #MainMenu, footer, .stDeployButton { display: none !important; }

    /* Push everything below the Streamlit header bar */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }

    /* ── Main title / subtitle ───────────────────────── */
    .main-title { margin-bottom: 2px; }
    .sub-title { margin-top: 0 !important; margin-bottom: 16px !important; }

    /* ── Sidebar ─────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: #151d2e !important;
        border-right: 1px solid #2a3654 !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
    }
    section[data-testid="stSidebar"] p {
        color: #8892b0 !important;
    }
    .sidebar-section {
        font-size: 0.85rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 8px;
        padding-bottom: 6px;
        border-bottom: 1px solid #2a3654;
    }
    .sidebar-section span { color: #a78bfa; }
    .sidebar-hint {
        font-size: 0.78rem;
        color: #546178;
        line-height: 1.7;
    }

    /* ── Tabs ────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #151d2e;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #2a3654;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #8892b0;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 500;
        border: none;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #e2e8f0;
        background: #1c2537;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c5cfc, #6366f1) !important;
        color: #fff !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.5rem !important;
        overflow: visible !important;
    }

    /* ── Section Headers ─────────────────────────────── */
    .section-header {
        font-size: 1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-top: 0;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #2a3654;
    }
    .section-header span { color: #a78bfa; }

    /* ── Metric Cards ────────────────────────────────── */
    .metric-card {
        background: #1c2537;
        border: 1px solid #2a3654;
        border-radius: 12px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        margin-bottom: 12px;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #7c5cfc, #6366f1, transparent);
    }
    .metric-card:hover {
        border-color: #7c5cfc;
        box-shadow: 0 0 24px rgba(124, 92, 252, 0.12);
    }
    .metric-card .icon {
        font-size: 1.3rem;
        margin-bottom: 6px;
        opacity: 0.9;
    }
    .metric-card .value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #e2e8f0;
        line-height: 1.2;
        word-break: break-word;
    }
    .metric-card .label {
        font-size: 0.72rem;
        color: #8892b0;
        margin-top: 4px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card.green .value { color: #34d399; }
    .metric-card.amber .value { color: #fbbf24; }
    .metric-card.red   .value { color: #f87171; }
    .metric-card.accent .value { color: #a78bfa; }
    .metric-card.text-card .value {
        font-size: 1.1rem;
        font-weight: 600;
    }

    /* ── Insight Block ───────────────────────────────── */
    .insight-block {
        background: #1c2537;
        border-left: 3px solid #7c5cfc;
        border-radius: 0 12px 12px 0;
        padding: 24px 28px;
        color: #e2e8f0;
        line-height: 1.75;
        font-size: 0.95rem;
        margin-top: 8px;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    .insight-block h1, .insight-block h2, .insight-block h3 {
        color: #a78bfa !important;
        margin-top: 16px !important;
    }

    /* ── Empty State ─────────────────────────────────── */
    .empty-state {
        text-align: center;
        padding: 60px 40px;
        color: #8892b0;
    }
    .empty-state .empty-icon { font-size: 3rem; margin-bottom: 12px; opacity: 0.5; }
    .empty-state h3 { color: #e2e8f0; font-weight: 600; margin-bottom: 8px; }
    .empty-state p { font-size: 0.9rem; max-width: 400px; margin: 0 auto; line-height: 1.6; }

    /* ── Form ────────────────────────────────────────── */
    div[data-testid="stForm"] {
        background: #151d2e;
        border: 1px solid #2a3654;
        border-radius: 12px;
        padding: 24px;
    }

    .stTextInput input,
    .stNumberInput input {
        background: #1c2537 !important;
        border: 1px solid #2a3654 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }
    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: #7c5cfc !important;
        box-shadow: 0 0 0 2px rgba(124, 92, 252, 0.15) !important;
    }
    .stTextArea textarea {
        background: #1c2537 !important;
        border: 1px solid #2a3654 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }
    .stTextArea textarea:focus {
        border-color: #7c5cfc !important;
        box-shadow: 0 0 0 2px rgba(124, 92, 252, 0.15) !important;
    }

    [data-testid="column"] {
        overflow: visible !important;
    }
    [data-testid="stHorizontalBlock"] {
        overflow: visible !important;
    }

    /* ── Buttons ─────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #7c5cfc, #6366f1) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        box-shadow: 0 4px 20px rgba(124, 92, 252, 0.3) !important;
    }

    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #7c5cfc, #6366f1) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.5rem 2rem !important;
    }

    /* ── File Uploader ───────────────────────────────── */
    section[data-testid="stFileUploadDropzone"] {
        background: #1c2537 !important;
        border: 2px dashed #2a3654 !important;
        border-radius: 12px !important;
    }
    section[data-testid="stFileUploadDropzone"]:hover {
        border-color: #7c5cfc !important;
        background: #212c42 !important;
    }

    .stAlert {
        border-radius: 8px !important;
    }

    /* ── Chart ───────────────────────────────────────── */
    [data-testid="stBarChart"] {
        background: #1c2537;
        border: 1px solid #2a3654;
        border-radius: 12px;
        padding: 16px;
    }

    /* ── Sidebar Slider ──────────────────────────────── */
    section[data-testid="stSidebar"] [data-baseweb="slider"] {
        padding-top: 4px !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="slider"] [data-testid="stThumbValue"] {
        color: #a78bfa !important;
    }

    /* Hide the space-labels so they don't render but keep input structure */
    [data-testid="stHorizontalBlock"] label[data-testid="stWidgetLabel"] {
        clip: rect(0 0 0 0) !important;
        clip-path: inset(50%) !important;
        height: 1px !important;
        overflow: hidden !important;
        position: absolute !important;
        white-space: nowrap !important;
        width: 1px !important;
    }

    /* Delete button: match input widget height */
    [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child [data-testid="stButton"] button {
        background: rgba(248, 113, 113, 0.1) !important;
        color: #f87171 !important;
        border: 1px solid rgba(248, 113, 113, 0.2) !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        font-size: 0.85rem !important;
        line-height: 1 !important;
        min-width: 0 !important;
        width: 100% !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s !important;
    }
    [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child [data-testid="stButton"] button:hover {
        background: rgba(248, 113, 113, 0.25) !important;
        border-color: #f87171 !important;
        box-shadow: 0 0 12px rgba(248, 113, 113, 0.15) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Gemini Client ────────────────────────────────────────────────────────────
@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("API_KEY")
    if not api_key:
        st.error("`API_KEY` environment variable not set.")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_gemini_client()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 12px 0 4px 0;">
            <div style="font-size:2.2rem; margin-bottom:2px;">\U0001f4f1</div>
            <div style="font-size:1.4rem; font-weight:700; color:#e2e8f0; letter-spacing:-0.5px;">DigiLife</div>
            <div style="font-size:0.75rem; color:#8892b0; margin-top:2px;">AI-powered Digital Wellbeing Tracker</div>
        </div>
        <div style="height:1px; background:linear-gradient(90deg, transparent, #2a3654, transparent); margin:12px 0;"></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section"><span>\U0001f4c2</span> Import Data</div>',
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

    st.markdown(
        '<div class="sidebar-section" style="margin-top:20px;"><span>\U0001f514</span> Daily Limit</div>',
        unsafe_allow_html=True,
    )
    daily_limit = st.slider(
        "Daily screen time limit (minutes)",
        min_value=30,
        max_value=720,
        value=180,
        step=15,
        format="%d min",
        label_visibility="collapsed",
    )
    limit_h, limit_m = divmod(daily_limit, 60)
    st.markdown(
        f'<div class="sidebar-hint">Set to <strong>{limit_h}h {limit_m}m</strong> per day</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section" style="margin-top:20px;"><span>\u2139\ufe0f</span> How to use</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sidebar-hint">1. Upload a CSV or enter apps manually<br>2. Click <strong>Analyze</strong><br>3. View dashboard and AI insights</div>',
        unsafe_allow_html=True,
    )

# ── Load CSV ─────────────────────────────────────────────────────────────────
uploaded_df = None
if uploaded_file:
    try:
        uploaded_df = pd.read_csv(uploaded_file)
        uploaded_df["Minutes Used"] = pd.to_numeric(
            uploaded_df["Minutes Used"], errors="coerce"
        ).fillna(0)
    except Exception as error:
        st.error(f"CSV error: {error}")
        uploaded_df = None

# ── Categories ───────────────────────────────────────────────────────────────
categories = [
    "Social Media",
    "Education",
    "Coding",
    "Entertainment",
    "Productivity",
    "Communication",
    "Music",
    "Shopping",
    "Finance",
]

# ── Session State ────────────────────────────────────────────────────────────
if "row_ids" not in st.session_state:
    st.session_state.row_ids = [0]
if "next_row_id" not in st.session_state:
    st.session_state.next_row_id = 1
if "analyze" not in st.session_state:
    st.session_state.analyze = False

# ── Main Content ─────────────────────────────────────────────────────────────
st.markdown(
    '<p class="main-title" style="font-size:1.5rem; font-weight:700; letter-spacing:-0.5px; margin-bottom:0;">DigiLife</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title" style="color:#8892b0; font-size:0.85rem; margin-top:0;">Track your screen time. Understand your habits. Improve your digital wellbeing.</p>',
    unsafe_allow_html=True,
)

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab_input, tab_dashboard, tab_insights = st.tabs(
    ["\u2328\ufe0f  Data Input", "\U0001f4ca  Dashboard", "\u2728  AI Insights"]
)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Data Input
# ─────────────────────────────────────────────────────────────────────────────
with tab_input:
    if uploaded_df is not None:
        st.markdown(
            '<div class="section-header"><span>\U0001f4cb</span> Loaded CSV Data</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(uploaded_df, use_container_width=True)
        st.success(
            f"Loaded **{len(uploaded_df)}** apps from **{uploaded_file.name}**"
        )
    else:
        st.markdown(
            '<div class="section-header"><span>\u270f\ufe0f</span> Manual Entry</div>',
            unsafe_allow_html=True,
        )

        for idx, row_id in enumerate(st.session_state.row_ids):
            c1, c2, c3, c4 = st.columns([3, 2, 1.2, 0.5])
            with c1:
                st.text_input(
                    "App Name", key=f"app_{row_id}",
                    label_visibility="collapsed", placeholder="e.g. Instagram"
                )
            with c2:
                st.selectbox(
                    "Category", categories, key=f"category_{row_id}",
                    label_visibility="collapsed"
                )
            with c3:
                st.number_input(
                    "Minutes", min_value=0, step=15, key=f"minutes_{row_id}",
                    label_visibility="collapsed"
                )
            with c4:
                if st.button("\U0001f5d1\ufe0f", key=f"del_{row_id}", help="Remove this app", use_container_width=True):
                    st.session_state.row_ids.remove(row_id)
                    for k in [f"app_{row_id}", f"category_{row_id}", f"minutes_{row_id}"]:
                        if k in st.session_state:
                            del st.session_state[k]
                    st.rerun()

        st.markdown(
            '<div style="height: 4px;"></div>',
            unsafe_allow_html=True,
        )

        b1, b2 = st.columns([1, 4])
        with b1:
            if st.button("\uff0b  Add app"):
                st.session_state.row_ids.append(st.session_state.next_row_id)
                st.session_state.next_row_id += 1
                st.rerun()
        with b2:
            if st.button("\u2728  Analyze", use_container_width=True):
                st.session_state.analyze = True
                st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# Build dataframe from session
# ─────────────────────────────────────────────────────────────────────────────
df = None
if uploaded_df is not None:
    df = uploaded_df.copy()
elif st.session_state.get("analyze"):
    active_ids = st.session_state.row_ids
    app_names = [st.session_state.get(f"app_{rid}", "") for rid in active_ids]
    app_categories = [st.session_state.get(f"category_{rid}", categories[0]) for rid in active_ids]
    app_minutes = [st.session_state.get(f"minutes_{rid}", 0) for rid in active_ids]
    df = pd.DataFrame({"App Name": app_names, "Category": app_categories, "Minutes Used": app_minutes})
    df = df[df["App Name"].str.strip() != ""]

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Dashboard
# ─────────────────────────────────────────────────────────────────────────────
with tab_dashboard:
    if df is not None and not df.empty:
        total = int(df["Minutes Used"].sum())
        average = round(df["Minutes Used"].mean(), 1)
        most_used = df.loc[df["Minutes Used"].idxmax(), "App Name"]
        top_cat = df.groupby("Category")["Minutes Used"].sum().idxmax()
        least_used = df.loc[df["Minutes Used"].idxmin(), "App Name"]
        num_apps = len(df)

        if total <= 120:
            rating_color, rating_label, rating_icon = "green", "Healthy", "\u2705"
        elif total <= 300:
            rating_color, rating_label, rating_icon = "amber", "Moderate", "\u26a0\ufe0f"
        else:
            rating_color, rating_label, rating_icon = "red", "Heavy", "\U0001f534"

        st.markdown(
            '<div class="section-header"><span>\U0001f4ca</span> Overview</div>',
            unsafe_allow_html=True,
        )

        usage_pct = min(total / daily_limit, 1.0) if daily_limit > 0 else 0
        remaining = max(daily_limit - total, 0)
        over = max(total - daily_limit, 0)

        if usage_pct < 0.5:
            bar_color, status_text = "#34d399", f"{remaining}m remaining"
        elif usage_pct < 0.8:
            bar_color, status_text = "#fbbf24", f"{remaining}m remaining"
        else:
            bar_color, status_text = "#f87171", (f"{over}m over limit" if over else "Almost at limit")

        st.markdown(
            f"""
            <div style="background:#1c2537; border:1px solid #2a3654; border-radius:12px; padding:16px 20px; margin-bottom:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:0.8rem; font-weight:600; color:#8892b0; text-transform:uppercase; letter-spacing:0.5px;">Daily Limit</span>
                    <span style="font-size:0.8rem; font-weight:600; color:{bar_color};">{total} / {daily_limit} min &mdash; {status_text}</span>
                </div>
                <div style="background:#0d1117; border-radius:6px; height:8px; overflow:hidden;">
                    <div style="width:{usage_pct * 100:.1f}%; height:100%; background:{bar_color}; border-radius:6px; transition:width 0.3s;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f'<div class="metric-card accent">'
                f'<div class="icon">\u23f1\ufe0f</div>'
                f'<div class="value">{total}</div>'
                f'<div class="label">Total Minutes</div></div>',
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="icon">\U0001f4c8</div>'
                f'<div class="value">{average}</div>'
                f'<div class="label">Average / App (Minutes)</div></div>',
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f'<div class="metric-card {rating_color}">'
                f'<div class="icon">{rating_icon}</div>'
                f'<div class="value">{total // 60}h {total % 60}m</div>'
                f'<div class="label">{rating_label}</div></div>',
                unsafe_allow_html=True,
            )
        with m4:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="icon">\U0001f4f1</div>'
                f'<div class="value">{num_apps}</div>'
                f'<div class="label">Apps Tracked</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="section-header" style="margin-top:8px;"><span>\U0001f3c6</span> Breakdown</div>',
            unsafe_allow_html=True,
        )

        m5, m6, m7 = st.columns(3)
        with m5:
            st.markdown(
                f'<div class="metric-card green text-card">'
                f'<div class="icon">\U0001f3c6</div>'
                f'<div class="value">{most_used}</div>'
                f'<div class="label">Most Used App</div></div>',
                unsafe_allow_html=True,
            )
        with m6:
            st.markdown(
                f'<div class="metric-card amber text-card">'
                f'<div class="icon">\U0001f4c2</div>'
                f'<div class="value">{top_cat}</div>'
                f'<div class="label">Top Category</div></div>',
                unsafe_allow_html=True,
            )
        with m7:
            st.markdown(
                f'<div class="metric-card text-card">'
                f'<div class="icon">\U0001f4c9</div>'
                f'<div class="value">{least_used}</div>'
                f'<div class="label">Least Used App</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="section-header" style="margin-top:8px;"><span>\U0001f4ca</span> Time by App</div>',
            unsafe_allow_html=True,
        )

        import altair as alt

        chart_df = df[["App Name", "Minutes Used"]].sort_values("Minutes Used", ascending=False).reset_index(drop=True)

        bars = (
            alt.Chart(chart_df)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("App Name:N", sort="-y", axis=alt.Axis(labelColor="#8892b0", title=None, labelAngle=-30, labelFontSize=11)),
                y=alt.Y("Minutes Used:Q", axis=alt.Axis(labelColor="#8892b0", gridColor="#1e2d42", domainColor="#2a3654", title="Minutes")),
                color=alt.Color("App Name:N", legend=None, scale=alt.Scale(scheme="tableau10")),
                tooltip=["App Name", "Minutes Used"],
            )
        )

        chart = bars.properties(
            height=320,
            background="transparent",
        ).configure_view(stroke=None)

        st.altair_chart(chart, use_container_width=True)

        # ── Pie Chart ────────────────────────────────────────────────
        st.markdown(
            '<div class="section-header" style="margin-top:8px;"><span>\U0001f967</span> Usage Breakdown</div>',
            unsafe_allow_html=True,
        )

        pie_df = chart_df.copy()
        pie_df["Percentage"] = (pie_df["Minutes Used"] / total * 100).round(1)
        pie_df["Label"] = pie_df.apply(
            lambda r: f"{r['App Name']}\n{int(r['Minutes Used'])}m ({r['Percentage']}%)", axis=1
        )

        pie = (
            alt.Chart(pie_df)
            .mark_arc(innerRadius=50, outerRadius=140, cornerRadius=4, padAngle=0.02)
            .encode(
                theta=alt.Theta("Minutes Used:Q", stack=True),
                color=alt.Color(
                    "App Name:N",
                    legend=alt.Legend(
                        orient="bottom",
                        columns=3,
                        labelColor="#8892b0",
                        title=None,
                        symbolType="square",
                        symbolSize=100,
                    ),
                    scale=alt.Scale(scheme="tableau10"),
                ),
                tooltip=["App Name", "Minutes Used", "Percentage"],
            )
        )

        pie_text = (
            alt.Chart(pie_df)
            .mark_text(radius=170, fontSize=11, fontWeight=500, color="#e2e8f0")
            .encode(
                theta=alt.Theta("Minutes Used:Q", stack=True),
                text=alt.Text("Label:N"),
            )
            .transform_filter("datum.Percentage >= 6")
        )

        pie_chart = (pie + pie_text).properties(
            height=400,
            background="transparent",
        ).configure_view(stroke=None)

        st.altair_chart(pie_chart, use_container_width=True)

        if total > daily_limit:
            over_mins = total - daily_limit
            over_h, over_m = divmod(over_mins, 60)
            time_str = f"{over_h}h {over_m}m" if over_h else f"{over_m}m"
            st.markdown(
                f"""
                <div style="background:rgba(248,113,113,0.1); border:1px solid rgba(248,113,113,0.25); border-radius:12px; padding:14px 20px; text-align:center; margin-top:4px;">
                    <span style="font-size:0.95rem; color:#f87171; font-weight:600;">
                        \U0001f534 You have exceeded your daily limit by <strong>{time_str}</strong> ({over_mins} minutes)
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">\U0001f4ca</div>
                <h3>No data yet</h3>
                <p>Upload a CSV file or manually enter your app usage in the <strong>Data Input</strong> tab to see your dashboard.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — AI Insights
# ─────────────────────────────────────────────────────────────────────────────
with tab_insights:
    if df is not None and not df.empty:
        st.markdown(
            '<div class="section-header"><span>\u2728</span> Ask Gemini</div>',
            unsafe_allow_html=True,
        )

        user_question = st.text_area(
            "Ask anything about your screen time",
            placeholder="e.g. How can I reduce my social media usage?",
            label_visibility="collapsed",
        )

        if st.button("\u2728  Generate Insights", use_container_width=True):
            prompt = (
                f"Analyze the following screen time data and summarize the user's app habits:\n\n"
                f"{df.to_string(index=False)}\n\n"
            )
            if user_question:
                prompt += f"User question: {user_question}\n\n"
            prompt += (
                "Describe patterns, trends, and recommendations for better digital wellbeing. "
                "Format your response in clean markdown with headers, bullet points, and bold text where appropriate."
            )

            with st.spinner("Analyzing your screen time habits..."):
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

            st.markdown(
                '<div class="section-header" style="margin-top:16px;"><span>\U0001f4a1</span> Gemini Analysis</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="insight-block">{response.text}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p style="text-align:center; font-size:0.7rem; color:#546178; margin-top:12px;">Powered by Google Gemini</p>',
                unsafe_allow_html=True,
            )

    else:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">\u2728</div>
                <h3>No data to analyze</h3>
                <p>Add your screen time data first, then come back here for AI-powered insights and suggestions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
