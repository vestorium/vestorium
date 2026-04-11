import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.github_scraper import GitHubScraper
from src.scoring_engine import ScoringEngine
from src.edge_case_tracker import EdgeCaseTracker
import pandas as pd

# ── Vertical selection ─────────────────────────────────────────────────
AVAILABLE_VERTICALS = {
    "fintech"          : "src.verticals.fintech",
    "developer_tools"  : "src.verticals.developer_tools",
}

def load_vertical(slug):
    if slug not in AVAILABLE_VERTICALS:
        print(f"Unknown vertical: {slug}")
        print(f"Available: {', '.join(AVAILABLE_VERTICALS.keys())}")
        sys.exit(1)
    import importlib
    module_path = AVAILABLE_VERTICALS[slug]
    config      = importlib.import_module(f"{module_path}.config")
    repos       = importlib.import_module(f"{module_path}.sample_repos")
    return config, repos.SAMPLE_REPOS

# Default to fintech if no argument passed
vertical_slug = sys.argv[1] if len(sys.argv) > 1 else "fintech"
config, SAMPLE_REPOS = load_vertical(vertical_slug)

TOKEN      = os.getenv("GITHUB_TOKEN", "")
quick_mode = True

tracker      = EdgeCaseTracker(config=config)
scorer       = ScoringEngine(config=config)
semaphore    = threading.Semaphore(1)
results      = []
results_lock = threading.Lock()

def analyze_single(url):
    with semaphore:
        try:
            thread_scraper = GitHubScraper(TOKEN, quick=quick_mode)
            data = thread_scraper.get_repo_info(url)
            if not data:
                print(f"  ✗ No data returned for {url}")
                return None

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

            print(f"  → {data.get('startup_name')}: {scores['total']}/100 — {scores['recommendation']}")
            return data

        except Exception as e:
            print(f"  ✗ Error for {url}: {e}")
            return None

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(analyze_single, url): url for url in SAMPLE_REPOS}
    for future in as_completed(futures):
        result = future.result()
        if result:
            with results_lock:
                results.append(result)

# Display
print(f"\n\n========== SCORING RESULTS — {config.VERTICAL_NAME} ==========\n")
if quick_mode:
    print("⚠️  Quick mode active — large repos may score lower than full analysis")
    print("   Set quick_mode = False for accurate investment research\n")
print(f"{'Startup':<25} {'Score':>6} {'Recommendation':<15} {'Flags':>5}")
print("-" * 55)
for r in sorted(results, key=lambda x: x.get('total_score', 0), reverse=True):
    name = r.get('startup_name') or 'Unknown'
    print(f"{name:<25} {r['total_score']:>5}/100  {r['recommendation']:<15} {r['flag_count']:>5} flags")

# Save — separate CSV per vertical
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(results)
if not df.empty:
    score_cols = ["startup_name", "total_score", "recommendation",
                  "technical_execution_score", "technical_moat_score",
                  "community_traction_score", "team_strength_score",
                  "engineering_discipline_score", "flag_count"]

    # Columns irrelevant to non-fintech verticals
    fintech_only_cols = ["fintech_signals", "llm_libs_found",
                         "pred_ai_libs_found", "fine_tune_libs"]

    if vertical_slug != "fintech":
        df = df.drop(columns=[c for c in fintech_only_cols if c in df.columns])

    other_cols = [c for c in df.columns if c not in score_cols]
    df = df[score_cols + other_cols]
    df = df.sort_values("total_score", ascending=False)
    output_file = f"data/{vertical_slug}_raw.csv"
    df.to_csv(output_file, index=False)
    tracker.save(f"data/{vertical_slug}_edge_cases.csv")
    print(f"\nSaved to {output_file}")