from entity.blank_locator import find_blank_coords


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 격자 (0이 2개)
    # When: find_blank_coords(grid_g1) 호출
    # Then: [(1,3),(2,2)] 반환 (0-index, row-major)
    assert find_blank_coords(grid_g1) == [(1, 3), (2, 2)]
