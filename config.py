from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import yaml


# ---------- Data models ----------


@dataclass
class AppConfig:
    name: str
    environment: str


@dataclass
class TokenLimits:
    max_output_tokens: int
    max_input_tokens: int


@dataclass
class RoutingConfig:
    providers: List[str]
    fallback_on: List[str]
    tokens: TokenLimits


@dataclass
class ProviderParams:
    temperature: float
    top_p: Optional[float] = None


@dataclass
class ProviderConfig:
    type: str
    model: str
    timeout_ms: int
    api_key_env: Optional[str] = None
    base_url: Optional[str] = None
    params: Optional[ProviderParams] = None


@dataclass
class PromptConfig:
    system_path: str
    user_path: str
    schema_path: Optional[str] = None


@dataclass
class RootConfig:
    app: AppConfig
    routing: RoutingConfig
    providers: Dict[str, ProviderConfig]
    prompts: Dict[str, PromptConfig]


# ---------- Loader ----------


def load_config(path: str | Path = "config.yaml") -> RootConfig:
    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    routing = RoutingConfig(
        providers=raw["routing"]["providers"],
        fallback_on=raw["routing"]["fallback_on"],
        tokens=TokenLimits(**raw["routing"]["tokens"]),
    )

    providers = {
        name: ProviderConfig(
            **{
                **cfg,
                "params": ProviderParams(**cfg["params"]) if "params" in cfg else None,
            }
        )
        for name, cfg in raw["providers"].items()
    }

    prompts = {name: PromptConfig(**cfg) for name, cfg in raw["prompts"].items()}

    return RootConfig(
        app=AppConfig(**raw["app"]),
        routing=routing,
        providers=providers,
        prompts=prompts,
    )
