"""
VibeForge LLM — Universal LLM connector powered by LiteLLM.

Supports: Ollama (local), Groq, OpenAI, Anthropic, Google Gemini, and 100+ more.
Model format examples:
    - ollama/llama3.2           (local, free)
    - groq/llama-3.3-70b-versatile  (fast, free tier)
    - gpt-4o                    (OpenAI)
    - claude-sonnet-4-20250514           (Anthropic)
    - gemini/gemini-2.5-pro       (Google)
"""

import os
from typing import Generator
from .config import get_api_key, load_config


def _setup_env():
    """Set up environment variables for LiteLLM from our config."""
    api_key = get_api_key()
    config = load_config()

    if api_key:
        os.environ.setdefault("OPENAI_API_KEY", api_key)
        os.environ.setdefault("GROQ_API_KEY", api_key)
        os.environ.setdefault("ANTHROPIC_API_KEY", api_key)

    if config.get("base_url"):
        os.environ.setdefault("OPENAI_API_BASE", config["base_url"])


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

    _setup_env()
    config = load_config()

    model = model or config.get("model", "groq/llama-3.3-70b-versatile")
    temperature = temperature if temperature is not None else config.get("temperature", 0.7)
    max_tokens = max_tokens or config.get("max_tokens", 16000)

    # Suppress LiteLLM's verbose logging
    litellm.suppress_debug_info = True

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
