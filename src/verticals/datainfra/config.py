"""
Data Infrastructure vertical configuration.
All vertical-specific settings live here — keywords, benchmarks,
flag thresholds, AI framework maps, and repo lists.
Shared code (scraper, scorer, tracker) reads from this config.

Sub-categories covered:
  Data Warehouses & Lakehouses, Stream Processing,
  Batch Orchestration & Pipelines, Query Engines,
  Data Quality & Observability, Data Catalog & Governance,
  Vector Databases, ETL / Reverse ETL

Moat framing (early-stage proxy):
  Is the tool embedded in production pipelines today?
  Leading indicator of system-of-record lock-in at scale.
  Three observable signals: connector ecosystem breadth,
  pipeline integration depth, active contributor growth.

Note on system-of-record moat:
  The long-term destination moat for data infrastructure is
  becoming the system of record — data stored here for years
  cannot be migrated without business risk. However, for
  early-stage startups (6-12 month repos), this moat has not
  yet materialized. Pipeline embedding is the detectable
  early-stage proxy.

Vertical-unique parameter:
  has_connector_ecosystem — checks for connectors/, integrations/,
  sources/, destinations/, or plugins/ directories. Connector breadth
  is a direct proxy for switching cost and TAM. A tool with 300
  connectors means replacing it requires rebuilding every connector.

Data Infrastructure-specific flags (beyond standard 13):
  PLATFORM_ABSORBED     — tool absorbed into cloud platform, standalone thesis dead
  COMMODITIZATION_RISK  — sub-category facing TAM compression from cloud providers
"""

VERTICAL_NAME = "Data Infrastructure"
VERTICAL_SLUG = "datainfra"

# ── Sub-category detection ─────────────────────────────────────────────
SUBCATEGORY_KEYWORDS = {
    "Data Warehouses & Lakehouses": [
        "data-lakehouse", "delta-lake", "apache-iceberg", "data-warehouse",
        "lakehouse", "hudi", "table-format", "open-table-format",
        "columnar-storage", "parquet",
    ],
    "Stream Processing": [
        "stream-processing", "real-time", "apache-kafka", "apache-flink",
        "event-streaming", "message-queue", "pub-sub", "redpanda",
        "event-driven", "streaming-data",
    ],
    "Batch Orchestration & Pipelines": [
        "data-pipeline", "workflow-orchestration", "apache-airflow",
        "dagster", "prefect", "data-engineering", "etl-pipeline",
        "dag", "pipeline-orchestration", "data-workflow",
    ],
    "Query Engines": [
        "query-engine", "analytical-database", "olap", "apache-spark",
        "duckdb", "trino", "presto", "columnar", "analytical-query",
        "in-process-database",
    ],
    "Data Quality & Observability": [
        "data-quality", "data-validation", "data-testing",
        "data-observability", "great-expectations", "data-contracts",
        "schema-validation", "data-monitoring", "data-reliability",
    ],
    "Data Catalog & Governance": [
        "data-catalog", "metadata-management", "data-lineage",
        "data-governance", "data-discovery", "openmetadata",
        "data-mesh", "data-documentation", "metadata",
    ],
    "Vector Databases": [
        "vector-database", "vector-search", "embeddings",
        "similarity-search", "ann", "approximate-nearest-neighbor",
        "semantic-search", "embedding-store", "dense-retrieval",
    ],
    "ETL / Reverse ETL": [
        "etl", "reverse-etl", "data-integration", "data-connector",
        "airbyte", "dbt", "data-sync", "elt", "data-transformation",
        "data-replication",
    ],
}

# ── Flat keyword list for vertical detection ───────────────────────────
KEYWORDS = [kw for kws in SUBCATEGORY_KEYWORDS.values() for kw in kws] + [
    "data-infrastructure", "modern-data-stack", "data-platform",
    "data-stack", "data-engineering", "big-data", "data-ops",
    "dataops", "cloud-data", "data-mesh", "data-lake",
    "data-warehouse", "analytics-engineering", "data-ops",
]

# ── Dependency detection ───────────────────────────────────────────────
DEPENDENCIES = [
    # Data Warehouses & Lakehouses
    "deltalake", "pyiceberg", "pyhudi", "pyarrow", "pandas",
    # Stream Processing
    "kafka-python", "confluent-kafka", "faust", "flink", "pyflink",
    "aiokafka",
    # Batch Orchestration
    "apache-airflow", "dagster", "prefect", "luigi", "argo-workflows",
    "mage-ai",
    # Query Engines
    "pyspark", "duckdb", "trino", "prestodb", "clickhouse-driver",
    "pyarrow", "polars",
    # Data Quality
    "great-expectations", "soda-core", "pandera", "deequ",
    "pydeequ",
    # Data Catalog
    "datahub", "openmetadata", "amundsen", "apache-atlas",
    # Vector Databases
    "qdrant-client", "weaviate-client", "chromadb", "pymilvus",
    "pinecone", "faiss-cpu", "annoy",
    # ETL / Reverse ETL
    "airbyte", "dbt-core", "singer-sdk", "meltano", "fivetran",
]

