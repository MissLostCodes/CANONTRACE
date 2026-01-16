from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load_prompt(filename: str) -> str:
    """
    Load a prompt from a .txt file inside the prompts folder
    """
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


# ---- (global system constraints) ----

SYSTEM_CONSTRAINTS = load_prompt("system_constraints.txt")


def build_prompt(agent_prompt: str) -> str:
    """
    Combine global system constraints with agent-specific prompt
    """
    return f"""{SYSTEM_CONSTRAINTS}

{agent_prompt}
"""
