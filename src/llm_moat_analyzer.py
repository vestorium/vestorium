"""
llm_moat_analyzer.py
LLM-powered moat analysis for Vestorium startup screener.
Reads repo content and returns structured moat assessment via Claude API.
"""

import os
import json
import anthropic
from datetime import datetime, timedelta


CACHE_EXPIRY_HOURS = 24


def _get_cache_path(repo_url: str) -> str:
    slug = repo_url.replace("https://github.com/", "").replace("/", "_")
    return f"data/cache/moat_{slug}.json"


def _load_cache(repo_url: str) -> dict | None:
    path = _get_cache_path(repo_url)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        cached = json.load(f)
    cached_at = datetime.fromisoformat(cached.get("cached_at", "2000-01-01"))
    if datetime.now() - cached_at > timedelta(hours=CACHE_EXPIRY_HOURS):
        return None
    return cached.get("result")


def _save_cache(repo_url: str, result: dict):
    os.makedirs("data/cache", exist_ok=True)
    path = _get_cache_path(repo_url)
    with open(path, "w") as f:
        json.dump({"cached_at": datetime.now().isoformat(), "result": result}, f, indent=2)


def _build_prompt(repo_data: dict, vertical_name: str, moat_context: str) -> str:
    return f"""You are an expert AI investment analyst performing technical due diligence on a startup GitHub repository.

Vertical: {vertical_name}
Moat context for this vertical: {moat_context}

Repository data:
- README: {repo_data.get('readme', 'Not available')[:3000]}
- Key code files: {json.dumps(repo_data.get('code_files', {}), indent=2)[:3000]}
- Recent PR descriptions: {json.dumps(repo_data.get('recent_prs', []), indent=2)[:1000]}

Return ONLY valid JSON with exactly these keys — no preamble, no markdown:
{{
  "build_classification": "one of: Custom model | Fine-tune | API wrapper | Undetermined",
  "moat_type": "one of: Data moat | Model moat | Workflow moat | No identifiable moat",
  "rationale": "2-3 sentences explaining the moat assessment",
  "analyst_prompts": ["question 1", "question 2", "question 3"]
}}

CRITICAL FIELD DEFINITIONS:
- build_classification: HOW the team built the AI — are they training custom models, fine-tuning, or just calling APIs? Must be one of: Custom model, Fine-tune, API wrapper, Undetermined.
- moat_type: WHAT makes the product defensible — data, model, workflow, or nothing? Must be one of: Data moat, Model moat, Workflow moat, No identifiable moat.
- These are TWO DIFFERENT fields. Never put a moat type value in build_classification.

Rules:
- analyst_prompts must be specific to this repo — not generic questions
- Each analyst prompt should implicitly surface a risk
- rationale must be 2-3 sentences maximum
- Return only JSON, nothing else
"""


def run_moat_analysis(repo_url: str, repo_data: dict, vertical_config) -> dict:
    cached = _load_cache(repo_url)
    if cached:
        return {"source": "cache", "result": cached}

    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    vertical_name = getattr(vertical_config, "VERTICAL_NAME", "Unknown")
    moat_context = getattr(vertical_config, "LLM_MOAT_CONTEXT", "Assess whether this repo has a defensible technical moat.")

    prompt = _build_prompt(repo_data, vertical_name, moat_context)

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)

    _save_cache(repo_url, result)
    return {"source": "api", "result": result}