# ── Scoring benchmarks ─────────────────────────────────────────────────
# Highest star benchmark of all verticals — data engineering communities
# are the largest and most active on GitHub.
# Slightly lower commit velocity than DevTools — data infrastructure
# prioritizes stability. Breaking changes in production pipelines
# are catastrophic.
BENCHMARKS = {
    "stars_seed"            : 1500,  # highest of all verticals — data engineers star tools heavily
    "commit_velocity"       : 80,    # slightly lower than DevTools — stability over speed
    "releases_per_year"     : 12,    # frequent releases expected — ecosystem moves fast
    "days_since_update"     : 90,    # same staleness threshold across all verticals
    "issue_resolution_rate" : 75,    # same as MLOps — production bugs are urgent
    "pr_merge_rate_min"     : 35,    # rigorous review expected
    "pr_merge_rate_max"     : 65,    # lower ceiling — infra PRs need careful scrutiny
    "contributors_per_year" : 9,     # highest of all verticals — data infra attracts most external contributors
}

# ── Flag thresholds ────────────────────────────────────────────────────
FLAG_THRESHOLDS = {
    "LOW_ISSUE_RESOLUTION"          : 75,    # same as MLOps
    "LOW_COMMIT_VELOCITY"           : 80,    # matches benchmark
    "STALE_REPO"                    : 90,    # same across all verticals
    "INFRASTRUCTURE_PLAY"           : 2000,  # high — data infra tools legitimately accumulate stars
    "LOW_PR_MERGE_RATE"             : 35,    # rigorous review
    # Data Infrastructure-specific flag thresholds
    "PLATFORM_ABSORBED_STARS"       : 5000,  # same as MLOps
    "COMMODITIZATION_RISK_STARS"    : 2000,  # below this + no custom model = commoditization flag
}

# ── Scoring dimension weights ──────────────────────────────────────────
# Mirrors DevTools, Cybersecurity, MLOps — not Fintech.
# Team Strength lower: small focused teams are normal in infra tooling.
# Engineering Discipline higher: data engineers judge tooling code harshly.
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

# ── Data Infrastructure-specific vertical parameters ──────────────────
# has_connector_ecosystem: checks for connector/integration directories.
# Connector breadth is a direct proxy for switching cost and TAM.
# A tool with 300+ connectors means replacing it requires rebuilding
# every connector — the highest switching cost in data infrastructure.
# Weighted at 40% of Engineering Discipline — same logic as
# has_security_policy in Cybersecurity and has_sdk in MLOps.
VERTICAL_PARAMS = {
    "has_connector_ecosystem": {
        "weight_in_engineering_discipline": 0.40,
        "detection_dirs": [
            "connectors/", "integrations/", "sources/",
            "destinations/", "plugins/",
        ],
        "detection_keywords": [
            "connector", "integration", "source", "destination", "plugin",
        ],
    },
}

# ── Data Infrastructure-specific flag definitions ─────────────────────
DATAINFRA_FLAGS = {
    "PLATFORM_ABSORBED": {
        "severity"   : "High",
        "description": "Tool shows signs of absorption into a cloud platform. "
                       "Stars above threshold but commit velocity declining and "
                       "near-zero recent commits. Standalone investment thesis may be dead — "
                       "tool may now exist as a feature inside Databricks, Confluent, "
                       "AWS, or Snowflake.",
        "threshold"  : "Stars > 5000 + commit velocity < 30 + commits_30d < 10",
        "action": "Verify whether tool has been acquired or bundled. "
          "Note: Databricks-absorbed repos (Delta Lake, Great Expectations) "
          "remain actively maintained post-acquisition — PLATFORM_ABSORBED "
          "will not fire on these from GitHub signals alone. "
          "Manual ownership verification required for high-star data infra repos.",
    },
    "COMMODITIZATION_RISK": {
        "severity"   : "Medium",
        "description": "Tool operates in a sub-category facing TAM compression from "
                       "cloud providers. Vector Databases and Data Quality tools are "
                       "being absorbed into managed cloud services (AWS, GCP, Azure). "
                       "Standalone tools in these sub-categories face existential risk "
                       "from hyperscaler competition.",
        "threshold"  : "Vector DB or Data Quality sub-category + no custom model + stars < 2000",
        "action"     : "Assess differentiation vs managed cloud alternatives. "
                       "Does the tool have a moat beyond feature parity? "
                       "Check pricing, performance benchmarks, and enterprise adoption.",
    },
}

