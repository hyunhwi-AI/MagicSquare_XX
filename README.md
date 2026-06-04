# MagicSquare_XX

4×4 **부분 마방진**(빈 칸 2개, 합 **34**, **10선** 검증)을 학습할 때, 틀린 행·열·대각선을 **즉시 짚어 주는 판정(validation)** 을 목표로 하는 프로젝트입니다.

> **v0.1 상태:** ECB Harness·Dual-Track TDD 골격 준비 완료. **M1 RED** 진행 중 — 실패 테스트(`test_d_*` / `test_u_*`) 작성 후 GREEN. 상세 목록: [docs/TDD-RED-TODO.md](docs/TDD-RED-TODO.md).

---

## 문제 한 줄

학습자가 격자를 손·코드로 채운 뒤 **어느 선(10선)이 합 34를 깨는지** 바로 알 수 없어, 같은 계산을 반복하고 **맞게 끝냈다는 확신 없이** 멈춘다.

**이 프로젝트가 하는 일:** 자동으로 퍼즐을 **풀어 주지 않고**, 채운 4×4 격자가 규칙을 만족하는지 검사하고, 실패 시 `row:2`, `diag:main`처럼 **깨진 선 ID**를 돌려 준다.

**이번에 하지 않는 일:** Solver(빈 칸 자동 채우기), GUI/데모 앱, 난이도 생성·공유.

---

## 도메인

| 항목 | 규칙 |
|------|------|
| 격자 | 4×4 정수 배열 |
| 빈 칸 | `0` 정확히 **2개** |
| 숫자 | 1~16 (완성 시 중복 없음) |
| 목표 합 | **34** |
| 검증 대상 (**10선**) | 4행 + 4열 + 주대각선 + 부대각선 |

### 예시 격자 (4교시 슬라이드)

| 16 | 3 | 2 | 13 |
| 5 | 10 | 11 | 0 |
| 9 | 6 | 0 | 12 |
| 4 | 15 | 14 | 1 |

---

## 저장소 구조

```text
MagicSquare_XX/
├── README.md                 # 이 파일
├── .cursorrules              # TDD·ECB·Dual-Track 규율
├── pyproject.toml            # pytest Harness
├── docs/
│   ├── PRD.md                # 제품 요구사항 (v0.1)
│   └── TDD-RED-TODO.md       # RED 설계·To Do (SSOT)
├── src/
│   ├── entity/  control/  boundary/
├── tests/
│   ├── entity/  control/  boundary/   # test_d_* / test_u_*
├── Report/
│   ├── 01.MagicSquare_ProblemDefinition_Report.md
│   ├── 01.REPORT.md
│   └── 02.REPORT.md          # STEP 2 Harness 보고서
└── Prompting/
```

---

## 문서 읽는 순서

1. **[Report/01.REPORT.md](Report/01.REPORT.md)** — Mom Test 인터뷰·워크북·증거 3줄  
2. **[Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md)** — 도메인, R-G-I-O, 성공 기준 S1~S3, 8계층 범위  
3. **[docs/PRD.md](docs/PRD.md)** — 기능 요구, API 입출력, 마일스톤, 비목표  
4. **[docs/TDD-RED-TODO.md](docs/TDD-RED-TODO.md)** — M1 RED 체크리스트·Given/Then·pytest  

프롬프트·세션 기록은 `Prompting/` 참고.

---

## Mom Test 요약

| 항목 | 내용 |
|------|------|
| **페르소나** | 4×4, 빈 칸 2(`0`), 1~16, 합 34를 맞추는 학습자 |
| **진짜 문제** | 틀린 줄·대각선을 즉시 못 짚어 반복 계산·확신 없는 중단 |
| **증거 (예)** | 종이 35분·3행 실패; 코드 두 실행 혼동; 대각선 사후 발견 |

인터뷰 일부는 STEP 1에서 **페르소나 기준 합성**되었습니다. 구현 전 **실인터뷰 1회**로 증거를 갱신하는 것을 권장합니다.

---

## v0.1 목표 (PRD)

