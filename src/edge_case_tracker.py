"""
edge_case_tracker.py
Structured edge case detection for Vestorium startup screening.
Reads thresholds from vertical config — vertical agnostic.
"""

from datetime import datetime


FLAG_DEFINITIONS = {
    "NO_AI_FRAMEWORK": {
        "category" : "AI Detection",
        "severity" : "High",
        "threshold": "Must detect at least one AI framework",
        "comment"  : "No AI framework detected via topics or dependencies — manual review required",
    },
    "LOW_CONFIDENCE_AI_DETECTION": {
        "category" : "AI Detection",
        "severity" : "Medium",
        "threshold": "Topics-based detection preferred",
        "comment"  : "AI framework detected via dependencies only — topics exist but no match found",
    },
    "FINTECH_KEYWORDS_ONLY": {
        "category" : "Vertical Classification",
        "severity" : "Medium",
        "threshold": "Fintech classification requires keyword + dependency confirmation",
        "comment"  : "Repo classified as fintech via keywords only — no fintech dependencies found",
    },
    "NO_CUSTOM_MODEL": {
        "category" : "Technical Moat",
        "severity" : "High",
        "threshold": "train.py or model.py expected at root level",
        "comment"  : "No custom model code detected — may be in subfolders or absent. Manual verification recommended if flag seems implausible.",
    },
    "INFRASTRUCTURE_PLAY": {
        "category" : "Technical Moat",
        "severity" : "Medium",
        "threshold": "Stars > 1000 with custom model and data pipeline expected",
        "comment"  : "High star count but no custom model or data pipeline — likely infrastructure or tooling, not AI product",
    },
    "KEY_PERSON_RISK": {
        "category" : "Team Signal",
        "severity" : "High",
        "threshold": "Minimum 2 contributors required",
        "comment"  : "Single contributor detected — extreme key person risk",
    },
    "LOW_ISSUE_RESOLUTION": {
        "category" : "Community Signal",
        "severity" : "High",
        "threshold": "Vertical-specific benchmark applies",
        "comment"  : "Issue resolution rate below vertical benchmark — indicates poor maintenance or overwhelmed team",
    },
    "LOW_COMMIT_VELOCITY": {
        "category" : "Activity Signal",
        "severity" : "High",
        "threshold": "Vertical-specific benchmark applies",
        "comment"  : "Commit velocity below vertical benchmark — low execution speed",
    },
    "STALE_REPO": {
        "category" : "Activity Signal",
        "severity" : "High",
        "threshold": "Updated within 90 days",
        "comment"  : "Repo not updated in 90+ days — possible abandonment",
    },
    "NO_LICENSE": {
        "category" : "Repository Basics",
        "severity" : "Medium",
        "threshold": "MIT or Apache 2.0 preferred",
        "comment"  : "No license found — legal risk for enterprise adoption",
    },
    "API_WRAPPER": {
        "category" : "Technical Moat",
        "severity" : "High",
        "threshold": "Custom model or fine-tuning expected",
        "comment"  : "Repo appears to be an API wrapper — no custom model code, weak moat",
    },
    "NO_CICD": {
        "category" : "Engineering Discipline",
        "severity" : "Low",
        "threshold": "CI/CD expected at Series A+",
        "comment"  : "No CI/CD pipeline detected — engineering discipline concern at later stages",
    },
    "LOW_PR_MERGE_RATE": {
        "category" : "Community Signal",
        "severity" : "Medium",
        "threshold": "40-70% merge rate",
        "comment"  : "PR merge rate outside healthy range — below 40% = low engagement, above 70% = possible low review standards",
    },
}


class EdgeCaseTracker:

    def __init__(self, config=None):
        """
        Pass a vertical config module or dict.
        Falls back to fintech defaults if no config provided.
        """
        if config is None:
            from src.verticals.fintech import config as default_config
            config = default_config

        self.vertical   = config.VERTICAL_NAME
        self.thresholds = config.FLAG_THRESHOLDS
        self.edge_cases = []

    def analyze(self, data: dict):
        flags_triggered = []
        name = data.get("startup_name", "Unknown")
        url  = data.get("github_url", "")
        date = datetime.now().strftime("%Y-%m-%d")

        checks = [
            (
                "NO_AI_FRAMEWORK",
                data.get("ai_framework") == "None detected",
                data.get("ai_framework"),
            ),
            (
                "LOW_CONFIDENCE_AI_DETECTION",
                data.get("ai_detection_method") == "dependencies" and bool(data.get("topics")),
                data.get("ai_detection_method"),
            ),
            (
                "FINTECH_KEYWORDS_ONLY",
                data.get("fintech_signals") == "None" and bool(data.get("fintech_keyword_hits")),
                data.get("fintech_signals"),
            ),
            (
                "NO_CUSTOM_MODEL",
                not data.get("has_custom_model"),
                str(data.get("has_custom_model")),
            ),
            (
                "INFRASTRUCTURE_PLAY",
                data.get("stars", 0) > self.thresholds["INFRASTRUCTURE_PLAY"]
                and not data.get("has_custom_model")
                and not data.get("has_data_pipeline"),
                f"Stars: {data.get('stars')}",
            ),
            (
                "KEY_PERSON_RISK",
                data.get("single_contributor_risk"),
                f"Contributors: {data.get('total_contributors')}",
            ),
            (
                "LOW_ISSUE_RESOLUTION",
                data.get("issue_resolution_rate", 0) < self.thresholds["LOW_ISSUE_RESOLUTION"],
                f"{data.get('issue_resolution_rate')}%",
            ),
            (
                "LOW_COMMIT_VELOCITY",
                data.get("commit_velocity", 0) < self.thresholds["LOW_COMMIT_VELOCITY"],
                f"{data.get('commit_velocity')} commits/month",
            ),
            (
                "STALE_REPO",
                data.get("days_since_update", 0) > self.thresholds["STALE_REPO"],
                f"{data.get('days_since_update')} days",
            ),
            (
                "NO_LICENSE",
                data.get("license") in ["None", None, ""],
                data.get("license"),
            ),
            (
                "API_WRAPPER",
                data.get("is_api_wrapper"),
                data.get("ai_approach"),
            ),
            (
                "NO_CICD",
                not data.get("has_cicd"),
                str(data.get("has_cicd")),
            ),
            (
                "LOW_PR_MERGE_RATE",
                data.get("pr_merge_rate", 0) < self.thresholds["LOW_PR_MERGE_RATE"],
                f"{data.get('pr_merge_rate')}%",
            ),
        ]

        for flag_code, condition, detected_value in checks:
            if condition:
                definition = FLAG_DEFINITIONS[flag_code]
                self.edge_cases.append({
                    "startup_name"  : name,
                    "github_url"    : url,
                    "vertical"      : self.vertical,
                    "flag_code"     : flag_code,
                    "flag_category" : definition["category"],
                    "flag_severity" : definition["severity"],
                    "detected_value": detected_value,
                    "threshold"     : definition["threshold"],
                    "comment"       : definition["comment"],
                    "date_flagged"  : date,
                })
                flags_triggered.append(flag_code)

        return flags_triggered

    def get_summary(self, flags_triggered: list):
        return {
            "flag_count": len(flags_triggered),
            "flag_codes": ", ".join(flags_triggered) if flags_triggered else "None",
        }

    def save(self, filepath="data/edge_cases.csv"):
        import pandas as pd
        import os
        os.makedirs("data", exist_ok=True)
        if self.edge_cases:
            df = pd.DataFrame(self.edge_cases)
            df.to_csv(filepath, index=False)
            return len(self.edge_cases)
        return 0