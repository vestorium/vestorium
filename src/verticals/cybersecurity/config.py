"""
Cybersecurity vertical configuration.
All vertical-specific settings live here — keywords, benchmarks,
flag thresholds, AI framework maps, and repo lists.
Shared code (scraper, scorer, tracker) reads from this config.

Sub-categories covered:
  Application Security (AppSec), Cloud Security,
  Threat Detection & Response, Supply Chain Security,
  Secret Scanning, Compliance & Governance,
  Container & Runtime Security, Penetration Testing Tools,
  Identity & Access Management (IAM), Network Security
"""

VERTICAL_NAME = "Cybersecurity"
VERTICAL_SLUG = "cybersecurity"

# ── Sub-category detection ─────────────────────────────────────────────
SUBCATEGORY_KEYWORDS = {
    "Application Security": [
        "appsec", "sast", "dast", "vulnerability-scanning",
        "code-security", "secure-coding", "owasp", "application-security",
        "static-analysis", "dynamic-analysis",
    ],
    "Cloud Security": [
        "cloud-security", "aws-security", "gcp-security", "azure-security",
        "cspm", "cloud-compliance", "infrastructure-security",
        "cloud-native-security", "misconfiguration",
    ],
    "Threat Detection & Response": [
        "threat-detection", "incident-response", "siem", "soar",
        "threat-intelligence", "malware-detection", "anomaly-detection",
        "edr", "xdr", "threat-hunting",
    ],
    "Supply Chain Security": [
        "supply-chain-security", "dependency-scanning", "sbom",
        "software-composition-analysis", "sca", "package-security",
        "dependency-vulnerability", "open-source-security",
    ],
    "Secret Scanning": [
        "secret-scanning", "secret-detection", "credential-scanning",
        "api-key-detection", "sensitive-data", "leaked-secrets",
        "git-secrets", "trufflesecurity",
    ],
    "Compliance & Governance": [
        "compliance", "governance", "soc2", "iso27001", "gdpr",
        "pci-dss", "hipaa", "audit", "policy-as-code", "regulatory",
    ],
    "Container & Runtime Security": [
        "container-security", "kubernetes-security", "docker-security",
        "runtime-security", "pod-security", "admission-control",
        "ebpf", "syscall-monitoring",
    ],
    "Penetration Testing": [
        "penetration-testing", "pentest", "red-team", "exploit",
        "vulnerability-assessment", "ethical-hacking", "ctf",
        "security-testing", "offensive-security",
    ],
    "Identity & Access Management": [
        "iam", "identity", "authentication", "authorization",
        "zero-trust", "rbac", "oauth", "sso", "mfa", "access-control",
    ],
    "Network Security": [
        "network-security", "firewall", "ids", "ips", "intrusion-detection",
        "packet-analysis", "network-monitoring", "ddos-protection",
        "vpn", "proxy",
    ],
}

# ── Flat keyword list for vertical detection ───────────────────────────
KEYWORDS = [kw for kws in SUBCATEGORY_KEYWORDS.values() for kw in kws] + [
    "security", "cybersecurity", "devsecops", "cve", "cwe",
    "vulnerability", "exploit", "breach", "attack", "malware",
    "ransomware", "phishing", "encryption", "cryptography",
    "zero-day", "patch", "hardening", "threat", "risk",
]

# ── Dependency detection ───────────────────────────────────────────────
DEPENDENCIES = [
    # Static analysis
    "bandit", "semgrep", "pylint", "flake8", "safety",
    # Vulnerability scanning
    "pip-audit", "cyclonedx", "syft", "grype",
    # Cryptography
    "cryptography", "pycryptodome", "nacl", "bcrypt",
    # Network security
    "scapy", "nmap", "pyshark",
    # Secret scanning
    "detect-secrets", "trufflesecurity",
    # Container security
    "docker", "kubernetes",
    # Compliance
    "boto3",  # AWS compliance tooling
    # Penetration testing
    "impacket", "pwntools",
    # Authentication
    "authlib", "python-jose", "pyjwt",
    # Threat detection
    "yara", "sigma",
]

