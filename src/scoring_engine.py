"""
scoring_engine.py
100-point GitHub scoring framework for Vestorium AI Startup Screener.
Reads benchmarks and weights from vertical config — vertical agnostic.

Dimensions (weights set per vertical config):
  Technical Execution   — commit velocity, releases/year, freshness
  Technical Moat        — custom model, data pipeline, AI approach
  Community Traction    — stars, forks, issue resolution, PR merge rate
  Team Strength         — contributors/year, key person risk, capability
  Engineering Discipline — CI/CD, tests, license
"""


class ScoringEngine:

    def __init__(self, config=None):
        """
        Pass a vertical config module or dict.
        Falls back to fintech defaults if no config provided.
        """
        if config is None:
            from src.verticals.fintech import config as default_config
            config = default_config

        # Load benchmarks
        self.benchmarks    = config.BENCHMARKS
        self.weights       = config.DIMENSION_WEIGHTS
        self.thresholds    = config.RECOMMENDATION_THRESHOLDS
        self.vertical_slug = getattr(config, 'VERTICAL_SLUG', 'fintech')

    def score(self, data: dict) -> dict:
        t1 = self._technical_execution(data)
        t2 = self._technical_moat(data)
        t3 = self._community_traction(data)
        t4 = self._team_strength(data)
        t5 = self._engineering_discipline(data)

        total = t1["score"] + t2["score"] + t3["score"] + t4["score"] + t5["score"]

        if total >= self.thresholds["strong_buy"]:
            recommendation = "Strong Buy"
        elif total >= self.thresholds["buy"]:
            recommendation = "Buy"
        else:
            recommendation = "Pass"

        return {
            "total"          : total,
            "recommendation" : recommendation,
            "breakdown"      : {
                "Technical Execution"   : t1,
                "Technical Moat"        : t2,
                "Community Traction"    : t3,
                "Team Strength"         : t4,
                "Engineering Discipline": t5,
            }
        }

    def _technical_execution(self, data: dict) -> dict:
        max_pts  = self.weights["technical_execution"]
        bench    = self.benchmarks

        # Commit velocity — 50% of dimension weight
        velocity = data.get("commit_velocity", 0)
        vel_max  = int(max_pts * 0.50)
        if velocity >= bench["commit_velocity"] * 2:   vel_pts = vel_max
        elif velocity >= bench["commit_velocity"]:      vel_pts = int(vel_max * 0.80)
        elif velocity >= bench["commit_velocity"] * 0.4: vel_pts = int(vel_max * 0.50)
        elif velocity >= bench["commit_velocity"] * 0.2: vel_pts = int(vel_max * 0.25)
        else:                                            vel_pts = 0

        # Releases per year — 33% of dimension weight
        releases = data.get("releases_per_year", 0)
        rel_max  = int(max_pts * 0.33)
        if releases >= bench["releases_per_year"] * 2:  rel_pts = rel_max
        elif releases >= bench["releases_per_year"]:     rel_pts = int(rel_max * 0.75)
        elif releases >= bench["releases_per_year"] * 0.33: rel_pts = int(rel_max * 0.40)
        elif releases >= 1:                              rel_pts = int(rel_max * 0.20)
        else:                                            rel_pts = 0

        # Freshness — remaining weight
        days     = data.get("days_since_update", 9999)
        fresh_max = max_pts - vel_max - rel_max
        if days <= 7:    fresh_pts = fresh_max
        elif days <= 30: fresh_pts = int(fresh_max * 0.80)
        elif days <= bench["days_since_update"]: fresh_pts = int(fresh_max * 0.40)
        else:            fresh_pts = 0

        score = vel_pts + rel_pts + fresh_pts
        return {
            "score"  : score,
            "max"    : max_pts,
            "details": {
                "commit_velocity_pts"  : vel_pts,
                "releases_per_year_pts": rel_pts,
                "freshness_pts"        : fresh_pts,
            }
        }

    def _technical_moat(self, data: dict) -> dict:
        max_pts = self.weights["technical_moat"]

        # Custom model: 40% of dimension weight
        custom_pts = int(max_pts * 0.40) if data.get("has_custom_model") else 0

        # Data pipeline: 27% of dimension weight
        data_pts = int(max_pts * 0.27) if data.get("has_data_pipeline") else 0

        # AI approach: remaining weight
        approach     = data.get("ai_approach", "")
        approach_max = max_pts - int(max_pts * 0.40) - int(max_pts * 0.27)
        if approach == "Fine-tuned Model":         approach_pts = approach_max
        elif approach == "RAG / Custom LLM":       approach_pts = int(approach_max * 0.70)
        elif approach == "Traditional ML / Other": approach_pts = int(approach_max * 0.50)
        elif approach == "API Wrapper":            approach_pts = 0
        else:                                      approach_pts = 0

        # API wrapper penalty
        api_penalty = -int(max_pts * 0.17) if data.get("is_api_wrapper") else 0

        score = max(0, custom_pts + data_pts + approach_pts + api_penalty)
        return {
            "score"  : score,
            "max"    : max_pts,
            "details": {
                "custom_model_pts" : custom_pts,
                "data_pipeline_pts": data_pts,
                "ai_approach_pts"  : approach_pts,
                "api_penalty"      : api_penalty,
            }
        }

    def _community_traction(self, data: dict) -> dict:
        max_pts   = self.weights["community_traction"]
        bench     = self.benchmarks
        stars     = data.get("stars", 0)
        forks     = data.get("forks", 0)
        issue_res = data.get("issue_resolution_rate", 0)
        pr_rate   = data.get("pr_merge_rate", 0)

        # Stars: 35% of dimension weight
        star_max = int(max_pts * 0.35)
        if stars >= bench["stars_seed"] * 10:    star_pts = star_max
        elif stars >= bench["stars_seed"] * 5:   star_pts = int(star_max * 0.85)
        elif stars >= bench["stars_seed"] * 2:   star_pts = int(star_max * 0.60)
        elif stars >= bench["stars_seed"]:        star_pts = int(star_max * 0.40)
        elif stars >= bench["stars_seed"] * 0.5: star_pts = int(star_max * 0.20)
        else:                                     star_pts = 0

        # Fork ratio: 20% of dimension weight
        fork_ratio = (forks / stars * 100) if stars > 0 else 0
        fork_max   = int(max_pts * 0.20)
        if 10 <= fork_ratio <= 30:  fork_pts = fork_max
        elif fork_ratio >= 5:       fork_pts = int(fork_max * 0.60)
        else:                       fork_pts = int(fork_max * 0.20) if forks > 0 else 0

        # Issue resolution: 25% of dimension weight
        issue_max = int(max_pts * 0.25)
        if issue_res >= 80:                              issue_pts = issue_max
        elif issue_res >= bench["issue_resolution_rate"]: issue_pts = int(issue_max * 0.80)
        elif issue_res >= 50:                            issue_pts = int(issue_max * 0.50)
        elif issue_res >= 30:                            issue_pts = int(issue_max * 0.25)
        else:                                            issue_pts = 0

        # PR merge rate: remaining weight
        pr_max = max_pts - star_max - fork_max - issue_max
        if bench["pr_merge_rate_min"] <= pr_rate <= bench["pr_merge_rate_max"]: pr_pts = pr_max
        elif 30 <= pr_rate <= 80:   pr_pts = int(pr_max * 0.60)
        elif pr_rate > 80:          pr_pts = int(pr_max * 0.30)
        else:                       pr_pts = 0

        score = star_pts + fork_pts + issue_pts + pr_pts
        return {
            "score"  : score,
            "max"    : max_pts,
            "details": {
                "stars_pts"    : star_pts,
                "fork_pts"     : fork_pts,
                "issue_pts"    : issue_pts,
                "pr_merge_pts" : pr_pts,
            }
        }

    def _team_strength(self, data: dict) -> dict:
        max_pts = self.weights["team_strength"]

        # Key person risk — hard zero
        if data.get("single_contributor_risk"):
            return {
                "score"  : 0,
                "max"    : max_pts,
                "details": {"note": "Single contributor — hard zero, key person risk"}
            }

        # Contributors per year: 67% of dimension weight
        contrib_year = data.get("contributors_per_year", 0)
        bench        = self.benchmarks
        contrib_max  = int(max_pts * 0.67)
        if contrib_year >= bench["contributors_per_year"] * 4:   contrib_pts = contrib_max
        elif contrib_year >= bench["contributors_per_year"] * 2: contrib_pts = int(contrib_max * 0.80)
        elif contrib_year >= bench["contributors_per_year"]:     contrib_pts = int(contrib_max * 0.60)
        elif contrib_year >= bench["contributors_per_year"] * 0.4: contrib_pts = int(contrib_max * 0.30)
        else:                                                     contrib_pts = int(contrib_max * 0.10)

        # Finetuning as capability proxy: remaining weight
        cap_max  = max_pts - contrib_max
        cap_pts  = cap_max if data.get("has_finetuning") else int(cap_max * 0.40)

        score = contrib_pts + cap_pts
        return {
            "score"  : score,
            "max"    : max_pts,
            "details": {
                "contributors_per_year_pts": contrib_pts,
                "team_capability_pts"      : cap_pts,
            }
        }

    def _engineering_discipline(self, data: dict) -> dict:
        max_pts  = self.weights["engineering_discipline"]

        if self.vertical_slug == "cybersecurity":
            # Cybersecurity: cicd 20%, tests 20%, security_policy 40%, license 20%
            cicd_pts = int(max_pts * 0.20) if data.get("has_cicd")  else 0
            test_pts = int(max_pts * 0.20) if data.get("has_tests") else 0
            sec_pts  = int(max_pts * 0.40) if data.get("has_security_policy") else 0
            lic_pts  = int(max_pts * 0.20) if data.get("license") not in ["None", None, ""] else 0
            score = cicd_pts + test_pts + sec_pts + lic_pts
            return {
                "score"  : score,
                "max"    : max_pts,
                "details": {
                    "cicd_pts"            : cicd_pts,
                    "test_pts"            : test_pts,
                    "security_policy_pts" : sec_pts,
                    "license_pts"         : lic_pts,
                }
            }
        else:
            # All other verticals: cicd 40%, tests 40%, license 20%
            cicd_pts = int(max_pts * 0.40) if data.get("has_cicd")  else 0
            test_pts = int(max_pts * 0.40) if data.get("has_tests") else 0
            lic_pts  = int(max_pts * 0.20) if data.get("license") not in ["None", None, ""] else 0
            score = cicd_pts + test_pts + lic_pts
            return {
                "score"  : score,
                "max"    : max_pts,
                "details": {
                    "cicd_pts"   : cicd_pts,
                    "test_pts"   : test_pts,
                    "license_pts": lic_pts,
                }
            }