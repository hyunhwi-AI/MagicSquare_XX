# D-* Logic 테스트 ID

| ID | 대상 | 요약 |
|----|------|------|
| D-01 | entity | `MagicConstant` SSOT — SUM=34, SIZE=16 |
| D-02 | entity | 빈칸 `0` 정확히 2개 |
| D-03 | entity | 값 범위 1~16, 완성 시 중복 없음 |
| D-04 | entity | 10선 합 = MagicConstant.SUM |
| D-05 | control | `validate()` — ok ↔ violations 빈 배열 |
| D-06 | control | violation ID 형식 `row:*`, `col:*`, `diag:*` |
| D-07 | control | **S1** 3행만 깨짐 → `row:2` 포함 |
| D-08 | control | **S3** 주대각선만 깨짐 → `diag:main` 포함 |
| D-09 | control | **S2** 동일 grid 재호출 → violations 동일 |
| D-10 | entity | Solver 출력 `int[6]` 1-index 좌표 |

> U-* ID는 boundary RED 시 `test_u_*.py`와 함께 추가한다.
