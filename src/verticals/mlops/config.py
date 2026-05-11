"""
MLOps / AI Infrastructure vertical configuration.
All vertical-specific settings live here — keywords, benchmarks,
flag thresholds, AI framework maps, and repo lists.
Shared code (scraper, scorer, tracker) reads from this config.

Sub-categories covered:
  Experiment Tracking & Model Registry,
  Training Orchestration & Pipelines,
  Model Serving & Inference,
  Feature Stores,
  LLMOps & Evaluation,
  Compute Orchestration,
  Training Optimization & Search

Moat framing:
  Does removing this tool require rewriting infrastructure,
  retraining teams, or losing institutional data?

Vertical-unique parameter:
  has_sdk — checks for a published Python SDK or client library.
  An MLOps tool with no programmatic integration surface is a
  UI-only product with low switching cost.

MLOps-specific flags (beyond standard 13):
  PLATFORM_ABSORBED     — tool absorbed into cloud platform, standalone thesis dead
  FRAMEWORK_LOCK        — tied to single ML framework, TAM risk
  CLOUD_VENDOR_DEPENDENT — single cloud SDK dependency, TAM capped
  NO_INTEGRATION_SURFACE — no SDK, no REST API, no CLI detected
"""

VERTICAL_NAME = "MLOps / AI Infrastructure"
VERTICAL_SLUG = "mlops"

# ── Sub-category detection ─────────────────────────────────────────────
SUBCATEGORY_KEYWORDS = {
    "Experiment Tracking & Model Registry": [
        "experiment-tracking", "model-registry", "mlflow", "wandb",
        "weights-and-biases", "neptune", "comet-ml", "experiment-management",
        "model-versioning", "run-tracking",
    ],
    "Training Orchestration & Pipelines": [
        "ml-pipeline", "training-pipeline", "kubeflow", "metaflow",
        "zenml", "ml-workflow", "pipeline-orchestration", "workflow-automation",
        "dag", "ml-ops-pipeline",
    ],
    "Model Serving & Inference": [
        "model-serving", "inference-server", "model-deployment",
        "bentoml", "torchserve", "triton", "ray-serve", "seldon",
        "model-api", "inference-optimization",
    ],
    "Feature Stores": [
        "feature-store", "feast", "feature-engineering",
        "feature-platform", "feature-management", "online-store",
        "offline-store", "feature-registry",
    ],
    "LLMOps & Evaluation": [
        "llmops", "llm-evaluation", "prompt-management", "langsmith",
        "promptflow", "llm-observability", "prompt-versioning",
        "llm-testing", "rag-evaluation", "llm-monitoring",
    ],
    "Compute Orchestration": [
        "gpu-orchestration", "cloud-compute", "compute-management",
        "modal", "skyplane", "runai", "gpu-scheduling",
        "multi-cloud", "distributed-training", "compute-abstraction",
    ],
    "Training Optimization & Search": [
        "hyperparameter-tuning", "optuna", "ray-tune", "automl",
        "neural-architecture-search", "hyperparameter-optimization",
        "model-selection", "bayesian-optimization", "nas",
    ],
}

# ── Flat keyword list for vertical detection ───────────────────────────
KEYWORDS = [kw for kws in SUBCATEGORY_KEYWORDS.values() for kw in kws] + [
    "mlops", "machine-learning-operations", "ml-infrastructure",
    "ml-platform", "model-lifecycle", "ml-workflow", "ai-infrastructure",
    "model-monitoring", "data-versioning", "ml-tooling",
    "machine-learning", "deep-learning", "neural-network",
    "model-training", "model-evaluation", "ai-platform",
]

# ── Dependency detection ───────────────────────────────────────────────
DEPENDENCIES = [
    # Experiment tracking
    "mlflow", "wandb", "neptune-client", "comet-ml", "aim",
    # Training orchestration
    "kubeflow", "metaflow", "zenml", "prefect", "apache-airflow",
    "luigi", "kedro",
    # Model serving
    "bentoml", "tritonclient", "torchserve", "ray", "seldon-core",
    "fastapi", "grpc",
    # Feature stores
    "feast", "tecton", "hopsworks",
    # LLMOps
    "langsmith", "promptflow", "helicone", "langfuse", "trulens",
    "ragas", "deepeval",
    # Compute orchestration
    "modal", "sky", "runai",
    # Training optimization
    "optuna", "hyperopt", "ray", "nni", "ax-platform",
    # Core ML frameworks (dependency signal)
    "torch", "tensorflow", "jax", "transformers",
    "peft", "accelerate", "deepspeed",
]

