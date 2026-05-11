"""
Agentic AI vertical configuration.
All vertical-specific settings live here — keywords, benchmarks,
flag thresholds, AI framework maps, and repo lists.
Shared code (scraper, scorer, tracker) reads from this config.

Sub-categories covered:
  Agent Frameworks & Orchestration,
  Autonomous Coding Agents,
  Browser & Web Agents,
  Data & Research Agents,
  Multi-Agent Systems,
  Agent Memory & State Management,
  Agent Evaluation & Testing,
  Vertical-Specific Agents

Moat framing:
  Primary moat = task success rate compounding.
  An agent that completes 70% of tasks successfully is dramatically
  more valuable than one at 50% — because the 70% agent gets trusted
  with higher-value tasks, generating more data, improving the model
  further, raising success rate further. This compounds with deployment.
  GitHub proxy: evidence of evaluation framework integration and
  feedback loops in the codebase.

Benchmark philosophy:
  Newest category of any vertical — most serious agent frameworks
  are less than 2 years old. Communities are enormous and growing
  faster than any other vertical. Commit velocity is the highest
  of all verticals — agent frameworks iterate extremely fast because
  underlying LLM APIs (OpenAI, Anthropic) change frequently.

Key weight differences from other verticals:
  Technical Execution: 25pts (vs 30pts elsewhere) — raw execution
  speed matters less than moat quality in this vertical.
  Community Traction: 25pts (vs 20pts elsewhere) — community adoption
  is direct signal of framework lock-in, precursor to moat compounding.
  Engineering Discipline: 5pts (vs 10pts elsewhere) — agentic AI moves
  so fast that engineering discipline lags behind innovation. Penalizing
  for missing CI/CD would incorrectly score legitimate frontier labs.
  Technical Moat: 35pts — task success rate compounding is uniquely
  powerful, same logic as Autonomous Systems vertical.

Vertical-unique parameter:
  has_tool_integration — checks for tool definitions, function calling
  schemas, API connector libraries. An agent without tools is just a
  chatbot. Tool ecosystem breadth determines what tasks the agent can
  complete and directly expands addressable market.
  Weighted at 40% of Engineering Discipline.

Agentic AI-specific flags (beyond standard 13):
  BENCHMARK_MISSING  — no evaluation evidence, cannot verify agent works
  LLM_DEPENDENT      — single LLM provider dependency, single point of failure
  NO_MEMORY_LAYER    — stateless agent, cannot complete multi-session tasks
"""

VERTICAL_NAME = "Agentic AI"
VERTICAL_SLUG = "agentic_ai"

# ── Sub-category detection ─────────────────────────────────────────────
SUBCATEGORY_KEYWORDS = {
    "Agent Frameworks & Orchestration": [
        "langchain", "agent-framework", "llm-agent", "ai-agent",
        "agent-orchestration", "agentic", "llm-orchestration",
        "autonomous-agent", "agent-workflow", "agent-loop",
    ],
    "Autonomous Coding Agents": [
        "coding-agent", "autonomous-coding", "swe-agent",
        "ai-programmer", "code-agent", "autonomous-developer",
        "software-engineer-agent", "ai-software-engineer",
        "autonomous-software", "code-generation-agent",
    ],
    "Browser & Web Agents": [
        "browser-agent", "web-agent", "browser-automation",
        "web-automation", "rpa-replacement", "browser-use",
        "web-scraping-agent", "computer-use", "gui-agent",
        "browser-control",
    ],
    "Data & Research Agents": [
        "research-agent", "data-agent", "autonomous-research",
        "deep-research", "information-retrieval-agent",
        "knowledge-agent", "web-research-agent", "report-generation",
        "autonomous-research-assistant",
    ],
    "Multi-Agent Systems": [
        "multi-agent", "agent-collaboration", "agent-swarm",
        "multi-agent-framework", "agent-coordination",
        "agentic-workflow", "agent-team", "collaborative-agents",
        "agent-society", "agent-network",
    ],
    "Agent Memory & State Management": [
        "agent-memory", "long-term-memory", "memory-layer",
        "agent-state", "persistent-memory", "context-management",
        "episodic-memory", "semantic-memory", "memory-management",
        "agent-context",
    ],
    "Agent Evaluation & Testing": [
        "agent-evaluation", "agent-benchmark", "agent-testing",
        "llm-evaluation", "agent-assessment", "benchmark",
        "agent-metrics", "task-completion-rate", "agent-reliability",
        "evaluation-framework",
    ],
    "Vertical-Specific Agents": [
        "legal-agent", "finance-agent", "sales-agent",
        "medical-agent", "domain-agent", "enterprise-agent",
        "industry-agent", "specialized-agent", "domain-specific-agent",
        "vertical-agent",
    ],
}

