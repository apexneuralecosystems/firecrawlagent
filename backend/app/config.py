import os
from dataclasses import dataclass


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


@dataclass(frozen=True)
class Settings:
    env: str
    allowed_origins: list[str]
    chroma_db_path: str
    require_single_worker: bool

    @property
    def is_production(self) -> bool:
        return self.env.lower() in {"prod", "production"}


def get_settings() -> Settings:
    env = os.getenv("ENV", os.getenv("ENVIRONMENT", "development"))
    allowed_origins = _parse_csv(os.getenv("ALLOWED_ORIGINS"))
    chroma_db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    require_single_worker = os.getenv("REQUIRE_SINGLE_WORKER", "1") != "0"
    return Settings(
        env=env,
        allowed_origins=allowed_origins,
        chroma_db_path=chroma_db_path,
        require_single_worker=require_single_worker,
    )


def validate_production_env(settings: Settings) -> None:
    """
    Fail fast on common misconfigurations when ENV=production.
    """
    if not settings.is_production:
        return

    missing: list[str] = []
    if not os.getenv("SECRET_KEY") or os.getenv("SECRET_KEY") in {"default-dev-secret-key", "change-me"}:
        missing.append("SECRET_KEY")
    if not os.getenv("DATABASE_URL"):
        missing.append("DATABASE_URL")
    if not os.getenv("FIRECRAWL_API_KEY"):
        missing.append("FIRECRAWL_API_KEY")
    if not os.getenv("OPENROUTER_API_KEY"):
        missing.append("OPENROUTER_API_KEY")
    if not settings.allowed_origins:
        missing.append("ALLOWED_ORIGINS (comma-separated)")

    if missing:
        raise RuntimeError(
            "Production configuration error. Missing/invalid: " + ", ".join(missing)
        )


