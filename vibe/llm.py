"""
VibeForge LLM — Universal LLM connector powered by LiteLLM.

Supports: Ollama (local), Groq, OpenAI, Anthropic, Google Gemini, and 100+ more.
Model format examples:
    - ollama/llama3.2                (local, free)
    - groq/llama-3.3-70b-versatile   (fast, free tier)
    - gpt-4o                         (OpenAI)
    - claude-sonnet-4-20250514                (Anthropic)
    - gemini/gemini-2.5-pro            (Google)
"""

import os
from typing import Generator
from .config import get_api_key, load_config


def _detect_provider(model: str) -> str:
    """
    Detect the LLM provider from the model string.

    LiteLLM model format:
        - OpenAI:    gpt-4o, gpt-4o-mini, o1-preview (no prefix)
        - Anthropic: claude-sonnet-4-20250514, claude-opus-4-20250514 (no prefix, starts with 'claude')
        - Groq:      groq/llama-3.3-70b-versatile (groq/ prefix)
        - Gemini:    gemini/gemini-2.5-pro (gemini/ prefix)
        - Ollama:    ollama/llama3.2 (ollama/ prefix)
        - Others:    provider/model format
    """
    model_lower = model.lower()

    if model_lower.startswith("ollama/") or model_lower.startswith("ollama_chat/"):
        return "ollama"
    elif model_lower.startswith("groq/"):
        return "groq"
    elif model_lower.startswith("gemini/") or model_lower.startswith("vertex_ai/"):
        return "gemini"
    elif model_lower.startswith("claude") or model_lower.startswith("anthropic/"):
        return "anthropic"
    elif model_lower.startswith("gpt") or model_lower.startswith("o1") or model_lower.startswith("o3") or model_lower.startswith("openai/"):
        return "openai"
    elif model_lower.startswith("deepseek/"):
        return "deepseek"
    elif model_lower.startswith("mistral/"):
        return "mistral"
    else:
        return "openai"  # Default fallback — most compatible


# Map provider to the env var LiteLLM expects
PROVIDER_ENV_VARS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "groq": "GROQ_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "mistral": "MISTRAL_API_KEY",
}


def _setup_env(model: str):
    """
    Set up the correct environment variable for the detected provider.

    IMPORTANT: We only set the env var for the specific provider being used.
    Setting an Anthropic key as OPENAI_API_KEY would cause auth failures.
    """
    api_key = get_api_key()
    config = load_config()

    if not api_key:
        return

    provider = _detect_provider(model)

    # Set the correct env var for this provider
    env_var = PROVIDER_ENV_VARS.get(provider)
    if env_var:
        os.environ[env_var] = api_key

    # Handle custom base_url (for OpenAI-compatible proxies like LMStudio, etc.)
    if config.get("base_url"):
        os.environ["OPENAI_API_BASE"] = config["base_url"]


def call_llm(
    messages: list[dict],
    model: str = None,
    temperature: float = None,
    max_tokens: int = None,
    stream: bool = False,
):
    """
    Call an LLM using LiteLLM's universal interface.

    Args:
        messages: List of message dicts [{"role": "system", "content": "..."}, ...]
        model: Model identifier (e.g., "groq/llama-3.3-70b-versatile")
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        stream: Whether to stream the response

    Returns:
        Full response string (non-streaming) or generator (streaming)
    """
    import litellm

    config = load_config()

    model = model or config.get("model", "groq/llama-3.3-70b-versatile")
    temperature = temperature if temperature is not None else config.get("temperature", 0.7)
    max_tokens = max_tokens or config.get("max_tokens", 16000)

    # Set up env vars for the specific provider
    _setup_env(model)

    # Suppress LiteLLM's verbose logging
    litellm.suppress_debug_info = True
    litellm.set_verbose = False

    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }

    if stream:
        return _stream_response(kwargs)
    else:
        response = litellm.completion(**kwargs)
        return response.choices[0].message.content


def _stream_response(kwargs: dict) -> Generator[str, None, None]:
    """Stream response chunks from LLM."""
    import litellm

    response = litellm.completion(**kwargs)
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def call_llm_simple(prompt: str, system: str = "", model: str = None) -> str:
    """
    Simple wrapper for quick LLM calls.

    Args:
        prompt: User prompt
        system: System prompt
        model: Model identifier

    Returns:
        Response string
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    return call_llm(messages, model=model, stream=False)
