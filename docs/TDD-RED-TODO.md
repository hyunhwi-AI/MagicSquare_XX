# MagicSquare_XX — TDD RED To Do List

| 항목 | 내용 |
|------|------|
| 문서 ID | `TDD-RED-TODO` |
| 프로젝트 | MagicSquare_XX |
| 단계 | M1 — RED 설계·구현 대기 |
| 작성일 | 2026-06-04 |
| 근거 | `docs/PRD.md`, `.cursorrules`, `.cursor/skills/magic-square-tdd/reference.md`, `Report/01.*`, `Report/02.*` |
| 생성 | `/tdd-red` RED 설계표 (Boundary + Logic) |

---

## 1. 현재 상태

- [x] ECB Harness (`pyproject.toml`, `src/`, `tests/` 디렉터리)
- [ ] `test_d_*` / `test_u_*` 본문 작성
- [ ] RED 단계 pytest **FAILED** 확인 (파일별)
- [ ] GREEN — `src/` 최소 구현

**RED 규칙:** `tests/`만 수정 · skip/xfail/assert 완화 금지 · Logic Track Domain Mock 금지 · entity E001~E005 emit 금지.

---

## 2. RED 묶음 권장 순서

| 순서 | Track | Layer | RED 묶음 | Test ID |
|:----:|-------|-------|----------|---------|
| 1 | Logic | entity | SSOT + LOC | D-01, D-LOC-01~03 |
| 2 | Logic | entity | 10선·빈칸 규칙 | D-02~D-04 |
| 3 | Logic | control | `validate()` + Mom Test | D-05~D-09 |
| 4 | UI | boundary | 입력 차단 | U-IN-01~05 |
| 5 | UI | boundary | 출력·플로우 | U-OUT-01~03, U-FLOW-01~02 |

---

## 3. Track A — UI / Boundary RED

**경로:** `tests/boundary/test_u_*.py`  
**선언 예:** `Phase: RED | Layer: boundary | Track: UI — U-IN-01 …`

### 3.1 U-IN (입력 검증 · E001~E005)

| Done | Test ID | Given | Then (기대값) | Expected RED Failure | 테스트 파일 (예) |
|:----:|---------|-------|---------------|----------------------|------------------|
| [ ] | **U-IN-01** | `grid=None` | **E004** `INVALID_FORMAT` | `ModuleNotFoundError` / `ImportError` | `test_u_invalid_format_e004.py` |
| [ ] | **U-IN-02** | `grid` = 3×4 | **E001** `INVALID_SIZE` | `AssertionError` | `test_u_invalid_grid_e001.py` |
| [ ] | **U-IN-03** | 빈칸 `0` 개수 ≠ 2 | **E002** `INVALID_BLANKS` | `AssertionError` | `test_u_invalid_blanks_e002.py` |
| [ ] | **U-IN-04** | 유효 4×4, 셀 값 `17` | **E003** `INVALID_RANGE` | `AssertionError` | `test_u_invalid_range_e003.py` |
| [ ] | **U-IN-05** | 유효 4×4, `1~16` 중복 | **E005** `INVALID_DUPLICATE` | `AssertionError` | `test_u_invalid_duplicate_e005.py` |

**To Do**

- [ ] boundary adapter 모듈·E코드 상수 정의 (RED: import 실패 허용)
- [ ] U-IN-01~05 AAA 테스트 작성
- [ ] `python -m pytest tests/boundary/test_u_invalid_grid_e001.py -v` → **FAILED** 확인
- [ ] entity/control이 E001~E005를 emit하지 않음 (ECB 점검)

### 3.2 U-OUT (출력·포맷)

| Done | Test ID | Given | Then (기대값) | Expected RED Failure | 테스트 파일 (예) |
|:----:|---------|-------|---------------|----------------------|------------------|
| [ ] | **U-OUT-01** | 유효 입력 **G1** (PRD §6.3) | `ok: bool`, `violations: list[str]` 스키마 | `ImportError` / `AssertionError` | `test_u_validate_output_schema.py` |
| [ ] | **U-OUT-02** | S1 fixture (3행만 깨짐) | `violations`에 `"row:2"` 포함 | `AssertionError` | `test_u_validate_s1_output.py` |
| [ ] | **U-OUT-03** | S3 fixture (주대각만 깨짐) | `violations`에 `"diag:main"` 포함 | `AssertionError` | `test_u_validate_s3_output.py` |

**To Do**

- [ ] G1·S1·S3 fixture를 `tests/boundary/conftest.py`에 raw grid로 고정
- [ ] U-OUT-01~03 AAA 테스트 작성
- [ ] `python -m pytest tests/boundary/ -v` (해당 파일) → **FAILED** 확인

### 3.3 U-FLOW (오케스트레이션)

| Done | Test ID | Given | Then (기대값) | Expected RED Failure | 비고 |
|:----:|---------|-------|---------------|----------------------|------|
| [ ] | **U-FLOW-01** | `grid=None` | `control.validate` **0회** 호출 | `pytest.fail()` RED / `ImportError` | control Mock **허용** |
| [ ] | **U-FLOW-02** | E002 격자 (빈칸 ≠ 2) | entity/control **미호출** | `AssertionError` / `pytest.fail()` RED | |

**To Do**

- [ ] U-FLOW-01~02 작성 (Mock은 control/IO만)
- [ ] 잘못된 입력 시 downstream 0회 호출 assert

### 3.4 Boundary — 후속 (Solver · v0.2+)

| Done | Test ID | Given | Then (기대값) | 비고 |
|:----:|---------|-------|---------------|------|
| [ ] | **U-OUT-04** | 유효 puzzle | `len(result)==6`, 1-index 좌표 | PRD v0.1 비목표 · `.cursorrules` Solver |