# ── Scoring benchmarks ─────────────────────────────────────────────────
# Sits between DevTools and Cybersecurity — MLOps practitioner community
# is technical and vocal but smaller than general developer community.
# Stars benchmark slightly below DevTools (1000) — MLOps is a specialist field.
BENCHMARKS = {
    "stars_seed"            : 800,   # technical community — stars carry strong signal
    "commit_velocity"       : 90,    # fast — production infra users demand rapid iteration
    "releases_per_year"     : 12,    # frequent releases — breaking changes in ML frameworks require fast response
    "days_since_update"     : 90,    # same staleness threshold across all verticals
    "issue_resolution_rate" : 75,    # high bar — MLOps tools break production pipelines when buggy
    "pr_merge_rate_min"     : 35,    # rigorous review expected
    "pr_merge_rate_max"     : 65,    # lower ceiling — infra PRs need careful scrutiny
    "contributors_per_year" : 7,     # between DevTools (8) and Cybersecurity (6)
}

# ── Flag thresholds ────────────────────────────────────────────────────
FLAG_THRESHOLDS = {
    "LOW_ISSUE_RESOLUTION"    : 75,    # adjusted — MLOps tools break pipelines, issues must be resolved fast
    "LOW_COMMIT_VELOCITY"     : 90,    # adjusted — must keep pace with ML framework ecosystem changes
    "STALE_REPO"              : 90,    # same as other verticals
    "INFRASTRUCTURE_PLAY"     : 2000,  # high threshold — MLOps tools legitimately accumulate stars without being AI products
    "LOW_PR_MERGE_RATE"       : 35,    # rigorous review — same as cybersecurity
    # MLOps-specific flag thresholds
    "PLATFORM_ABSORBED_STARS" : 2000,  # stars above which absorption risk is assessed
    "FRAMEWORK_LOCK_DEPS"     : 1,     # single framework dependency = lock risk
    "NO_INTEGRATION_SURFACE"  : True,  # fires when has_sdk=False AND no REST API AND no CLI detected
}

# ── Scoring dimension weights ──────────────────────────────────────────
# Mirrors DevTools and Cybersecurity — not Fintech.
# Team Strength lower: small focused teams are normal in MLOps tooling.
# Engineering Discipline higher: ML practitioners judge tooling code harshly.
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

# ── MLOps-specific vertical parameters ────────────────────────────────
# has_sdk: checks for a published Python SDK or client library.
# Detection: looks for sdk/, client/, __init__.py with import patterns,
# or setup.py/pyproject.toml with installable package configuration.
# Weighted at 40% of Engineering Discipline dimension — same logic as
# has_security_policy in Cybersecurity.
VERTICAL_PARAMS = {
    "has_sdk": {
        "weight_in_engineering_discipline": 0.40,
        "detection_files": [
            "sdk/", "client/", "clients/",
            "setup.py", "pyproject.toml", "setup.cfg",
        ],
        "detection_keywords": [
            "install_requires", "packages=find_packages",
            "from setuptools", "pip install",
        ],
    },
}

# ── MLOps-specific flag definitions ───────────────────────────────────
MLOPS_FLAGS = {
    "PLATFORM_ABSORBED": {
        "severity"   : "High",
        "description": "Tool shows signs of absorption into a cloud platform. "
                       "Stars above threshold but commit velocity declining and "
                       "no recent releases. Standalone investment thesis may be dead — "
                       "tool may now exist as a feature inside AWS/GCP/Azure/Databricks.",
        "threshold"  : "Stars > 2000 + declining velocity + no releases in 90 days",
        "action"     : "Verify whether tool has been acquired or bundled. "
                       "Check Databricks, AWS SageMaker, Vertex AI release notes.",
    },
    "FRAMEWORK_LOCK": {
        "severity"   : "High",
        "description": "Dependencies tied to a single ML framework (e.g., TensorFlow-only "
                       "or PyTorch-only). TAM is capped at that framework's user base. "
                       "Framework-agnostic tools survive ML framework shifts — "
                       "framework-specific tools do not.",
        "threshold"  : "Only one of: torch, tensorflow, jax detected — no cross-framework support",
        "action"     : "Assess framework market share trajectory. "
                       "PyTorch dominance is strong but not permanent.",
    },
    "CLOUD_VENDOR_DEPENDENT": {
        "severity"   : "Medium",
        "description": "Heavy dependency on a single cloud provider SDK. "
                       "TAM is capped at that cloud's customer base. "
                       "Multi-cloud abstraction is the core value proposition "
                       "of infrastructure tooling — single cloud dependency undermines it.",
        "threshold"  : "Only one of: boto3, google-cloud-*, azure-* detected",
        "action"     : "Verify whether multi-cloud support is on roadmap. "
                       "Single-cloud tools can still be investable if TAM is large enough.",
    },
    "NO_INTEGRATION_SURFACE": {
        "severity"   : "High",
        "description": "No SDK, REST API, or CLI tooling detected. "
                       "An MLOps tool with no programmatic integration surface "
                       "is a UI-only product with low switching cost. "
                       "Users leave when a better UI appears — no lock-in mechanism.",
        "threshold"  : "has_sdk=False AND no REST API pattern AND no CLI entry point",
        "action"     : "Verify manually — SDK may exist but not be detectable from repo structure. "
                       "Check PyPI for installable package.",
    },
}

