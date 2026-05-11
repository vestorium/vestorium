"""
Data Infrastructure vertical — sample repos for analysis.
One repo per sub-category minimum, two for sub-categories with
enough variation to show score differences.
Add or remove URLs here to change which repos get analyzed.

Note on great-expectations: acquired by Databricks in 2023.
Expect PLATFORM_ABSORBED flag to fire — validates flag detection.

Note on apache/kafka: Apache Foundation repo — expect high stars
but potentially slower core repo activity as development moves
to sub-projects. Same pattern as kubeflow in MLOps vertical.

Note on overlap with MLOps: Batch Orchestration repos (dagster)
are data-focused, not ML-focused. MLOps vertical scored
kubeflow, zenml — explicitly ML pipeline tools. No repo repeats
across verticals.
"""

SAMPLE_REPOS = [
    # Data Warehouses & Lakehouses
    "https://github.com/delta-io/delta",

    # Stream Processing
    "https://github.com/apache/kafka",
    "https://github.com/redpanda-data/redpanda",

    # Batch Orchestration & Pipelines
    "https://github.com/dagster-io/dagster",

    # Query Engines
    "https://github.com/duckdb/duckdb",

    # Data Quality & Observability
    "https://github.com/great-expectations/great_expectations",

    # Data Catalog & Governance
    "https://github.com/datahub-project/datahub",

    # Vector Databases
    "https://github.com/qdrant/qdrant",

    # ETL / Reverse ETL
    "https://github.com/airbytehq/airbyte",
    "https://github.com/dbt-labs/dbt-core",
]