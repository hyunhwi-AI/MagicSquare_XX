"""Golden Master — 고정 텍스트 포맷 비교 (int[6] 1-index · 에러 코드 문자열)."""

from __future__ import annotations

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def format_solver_success(values: list[int]) -> str:
    """성공: `ok` + 6개 정수(1-index 좌표·값), 쉼표 구분."""
    if len(values) != 6:
        raise ValueError(f"int[6] required, got {len(values)}")
    return "ok\n" + ",".join(str(v) for v in values)


def format_solver_error(code: str) -> str:
    """실패: `error` + E006 등 에러 코드 문자열 한 줄."""
    return f"error\n{code}"


def assert_matches_golden(actual: str, relative: str) -> None:
    """`tests/golden/{relative}` 와 actual 문자열을 비교한다."""
    path = GOLDEN_DIR / relative
    normalized = actual if actual.endswith("\n") else actual + "\n"

    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(normalized, encoding="utf-8")
        return

    if not path.is_file():
        raise AssertionError(f"golden file missing: {path}")

    expected = path.read_text(encoding="utf-8")
    if expected != normalized:
        raise AssertionError(
            f"golden mismatch: {path}\n--- expected ---\n{expected}--- actual ---\n{normalized}"
        )
