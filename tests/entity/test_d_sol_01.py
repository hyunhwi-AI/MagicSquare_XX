from entity.solver import solve_step_a

from tests._approval import assert_matches_golden, format_solver_success

GOLDEN_D_SOL_01_G1_STEP_A = "d_sol_01_g1_step_a.approved.txt"


def test_d_sol_01_step_a_success(grid_g1):
    # Given: G1 (PRD §6.3)
    # When: solve_step_a(grid_g1)
    result = solve_step_a(grid_g1)
    actual = format_solver_success(result)
    # Then: golden 고정 포맷 (int[6] 1-index)
    assert_matches_golden(actual, GOLDEN_D_SOL_01_G1_STEP_A)
