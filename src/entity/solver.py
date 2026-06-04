"""부분 마방진 1-step 채우기 — D-SOL-01 (유효 격자·빈칸 2개 전제)."""

from entity.blank_locator import find_blank_coords
from entity.constants import GRID_COLS, MAGIC_SUM


def solve_step_a(grid: list[list[int]]) -> list[int]:
    """첫·둘째 빈칸(row-major)에 행 합 기준 값을 채운 `int[6]` 1-index를 반환한다."""
    blanks = find_blank_coords(grid)
    if len(blanks) != 2:
        raise ValueError("solve_step_a expects exactly 2 blanks")

    r1, c1 = blanks[0]
    r2, c2 = blanks[1]
    n1 = MAGIC_SUM - sum(grid[r1][c] for c in range(GRID_COLS) if c != c1)
    n2 = MAGIC_SUM - sum(grid[r2][c] for c in range(GRID_COLS) if c != c2)
    return [r1 + 1, c1 + 1, n1, r2 + 1, c2 + 1, n2]
