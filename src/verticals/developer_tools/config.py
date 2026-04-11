"""
Developer Tools vertical configuration.
All vertical-specific settings live here — keywords, benchmarks,
flag thresholds, AI framework maps, and repo lists.
Shared code (scraper, scorer, tracker) reads from this config.

Sub-categories covered:
  Testing & QA, Observability & Monitoring, Security Scanning,
  AI Model Development (MLOps), Database Developer Tools,
  Package & Dependency Management, Editor Integration / LSP,
  Runtime & Performance, API Development & Management,
  Code Search & Navigation
"""

VERTICAL_NAME = "Developer Tools"
VERTICAL_SLUG = "developer_tools"

# ── Sub-category detection ─────────────────────────────────────────────
SUBCATEGORY_KEYWORDS = {
    "Testing & QA": [
        "testing", "test-automation", "code-coverage", "fuzzing",
        "unit-test", "integration-test", "qa", "quality-assurance",
        "test-generation", "mutation-testing",
    ],
    "Observability & Monitoring": [
        "observability", "monitoring", "logging", "tracing", "profiling",
        "debugging", "apm", "metrics", "alerting", "distributed-tracing",
    ],
    "Security Scanning": [
        "sast", "vulnerability-scanning", "dependency-scanning",
        "security", "devsecops", "supply-chain-security", "cve",
        "secret-scanning", "code-security",
    ],
    "AI Model Development": [
        "mlops", "experiment-tracking", "model-registry", "model-versioning",
        "dataset-management", "feature-store", "ml-pipeline", "llmops",
        "ai-infrastructure", "model-serving",
    ],
    "Database Developer Tools": [
        "database", "schema-migration", "orm", "query-builder",
        "database-tooling", "migration", "sql", "nosql", "prisma",
    ],
    "Package & Dependency Management": [
        "dependency-management", "package-manager", "supply-chain",
        "dependency-update", "vulnerability-management", "sbom",
    ],
    "Editor Integration": [
        "lsp", "language-server", "vscode-extension", "ide-plugin",
        "editor-extension", "code-intelligence", "autocomplete",
        "syntax-highlighting", "language-server-protocol",
    ],
    "Runtime & Performance": [
        "profiler", "performance", "optimization", "compiler",
        "jit", "runtime", "benchmarking", "memory-profiling",
        "cpu-profiling", "performance-analysis",
    ],
    "API Development & Management": [
        "api", "api-gateway", "rest-api", "graphql", "openapi",
        "swagger", "api-documentation", "api-testing", "rate-limiting",
        "api-management",
    ],
    "Code Search & Navigation": [
        "code-search", "semantic-search", "code-intelligence",
        "code-navigation", "symbol-search", "code-indexing",
        "repository-search",
    ],
}

# ── Flat keyword list for vertical detection ───────────────────────────
KEYWORDS = [kw for kws in SUBCATEGORY_KEYWORDS.values() for kw in kws] + [
    # Additional general devtools keywords
    "developer-tools", "devtools", "developer-experience", "dx",
    "cli", "command-line", "terminal", "sdk", "plugin", "extension",
    "open-source-tooling", "developer-productivity",
]

# ── Dependency detection ───────────────────────────────────────────────
DEPENDENCIES = [
    # Code parsing & analysis
    "tree-sitter", "libcst", "astroid", "pygments",
    # CLI frameworks — stickiness signal
    "click", "typer", "argparse", "rich", "textual",
    # Observability
    "opentelemetry", "prometheus-client", "jaeger", "zipkin",
    # Testing infrastructure
    "pytest", "coverage", "hypothesis", "faker",
    # Database tooling
    "alembic", "sqlalchemy", "prisma", "flyway",
    # LSP & editor integration
    "pygls", "lsp-types",
    # Performance & runtime
    "cython", "numba", "dask", "ray",
    # AI/ML tooling
    "mlflow", "wandb", "dvc", "bentoml", "ray",
    # API tooling
    "fastapi", "grpc", "protobuf", "graphene",
    # Security
    "bandit", "safety", "semgrep",
    # Package management
    "pip-audit", "cyclonedx",
    # Vector/AI infrastructure
    "faiss", "chromadb", "qdrant",
]

# ── Moat signals specific to Developer Tools ───────────────────────────
MOAT_SIGNALS = {
    "has_cli"           : ["click", "typer", "argparse"],
    "has_sdk"           : ["sdk", "client-library", "api-client"],
    "has_plugin_system" : ["plugin", "extension", "middleware", "hooks"],
    "has_lsp"           : ["pygls", "lsp-types", "language-server"],
}

