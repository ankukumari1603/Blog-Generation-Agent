import os
from dataclasses import dataclass

from dotenv import load_dotenv


DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"


class SettingsError(Exception):
    """Raised when required application configuration is missing."""


@dataclass(frozen=True)
class Settings:
    groq_api_key: str
    groq_model: str


def get_settings() -> Settings:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise SettingsError(
            "GROQ_API_KEY is not set. Add your Groq API key to the environment "
            "or a local .env file."
        )

    model = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip()
    if not model:
        raise SettingsError("GROQ_MODEL cannot be empty.")

    return Settings(groq_api_key=api_key, groq_model=model)
