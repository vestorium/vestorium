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
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #E8F1EE;
        color: #042433;
    }

    .block-container {
        padding-top: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* ── Navbar ── */
    .v-navbar {
        background-color: #042433;
        padding: 0.8rem 1.5rem;
        margin-left: -2rem;
        margin-right: -2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }

    /* ── Control bar ── */
    .v-controlbar {
        background-color: #ffffff;
        border: 1px solid #d0ddd8;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
    }

    /* ── Repo cards ── */
    .stExpander {
        background-color: #ffffff !important;
        border: 1px solid #d0ddd8 !important;
        border-radius: 8px !important;
        margin-bottom: 0.5rem !important;
    }
    .stExpander:hover {
        border-color: #042433 !important;
    }

    /* ── Score bars ── */
    .score-bar-bg {
        background: #d0ddd8;
        border-radius: 4px;
        height: 8px;
        margin-top: 4px;
        margin-bottom: 10px;
    }
    .score-bar-fill {
        height: 8px;
        border-radius: 4px;
        background: #598D7F;
    }

    /* ── Dimension rows ── */
    .dim-row {
        display: flex;
        justify-content: space-between;
        padding: 5px 0;
        border-bottom: 1px solid #E8F1EE;
        font-size: 0.87rem;
    }
    .dim-label { color: #042433; font-weight: 500; }
    .dim-score {
        font-family: 'DM Mono', monospace;
        font-weight: 500;
        color: #042433;
    }

    /* ── Flags ── */
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

    /* ── New Analysis badge ── */
    .new-badge {
        background: #598D7F;
        color: white;
        padding: 2px 10px;
        border-radius: 10px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 0.5rem;
    }

    /* ── Meta text ── */
    .meta-text {
        font-size: 0.82rem;
        color: #6B7C8D;
        margin-bottom: 0.75rem;
    }

    /* ── Vertical badge ── */
    .vertical-badge {
        display: inline-block;
        background: #042433;
        color: #E8F1EE;
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 12px;
        margin-bottom: 0.75rem;
    }

    /* ── Moat divider ── */
    .moat-divider {
        border-left: 2px solid #d0ddd8;
        padding-left: 1.5rem;
    }

    /* ── Analyze button ── */
    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #598D7F !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background-color: #4a7a6d !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    section[data-testid="stSidebar"] {display: none;}
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

# ── Navbar ─────────────────────────────────────────────────────────────
st.markdown('<div class="v-navbar">', unsafe_allow_html=True)
col_logo, col_spacer = st.columns([1, 11])
with col_logo:
    st.image("Assets/VestoriumLogo.png", width=110)
st.markdown('</div>', unsafe_allow_html=True)

# ── Control bar ────────────────────────────────────────────────────────
st.markdown('<div class="v-controlbar">', unsafe_allow_html=True)
t1, t2, t3, t4 = st.columns([2, 4, 1.2, 1])

with t1:
    selected_vertical = st.selectbox(
        "Vertical",
        options=list(VERTICALS.keys()),
        label_visibility="collapsed"
    )

config = load_vertical_config(selected_vertical)

with t2:
    new_url = st.text_input(
        "GitHub URL",
        placeholder="https://github.com/owner/repo",
        label_visibility="collapsed"
    )
with t3:
    quick_toggle = st.checkbox("Quick Mode", value=True,
                               help="Faster but may undercount large repos")
with t4:
    analyze_clicked = st.button("Analyze", type="primary",
                                use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if analyze_clicked:
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
                st.session_state["new_repo_url"] = new_url
                st.success(
                    f"✅ {data['startup_name']} — "
                    f"{data['total_score']}/100 {data['recommendation']}"
                )
                st.rerun()
            else:
                st.error("Could not save — close Excel if open and try again.")
        else:
            st.error("Could not fetch repo. Check the URL.")
    else:
        st.warning("Please enter a GitHub URL.")

# ── Main list ──────────────────────────────────────────────────────────
st.markdown(
    f'<div class="vertical-badge">{config.VERTICAL_NAME}</div>',
    unsafe_allow_html=True
)

df = load_data(config)

if df.empty:
    st.info(f"No repos analyzed yet for {config.VERTICAL_NAME}. "
            f"Add a GitHub URL above or run test_scraper.py.")
else:
    df = df.sort_values("total_score", ascending=False)
    new_repo_url = st.session_state.get("new_repo_url", "")

    if new_repo_url and "github_url" in df.columns:
        new_row = df[df["github_url"] == new_repo_url]
        rest    = df[df["github_url"] != new_repo_url]
        df      = pd.concat([new_row, rest], ignore_index=True)

    st.markdown(
        f"<div style='color:#6B7C8D;font-size:0.85rem;margin-bottom:0.75rem;'>"
        f"<b>{len(df)}</b> sample repos — sorted by score</div>",
        unsafe_allow_html=True
    )

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

        is_new   = (url == new_repo_url and new_repo_url != "")
        new_tag  = "   🟢 New Analysis" if is_new else ""

        with st.expander(
            f"{name}   |   {score}/100   |   {rec}   |   {flag_label}{new_tag}",
            expanded=is_new
        ):
            if is_new:
                st.markdown(
                    '<span class="new-badge">✦ New Analysis</span>',
                    unsafe_allow_html=True
                )

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Score",           f"{score}/100")
            c2.metric("Recommendation",  rec)
            c3.metric("Stars",           f"{stars:,}")
            c4.metric("Commit Velocity", f"{velocity}/mo")

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

            has_moat = f"moat_{url}" in st.session_state

            if has_moat:
                left_col, right_col = st.columns([1, 1])
            else:
                left_col = st.container()

            with left_col:
                st.markdown("**Score Breakdown**")
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

            if has_moat:
                with right_col:
                    moat      = st.session_state[f"moat_{url}"]
                    build     = moat.get("build_classification", "Undetermined")
                    moat_type = moat.get("moat_type", "Unknown")
                    rationale = moat.get("rationale", "")
                    prompts   = moat.get("analyst_prompts", [])

                    build_color = (
                        "#2e7d5e" if build in ["Custom model", "Fine-tune"]
                        else "#e07b00" if build == "API wrapper"
                        else "#6B7C8D"
                    )
                    moat_color = (
                        "#2e7d5e" if moat_type in ["Data moat", "Model moat"]
                        else "#e07b00" if moat_type == "Workflow moat"
                        else "#c0392b"
                    )

                    st.markdown('<div class="moat-divider">', unsafe_allow_html=True)
                    st.markdown("**Moat Analysis**")
                    st.markdown(
                        f'<span style="background:{build_color};color:white;'
                        f'padding:4px 12px;border-radius:12px;font-weight:bold;'
                        f'font-size:0.85rem">{build}</span>'
                        f'&nbsp;&nbsp;'
                        f'<span style="background:{moat_color};color:white;'
                        f'padding:4px 12px;border-radius:12px;'
                        f'font-size:0.8rem">{moat_type}</span>',
                        unsafe_allow_html=True
                    )
                    st.markdown("")
                    st.markdown(f"**Assessment:** {rationale}")
                    if prompts:
                        st.markdown("**Analyst Prompts:**")
                        for i, q in enumerate(prompts, 1):
                            st.markdown(f"{i}. {q}")
                    st.markdown('</div>', unsafe_allow_html=True)

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
            cb1, cb2, cb3 = st.columns([1.5, 1.5, 5])

            with cb1:
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

            with cb2:
                if st.button("🧠 Run Moat Analysis", key=f"moat_{name}_{score}"):
                    with st.spinner(f"Running moat analysis for {name}..."):
                        try:
                            from src.llm_moat_analyzer import run_moat_analysis
                            from src.github_scraper import GitHubScraper
                            import os
                            token = os.getenv("GITHUB_TOKEN", "")
                            scraper = GitHubScraper(token=token, quick=True)
                            owner, repo_name = url.replace(
                                "https://github.com/", ""
                            ).split("/")[:2]
                            repo_data = {
                                "readme"    : scraper.get_readme(owner, repo_name),
                                "code_files": scraper.get_named_code_files(owner, repo_name),
                                "recent_prs": scraper.get_recent_prs(owner, repo_name)
                            }
                            moat_result = run_moat_analysis(url, repo_data, config)
                            st.session_state[f"moat_{url}"] = moat_result["result"]
                            st.rerun()
                        except Exception as e:
                            st.error(f"Moat analysis failed: {e}")