---

## 4. Track B — Logic RED

### 4.1 Entity — SSOT · LOC · 규칙

**경로:** `tests/entity/test_d_*.py`  
**선언 예:** `Phase: RED | Layer: entity | Track: Logic — D-01 …`

| Done | Test ID | Given | Then (기대값) | Expected RED Failure | 테스트 파일 (예) |
|:----:|---------|-------|---------------|----------------------|------------------|
| [ ] | **D-01** | — | `MagicConstant.SUM==34`, `SIZE==16` (리터럴 `34`/`16` 금지) | `ModuleNotFoundError` | `test_d_magic_constant.py` |
| [ ] | **D-LOC-01** | **G1**, `0`×2 | `blank_coords(g1)==[(1,3),(2,2)]` 0-index·row-major | `ImportError` / `AssertionError` | `test_d_loc_01.py` |
| [ ] | **D-LOC-02** | `(0,0)`, `(0,2)`만 `0` | `[(0,0),(0,2)]` | `AssertionError` | `test_d_loc_01.py` |
| [ ] | **D-LOC-03** | G1 | 2회 호출 결과 동일 | `AssertionError` | `test_d_loc_01.py` |
| [ ] | **D-02** | `0`이 3개인 4×4 | `count_blanks(grid)==3` | `AssertionError` | `test_d_blank_count.py` |
| [ ] | **D-03** | 완성 격자에 `17` | `in_range` → `False` | `AssertionError` | `test_d_value_range.py` |
| [ ] | **D-04** | G1 또는 10선 OK 격자 | 10선 합 = `MagicConstant.SUM` | `AssertionError` | `test_d_line_sums.py` |
| [ ] | **D-10** | Solver puzzle (v0.2+) | `int[6]` 1-index | `ModuleNotFoundError` | `test_d_solver_output.py` |

**To Do**

- [ ] `tests/entity/conftest.py` — `g1_grid` (PRD §6.3), `grid_blanks_row0` fixture
- [ ] D-01 RED: `pytest tests/entity/test_d_magic_constant.py -v` → **FAILED**
- [ ] D-LOC-01~03 RED: `pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v` → **FAILED**
- [ ] D-02~D-04 RED 테스트 추가
- [ ] entity에서 E001~E005 분기·메시지 없음 확인

### 4.2 Control — `validate()` · Mom Test

**경로:** `tests/control/test_d_*.py`  
**선언 예:** `Phase: RED | Layer: control | Track: Logic — D-07 S1 …`

| Done | Test ID | Given | Then (기대값) | Expected RED Failure | Mom Test |
|:----:|---------|-------|---------------|----------------------|----------|
| [ ] | **D-05** | G1 (10선 OK) | `ok is True`, `violations==[]` | `ImportError` | — |
| [ ] | **D-06** | S1 fixture | violation ID `row:*`/`col:*`/`diag:*` | `AssertionError` | — |
| [ ] | **D-07** | S1 — 3행만 깨짐 | `"row:2" in violations` | `AssertionError` | **S1** |
| [ ] | **D-08** | S3 — `diag:main`만 깨짐 | `"diag:main" in violations` | `AssertionError` | **S3** |
| [ ] | **D-09** | S2 — 동일 grid 2회 | `violations` 완전 동일 | `AssertionError` | **S2** |

**To Do**

- [ ] `tests/control/conftest.py` — S1·S2·S3 Mom Test fixture 고정
- [ ] D-05~D-09 AAA 테스트 작성
- [ ] `pytest tests/control/test_d_validate_s1.py -v` → **FAILED**
- [ ] GREEN 후 `pytest tests/entity tests/control -q` smoke

---

## 5. Fixture 참조 (공통)

### G1 (PRD §6.3 / Report §2.3)

```text
16  3  2  13
 5 10 11   0
 9  6  0  12
 4 15 14   1
```

- 빈칸 (0-index): `(1, 3)`, `(2, 2)`

### Mom Test (PRD §5 · Report §4.3)

| ID | RED Test ID | 기대 violation |
|----|-------------|----------------|
| S1 | D-07, U-OUT-02 | `row:2` |
| S2 | D-09 | 동일 grid → 동일 `violations` |
| S3 | D-08, U-OUT-03 | `diag:main` |

---

## 6. ECB · Mock 체크리스트 (RED 설계 준수)

- [ ] Logic Track: Domain/entity `MagicMock`·`patch` **금지**
- [ ] UI Track: control·IO Mock **허용** (U-FLOW만)
- [ ] entity → control/boundary import **금지**
- [ ] 코드·테스트에 `34`, `16` 리터럴 산재 **금지** (`MagicConstant` SSOT)
- [ ] RED 중 `src/` 수정 **금지** (GREEN까지)

---

## 7. pytest 명령 모음

```bash
# Logic — entity
python -m pytest tests/entity/test_d_magic_constant.py -v
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v

# Logic — control
python -m pytest tests/control/test_d_validate_s1.py -v

# UI — boundary
python -m pytest tests/boundary/test_u_invalid_grid_e001.py -v

# RED 완료 기준: FAILED (exit code 1). PASS / no tests = RED 미완료.
```

---

## 8. 완료 정의 (RED → GREEN handoff)

| 항목 | RED 완료 | GREEN 시작 |
|------|----------|------------|
| 테스트 | 해당 ID pytest **FAILED** | 동일 ID **PASS** |
| 변경 범위 | `tests/` only | `src/` 최소 구현 |
| 다음 | `/tdd-green` 또는 Agent GREEN 지시 | Logic smoke: `pytest tests/entity tests/control -q` |

---

## 9. 변경 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 0.1 | 2026-06-04 | Boundary(U-*)·Logic(D-*) RED To Do List 최초 작성 |