# ── Flat keyword list for vertical detection ───────────────────────────
KEYWORDS = [kw for kws in SUBCATEGORY_KEYWORDS.values() for kw in kws] + [
    "agentic-ai", "ai-agent", "autonomous-agent", "llm-agent",
    "agent-framework", "multi-agent", "agentic-workflow",
    "tool-use", "function-calling", "agent-loop",
    "reasoning-agent", "ai-assistant-agent", "autonomous-ai",
    "agent", "agentic", "llm-application", "llm-app",
]

# ── Dependency detection ───────────────────────────────────────────────
DEPENDENCIES = [
    # Agent Frameworks
    "langchain", "langgraph", "llamaindex", "llama-index",
    "autogen", "crewai", "smolagents", "agentscope",
    # Coding Agents
    "swe-agent", "aider", "sweepai",
    # Browser Agents
    "playwright", "selenium", "browser-use", "skyvern",
    "pyautogui",
    # Research Agents
    "tavily", "serper", "duckduckgo-search", "exa-py",
    "googlesearch-python",
    # Memory
    "mem0", "zep", "chromadb", "pinecone", "redis",
    "weaviate-client",
    # Evaluation
    "ragas", "deepeval", "inspect-ai", "agentbench",
    # LLM providers (dependency signal)
    "openai", "anthropic", "google-generativeai",
    "mistralai", "groq", "together",
    # Tool libraries
    "langchain-tools", "pydantic", "instructor",
]

# ── Scoring benchmarks ─────────────────────────────────────────────────
# Highest commit velocity of all verticals — agent frameworks iterate
# extremely fast. Underlying LLM APIs change frequently, requiring
# constant updates. AI community stars repos aggressively — high star
# benchmark but below Data Infra since category is newer.
BENCHMARKS = {
    "stars_seed"            : 1200,  # high — AI community stars agent repos aggressively
    "commit_velocity"       : 120,   # highest of all verticals — agent frameworks move fastest
    "releases_per_year"     : 24,    # bi-weekly releases expected — fast iteration cycle
    "days_since_update"     : 90,    # same staleness threshold across all verticals
    "issue_resolution_rate" : 65,    # between fintech and devtools — large issue volumes
    "pr_merge_rate_min"     : 35,    # rigorous review expected
    "pr_merge_rate_max"     : 65,    # same upper ceiling
    "contributors_per_year" : 10,    # highest of all verticals — agent frameworks attract massive contributor bases
}

# ── Flag thresholds ────────────────────────────────────────────────────
FLAG_THRESHOLDS = {
    "LOW_ISSUE_RESOLUTION"          : 65,    # matches benchmark
    "LOW_COMMIT_VELOCITY"           : 120,   # highest threshold of all verticals
    "STALE_REPO"                    : 90,    # same across all verticals
    "INFRASTRUCTURE_PLAY"           : 3000,  # high — agent frameworks legitimately accumulate stars
    "LOW_PR_MERGE_RATE"             : 35,    # rigorous review
    # Agentic AI-specific flag thresholds
    "PLATFORM_ABSORBED_STARS"       : 5000,  # same as other verticals
    "LLM_DEPENDENT_PROVIDERS"       : 1,     # single provider = flag
    "NO_MEMORY_STARS"               : 500,   # above this + no memory = flag
}

# ── Scoring dimension weights ──────────────────────────────────────────
# KEY DIFFERENCES from standard verticals:
# Technical Execution: 25 — raw speed matters less than moat quality
# Community Traction: 25 — highest of any vertical — framework adoption
#                          is direct precursor to lock-in moat
# Engineering Discipline: 5 — back to Fintech level — agentic AI moves
#                             too fast to penalize for missing CI/CD
# Technical Moat: 35 — task success rate compounding is uniquely powerful
DIMENSION_WEIGHTS = {
    "technical_execution"   : 25,
    "technical_moat"        : 35,
    "community_traction"    : 25,
    "team_strength"         : 10,
    "engineering_discipline": 5,
}

# ── Investment recommendation thresholds ───────────────────────────────
RECOMMENDATION_THRESHOLDS = {
    "strong_buy" : 80,
    "buy"        : 50,
}

