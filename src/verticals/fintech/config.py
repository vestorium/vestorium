"""
Fintech vertical configuration.
All vertical-specific settings live here — keywords, benchmarks,
flag thresholds, AI framework maps, and repo lists.
Shared code (scraper, scorer, tracker) reads from this config.
"""

VERTICAL_NAME = "Finance/Fintech"
VERTICAL_SLUG = "fintech"

# ── Keyword & dependency detection ────────────────────────────────────
KEYWORDS = [
    # Core fintech
    "trading", "risk", "fraud", "portfolio", "finance", "fintech",
    "investment", "quant", "algorithmic", "payment", "banking", "credit",
    "insurance", "blockchain", "defi",
    # Wealth & advisory
    "wealth", "wealthtech", "robo-advisor", "asset-management",
    "portfolio-management",
    # Banking & neobank
    "neobank", "digital-banking", "challenger-bank", "core-banking",
    "open-banking",
    # Payments & wallet
    "wallet", "remittance", "money-transfer", "settlement", "clearing",
    # Capital markets
    "capital-markets", "derivatives", "options", "futures", "bond",
    "fixed-income", "equity",
    # Lending & credit
    "lending", "loan", "mortgage", "underwriting", "credit-scoring",
    "bnpl", "buy-now-pay-later",
    # Insurance
    "insurtech", "claims", "actuarial",
    # Micro & emerging
    "microfinance", "crowdfunding", "p2p-lending", "financial-inclusion",
    # Funds
    "mutual-funds", "hedge-fund", "etf", "fund-management", "nav",
    # Compliance
    "regtech", "kyc", "aml", "sanctions",
]

DEPENDENCIES = [
    "yfinance", "alpaca", "quantlib", "zipline", "backtrader",
    "ccxt", "web3", "pyfolio", "ta-lib", "empyrical", "bt",
    "ffn", "pandas-datareader", "alpha-vantage", "plaid",
    "stripe", "dwolla", "polygon-api-client",
]

# ── Scoring benchmarks ─────────────────────────────────────────────────
BENCHMARKS = {
    "stars_seed"            : 200,   # minimum stars for credible fintech seed
    "commit_velocity"       : 50,    # commits/month
    "releases_per_year"     : 6,     # releases/year
    "days_since_update"     : 90,    # max days before stale flag
    "issue_resolution_rate" : 65,    # % closed issues
    "pr_merge_rate_min"     : 40,    # % minimum healthy merge rate
    "pr_merge_rate_max"     : 70,    # % above this = possible low standards
    "contributors_per_year" : 5,     # minimum for healthy team growth
}

# ── Flag thresholds ────────────────────────────────────────────────────
FLAG_THRESHOLDS = {
    "LOW_ISSUE_RESOLUTION" : 40,     # below this % = flag
    "LOW_COMMIT_VELOCITY"  : 50,     # below this commits/month = flag
    "STALE_REPO"           : 90,     # above this days since update = flag
    "INFRASTRUCTURE_PLAY"  : 1000,   # above this stars + no custom model = flag
    "LOW_PR_MERGE_RATE"    : 40,     # below this % = flag
}

# ── Scoring dimension weights ──────────────────────────────────────────
DIMENSION_WEIGHTS = {
    "technical_execution"   : 30,
    "technical_moat"        : 30,
    "community_traction"    : 20,
    "team_strength"         : 15,
    "engineering_discipline": 5,
}

# ── Investment recommendation thresholds ───────────────────────────────
RECOMMENDATION_THRESHOLDS = {
    "strong_buy" : 80,
    "buy"        : 50,
    # below buy = Pass
}

# ── Info tooltip text (for UI "i" buttons) ────────────────────────────
METRIC_INFO = {
    "commit_velocity": {
        "label"      : "Commit Velocity",
        "explanation": "Number of code commits per month, normalized by repo age. Measures execution speed.",
        "benchmark"  : "Fintech benchmark: >50 commits/month",
        "note"       : "Deliberately simplified: uses total commits / age. Does not capture recent acceleration vs historical slowdown.",
    },
    "issue_resolution_rate": {
        "label"      : "Issue Resolution Rate",
        "explanation": "Percentage of GitHub issues that have been closed. Measures maintenance discipline.",
        "benchmark"  : "Fintech benchmark: >65% resolved",
        "note"       : "Sampled from most recent 100 issues. Full history not always fetched due to API rate limits.",
    },
    "pr_merge_rate": {
        "label"      : "PR Merge Rate",
        "explanation": "Percentage of pull requests that were merged. Ideal range is 40-70%.",
        "benchmark"  : "Below 40% = low engagement. Above 70% = possible low review standards.",
        "note"       : "Sampled from most recent 100 PRs. Does not distinguish internal vs external contributors.",
    },
    "stars": {
        "label"      : "Stars",
        "explanation": "GitHub stars indicate market awareness and community interest.",
        "benchmark"  : "Fintech seed benchmark: >200 stars",
        "note"       : "Vanity metric alone — weighted at only 7/100 points. Scored alongside fork ratio and issue resolution for fuller picture.",
    },
    "has_custom_model": {
        "label"      : "Custom Model",
        "explanation": "Checks for model training code (train.py, model.py, agent.py, trainer.py) anywhere in the repo.",
        "benchmark"  : "Presence = strong moat signal. Absence = possible API wrapper.",
        "note"       : "Root-level search only. Some projects store model code in subfolders — manual verification recommended if flag seems implausible.",
    },
    "contributors_per_year": {
        "label"      : "Contributors Per Year",
        "explanation": "Total contributors normalized by repo age. Age-adjusted to avoid penalizing young startups.",
        "benchmark"  : "Fintech benchmark: >5 contributors/year",
        "note"       : "Capped at 300 contributors in quick mode. Large repos may be undercounted.",
    },
    "releases_per_year": {
        "label"      : "Releases Per Year",
        "explanation": "Number of versioned releases normalized by repo age. Measures shipping discipline.",
        "benchmark"  : "Fintech benchmark: >6 releases/year",
        "note"       : "Capped at 300 releases in quick mode. GitHub releases only — some teams use tags instead.",
    },
    "pr_merge_rate": {
        "label"      : "PR Merge Rate",
        "explanation": "Percentage of pull requests merged. Ideal range 40-70%.",
        "benchmark"  : "40-70% is healthy. Above 70% may indicate rubber-stamping.",
        "note"       : "Sampled from most recent 100 PRs only.",
    },
}