# ── Scoring benchmarks ─────────────────────────────────────────────────
# Between fintech and developer tools — security communities are
# serious but smaller than general dev communities
BENCHMARKS = {
    "stars_seed"            : 500,   # security tools need credibility signals
    "commit_velocity"       : 75,    # fast — threats evolve, tools must keep up
    "releases_per_year"     : 10,    # frequent releases for vulnerability patches
    "days_since_update"     : 90,    # same staleness threshold
    "issue_resolution_rate" : 80,    # highest of all verticals — security issues are urgent
    "pr_merge_rate_min"     : 35,    # rigorous review expected
    "pr_merge_rate_max"     : 65,    # lower ceiling — security PRs need careful review
    "contributors_per_year" : 6,     # between fintech and devtools
}

# ── Flag thresholds ────────────────────────────────────────────────────
FLAG_THRESHOLDS = {
    "LOW_ISSUE_RESOLUTION" : 60,     # higher than fintech — security issues must be fixed fast
    "LOW_COMMIT_VELOCITY"  : 75,     # must keep up with threat landscape
    "STALE_REPO"           : 90,     # same as other verticals
    "INFRASTRUCTURE_PLAY"  : 1500,   # between fintech and devtools
    "LOW_PR_MERGE_RATE"    : 35,     # rigorous review — lower threshold
}

# ── Scoring dimension weights ──────────────────────────────────────────
# Technical Execution weighted high — threats evolve fast, tools must keep up
# Engineering Discipline higher than fintech — security tools must practice what they preach
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

# ── Info tooltip text (for UI "i" buttons) ────────────────────────────
METRIC_INFO = {
    "commit_velocity": {
        "label"      : "Commit Velocity",
        "explanation": "Number of code commits per month, normalized by repo age.",
        "benchmark"  : "Cybersecurity benchmark: >75 commits/month",
        "note"       : "Higher than fintech — security tools must respond rapidly to new threats and CVEs.",
    },
    "issue_resolution_rate": {
        "label"      : "Issue Resolution Rate",
        "explanation": "Percentage of GitHub issues that have been closed.",
        "benchmark"  : "Cybersecurity benchmark: >80% resolved — highest of all verticals",
        "note"       : "Security vulnerabilities reported as issues must be addressed urgently. Slow resolution is a liability signal.",
    },
    "has_security_policy": {
        "label"      : "Security Policy",
        "explanation": "Checks for a SECURITY.md file — the standard location for responsible disclosure policies.",
        "benchmark"  : "Presence expected for any credible cybersecurity tool",
        "note"       : "A security company without a documented responsible disclosure policy loses credibility with its own target users. Proxy signal only — does not verify policy quality.",
    },
    "has_custom_model": {
        "label"      : "Custom Model",
        "explanation": "Checks for model training code anywhere in the repo.",
        "benchmark"  : "Presence = AI-native security tool with proprietary detection. Absence = rules-based detection.",
        "note"       : "Rules-based security tools can still be valuable but are more easily replicated. AI-native threat detection with proprietary training data has significantly stronger moat.",
    },
    "stars": {
        "label"      : "Stars",
        "explanation": "GitHub stars in cybersecurity indicate trust and adoption from security professionals.",
        "benchmark"  : "Cybersecurity seed benchmark: >500 stars",
        "note"       : "Security communities are smaller but more serious than general dev communities. 500 stars from security professionals carries more signal than 5000 stars from general developers.",
    },
    "engineering_discipline": {
        "label"      : "Engineering Discipline",
        "explanation": "CI/CD, tests, security policy, and license. Weighted higher for cybersecurity.",
        "benchmark"  : "All four expected for credible cybersecurity tools.",
        "note"       : "A cybersecurity company that does not practice secure engineering disciplines loses credibility with its target users. SECURITY.md weighted highest within this dimension.",
    },
    "monetization_note": {
        "label"      : "Cybersecurity Investment Note",
        "explanation": "Cybersecurity is non-discretionary spend — one of the last budget lines to be cut.",
        "benchmark"  : "N/A — GitHub signals do not measure revenue.",
        "note"       : "Deliberately noted: cybersecurity tools embedded in CI/CD pipelines or production infrastructure have high switching costs. Validate pipeline integration depth separately from GitHub signals.",
    },
}