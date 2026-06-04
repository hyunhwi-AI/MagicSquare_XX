import pytest

from entity.constants import BLANK_COUNT, GRID_COLS, GRID_ROWS


@pytest.fixture
def grid_g1():
    """G1 (PRD §6.3): `0`이 BLANK_COUNT개, row-major 스캔용 격자 데이터."""
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 0],
        [9, 6, 0, 12],
        [4, 15, 14, 1],
    ]
    assert len(grid) == GRID_ROWS
    assert all(len(row) == GRID_COLS for row in grid)
    assert sum(cell == 0 for row in grid for cell in row) == BLANK_COUNT
    return grid
