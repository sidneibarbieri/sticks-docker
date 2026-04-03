from pathlib import Path

# Minimal frozen configuration required by the Paper 1 public artifact.
STIX_URL = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"
DATA_DIR = Path("data")
ATOMIC_RED_DIR = DATA_DIR / "atomic-red"
STIX_DIR = DATA_DIR / "stix"
APT_DIR = DATA_DIR / "stix_adversaries"
CALDERA_ABILITIES_DIR = DATA_DIR / "caldera_abilities"
CALDERA_ADVERSARIES_DIR = DATA_DIR / "caldera_adversaries"
CALDERA_API_FILES = DATA_DIR / "api"
CALDERA_DAG_FILES = DATA_DIR / "dag"
STIX_FILE = STIX_DIR / "stix_full.json"
CALDERA_URL = "http://localhost:8888"
CALDERA_API_KEY_RED = "ADMIN123"
AGENT_PATH = DATA_DIR / "agents"
