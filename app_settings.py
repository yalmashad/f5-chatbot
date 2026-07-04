from __future__ import annotations

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_COMPATIBLE_MODEL = "meta-llama/Llama-3.1-8B-Instruct"
DEFAULT_COMPATIBLE_BASE_URL = ""
DEFAULT_OLLAMA_MODEL = "llama3.2"
DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434/v1"
DEFAULT_ENABLE_OLLAMA = "true"
MODEL_PROVIDERS = ("OpenAI", "OpenAI compatible", "Ollama")

DEFAULT_GUARDRAIL_HOSTNAME = "https://www.us1.calypsoai.app"
GUARDRAIL_SCAN_PATH = "/backend/v1/scans"
GUARDRAIL_PROMPT_API_PATH = "/backend/v1/prompts"


def build_guardrail_url(hostname: str, path: str) -> str:
    return f"{hostname.rstrip('/')}{path}"


def _first_env(env: dict, *keys: str, default: str = "") -> str:
    for key in keys:
        value = env.get(key)
        if value:
            return str(value)
    return default


def _normalize_provider(provider: str) -> str:
    return provider if provider in MODEL_PROVIDERS else "OpenAI"


def _is_truthy(value: str | bool | None) -> bool:
    return str(value if value is not None else "").strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
        "on",
    }


def get_available_model_providers(settings: dict[str, str]) -> tuple[str, ...]:
    if _is_truthy(settings.get("enable_ollama", DEFAULT_ENABLE_OLLAMA)):
        return MODEL_PROVIDERS
    return tuple(provider for provider in MODEL_PROVIDERS if provider != "Ollama")


def _normalize_base_url(base_url: str) -> str:
    return base_url.strip().rstrip("/")


def _settings_from_env(env: dict) -> dict[str, str]:
    enable_ollama = _first_env(
        env,
        "ENABLE_OLLAMA",
        "OLLAMA_ENABLED",
        default=DEFAULT_ENABLE_OLLAMA,
    )
    provider = _normalize_provider(_first_env(env, "MODEL_PROVIDER", default="OpenAI"))
    if provider == "Ollama" and not _is_truthy(enable_ollama):
        provider = "OpenAI"
    guardrail_hostname = _first_env(
        env,
        "GUARDRAIL_HOSTNAME",
        "CALYPSO_HOSTNAME",
        default=DEFAULT_GUARDRAIL_HOSTNAME,
    ).strip() or DEFAULT_GUARDRAIL_HOSTNAME

    settings = {
        "model_provider": provider,
        "enable_ollama": enable_ollama,
        "openai_api_key": _first_env(env, "OPENAI_API_KEY"),
        "openai_model": _first_env(env, "OPENAI_MODEL", default=DEFAULT_OPENAI_MODEL),
        "openai_compatible_api_key": _first_env(
            env,
            "OPENAI_COMPATIBLE_API_KEY",
            "OPENAI_COMPATIBLE_KEY",
        ),
        "openai_compatible_base_url": _normalize_base_url(
            _first_env(
                env,
                "OPENAI_COMPATIBLE_BASE_URL",
                "OPENAI_COMPATIBLE_HOSTNAME",
                default=DEFAULT_COMPATIBLE_BASE_URL,
            )
        ),
        "openai_compatible_model": _first_env(
            env,
            "OPENAI_COMPATIBLE_MODEL",
            default=DEFAULT_COMPATIBLE_MODEL,
        ),
        "ollama_model": _first_env(env, "OLLAMA_MODEL", default=DEFAULT_OLLAMA_MODEL),
        "ollama_base_url": _normalize_base_url(
            _first_env(env, "OLLAMA_BASE_URL", default=DEFAULT_OLLAMA_BASE_URL)
        ),
        "guardrail_api_key": _first_env(
            env,
            "GUARDRAIL_API_KEY",
            "F5AI_API_KEY",
            "F5_GUARDRAIL_API_KEY",
        ),
        "guardrail_hostname": guardrail_hostname.rstrip("/"),
    }
    return _with_derived_urls(settings)


def _with_derived_urls(settings: dict[str, str]) -> dict[str, str]:
    updated = dict(settings)
    hostname = (updated.get("guardrail_hostname") or DEFAULT_GUARDRAIL_HOSTNAME).strip()
    updated["guardrail_hostname"] = hostname.rstrip("/") or DEFAULT_GUARDRAIL_HOSTNAME
    updated["guardrail_scan_url"] = build_guardrail_url(
        updated["guardrail_hostname"], GUARDRAIL_SCAN_PATH
    )
    updated["guardrail_prompt_api_url"] = build_guardrail_url(
        updated["guardrail_hostname"], GUARDRAIL_PROMPT_API_PATH
    )
    return updated


def seed_session_settings(session: dict, env: dict) -> dict[str, str]:
    if "app_settings" not in session:
        session["app_settings"] = _settings_from_env(env)
    return session["app_settings"]


def reset_session_settings(session: dict, env: dict) -> dict[str, str]:
    session["app_settings"] = _settings_from_env(env)
    return session["app_settings"]


def update_session_settings(session: dict, updates: dict[str, str]) -> dict[str, str]:
    current = dict(session.get("app_settings", _settings_from_env({})))
    current.update(
        {
            key: value.strip() if isinstance(value, str) else value
            for key, value in updates.items()
        }
    )
    current["model_provider"] = _normalize_provider(current.get("model_provider", "OpenAI"))
    current["enable_ollama"] = current.get("enable_ollama", DEFAULT_ENABLE_OLLAMA)
    if current["model_provider"] == "Ollama" and "Ollama" not in get_available_model_providers(current):
        current["model_provider"] = "OpenAI"
    current["openai_model"] = current.get("openai_model") or DEFAULT_OPENAI_MODEL
    current["openai_compatible_base_url"] = _normalize_base_url(
        current.get("openai_compatible_base_url", "")
    )
    current["openai_compatible_model"] = (
        current.get("openai_compatible_model") or DEFAULT_COMPATIBLE_MODEL
    )
    current["ollama_model"] = current.get("ollama_model") or DEFAULT_OLLAMA_MODEL
    current["ollama_base_url"] = _normalize_base_url(
        current.get("ollama_base_url") or DEFAULT_OLLAMA_BASE_URL
    )
    session["app_settings"] = _with_derived_urls(current)
    return session["app_settings"]


def get_selected_model(settings: dict[str, str]) -> str:
    if settings["model_provider"] == "Ollama":
        return settings["ollama_model"]
    if settings["model_provider"] == "OpenAI compatible":
        return settings["openai_compatible_model"]
    return settings["openai_model"]
