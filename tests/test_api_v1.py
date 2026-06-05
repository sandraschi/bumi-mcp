"""REST v1 contract tests (mock bridge)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from bumi_mcp.app import build_app


def test_health_v1_mock_connected() -> None:
    with TestClient(build_app()) as client:
        r = client.get("/api/v1/health")
        assert r.status_code == 200
        body = r.json()
        assert body["robot"] == "noetix_bumi"
        assert body["mock"] is True
        assert body["connected"] is True


def test_telemetry_v1() -> None:
    with TestClient(build_app()) as client:
        r = client.get("/api/v1/telemetry")
        assert r.status_code == 200
        tel = r.json()["telemetry"]
        assert tel["expected_dof"] == 21
        assert tel["joint_count"] >= 1


def test_estop_and_walk_mock() -> None:
    with TestClient(build_app()) as client:
        assert client.post("/api/v1/control/estop").status_code == 200
        assert client.post("/api/v1/control/walk", params={"linear": 0.2, "angular": 0.0}).status_code == 200