| ID | 목표 |
|----|------|
| G1 | 10선 합 34 검증 |
| G2 | 실패 시 `violations[]` (`row:*`, `col:*`, `diag:*`) |
| G3 | 동일 격자 → 동일 결과 (재현) |
| G4 | Mom Test S1~S3 자동 테스트 |

### API (계획)

```text
validate(grid, target_sum=34) → { ok: bool, violations: string[] }
```

### 이번 세션 8계층

| 계층 | v0.1 |
|------|------|
| Rule | ✅ |
| Command (`validate`) | ✅ |
| Skill (`listViolations`) | △ 선택 |
| Test Loop | ✅ |
| Boundary / Solver / UI | ❌ 후속 |

---

## 마일스톤

| 단계 | 산출 | 완료 조건 |
|------|------|-----------|
| **M1** | Rule + Command + Test Loop | S1~S3 테스트 Green |
| M2 | Skill + 문서 | `listViolations` |
| M3+ | Entity, MissingFinder, UI | PRD v0.2+ |

---

## TDD RED 체크리스트 (M1)

근거: [docs/TDD-RED-TODO.md](docs/TDD-RED-TODO.md) · `.cursorrules` · Dual-Track (`D-*` Logic / `U-*` UI).

**RED 규칙:** `tests/`만 수정 · skip/xfail/assert 완화 금지 · Logic Track Domain Mock 금지 · entity E001~E005 emit 금지 · pytest **FAILED** = RED 완료.

### 공통 · Harness

- [x] ECB Harness (`pyproject.toml`, `src/`, `tests/` 디렉터리)
- [ ] `test_d_*` / `test_u_*` 본문 작성
- [ ] RED 단계 pytest **FAILED** 확인 (Test ID별)
- [ ] GREEN — `src/` 최소 구현

### ECB · Mock (RED 설계 준수)

- [ ] Logic Track: Domain/entity `MagicMock`·`patch` 금지
- [ ] UI Track: control·IO Mock 허용 (U-FLOW만)
- [ ] entity → control/boundary import 금지
- [ ] `34` / `16` 리터럴 산재 금지 (`MagicConstant` SSOT)
- [ ] RED 중 `src/` 수정 금지 (GREEN까지)

### 권장 순서

| 순서 | Track | Layer | Test ID |
|:----:|-------|-------|---------|
| 1 | Logic | entity | D-01, D-LOC-01~03 |
| 2 | Logic | entity | D-02~D-04 |
| 3 | Logic | control | D-05~D-09 |
| 4 | UI | boundary | U-IN-01~05 |
| 5 | UI | boundary | U-OUT-01~03, U-FLOW-01~02 |

---

### Track B — Logic (`tests/entity`, `tests/control`)

**선언 예:** `Phase: RED | Layer: entity | Track: Logic — D-01 …`

#### Entity — SSOT · LOC · 규칙

- [ ] **D-01** — `MagicConstant.SUM==34`, `SIZE==16` (`test_d_magic_constant.py`)
- [ ] **D-LOC-01** — G1 → `blank_coords` → `[(1,3),(2,2)]` (`test_d_loc_01.py`)
- [ ] **D-LOC-02** — `(0,0)(0,2)` → row-major `[(0,0),(0,2)]`
- [ ] **D-LOC-03** — G1 두 번 호출 → 동일 결과
- [ ] **D-02** — 빈칸 개수 규칙 (`test_d_blank_count.py`)
- [ ] **D-03** — 값 범위 1~16 (`test_d_value_range.py`)
- [ ] **D-04** — 10선 합 = `MagicConstant.SUM` (`test_d_line_sums.py`)
- [ ] `tests/entity/conftest.py` — `g1_grid`, `grid_blanks_row0` fixture
- [ ] entity E001~E005 분기·메시지 없음 확인
- [ ] **D-10** — Solver `int[6]` 1-index (v0.2+, 후속)

#### Control — `validate()` · Mom Test

- [ ] **D-05** — G1 → `ok is True`, `violations==[]`
- [ ] **D-06** — violation ID `row:*` / `col:*` / `diag:*` 형식
- [ ] **D-07** — **S1** → `"row:2" in violations`
- [ ] **D-08** — **S3** → `"diag:main" in violations`
- [ ] **D-09** — **S2** → 동일 grid 재호출 시 `violations` 동일
- [ ] `tests/control/conftest.py` — S1·S2·S3 fixture 고정
- [ ] `pytest tests/control/test_d_validate_s1.py -v` → **FAILED**

