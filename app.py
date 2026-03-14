import streamlit as st
import pandas as pd
import os
from src.github_scraper import GitHubScraper
from src.scoring_engine import ScoringEngine
from src.edge_case_tracker import EdgeCaseTracker

st.set_page_config(
    page_title="Vestorium AI Startup Screener",
    page_icon="Assets/VestoriumLogo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #E8F1EE;
        color: #042433;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #042433;
    }
    section[data-testid="stSidebar"] * {
        color: #E8F1EE !important;
    }
    section[data-testid="stSidebar"] .stTextInput input {
        background-color: #0a3a4f;
        border: 1px solid #6B7C8D;
        color: #E8F1EE !important;
        border-radius: 6px;
    }
    section[data-testid="stSidebar"] .stButton button {
        background-color: #598D7F;
        color: #E8F1EE !important;
        border: none;
        font-weight: 600;
        border-radius: 6px;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #4a7a6d;
    }

    /* Header */
    .v-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #042433;
        margin-bottom: 1.5rem;
    }
    .v-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #042433;
        letter-spacing: -0.5px;
    }
    .v-tagline {
        font-size: 0.85rem;
        color: #6B7C8D;
        margin-top: 0.2rem;
    }

    /* Repo cards */
    .stExpander {
        background-color: #ffffff;
        border: 1px solid #d0ddd8;
        border-radius: 8px;
        margin-bottom: 0.6rem;
    }
    .stExpander:hover {
        border-color: #042433;
    }

    /* Score bar */
    .score-bar-bg {
        background: #d0ddd8;
        border-radius: 4px;
        height: 5px;
        margin-top: 4px;
        margin-bottom: 10px;
    }
    .score-bar-fill {
        height: 5px;
        border-radius: 4px;
        background: #598D7F;
    }

    /* Dimension row */
    .dim-row {
        display: flex;
        justify-content: space-between;
        padding: 5px 0;
        border-bottom: 1px solid #E8F1EE;
        font-size: 0.87rem;
    }
    .dim-label { color: #6B7C8D; }
    .dim-score {
        font-family: 'DM Mono', monospace;
        font-weight: 500;
        color: #042433;
    }

    /* Badges */
    .badge-strong-buy {
        background: #598D7F;
        color: #E8F1EE;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-buy {
        background: #E8F1EE;
        color: #042433;
        border: 1px solid #042433;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-pass {
        background: #f0f0f0;
        color: #6B7C8D;
        border: 1px solid #6B7C8D;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Flag pill */
    .flag-pill {
        background: #fff3cd;
        color: #856404;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75rem;
        margin-right: 4px;
        display: inline-block;
        margin-top: 4px;
    }

    /* Meta text */
    .meta-text {
        font-size: 0.82rem;
        color: #6B7C8D;
        margin-bottom: 0.75rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Config ─────────────────────────────────────────────────────────────────
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
CSV_PATH     = "data/fintech_raw.csv"

# ── Helpers ────────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame()

def save_data(df):
    os.makedirs("data", exist_ok=True)
    try:
        df.to_csv(CSV_PATH, index=False)
        return True
    except PermissionError:
        return False

def analyze_repo(url, quick=True):
    scraper = GitHubScraper(GITHUB_TOKEN, quick=quick)
    tracker = EdgeCaseTracker(vertical="Finance/Fintech")
    scorer  = ScoringEngine()

    data = scraper.get_repo_info(url)
    if not data:
        return None, None

    flags   = tracker.analyze(data)
    summary = tracker.get_summary(flags)
    data["flag_count"] = summary["flag_count"]
    data["flag_codes"] = summary["flag_codes"]

    scores = scorer.score(data)
    data["total_score"]    = scores["total"]
    data["recommendation"] = scores["recommendation"]

    for dim, vals in scores["breakdown"].items():
        col = dim.lower().replace(" ", "_") + "_score"
        data[col] = vals["score"]

    return data, scores

# ── Header ─────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([2, 7])
with col_logo:
    st.image("Assets/VestoriumLogo.png", width=280)
with col_title:
    st.markdown("""
    <div style="padding-top:0.5rem;">
        <div class="v-title">Vestorium</div>
        <div class="v-tagline">AI Startup Screener — Technical Due Diligence for Fintech</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border:2px solid #042433;margin-bottom:1.5rem;'>", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")

    st.markdown("### Add New Repo")
    new_url      = st.text_input("GitHub URL", placeholder="https://github.com/owner/repo")
    quick_toggle = st.checkbox("Quick mode", value=True,
                               help="Faster but may undercount large repos (300+ contributors)")

    if st.button("Analyze", type="primary", use_container_width=True):
        if new_url:
            with st.spinner("Analyzing repo..."):
                data, scores = analyze_repo(new_url, quick=quick_toggle)
            if data:
                df = load_data()
                if not df.empty and "github_url" in df.columns:
                    df = df[df["github_url"] != new_url]
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                df = df.sort_values("total_score", ascending=False)
                saved = save_data(df)
                if saved:
                    st.success(f"✅ {data['startup_name']} — {data['total_score']}/100 {data['recommendation']}")
                    st.rerun()
                else:
                    st.error("Could not save — close Excel if open and try again.")
            else:
                st.error("Could not fetch repo. Check the URL.")
        else:
            st.warning("Please enter a GitHub URL.")

    st.markdown("---")
    st.markdown("### Filters")

    rec_filter  = st.multiselect(
        "Recommendation",
        options=["Strong Buy", "Buy", "Pass"],
        default=["Strong Buy", "Buy", "Pass"]
    )
    score_range = st.slider("Score Range", 0, 100, (0, 100))
    max_flags   = st.slider("Max Flags", 0, 10, 10)

    st.markdown("---")
    df_all = load_data()
    st.markdown(f"<div style='font-size:0.75rem;color:#6B7C8D;'>Vertical: Finance / Fintech<br>Repos loaded: {len(df_all)}</div>",
                unsafe_allow_html=True)

# ── Main list ──────────────────────────────────────────────────────────────
df = load_data()

if df.empty:
    st.info("No repos analyzed yet. Add a GitHub URL in the sidebar to get started.")
else:
    # Apply filters
    if "recommendation" in df.columns:
        df = df[df["recommendation"].isin(rec_filter)]
    if "total_score" in df.columns:
        df = df[(df["total_score"] >= score_range[0]) & (df["total_score"] <= score_range[1])]
    if "flag_count" in df.columns:
        df = df[df["flag_count"] <= max_flags]

    st.markdown(f"<div style='color:#6B7C8D;font-size:0.85rem;margin-bottom:1rem;'><b>{len(df)}</b> repos matching filters — sorted by score</div>",
                unsafe_allow_html=True)

    dims = [
        ("Technical Execution",    "technical_execution_score",    30),
        ("Technical Moat",         "technical_moat_score",         30),
        ("Community Traction",     "community_traction_score",     20),
        ("Team Strength",          "team_strength_score",          15),
        ("Engineering Discipline", "engineering_discipline_score",  5),
    ]

    for _, row in df.iterrows():
        name      = str(row.get("startup_name") or "Unknown")
        score     = int(row.get("total_score", 0))
        rec       = str(row.get("recommendation", "Pass"))
        flags     = int(row.get("flag_count", 0))
        url       = str(row.get("github_url", ""))
        stars     = int(row.get("stars", 0))
        age       = float(row.get("repo_age_months", 0))
        lang      = str(row.get("language", ""))
        framework = str(row.get("ai_framework", ""))
        created   = str(row.get("repo_created_date", ""))
        velocity  = float(row.get("commit_velocity", 0))

        badge = {
            "Strong Buy": '<span class="badge-strong-buy">Strong Buy</span>',
            "Buy"       : '<span class="badge-buy">Buy</span>',
            "Pass"      : '<span class="badge-pass">Pass</span>',
        }.get(rec, '<span class="badge-pass">Pass</span>')

        flag_label = f"⚠️ {flags} flag{'s' if flags != 1 else ''}" if flags > 0 else "✅ Clean"

        with st.expander(f"{name}   |   {score}/100   |   {rec}   |   {flag_label}"):

            # Metrics row
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Score",            f"{score}/100")
            c2.metric("Recommendation",   rec)
            c3.metric("Stars",            f"{stars:,}")
            c4.metric("Commit Velocity",  f"{velocity}/mo")
            c5.metric("Flags",            flags)

            # Meta row
            st.markdown(f"""
            <div class="meta-text">
                <b>Language:</b> {lang} &nbsp;|&nbsp;
                <b>AI Framework:</b> {framework} &nbsp;|&nbsp;
                <b>Repo Age:</b> {age:.0f} months &nbsp;|&nbsp;
                <b>Created:</b> {created}
            </div>
            """, unsafe_allow_html=True)

            if url and url != "nan":
                st.markdown(f"🔗 [{url}]({url})")

            st.markdown("---")

            # Score breakdown
            st.markdown("**Score Breakdown**")
            for dim_name, col_name, max_pts in dims:
                dim_score = int(row.get(col_name, 0))
                pct       = int((dim_score / max_pts) * 100)
                st.markdown(f"""
                <div class="dim-row">
                    <span class="dim-label">{dim_name}</span>
                    <span class="dim-score">{dim_score}/{max_pts}</span>
                </div>
                <div class="score-bar-bg">
                    <div class="score-bar-fill" style="width:{pct}%"></div>
                </div>
                """, unsafe_allow_html=True)

            # Flags
            if flags > 0:
                st.markdown("---")
                st.markdown("**Edge Case Flags**")
                flag_codes = str(row.get("flag_codes", ""))
                for flag in flag_codes.split(","):
                    flag = flag.strip()
                    if flag and flag != "None" and flag != "nan":
                        st.markdown(f'<span class="flag-pill">⚠️ {flag}</span>',
                                    unsafe_allow_html=True)

            # Re-analyze
            st.markdown("")
            if st.button("🔄 Re-analyze", key=f"re_{name}_{score}"):
                with st.spinner(f"Re-analyzing {name}..."):
                    new_data, _ = analyze_repo(url, quick=quick_toggle)
                if new_data:
                    full_df = load_data()
                    full_df = full_df[full_df["github_url"] != url]
                    full_df = pd.concat([full_df, pd.DataFrame([new_data])], ignore_index=True)
                    full_df = full_df.sort_values("total_score", ascending=False)
                    saved = save_data(full_df)
                    if saved:
                        st.success("Re-analyzed successfully!")
                        st.rerun()
                    else:
                        st.error("Could not save — close Excel if open and try again.")
