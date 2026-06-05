"""Settings from environment."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BUMI_MCP_",
        env_file=".env",
        extra="ignore",
    )

    host: str = "127.0.0.1"
    port: int = 10774
    robot_ip: str = ""
    fallback_ip: str = ""
    bridge_port: int = 9090
    use_mock_bridge: bool = False
    connect_timeout_s: float = 15.0

    @model_validator(mode="after")
    def _apply_fleet_env(self) -> Self:
        if not self.robot_ip:
            self.robot_ip = (os.environ.get("BUMI_IP") or "").strip()
        if not self.fallback_ip:
            self.fallback_ip = (os.environ.get("BUMI_FALLBACK_IP") or "").strip()
        bp = (os.environ.get("BUMI_BRIDGE_PORT") or "").strip()
        if bp.isdigit():
            self.bridge_port = int(bp)
        mock = (os.environ.get("BUMI_USE_MOCK_BRIDGE") or "").strip().lower()
        if mock in ("1", "true", "yes", "on"):
            self.use_mock_bridge = True
        return self


@lru_cache
def load_settings() -> Settings:
    return Settings()