# ── Info tooltip text (for UI "i" buttons) ────────────────────────────
METRIC_INFO = {
    "commit_velocity": {
        "label"      : "Commit Velocity",
        "explanation": "Number of code commits per month, normalized by repo age.",
        "benchmark"  : "MLOps benchmark: >90 commits/month",
        "note"       : "Higher than fintech — MLOps tools must respond rapidly to "
                       "breaking changes in ML frameworks (PyTorch, CUDA, Kubernetes versions). "
                       "Slow velocity = tool falls behind the ecosystem.",
    },
    "issue_resolution_rate": {
        "label"      : "Issue Resolution Rate",
        "explanation": "Percentage of GitHub issues that have been closed.",
        "benchmark"  : "MLOps benchmark: >75% resolved",
        "note"       : "MLOps tools sit in production pipelines. An unresolved bug "
                       "can block an entire team's training runs. "
                       "Low resolution rate signals maintenance backlog in critical infrastructure.",
    },
    "has_sdk": {
        "label"      : "SDK / Client Library",
        "explanation": "Checks for a published Python SDK or installable client library.",
        "benchmark"  : "Presence expected for any credible MLOps tool",
        "note"       : "The SDK is the lock-in mechanism. 'import mlflow' appearing in "
                       "a user's training script is the switching cost event. "
                       "UI-only MLOps tools have no lock-in — users migrate when a better UI appears. "
                       "Proxy signal only — does not verify SDK quality or adoption.",
    },
    "has_custom_model": {
        "label"      : "Custom Model",
        "explanation": "Checks for model training code anywhere in the repo.",
        "benchmark"  : "Presence signals AI-native tooling with proprietary optimization logic.",
        "note"       : "Most MLOps tools are infrastructure, not AI products themselves. "
                       "Custom model code here signals proprietary optimization — "
                       "e.g., AutoML search algorithms, anomaly detection for model monitoring. "
                       "Absence is not automatically a red flag for infrastructure tools.",
    },
    "stars": {
        "label"      : "Stars",
        "explanation": "GitHub stars in MLOps indicate trust and adoption from ML practitioners.",
        "benchmark"  : "MLOps seed benchmark: >800 stars",
        "note"       : "MLOps practitioner community is smaller than general dev but highly technical. "
                       "800 stars from ML engineers carries more signal than equivalent "
                       "stars from general developers. Watch for sudden spikes — "
                       "HackerNews/Reddit virality inflates stars without reflecting real adoption.",
    },
    "engineering_discipline": {
        "label"      : "Engineering Discipline",
        "explanation": "CI/CD, tests, SDK presence, and license. Weighted higher for MLOps.",
        "benchmark"  : "All four expected for credible MLOps tooling.",
        "note"       : "ML practitioners judge tooling code harshly — they read the source. "
                       "Poor engineering discipline in an MLOps tool signals the team "
                       "does not use its own product in production.",
    },
    "platform_absorbed_note": {
        "label"      : "Platform Absorption Risk",
        "explanation": "High-star MLOps tools with declining activity may have been absorbed "
                       "into a cloud platform (Databricks, AWS SageMaker, Vertex AI).",
        "benchmark"  : "Flag fires at: Stars > 2000 + declining velocity + no recent releases",
        "note"       : "This is an MLOps-specific risk not present in other verticals. "
                       "MLflow (Databricks), Kubeflow (Vertex AI), and others have been absorbed. "
                       "The GitHub repo continues but the standalone investment thesis is dead. "
                       "Always verify current ownership and roadmap for high-star MLOps repos.",
    },
    "moat_note": {
        "label"      : "MLOps Moat Assessment Note",
        "explanation": "Primary moat question: does removing this tool require rewriting "
                       "infrastructure, retraining teams, or losing institutional data?",
        "benchmark"  : "N/A — GitHub signals approximate but do not directly measure switching cost.",
        "note"       : "Three lock-in vectors: (1) Infra lock-in — tool written into Kubernetes "
                       "configs or cloud IAM policies. (2) Workflow lock-in — tool embedded in "
                       "how teams train and experiment. (3) Data lock-in — experiment history, "
                       "model registry, feature definitions stored in proprietary format. "
                       "Validate lock-in depth separately from GitHub signals.",
    },
}
# ── LLM Moat Analyzer context ─────────────────────────────────────────
LLM_MOAT_CONTEXT = (
    "For MLOps AI startups, the key moat question is whether the orchestration or "
    "infrastructure logic is novel or simply Airflow/Kubernetes with an AI label. "
    "Watch for PLATFORM_ABSORBED risk — tools being absorbed into cloud platforms "
    "lose standalone thesis. Retraining teams and institutional data lock-in are "
    "the strongest moat signals at early stage."
)