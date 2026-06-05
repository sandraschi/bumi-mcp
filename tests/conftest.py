import os

import pytest

# Default mock bridge for API tests (no Jetson required).
os.environ.setdefault("BUMI_USE_MOCK_BRIDGE", "1")

from bumi_mcp.config import load_settings

load_settings.cache_clear()


@pytest.fixture
def anyio_backend():
    return "asyncio"
