"""
scoring_engine.py
100-point GitHub scoring framework for Vestorium AI Startup Screener.

Dimensions:
  Technical Execution   30 pts  (commit velocity, releases/year, freshness)
  Technical Moat        30 pts  (custom model, data pipeline, AI approach)
  Community Traction    20 pts  (stars, forks, issue resolution, PR merge rate)
  Team Strength         15 pts  (contributors/year, concentration, key person risk)
  Engineering Discipline 5 pts  (CI/CD, tests, license)

Total: 100 points
Fintech peer benchmarks applied per Master Reference §4.
"""


class ScoringEngine:

    # Fintech peer benchmarks (Master Reference §4)
    BENCHMARKS = {
        "commit_velocity"       : 50,    # commits/month
        "releases_per_year"     : 6,     # releases/year
        "days_since_update"     : 90,    # max days before stale
        "stars_seed"            : 200,   # fintech seed benchmark
        "issue_resolution_rate" : 65,    # % closed
        "pr_merge_rate_min"     : 40,    # % minimum
        "pr_merge_rate_max"     : 70,    # % maximum — above this may indicate low standards
        "contributors_per_year" : 5,     # fintech seed benchmark
    }

    def score(self, data: dict) -> dict:
        """
        Score a single repo across all 5 dimensions.
        Returns total score, dimension breakdown, and recommendation.
        """
        t1 = self._technical_execution(data)
        t2 = self._technical_moat(data)
        t3 = self._community_traction(data)
        t4 = self._team_strength(data)
        t5 = self._engineering_discipline(data)

        total = t1["score"] + t2["score"] + t3["score"] + t4["score"] + t5["score"]

        if total >= 80:
            recommendation = "Strong Buy"
        elif total >= 50:
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

    # ── Dimension 1: Technical Execution (30 pts) ─────────────────────────
    def _technical_execution(self, data: dict) -> dict:
        score = 0

        # Commit velocity: 15 pts (age-adjusted — already commits/month)
        velocity = data.get("commit_velocity", 0)
        if velocity >= 100:   vel_pts = 15
        elif velocity >= 50:  vel_pts = 12
        elif velocity >= 20:  vel_pts = 8
        elif velocity >= 10:  vel_pts = 4
        else:                 vel_pts = 0

        # Releases per year: 10 pts (age-adjusted)
        releases = data.get("releases_per_year", 0)
        if releases >= 12:    rel_pts = 10
        elif releases >= 6:   rel_pts = 7
        elif releases >= 2:   rel_pts = 4
        elif releases >= 1:   rel_pts = 2
        else:                 rel_pts = 0

        # Freshness: 5 pts
        days = data.get("days_since_update", 9999)
        if days <= 7:         fresh_pts = 5
        elif days <= 30:      fresh_pts = 4
        elif days <= 90:      fresh_pts = 2
        else:                 fresh_pts = 0

        score = vel_pts + rel_pts + fresh_pts
        return {
            "score"  : score,
            "max"    : 30,
            "details": {
                "commit_velocity_pts" : vel_pts,
                "releases_per_year_pts": rel_pts,
                "freshness_pts"       : fresh_pts,
            }
        }

    # ── Dimension 2: Technical Moat (30 pts) ──────────────────────────────
    def _technical_moat(self, data: dict) -> dict:
        score = 0

        # Custom model presence: 12 pts
        custom_pts = 12 if data.get("has_custom_model") else 0

        # Data pipeline presence: 8 pts
        data_pts = 8 if data.get("has_data_pipeline") else 0

        # AI approach: 10 pts
        approach = data.get("ai_approach", "")
        if approach == "Fine-tuned Model":          approach_pts = 10
        elif approach == "RAG / Custom LLM":        approach_pts = 7
        elif approach == "Traditional ML / Other":  approach_pts = 5
        elif approach == "API Wrapper":             approach_pts = 0
        else:                                       approach_pts = 3

        # API wrapper penalty
        api_penalty = -5 if data.get("is_api_wrapper") else 0

        score = max(0, custom_pts + data_pts + approach_pts + api_penalty)
        return {
            "score"  : score,
            "max"    : 30,
            "details": {
                "custom_model_pts" : custom_pts,
                "data_pipeline_pts": data_pts,
                "ai_approach_pts"  : approach_pts,
                "api_penalty"      : api_penalty,
            }
        }

    # ── Dimension 3: Community Traction (20 pts) ──────────────────────────
    def _community_traction(self, data: dict) -> dict:
        score = 0
        stars     = data.get("stars", 0)
        forks     = data.get("forks", 0)
        issue_res = data.get("issue_resolution_rate", 0)
        pr_rate   = data.get("pr_merge_rate", 0)
        benchmark = self.BENCHMARKS["stars_seed"]

        # Stars vs fintech benchmark: 7 pts
        if stars >= benchmark * 10:   star_pts = 7
        elif stars >= benchmark * 5:  star_pts = 6
        elif stars >= benchmark * 2:  star_pts = 4
        elif stars >= benchmark:      star_pts = 3
        elif stars >= benchmark * 0.5: star_pts = 1
        else:                         star_pts = 0

        # Fork ratio: 4 pts (ideal 10-30% of stars)
        fork_ratio = (forks / stars * 100) if stars > 0 else 0
        if 10 <= fork_ratio <= 30:    fork_pts = 4
        elif fork_ratio >= 5:         fork_pts = 2
        else:                         fork_pts = 1 if forks > 0 else 0

        # Issue resolution rate: 5 pts
        if issue_res >= 80:           issue_pts = 5
        elif issue_res >= 65:         issue_pts = 4
        elif issue_res >= 50:         issue_pts = 2
        elif issue_res >= 30:         issue_pts = 1
        else:                         issue_pts = 0

        # PR merge rate: 4 pts (penalise both extremes)
        if 40 <= pr_rate <= 70:       pr_pts = 4
        elif 30 <= pr_rate <= 80:     pr_pts = 2
        elif pr_rate > 80:            pr_pts = 1  # too permissive
        else:                         pr_pts = 0

        score = star_pts + fork_pts + issue_pts + pr_pts
        return {
            "score"  : score,
            "max"    : 20,
            "details": {
                "stars_pts"       : star_pts,
                "fork_ratio_pts"  : fork_pts,
                "issue_res_pts"   : issue_pts,
                "pr_merge_pts"    : pr_pts,
            }
        }

    # ── Dimension 4: Team Strength (15 pts) ───────────────────────────────
    def _team_strength(self, data: dict) -> dict:
        score = 0

        # Key person risk — hard penalty
        if data.get("single_contributor_risk"):
            return {
                "score"  : 0,
                "max"    : 15,
                "details": {"note": "Single contributor — hard zero, key person risk"}
            }

        # Contributors per year: 10 pts (age-adjusted)
        contrib_year = data.get("contributors_per_year", 0)
        if contrib_year >= 20:    contrib_pts = 10
        elif contrib_year >= 10:  contrib_pts = 8
        elif contrib_year >= 5:   contrib_pts = 6
        elif contrib_year >= 2:   contrib_pts = 3
        else:                     contrib_pts = 1

        # Finetuning as team capability proxy: 5 pts
        # A team doing fine-tuning signals ML depth beyond basic API usage
        capability_pts = 5 if data.get("has_finetuning") else 2

        score = contrib_pts + capability_pts
        return {
            "score"  : score,
            "max"    : 15,
            "details": {
                "contributors_per_year_pts": contrib_pts,
                "team_capability_pts"      : capability_pts,
            }
        }

    # ── Dimension 5: Engineering Discipline (5 pts) ───────────────────────
    def _engineering_discipline(self, data: dict) -> dict:

        cicd_pts    = 2 if data.get("has_cicd")  else 0
        test_pts    = 2 if data.get("has_tests") else 0
        license_pts = 1 if data.get("license") not in ["None", None, ""] else 0

        score = cicd_pts + test_pts + license_pts
        return {
            "score"  : score,
            "max"    : 5,
            "details": {
                "cicd_pts"   : cicd_pts,
                "test_pts"   : test_pts,
                "license_pts": license_pts,
            }
        }