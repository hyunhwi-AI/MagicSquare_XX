"""빈칸(`0`) 좌표 추출 — FR-LOC-01, row-major·0-index (Report §2.3)."""


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """격자에서 `0`인 셀의 (row, col)을 행 우선 스캔 순으로 반환한다."""
    coords: list[tuple[int, int]] = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == 0:
                coords.append((row_idx, col_idx))
    return coords