# ── Scoring benchmarks ─────────────────────────────────────────────────
# Higher than fintech — developer communities are larger and more active
BENCHMARKS = {
    "stars_seed"            : 1000,  # devtools need more stars to validate
    "commit_velocity"       : 100,   # devtools teams ship faster
    "releases_per_year"     : 12,    # monthly releases expected
    "days_since_update"     : 90,    # same staleness threshold
    "issue_resolution_rate" : 70,    # developers expect faster responses
    "pr_merge_rate_min"     : 35,    # slightly lower — more rigorous review
    "pr_merge_rate_max"     : 65,    # lower ceiling — higher review standards
    "contributors_per_year" : 8,     # open source devtools attract more contributors
}

# ── Flag thresholds ────────────────────────────────────────────────────
FLAG_THRESHOLDS = {
    "LOW_ISSUE_RESOLUTION" : 50,     # higher than fintech — developers expect responsiveness
    "LOW_COMMIT_VELOCITY"  : 100,    # higher than fintech — devtools ship faster
    "STALE_REPO"           : 90,     # same as fintech
    "INFRASTRUCTURE_PLAY"  : 2000,   # higher threshold — devtools legitimately have high stars
    "LOW_PR_MERGE_RATE"    : 35,     # slightly lower than fintech
}

# ── Scoring dimension weights ──────────────────────────────────────────
# Engineering discipline weighted higher for devtools —
# developers judge other developers' code quality harshly
DIMENSION_WEIGHTS = {
    "technical_execution"   : 30,
    "technical_moat"        : 30,
    "community_traction"    : 20,
    "team_strength"         : 10,
    "engineering_discipline": 10,
}

# ── Investment recommendation thresholds ───────────────────────────────
RECOMMENDATION_THRESHOLDS = {
    "strong_buy" : 80,
    "buy"        : 50,
}

# ── Info tooltip text (for UI "i" buttons) ────────────────────────────
METRIC_INFO = {
    "commit_velocity": {
        "label"      : "Commit Velocity",
        "explanation": "Number of code commits per month, normalized by repo age.",
        "benchmark"  : "Developer Tools benchmark: >100 commits/month",
        "note"       : "Higher than fintech — devtools teams ship faster and users expect rapid iteration.",
    },
    "issue_resolution_rate": {
        "label"      : "Issue Resolution Rate",
        "explanation": "Percentage of GitHub issues that have been closed.",
        "benchmark"  : "Developer Tools benchmark: >70% resolved",
        "note"       : "Higher than fintech — developers file detailed bugs and expect fast responses.",
    },
    "stars": {
        "label"      : "Stars",
        "explanation": "GitHub stars indicate market awareness. Developer communities are more active on GitHub than other verticals.",
        "benchmark"  : "Developer Tools seed benchmark: >1,000 stars",
        "note"       : "Deliberately higher than fintech — developer adoption is more visible on GitHub. Stars alone are still a vanity metric.",
    },
    "has_custom_model": {
        "label"      : "Custom Model",
        "explanation": "Checks for model training code anywhere in the repo.",
        "benchmark"  : "Presence = strong moat. Absence in AI-native devtools = possible API wrapper.",
        "note"       : "Less critical for non-AI devtools (e.g. database migration tools). More critical for AI-native tools (e.g. code generation, testing AI).",
    },
    "contributors_per_year": {
        "label"      : "Contributors Per Year",
        "explanation": "Total contributors normalized by repo age.",
        "benchmark"  : "Developer Tools benchmark: >8 contributors/year",
        "note"       : "Higher than fintech — open source devtools naturally attract more external contributors.",
    },
    "engineering_discipline": {
        "label"      : "Engineering Discipline",
        "explanation": "CI/CD, test coverage, and license. Weighted higher for devtools — developers judge other developers' code quality harshly.",
        "benchmark"  : "CI/CD and tests are non-negotiable for credible devtools startups.",
        "note"       : "A devtools company without CI/CD or tests loses credibility with its own target users.",
    },
    "monetization_note": {
        "label"      : "Monetization Warning",
        "explanation": "Developer Tools vertical specific: high scores indicate strong adoption signals.",
        "benchmark"  : "N/A — GitHub signals do not measure revenue.",
        "note"       : "Deliberately flagged: developer adoption does not equal enterprise revenue. High stars and contributors do not guarantee a monetization path. Always validate the enterprise upsell story separately.",
    },
}