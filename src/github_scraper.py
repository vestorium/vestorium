import requests
import base64
import os
import json
from datetime import datetime, timezone, timedelta


class GitHubScraper:
    BASE = "https://api.github.com"

    FINTECH_KEYWORDS = [
        "trading", "risk", "fraud", "portfolio", "finance", "fintech",
        "investment", "quant", "algorithmic", "payment", "banking", "credit",
        "insurance", "blockchain", "defi",
        "wealth", "wealthtech", "robo-advisor", "asset-management",
        "portfolio-management",
        "neobank", "digital-banking", "challenger-bank", "core-banking",
        "open-banking",
        "wallet", "remittance", "money-transfer", "settlement", "clearing",
        "capital-markets", "derivatives", "options", "futures", "bond",
        "fixed-income", "equity",
        "lending", "loan", "mortgage", "underwriting", "credit-scoring",
        "bnpl", "buy-now-pay-later",
        "insurtech", "claims", "actuarial",
        "microfinance", "crowdfunding", "p2p-lending", "financial-inclusion",
        "mutual-funds", "hedge-fund", "etf", "fund-management", "nav",
        "regtech", "kyc", "aml", "sanctions",
    ]
    FINTECH_DEPS = [
        "yfinance", "alpaca", "quantlib", "zipline", "backtrader",
        "ccxt", "web3", "pyfolio", "ta-lib", "empyrical", "bt",
        "ffn", "pandas-datareader", "alpha-vantage", "plaid",
        "stripe", "dwolla", "polygon-api-client",
    ]
    LLM_LIBS        = ["transformers", "langchain", "llamaindex", "tokenizers",
                       "vllm", "peft", "trl", "llama", "mistral"]
    CV_LIBS         = ["opencv", "torchvision", "ultralytics", "yolo", "timm"]
    GEN_AI_LIBS     = ["diffusers", "stable-diffusion"]
    PRED_AI_LIBS    = ["scikit-learn", "sklearn", "xgboost", "lightgbm", "catboost"]
    DEEP_LEARNING   = ["torch", "tensorflow", "keras", "jax", "mxnet"]
    RL_LIBS         = ["gymnasium", "gym", "stable-baselines", "ray", "rllib"]
    FINE_TUNE_LIBS  = ["peft", "lora", "qlora", "bitsandbytes"]
    API_ONLY_SIGNAL = ["openai", "anthropic"]

    def __init__(self, token="", quick=False, cache_hours=24):
        self.token      = token
        self.quick      = quick
        self.max_pages  = 3 if quick else 999
        self.cache_hours = cache_hours
        self.cache_dir  = "data/cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        self.session    = self._make_session()

    def _make_session(self):
        session = requests.Session()
        if self.token:
            session.headers.update({"Authorization": f"token {self.token}"})
        session.headers.update({"Accept": "application/vnd.github.v3+json"})
        return session

    def _cache_path(self, repo_url):
        safe_name = repo_url.replace("https://github.com/", "").replace("/", "__")
        mode = "quick" if self.quick else "full"
        return os.path.join(self.cache_dir, f"{safe_name}__{mode}.json")

    def _get_cached(self, repo_url):
        path = self._cache_path(repo_url)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                cached = json.load(f)
            cached_at = datetime.fromisoformat(cached.get("_cached_at", "2000-01-01"))
            age = datetime.now() - cached_at
            if age < timedelta(hours=self.cache_hours):
                print(f"  ✓ Cache hit: {repo_url} ({age.seconds // 3600}h {(age.seconds % 3600) // 60}m old)")
                return cached
            else:
                print(f"  ↻ Cache expired: {repo_url}")
                return None
        except Exception:
            return None

    def _save_cache(self, repo_url, data):
        path = self._cache_path(repo_url)
        try:
            data["_cached_at"] = datetime.now().isoformat()
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"  ⚠️ Cache save failed: {e}")

    def _safe_get(self, session, url, params=None, retries=3):
        import time
        wait = 5
        for attempt in range(retries):
            try:
                r = session.get(url, params=params, timeout=15)
                if r.status_code == 200:
                    return r
                elif r.status_code in (403, 429):
                    print(f"  ⚠️ Rate limit hit, waiting {wait}s... (attempt {attempt+1}/{retries})")
                    time.sleep(wait)
                    wait *= 2
                elif r.status_code == 404:
                    return None
                else:
                    return None
            except Exception as e:
                print(f"  ⚠️ Request error: {e}, retrying in {wait}s...")
                time.sleep(wait)
                wait *= 2
        return None

    def _paginate(self, url, params=None):
        if params is None:
            params = {}
        params["per_page"] = 100
        results = []
        page = 1
        session = self._make_session()
        while page <= self.max_pages:
            page_params = {**params, "page": page}
            r = self._safe_get(session, url, params=page_params)
            if r is None:
                break
            data = r.json()
            if not data:
                break
            results.extend(data)
            if len(data) < 100:
                break
            page += 1
        return results

    def _parse_owner_repo(self, url):
        url = url.rstrip("/").replace("https://github.com/", "")
        parts = url.split("/")
        return parts[0], parts[1]

    def _days_since(self, iso_str):
        if not iso_str:
            return 9999
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days

    def _months_since(self, iso_str):
        if not iso_str:
            return 0
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return round((datetime.now(timezone.utc) - dt).days / 30.44, 1)

    def _format_date(self, iso_str):
        if not iso_str:
            return "Unknown"
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")

    def _get_requirements(self, owner, repo):
        combined = ""
        session = self._make_session()
        for filepath in ["requirements.txt", "setup.py", "pyproject.toml"]:
            url = f"{self.BASE}/repos/{owner}/{repo}/contents/{filepath}"
            r = self._safe_get(session, url)
            if r and r.status_code == 200:
                content = r.json().get("content", "")
                try:
                    decoded = base64.b64decode(content).decode("utf-8", errors="ignore").lower()
                    combined += decoded + "\n"
                except Exception:
                    pass
        return combined

    def _check_file_exists(self, owner, repo, filepath):
        url = f"{self.BASE}/repos/{owner}/{repo}/contents/{filepath}"
        session = self._make_session()
        r = self._safe_get(session, url)
        return r is not None

    def _search_file_in_repo(self, owner, repo, filename):
        url = f"{self.BASE}/search/code"
        params = {"q": f"filename:{filename} repo:{owner}/{repo}", "per_page": 1}
        session = self._make_session()
        r = self._safe_get(session, url, params=params)
        if r:
            return r.json().get("total_count", 0) > 0
        return False

    def _detect_libs(self, requirements_text, lib_list):
        return [lib for lib in lib_list if lib.lower() in requirements_text]

    def get_repo_info(self, repo_url):
        owner, repo = self._parse_owner_repo(repo_url)

        # Check cache first
        cached = self._get_cached(repo_url)
        if cached:
            cached.pop("_cached_at", None)
            return cached

        print(f"Fetching data for: {owner}/{repo}")

        # Basic repo data
        session = self._make_session()
        r = self._safe_get(session, f"{self.BASE}/repos/{owner}/{repo}")
        if not r:
            return {}
        repo_data = r.json()
        stars  = repo_data.get("stargazers_count", 0)
        topics = repo_data.get("topics", [])

        # Age fields
        repo_age_months   = self._months_since(repo_data.get("created_at"))
        repo_created_date = self._format_date(repo_data.get("created_at"))
        days_since_update = self._days_since(repo_data.get("pushed_at"))
        since_30d         = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        years             = repo_age_months / 12 if repo_age_months > 0 else 1

        # Threaded parallel fetch of all paginated endpoints
        def fetch_contributors():
            return self._paginate(f"{self.BASE}/repos/{owner}/{repo}/contributors")

        def fetch_commits_30d():
            return self._paginate(
                f"{self.BASE}/repos/{owner}/{repo}/commits",
                params={"since": since_30d}
            )

        def fetch_releases():
            return self._paginate(f"{self.BASE}/repos/{owner}/{repo}/releases")

        def fetch_prs():
            return self._paginate(
                f"{self.BASE}/repos/{owner}/{repo}/pulls",
                params={"state": "all"}
            )

        def fetch_issues():
            return self._paginate(
                f"{self.BASE}/repos/{owner}/{repo}/issues",
                params={"state": "all"}
            )

        contributors     = fetch_contributors()
        commits_30d_list = fetch_commits_30d()
        releases         = fetch_releases()
        pr_list          = fetch_prs()
        issue_list       = fetch_issues()

        # Process results
        total_contributors      = len(contributors)
        single_contributor_risk = total_contributors == 1
        total_commits           = sum(c.get("contributions", 0) for c in contributors)
        commits_30d             = len(commits_30d_list)
        commit_velocity         = round(total_commits / repo_age_months if repo_age_months > 0 else 0, 1)
        release_count           = len(releases)
        releases_per_year       = round(release_count / years, 1)
        contributors_per_year   = round(total_contributors / years, 1)
        merged_prs              = sum(1 for p in pr_list if p.get("merged_at"))
        pr_merge_rate           = round((merged_prs / len(pr_list) * 100) if pr_list else 0, 1)
        real_issues             = [i for i in issue_list if "pull_request" not in i]
        closed_issues           = sum(1 for i in real_issues if i.get("state") == "closed")
        issue_resolution_rate   = round(
            (closed_issues / len(real_issues) * 100) if real_issues else 0, 1
        )
        total_issues            = len(real_issues)

        # Requirements & AI detection
        requirements    = self._get_requirements(owner, repo)
        llm_found       = self._detect_libs(requirements, self.LLM_LIBS)
        cv_found        = self._detect_libs(requirements, self.CV_LIBS)
        gen_ai_found    = self._detect_libs(requirements, self.GEN_AI_LIBS)
        pred_ai_found   = self._detect_libs(requirements, self.PRED_AI_LIBS)
        dl_found        = self._detect_libs(requirements, self.DEEP_LEARNING)
        rl_found        = self._detect_libs(requirements, self.RL_LIBS)
        fine_tune_found = self._detect_libs(requirements, self.FINE_TUNE_LIBS)
        api_only_found  = self._detect_libs(requirements, self.API_ONLY_SIGNAL)
        fintech_deps    = self._detect_libs(requirements, self.FINTECH_DEPS)

        # AI framework — topics first, deps fallback
        topic_framework_map = {
            "pytorch": "Deep Learning", "tensorflow": "Deep Learning",
            "keras": "Deep Learning", "jax": "Deep Learning",
            "llm": "LLM", "large-language-model": "LLM",
            "gpt": "LLM", "transformers": "LLM", "langchain": "LLM",
            "computer-vision": "Computer Vision",
            "image-classification": "Computer Vision",
            "object-detection": "Computer Vision",
            "generative-ai": "Generative AI",
            "stable-diffusion": "Generative AI", "gan": "Generative AI",
            "reinforcement-learning": "Reinforcement Learning",
            "rl": "Reinforcement Learning",
            "deep-learning": "Deep Learning",
            "machine-learning": "Predictive AI",
            "scikit-learn": "Predictive AI", "xgboost": "Predictive AI",
        }

        topics_lower     = [t.lower() for t in topics]
        ai_framework     = None
        detection_method = None

        for topic in topics_lower:
            if topic in topic_framework_map:
                ai_framework     = topic_framework_map[topic]
                detection_method = "topics"
                break

        if not ai_framework:
            if llm_found:       ai_framework = "LLM"
            elif cv_found:      ai_framework = "Computer Vision"
            elif gen_ai_found:  ai_framework = "Generative AI"
            elif rl_found:      ai_framework = "Reinforcement Learning"
            elif pred_ai_found: ai_framework = "Predictive AI"
            elif dl_found:      ai_framework = "Deep Learning"
            else:               ai_framework = "None detected"
            detection_method = "dependencies" if ai_framework != "None detected" else "none"

        # AI approach
        has_finetuning = bool(fine_tune_found)
        is_api_wrapper = bool(api_only_found) and not (llm_found or has_finetuning)

        if has_finetuning:                     ai_approach = "Fine-tuned Model"
        elif llm_found and not is_api_wrapper: ai_approach = "RAG / Custom LLM"
        elif is_api_wrapper:                   ai_approach = "API Wrapper"
        else:                                  ai_approach = "Traditional ML / Other"

        # File-level signals
        has_custom_model  = (self._search_file_in_repo(owner, repo, "train.py") or
                             self._search_file_in_repo(owner, repo, "model.py") or
                             self._search_file_in_repo(owner, repo, "agent.py") or
                             self._search_file_in_repo(owner, repo, "trainer.py"))
        has_data_pipeline = (self._search_file_in_repo(owner, repo, "data_pipeline.py") or
                             self._search_file_in_repo(owner, repo, "preprocess.py") or
                             self._search_file_in_repo(owner, repo, "etl.py"))
        has_cicd  = self._check_file_exists(owner, repo, ".github/workflows")
        has_tests = (self._check_file_exists(owner, repo, "tests") or
                     self._check_file_exists(owner, repo, "test"))

        # Fintech signals
        description      = (repo_data.get("description") or "").lower()
        keyword_hits     = [kw for kw in self.FINTECH_KEYWORDS if kw in description]
        topic_hits       = [t for t in topics_lower if t in self.FINTECH_DEPS]
        fintech_signals  = ", ".join(set(keyword_hits + topic_hits + fintech_deps)) or "None"

        result = {
            # ── GROUP 1: Scoring Parameters ───────────────────────────
            "startup_name"           : repo_data.get("name"),
            "repo_created_date"      : repo_created_date,
            "repo_age_months"        : repo_age_months,
            "stars"                  : stars,
            "forks"                  : repo_data.get("forks_count", 0),
            "commit_velocity"        : commit_velocity,
            "commits_30d"            : commits_30d,
            "releases_per_year"      : releases_per_year,
            "contributors_per_year"  : contributors_per_year,
            "days_since_update"      : days_since_update,
            "issue_resolution_rate"  : issue_resolution_rate,
            "pr_merge_rate"          : pr_merge_rate,
            "has_custom_model"       : has_custom_model,
            "has_data_pipeline"      : has_data_pipeline,
            "has_finetuning"         : has_finetuning,
            "is_api_wrapper"         : is_api_wrapper,
            "ai_framework"           : ai_framework,
            "ai_approach"            : ai_approach,
            "has_cicd"               : has_cicd,
            "has_tests"              : has_tests,
            "license"                : (repo_data.get("license") or {}).get("spdx_id", "None"),
            "flag_count"             : 0,
            # ── GROUP 2: Diagnostic / Nuance Columns ──────────────────
            "total_commits"          : total_commits,
            "total_contributors"     : total_contributors,
            "release_count"          : release_count,
            "total_issues"           : total_issues,
            "open_issues"            : repo_data.get("open_issues_count", 0),
            "single_contributor_risk": single_contributor_risk,
            "language"               : repo_data.get("language", "Unknown"),
            "description"            : repo_data.get("description", ""),
            "topics"                 : ", ".join(topics),
            "has_website"            : bool(repo_data.get("homepage")),
            "llm_libs_found"         : ", ".join(llm_found) or "None",
            "pred_ai_libs_found"     : ", ".join(pred_ai_found) or "None",
            "fine_tune_libs"         : ", ".join(fine_tune_found) or "None",
            "fintech_signals"        : fintech_signals,
            "ai_detection_method"    : detection_method,
            "flag_codes"             : "",
            "github_url"             : repo_url,
            "analyzed_date"          : datetime.now().strftime("%Y-%m-%d"),
        }
        self._save_cache(repo_url, result)
        return result