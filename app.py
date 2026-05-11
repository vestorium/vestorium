import streamlit as st
import pandas as pd
import os
import importlib
from src.github_scraper import GitHubScraper
from src.scoring_engine import ScoringEngine
from src.edge_case_tracker import EdgeCaseTracker

st.set_page_config(
    page_title="Vestorium AI Startup Screener",
    page_icon="Assets/VestoriumLogo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styling ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #E8F1EE;
        color: #042433;
    }

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
    section[data-testid="stSidebar"] .stSelectbox select,
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] *,
    section[data-testid="stSidebar"] .stSelectbox span {
        background-color: #0a3a4f !important;
        color: #E8F1EE !important;
    }

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

    .stExpander {
        background-color: #ffffff;
        border: 1px solid #d0ddd8;
        border-radius: 8px;
        margin-bottom: 0.6rem;
    }
    .stExpander:hover { border-color: #042433; }

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

    .meta-text {
        font-size: 0.82rem;
        color: #6B7C8D;
        margin-bottom: 0.75rem;
    }

    .vertical-badge {
        display: inline-block;
        background: #042433;
        color: #E8F1EE;
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Vertical registry ──────────────────────────────────────────────────
VERTICALS = {
    "Finance / Fintech"  : "src.verticals.fintech",
    "Developer Tools"    : "src.verticals.developer_tools",
    "Cybersecurity"      : "src.verticals.cybersecurity",
    "MLOps"              : "src.verticals.mlops",
    "Data Infrastructure": "src.verticals.datainfra",
    "Autonomous Systems" : "src.verticals.autonomous_systems",
    "Agentic AI"         : "src.verticals.agentic_ai"
}

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

def load_vertical_config(vertical_name):
    module_path = VERTICALS[vertical_name]
    return importlib.import_module(f"{module_path}.config")

def get_csv_path(config):
    return f"data/{config.VERTICAL_SLUG}_raw.csv"

def load_data(config):
    path = get_csv_path(config)
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

def save_data(df, config):
    os.makedirs("data", exist_ok=True)
    try:
        df.to_csv(get_csv_path(config), index=False)
        return True
    except PermissionError:
        return False

def analyze_repo(url, config, quick=True):
    scraper = GitHubScraper(GITHUB_TOKEN, quick=quick)
    tracker = EdgeCaseTracker(config=config)
    scorer  = ScoringEngine(config=config)

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

# ── Header ─────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([2, 7])
with col_logo:
    st.image("Assets/VestoriumLogo.png", width=140)
with col_title:
    st.markdown("""
    <div style="padding-top:0.5rem;">
        <div class="v-title">Vestorium</div>
        <div class="v-tagline">AI Startup Screener — Technical Due Diligence</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border:2px solid #042433;margin-bottom:1.5rem;'>",
            unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Vertical")
    selected_vertical = st.selectbox(
        "Select vertical",
        options=list(VERTICALS.keys()),
        label_visibility="collapsed"
    )

    config = load_vertical_config(selected_vertical)

    st.markdown("---")
    st.markdown("### Add New Repo")
    new_url      = st.text_input("GitHub URL",
                                  placeholder="https://github.com/owner/repo")
    quick_toggle = st.checkbox("Quick mode", value=True,
                                help="Faster but may undercount large repos")

    if st.button("Analyze", type="primary", use_container_width=True):
        if new_url:
            with st.spinner("Analyzing repo..."):
                data, scores = analyze_repo(new_url, config, quick=quick_toggle)
            if data:
                df = load_data(config)
                if not df.empty and "github_url" in df.columns:
                    df = df[df["github_url"] != new_url]
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                df = df.sort_values("total_score", ascending=False)
                saved = save_data(df, config)
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
    df_all = load_data(config)
    st.markdown(
        f"<div style='font-size:0.75rem;color:#6B7C8D;'>"
        f"Vertical: {config.VERTICAL_NAME}<br>"
        f"Repos loaded: {len(df_all)}</div>",
        unsafe_allow_html=True
    )

# ── Main list ──────────────────────────────────────────────────────────
st.markdown(
    f'<div class="vertical-badge">{config.VERTICAL_NAME}</div>',
    unsafe_allow_html=True
)

df = load_data(config)

if df.empty:
    st.info(f"No repos analyzed yet for {config.VERTICAL_NAME}. "
            f"Run test_scraper.py or add a GitHub URL in the sidebar.")
else:
    if "recommendation" in df.columns:
        df = df[df["recommendation"].isin(rec_filter)]
    if "total_score" in df.columns:
        df = df[(df["total_score"] >= score_range[0]) &
                (df["total_score"] <= score_range[1])]
    if "flag_count" in df.columns:
        df = df[df["flag_count"] <= max_flags]

    st.markdown(
        f"<div style='color:#6B7C8D;font-size:0.85rem;margin-bottom:1rem;'>"
        f"<b>{len(df)}</b> repos — sorted by score</div>",
        unsafe_allow_html=True
    )

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

        flag_label = (f"⚠️ {flags} flag{'s' if flags != 1 else ''}"
                      if flags > 0 else "✅ Clean")

        with st.expander(
            f"{name}   |   {score}/100   |   {rec}   |   {flag_label}"
        ):
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Score",           f"{score}/100")
            c2.metric("Recommendation",  rec)
            c3.metric("Stars",           f"{stars:,}")
            c4.metric("Commit Velocity", f"{velocity}/mo")
            c5.metric("Flags",           flags)

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
            st.markdown("**Score Breakdown**")

            # Use vertical-specific max points
            weights = config.DIMENSION_WEIGHTS
            dims_display = [
                ("Technical Execution",    "technical_execution_score",
                 weights["technical_execution"]),
                ("Technical Moat",         "technical_moat_score",
                 weights["technical_moat"]),
                ("Community Traction",     "community_traction_score",
                 weights["community_traction"]),
                ("Team Strength",          "team_strength_score",
                 weights["team_strength"]),
                ("Engineering Discipline", "engineering_discipline_score",
                 weights["engineering_discipline"]),
            ]

            for dim_name, col_name, max_pts in dims_display:
                dim_score = int(row.get(col_name, 0))
                pct       = int((dim_score / max_pts) * 100) if max_pts > 0 else 0
                st.markdown(f"""
                <div class="dim-row">
                    <span class="dim-label">{dim_name}</span>
                    <span class="dim-score">{dim_score}/{max_pts}</span>
                </div>
                <div class="score-bar-bg">
                    <div class="score-bar-fill" style="width:{pct}%"></div>
                </div>
                """, unsafe_allow_html=True)

            if flags > 0:
                st.markdown("---")
                st.markdown("**Edge Case Flags**")
                flag_codes = str(row.get("flag_codes", ""))
                for flag in flag_codes.split(","):
                    flag = flag.strip()
                    if flag and flag != "None" and flag != "nan":
                        st.markdown(
                            f'<span class="flag-pill">⚠️ {flag}</span>',
                            unsafe_allow_html=True
                        )

            st.markdown("")
            if st.button("🔄 Re-analyze", key=f"re_{name}_{score}"):
                with st.spinner(f"Re-analyzing {name}..."):
                    new_data, _ = analyze_repo(url, config, quick=quick_toggle)
                if new_data:
                    full_df = load_data(config)
                    full_df = full_df[full_df["github_url"] != url]
                    full_df = pd.concat(
                        [full_df, pd.DataFrame([new_data])],
                        ignore_index=True
                    )
                    full_df = full_df.sort_values("total_score", ascending=False)
                    saved = save_data(full_df, config)
                    if saved:
                        st.success("Re-analyzed successfully!")
                        st.rerun()
                    else:
                        st.error("Could not save — close Excel if open.")
                        
            # ── LLM Moat Analyzer ─────────────────────────────────────
            st.markdown("")
            if st.button("🧠 Run Moat Analysis", key=f"moat_{name}_{score}"):
                with st.spinner(f"Running moat analysis for {name}..."):
                    try:
                        from src.llm_moat_analyzer import run_moat_analysis
                        from src.github_scraper import GitHubScraper
                        import os
                        token = os.getenv("GITHUB_TOKEN", "")
                        scraper = GitHubScraper(token=token, quick=True)
                        owner, repo_name = url.replace("https://github.com/", "").split("/")[:2]
                        repo_data = {
                            "readme": scraper.get_readme(owner, repo_name),
                            "code_files": scraper.get_named_code_files(owner, repo_name),
                            "recent_prs": scraper.get_recent_prs(owner, repo_name)
                        }
                        moat_result = run_moat_analysis(url, repo_data, config)
                        st.session_state[f"moat_{url}"] = moat_result["result"]
                    except Exception as e:
                        st.error(f"Moat analysis failed: {e}")

            if f"moat_{url}" in st.session_state:
                moat = st.session_state[f"moat_{url}"]
                with st.expander("🧠 Moat Analysis", expanded=True):
                    build = moat.get("build_classification", "Undetermined")
                    moat_type = moat.get("moat_type", "Unknown")
                    rationale = moat.get("rationale", "")
                    prompts = moat.get("analyst_prompts", [])

                    build_color = (
                        "green" if build in ["Custom model", "Fine-tune"]
                        else "orange" if build == "API wrapper"
                        else "gray"
                    )
                    moat_color = (
                        "green" if moat_type in ["Data moat", "Model moat"]
                        else "orange" if moat_type == "Workflow moat"
                        else "red"
                    )

                    st.markdown(
                        f'<span style="background:{build_color};color:white;padding:4px 12px;'
                        f'border-radius:12px;font-weight:bold;font-size:1rem">{build}</span>'
                        f'&nbsp;&nbsp;'
                        f'<span style="background:{moat_color};color:white;padding:4px 12px;'
                        f'border-radius:12px;font-size:0.9rem">{moat_type}</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown("")
                    st.markdown(f"**Assessment:** {rationale}")
                    if prompts:
                        st.markdown("**Analyst Prompts:**")
                        for i, q in enumerate(prompts, 1):
                            st.markdown(f"{i}. {q}")