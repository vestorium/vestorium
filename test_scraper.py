import os
from src.github_scraper import GitHubScraper
from src.edge_case_tracker import EdgeCaseTracker
from src.scoring_engine import ScoringEngine
import pandas as pd

TOKEN      = os.getenv("GITHUB_TOKEN", "")
quick_mode = True

scraper = GitHubScraper(TOKEN, quick=quick_mode)
tracker = EdgeCaseTracker(vertical="Finance/Fintech")
scorer  = ScoringEngine()
results = []

REPOS = [
    "https://github.com/microsoft/qlib",
    "https://github.com/tensortrade-org/tensortrade",
    "https://github.com/google/tf-quant-finance",
    "https://github.com/feast-dev/feast",
    "https://github.com/AI4Finance-Foundation/FinRL",
    "https://github.com/openbb-finance/OpenBBTerminal",
    "https://github.com/kernc/backtesting.py",
    "https://github.com/ranaroussi/quantstats",
    "https://github.com/domokane/FinancePy",
    "https://github.com/bsolomon1124/pyfinance",
    "https://github.com/explosion/spacy",
    "https://github.com/jealousmarkup/text2phenotype",
]

for url in REPOS:
    print(f"Fetching: {url}")
    data = scraper.get_repo_info(url)
    if not data:
        print(f"  ✗ Failed: {url}")
        continue

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

    results.append(data)
    print(f"  → {data.get('startup_name')}: {scores['total']}/100 — {scores['recommendation']}")

# Display
print("\n\n========== SCORING RESULTS ==========\n")
if quick_mode:
    print("⚠️  Quick mode active — large repos may score lower than full analysis")
    print("   Set quick_mode = False for accurate investment research\n")
print(f"{'Startup':<25} {'Score':>6} {'Recommendation':<15} {'Flags':>5}")
print("-" * 55)
for r in results:
    name = r.get('startup_name') or 'Unknown'
    print(f"{name:<25} {r['total_score']:>5}/100  {r['recommendation']:<15} {r['flag_count']:>5} flags")

# Save
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(results)
score_cols = ["startup_name", "total_score", "recommendation",
              "technical_execution_score", "technical_moat_score",
              "community_traction_score", "team_strength_score",
              "engineering_discipline_score", "flag_count"]
other_cols = [c for c in df.columns if c not in score_cols]
df = df[score_cols + other_cols]
df = df.sort_values("total_score", ascending=False)
df.to_csv("data/fintech_raw.csv", index=False)
tracker.save("data/edge_cases.csv")
print(f"\nSaved to data/fintech_raw.csv")