# ── Agentic AI-specific vertical parameters ───────────────────────────
# has_tool_integration: checks for tool use definitions, function calling
# schemas, and API connector libraries.
# An agent without tools is just a chatbot. Tool ecosystem breadth
# determines what tasks the agent can complete. Each new tool expands
# the addressable market. This is the agent equivalent of connector
# ecosystem breadth in Data Infrastructure.
# Weighted at 40% of Engineering Discipline.
VERTICAL_PARAMS = {
    "has_tool_integration": {
        "weight_in_engineering_discipline": 0.40,
        "detection_dirs": [
            "tools/", "functions/", "actions/", "plugins/",
            "integrations/", "connectors/",
        ],
        "detection_keywords": [
            "tool_call", "function_call", "tool_use",
            "langchain_tools", "openai_tools", "smolagents",
            "@tool", "BaseTool", "StructuredTool",
        ],
        "detection_files": [
            "tools.py", "functions.py", "actions.py",
            "tool_registry.py", "function_calling.py",
        ],
    },
}

# ── Agentic AI-specific flag definitions ──────────────────────────────
AGENTIC_AI_FLAGS = {
    "BENCHMARK_MISSING": {
        "severity"   : "High",
        "description": "No evaluation framework detected, no benchmark results "
                       "in README, no test suite for agent behavior. "
                       "In every other software category, 'it works' is "
                       "demonstrable by running the code. For agents, 'it works' "
                       "requires benchmark evidence — agent failure modes are "
                       "subtle and context-dependent. A 70% success rate agent "
                       "and a 40% success rate agent look identical without benchmarks.",
        "threshold"  : "No evaluation framework in deps + no benchmark in README "
                       "+ no agent test suite detected",
        "action"     : "Ask founder: what is the agent's task completion rate? "
                       "On which benchmark suite? "
                       "What is the human baseline for the same tasks? "
                       "Do not invest in an agent startup without benchmark data.",
    },
    "LLM_DEPENDENT": {
        "severity"   : "High",
        "description": "Agent calls only one LLM provider API with no "
                       "model-agnostic abstraction layer detected. "
                       "Agent is entirely dependent on a single provider. "
                       "If that provider changes pricing, API structure, or "
                       "model capabilities — the product breaks or degrades. "
                       "Strongest agents are model-agnostic and can swap "
                       "underlying LLMs without product changes.",
        "threshold"  : "Only one of: openai, anthropic, google-generativeai "
                       "detected + no abstraction layer",
        "action"     : "Ask founder: what happens if OpenAI raises prices 10x? "
                       "Is there a model-agnostic roadmap? "
                       "Single-provider dependency is acceptable at very early "
                       "stage but must be on the roadmap to resolve.",
    },
    "NO_MEMORY_LAYER": {
        "severity"   : "Medium",
        "description": "No persistent memory, state management, or context "
                       "management detected. Agent can only complete "
                       "single-session tasks. Any task requiring memory across "
                       "sessions — which is most enterprise workflows — will fail. "
                       "A sales agent that forgets previous customer interactions, "
                       "or a research agent that cannot build on prior findings, "
                       "has fundamentally limited enterprise utility.",
        "threshold"  : "No memory deps detected + no state management files "
                       "+ stars > 500",
        "action"     : "Ask founder: how does the agent handle tasks spanning "
                       "multiple sessions? "
                       "What is the context window management strategy? "
                       "Is persistent memory on the roadmap?",
    },
}

