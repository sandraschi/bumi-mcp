"""Parse common JSON shapes from vision / detector nodes (no rclpy dependency)."""

from __future__ import annotations

import json
import re
from typing import Any


def tokenize_target(text: str) -> list[str]:
    """Lowercase tokens (letters, digits, underscore) length >= 2 for fuzzy match."""
    raw = (text or "").lower()
    return sorted(
        {t for t in re.findall(r"[a-z0-9][a-z0-9_-]{1,}", raw) if len(t) >= 2},
        key=len,
        reverse=True,
    )


def extract_detection_labels(obj: Any) -> list[str]:
    """
    Normalize labels from flexible JSON payloads on std_msgs/String topics.

    Supported shapes include:
    - {"detections": [{"label": "dog", "score": 0.9}, ...]}
    - {"objects": [{"class_name": "german_shepherd"}, ...]}
    - {"results": [{"class": "person", "confidence": 0.5}]}
    - [{"name": "dog"}, ...]
    """
    labels: list[str] = []

    def _add(s: str | None) -> None:
        if s and str(s).strip():
            labels.append(str(s).strip())

    if obj is None:
        return labels

    if isinstance(obj, str):
        try:
            obj = json.loads(obj)
        except json.JSONDecodeError:
            return labels

    if isinstance(obj, list):
        for it in obj:
            if isinstance(it, dict):
                _add(it.get("label") or it.get("class") or it.get("class_name") or it.get("name"))
        return labels

    if not isinstance(obj, dict):
        return labels

    for key in ("detections", "objects", "results", "labels", "predictions"):
        arr = obj.get(key)
        if not isinstance(arr, list):
            continue
        for it in arr:
            if isinstance(it, str):
                _add(it)
            elif isinstance(it, dict):
                _add(it.get("label") or it.get("class") or it.get("class_name") or it.get("name"))
                # nested "attributes"
                sub = it.get("attributes")
                if isinstance(sub, dict):
                    _add(sub.get("label") or sub.get("name"))

    # single-object shortcut
    if not labels:
        _add(obj.get("label") or obj.get("class") or obj.get("class_name"))

    return labels


def labels_match_target(labels: list[str], target_tokens: list[str]) -> bool:
    """True if any label token-overlaps any target token (substring either way)."""
    if not labels or not target_tokens:
        return False
    low = [x.lower() for x in labels]
    for tok in target_tokens:
        for L in low:
            if tok in L or L in tok:
                return True
    return False
