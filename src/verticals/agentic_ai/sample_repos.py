"""
Agentic AI vertical — sample repos for analysis.
12 repos across 8 sub-categories — slightly above standard 10
given the breadth of sub-categories in this vertical.
Add or remove URLs here to change which repos get analyzed.

Note on langchain: highest starred agent framework. Expect high
score. Benchmark setter for the vertical.

Note on browser-use: extremely young repo (months old). Age-adjusted
metrics will compensate — watch for LOW_COMMIT_VELOCITY misfiring
on a repo that is genuinely new, not declining.

Note on n8n: sits at the boundary between workflow automation and
agentic AI. Will test whether vertical detection correctly identifies
it as an agent framework vs traditional RPA tool.

Note on dify: LLM application platform with agent capabilities.
80k+ stars — one of fastest growing repos in the space.
"""

SAMPLE_REPOS = [
    # Agent Frameworks & Orchestration
    "https://github.com/langchain-ai/langchain",
    "https://github.com/langchain-ai/langgraph",
    "https://github.com/n8n-io/n8n",
    "https://github.com/langgenius/dify",

    # Multi-Agent Systems
    "https://github.com/microsoft/autogen",
    "https://github.com/crewAIinc/crewAI",
    "https://github.com/geekan/MetaGPT",

    # Autonomous Coding Agents
    "https://github.com/princeton-nlp/SWE-agent",
    "https://github.com/All-Hands-AI/OpenHands",

    # Browser & Web Agents
    "https://github.com/browser-use/browser-use",

    # Agent Memory & State Management
    "https://github.com/mem0ai/mem0",

    # Data & Research Agents
    "https://github.com/assafelovic/gpt-researcher",
]