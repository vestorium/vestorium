"""
MLOps / AI Infrastructure vertical — sample repos for analysis.
One repo per sub-category minimum, two for sub-categories with
enough variation to show score differences.
Add or remove URLs here to change which repos get analyzed.

Note on feast: already analyzed in Fintech vertical.
Cached data will be reused — demonstrates cross-vertical scoring consistency.

Note on ray-project/ray: intentionally spans Compute Orchestration and
Training Optimization. Tests whether detection handles multi-purpose tools correctly.
"""

SAMPLE_REPOS = [
    # Experiment Tracking & Model Registry
    "https://github.com/mlflow/mlflow",
    "https://github.com/wandb/wandb",

    # Training Orchestration & Pipelines
    "https://github.com/kubeflow/kubeflow",
    "https://github.com/zenml-io/zenml",

    # Model Serving & Inference
    "https://github.com/bentoml/BentoML",

    # Feature Stores
    "https://github.com/feast-dev/feast",

    # LLMOps & Evaluation
    "https://github.com/langfuse/langfuse",

    # Compute Orchestration
    "https://github.com/modal-labs/modal-client",

    # Training Optimization & Search
    "https://github.com/optuna/optuna",

    # Compute Orchestration + Training Optimization (multi-purpose edge case)
    "https://github.com/ray-project/ray",
]