# ── Info tooltip text (for UI "i" buttons) ────────────────────────────
METRIC_INFO = {
    "commit_velocity": {
        "label"      : "Commit Velocity",
        "explanation": "Number of code commits per month, normalized by repo age.",
        "benchmark"  : "Data Infrastructure benchmark: >80 commits/month",
        "note"       : "Slightly lower than DevTools — data infrastructure tools prioritize "
                       "stability over rapid iteration. A breaking change in a production "
                       "query engine or pipeline is more damaging than a breaking change "
                       "in a developer tool.",
    },
    "issue_resolution_rate": {
        "label"      : "Issue Resolution Rate",
        "explanation": "Percentage of GitHub issues that have been closed.",
        "benchmark"  : "Data Infrastructure benchmark: >75% resolved",
        "note"       : "Data pipeline bugs are urgent — unresolved issues can block "
                       "entire data teams from shipping. Low resolution rate signals "
                       "maintenance backlog in production-critical infrastructure.",
    },
    "has_connector_ecosystem": {
        "label"      : "Connector Ecosystem",
        "explanation": "Checks for connectors/, integrations/, sources/, destinations/, "
                       "or plugins/ directories in the repo.",
        "benchmark"  : "Presence expected for ETL, orchestration, and catalog tools",
        "note"       : "Connector breadth is the primary switching cost mechanism in "
                       "data infrastructure. A tool with 300+ connectors means replacing "
                       "it requires rebuilding every data source connection. "
                       "Proxy signal only — does not verify connector quality or count. "
                       "Not all sub-categories require connectors (e.g., query engines, "
                       "stream processors).",
    },
    "has_custom_model": {
        "label"      : "Custom Model",
        "explanation": "Checks for model training code anywhere in the repo.",
        "benchmark"  : "Presence signals AI-native data tooling with proprietary intelligence.",
        "note"       : "Most data infrastructure tools are not AI products themselves. "
                       "Custom model code here signals AI-augmented data quality, "
                       "anomaly detection, or query optimization. Absence is not "
                       "automatically a red flag for pure infrastructure tools.",
    },
    "stars": {
        "label"      : "Stars",
        "explanation": "GitHub stars in data infrastructure indicate adoption from "
                       "data engineers and platform teams.",
        "benchmark"  : "Data Infrastructure seed benchmark: >1,500 stars — "
                       "highest of all verticals",
        "note"       : "Data engineering communities are the largest and most active "
                       "on GitHub. 1,500 stars is a meaningful adoption signal in this "
                       "space. Watch for Apache Foundation repos — they accumulate "
                       "stars at scale but may have slowing core repo activity as "
                       "development moves to sub-projects.",
    },
    "engineering_discipline": {
        "label"      : "Engineering Discipline",
        "explanation": "CI/CD, tests, connector ecosystem, and license. "
                       "Weighted higher for data infrastructure.",
        "benchmark"  : "All four expected for credible data infrastructure tooling.",
        "note"       : "Data engineers read the source code of tools they depend on. "
                       "Poor engineering discipline in a data infrastructure tool signals "
                       "the team does not run their own tool in production.",
    },
    "platform_absorbed_note": {
        "label"      : "Platform Absorption Risk",
        "explanation": "High-star data tools with declining activity may have been "
                       "absorbed into a cloud platform.",
        "benchmark"  : "Flag fires at: Stars > 5000 + velocity < 30 + commits_30d < 10",
        "note"       : "Known absorption cases: Great Expectations → Databricks (2023), "
                       "Kafka → Confluent Cloud, Spark → Databricks. The GitHub repo "
                       "continues but standalone investment thesis is dead. "
                       "Always verify current ownership for high-star data infra repos.",
    },
    "commoditization_note": {
        "label"      : "Commoditization Risk",
        "explanation": "Some data infrastructure sub-categories face TAM compression "
                       "from hyperscalers offering managed alternatives.",
        "benchmark"  : "Highest risk sub-categories: Vector Databases, Data Quality",
        "note"       : "AWS, GCP, and Azure now offer managed vector search and "
                       "built-in data quality monitoring. Standalone tools in these "
                       "sub-categories must demonstrate clear differentiation — "
                       "performance, cost, or enterprise features — to justify "
                       "independent existence.",
    },
    "moat_note": {
        "label"      : "Data Infrastructure Moat Assessment Note",
        "explanation": "Primary moat signal (early-stage): is the tool embedded "
                       "in production pipelines today? Leading indicator of "
                       "system-of-record lock-in at scale.",
        "benchmark"  : "N/A — GitHub signals approximate but do not directly measure "
                       "pipeline embedding depth.",
        "note"       : "Long-term destination moat: becoming the system of record — "
                       "data stored here for years cannot be migrated without business risk. "
                       "For early-stage startups, this moat has not yet materialized. "
                       "Observable early proxies: connector ecosystem breadth, "
                       "CI/CD integration depth, active contributor growth rate. "
                       "Validate pipeline embedding depth separately from GitHub signals.",
    },
}
# ── LLM Moat Analyzer context ─────────────────────────────────────────
LLM_MOAT_CONTEXT = (
    "For Data Infrastructure AI startups, the key moat question is whether the tool "
    "is embedded in production pipelines as a system of record. Connector ecosystem "
    "breadth is the switching cost signal — 300 connectors means rebuilding all of "
    "them to switch. At early stage, look for connector ecosystem growth rate and "
    "pipeline embedding depth rather than mature system-of-record lock-in."
)