---

### Track A — UI / Boundary (`tests/boundary`)

**선언 예:** `Phase: RED | Layer: boundary | Track: UI — U-IN-01 …`

#### U-IN — 입력 검증 (E001~E005)

- [ ] **U-IN-01** — `grid=None` → **E004** `INVALID_FORMAT`
- [ ] **U-IN-02** — 3×4 → **E001** `INVALID_SIZE`
- [ ] **U-IN-03** — 빈칸 `0` ≠ 2 → **E002** `INVALID_BLANKS`
- [ ] **U-IN-04** — 셀 `17` → **E003** `INVALID_RANGE`
- [ ] **U-IN-05** — 1~16 중복 → **E005** `INVALID_DUPLICATE`
- [ ] boundary adapter·E코드 상수 (RED: import 실패 허용)
- [ ] entity/control이 E001~E005 emit하지 않음

#### U-OUT — 출력·포맷

- [ ] **U-OUT-01** — G1 → `ok`, `violations` 스키마
- [ ] **U-OUT-02** — S1 → `violations`에 `"row:2"`
- [ ] **U-OUT-03** — S3 → `violations`에 `"diag:main"`
- [ ] `tests/boundary/conftest.py` — G1·S1·S3 fixture
- [ ] **U-OUT-04** — Solver `len(result)==6` (v0.2+, 후속)

#### U-FLOW — 오케스트레이션

- [ ] **U-FLOW-01** — `grid=None` → `control.validate` 0회 (Mock 허용)
- [ ] **U-FLOW-02** — E002 격자 → entity/control 미호출

---

### Fixture · Mom Test 매핑

| Fixture | 용도 | RED Test ID |
|---------|------|-------------|
| **G1** (PRD §6.3) | 슬라이드 예제, 빈칸 `(1,3)(2,2)` | D-LOC-01, D-05, U-OUT-01 |
| **S1** | 3행만 깨짐 | D-07, U-OUT-02 |
| **S2** | 재현 | D-09 |
| **S3** | 주대각만 깨짐 | D-08, U-OUT-03 |

---

### pytest (RED 확인)

```bash
pip install -e ".[dev]"

# Logic — entity
python -m pytest tests/entity/test_d_magic_constant.py -v
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v

# Logic — control
python -m pytest tests/control/test_d_validate_s1.py -v

# UI — boundary
python -m pytest tests/boundary/test_u_invalid_grid_e001.py -v
```

RED 완료: **FAILED** (exit 1). PASS 또는 no tests → RED 미완료.

---

## ECB 로드맵 (참고)

4교시 실습 맥락의 ECB 분류. **v0.1**에서는 `SquareValidator`(판정)만 해당합니다.

| 계층 | 컴포넌트 | v0.1 |
|------|----------|------|
| Control | `SquareValidator` | ✅ |
| Control | `MissingFinder`, `Solver` | ❌ |
| Entity | `MagicSquare`, `Cell`, `SolveResult` | fixture 수준 |
| Boundary | `GridUI`, `InputHandler`, `ResultDisplay` | ❌ |

---

## 시작하기

### Harness (현재)

```bash
pip install -e ".[dev]"
pytest   # 테스트 0건이면 exit 5 — Harness 정상
```

M1은 **RED 체크리스트** 순서대로 `tests/`에 실패 테스트를 추가한 뒤 GREEN에서 `src/`를 구현합니다. Cursor: `/tdd-red`, `/tdd-green` (`.cursor/commands/`).

### CLI (M1 GREEN 이후 예정)

```bash
python -m magicsquare validate --grid examples/slide_partial.txt
```

---

## 라이선스 / 기여

교육·실습용 프로젝트입니다. 기여·라이선스 정책은 저장소에 파일이 추가되면 명시합니다.

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-06-04 | README 초안 — Mom Test·문제 정의·PRD 반영 |
| 2026-06-04 | M1 TDD RED 체크리스트·Harness 구조 반영 (`docs/TDD-RED-TODO.md`) |