# ── Info tooltip text (for UI "i" buttons) ────────────────────────────
METRIC_INFO = {
    "commit_velocity": {
        "label"      : "Commit Velocity",
        "explanation": "Number of code commits per month, normalized by repo age.",
        "benchmark"  : "Agentic AI benchmark: >120 commits/month — "
                       "highest of all verticals",
        "note"       : "Agent frameworks must update constantly as underlying "
                       "LLM APIs change. OpenAI and Anthropic release breaking "
                       "changes frequently — frameworks that don't keep pace "
                       "lose adoption rapidly. Low velocity in this vertical "
                       "is a more serious signal than in any other category.",
    },
    "issue_resolution_rate": {
        "label"      : "Issue Resolution Rate",
        "explanation": "Percentage of GitHub issues that have been closed.",
        "benchmark"  : "Agentic AI benchmark: >65% resolved",
        "note"       : "Agent frameworks attract enormous issue volumes from "
                       "rapid user adoption. Resolution rate reflects team "
                       "capacity relative to community size. "
                       "Fast-growing frameworks may temporarily show lower "
                       "resolution rates as community outpaces team size.",
    },
    "has_tool_integration": {
        "label"      : "Tool Integration",
        "explanation": "Checks for tool definitions, function calling schemas, "
                       "and API connector libraries in the repo.",
        "benchmark"  : "Presence expected for any serious agent framework",
        "note"       : "An agent without tools is just a chatbot. "
                       "Tool ecosystem breadth determines what tasks the agent "
                       "can complete and directly expands the addressable market. "
                       "Each new tool integration is a new use case unlocked. "
                       "This is the agent equivalent of connector ecosystem "
                       "breadth in Data Infrastructure. "
                       "Proxy signal only — does not verify tool quality or count.",
    },
    "has_custom_model": {
        "label"      : "Custom Model",
        "explanation": "Checks for model training code anywhere in the repo.",
        "benchmark"  : "Presence signals agent with proprietary reasoning or "
                       "task-specific fine-tuned models.",
        "note"       : "Most agent frameworks are model-agnostic wrappers — "
                       "absence of custom model is expected and not a red flag. "
                       "Presence is a strong positive signal — it means the "
                       "team is building proprietary intelligence, not just "
                       "orchestrating third-party LLMs. "
                       "Combined with has_tool_integration, this is the "
                       "strongest possible moat signal in this vertical.",
    },
    "stars": {
        "label"      : "Stars",
        "explanation": "GitHub stars in Agentic AI indicate adoption from "
                       "developers building agent applications.",
        "benchmark"  : "Agentic AI seed benchmark: >1,200 stars",
        "note"       : "The AI community stars agent repos faster than any "
                       "other category — LangChain reached 50,000 stars in "
                       "under 12 months. Stars here are a strong adoption "
                       "signal but watch for viral moments — a HackerNews "
                       "front page or Twitter thread can inflate stars without "
                       "reflecting real production adoption. "
                       "Pair star count with issue volume and commit velocity "
                       "for accurate adoption assessment.",
    },
    "community_traction": {
        "label"      : "Community Traction",
        "explanation": "Weighted at 25 points — higher than most verticals (20pts).",
        "benchmark"  : "Stars, forks, issue resolution, PR merge rate",
        "note"       : "Deliberately up-weighted for Agentic AI. "
                       "Community adoption is the direct precursor to framework "
                       "lock-in — the moat that makes task success rate "
                       "compounding possible. Once enterprise teams build "
                       "50 internal agents on LangChain, migrating means "
                       "rewriting all of them. Community traction today is "
                       "the lock-in moat tomorrow.",
    },
    "engineering_discipline": {
        "label"      : "Engineering Discipline",
        "explanation": "CI/CD, tests, tool integration, and license. "
                       "Weighted lower for Agentic AI (5pts vs 10pts elsewhere).",
        "benchmark"  : "Lower bar — fast-moving category",
        "note"       : "Deliberately down-weighted. Agentic AI moves so fast "
                       "that engineering discipline lags behind innovation. "
                       "Penalizing serious frontier labs for missing CI/CD "
                       "would produce analytically incorrect signals. "
                       "Focus on moat and community signals over process signals "
                       "in this vertical.",
    },
    "benchmark_missing_note": {
        "label"      : "Agent Benchmark Risk",
        "explanation": "BENCHMARK_MISSING flag fires when no evaluation "
                       "framework or benchmark results are detected.",
        "benchmark"  : "Any serious agent framework should have benchmark data",
        "note"       : "The most important due diligence question for agent "
                       "startups: what is the task completion rate, on which "
                       "benchmark, compared to what baseline? "
                       "Agent failure modes are subtle — a system that appears "
                       "to work in demos may fail on 60% of real-world tasks. "
                       "No benchmark = no way to verify the core product claim.",
    },
    "moat_note": {
        "label"      : "Agentic AI Moat Assessment Note",
        "explanation": "Primary moat: task success rate compounding. "
                       "GitHub proxy: evaluation framework integration + "
                       "feedback loops in codebase.",
        "benchmark"  : "N/A — GitHub signals approximate but do not directly "
                       "measure task success rate.",
        "note"       : "Three questions every agent investor should ask: "
                       "(1) What is the agent's task completion rate and on "
                       "which benchmark suite? "
                       "(2) Does the success rate improve with more deployment "
                       "data — is there a feedback loop? "
                       "(3) Is the framework model-agnostic or locked to one "
                       "LLM provider? "
                       "None of these are fully answerable from GitHub — "
                       "they require direct founder conversation and product demo.",
    },
}
# ── LLM Moat Analyzer context ─────────────────────────────────────────
LLM_MOAT_CONTEXT = (
    "For Agentic AI startups, the key moat question is whether the agent architecture "
    "is custom or simply LangChain with a thin wrapper. Task success rate compounding "
    "with deployment data is the real moat — agents improve with use. Look for custom "
    "tool integration logic, proprietary benchmark results, and evidence the agent "
    "actually works beyond demos. BENCHMARK_MISSING is the highest risk flag."
)