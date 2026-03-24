"""
VibeForge Config — Manages user preferences and API keys.
"""

import os
import yaml
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path.home() / ".vibeforge"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

DEFAULT_CONFIG = {
    "model": "groq/llama-3.3-70b-versatile",
    "api_key": None,
    "base_url": None,
    "temperature": 0.7,
    "max_tokens": 16000,
    "auto_git": True,
    "auto_polish": True,
}


def ensure_config_dir():
    """Create config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """Load config from ~/.vibeforge/config.yaml, merged with defaults."""
    config = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                user_config = yaml.safe_load(f) or {}
            config.update(user_config)
        except Exception:
            pass
    return config


def save_config(config: dict):
    """Save config to disk."""
    ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def get_value(key: str) -> Optional[str]:
    """Get a single config value."""
    config = load_config()
    return config.get(key)


def set_value(key: str, value: str):
    """Set a single config value."""
    config = load_config()
    # Try to cast to appropriate type
    if value.lower() in ("true", "false"):
        value = value.lower() == "true"
    elif value.isdigit():
        value = int(value)
    else:
        try:
            value = float(value)
        except ValueError:
            pass
    config[key] = value
    save_config(config)


def get_api_key() -> Optional[str]:
    """Get API key from config or environment."""
    # Priority: env var > config file
    env_key = os.environ.get("VIBEFORGE_API_KEY") or os.environ.get("OPENAI_API_KEY") or os.environ.get("GROQ_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if env_key:
        return env_key
    return get_value("api_key")


def get_model() -> str:
    """Get the configured model string."""
    env_model = os.environ.get("VIBEFORGE_MODEL")
    if env_model:
        return env_model
    return get_value("model") or DEFAULT_CONFIG["model"]
