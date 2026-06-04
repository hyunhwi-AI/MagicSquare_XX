# MagicSquare_XX — Product Requirements Document (PRD)

| 항목 | 내용 |
|------|------|
| 제품 | MagicSquare_XX |
| 버전 | 0.1 (초안) |
| 작성일 | 2026-06-04 |
| 상태 | Draft |
| 상세 문제 정의 | `Report/01.MagicSquare_ProblemDefinition_Report.md` |

---

## 1. 개요

### 1.1 한 줄 요약

4×4 부분 마방진(빈 칸 2, **10선** 합 34)을 학습할 때, **어느 선이 깨졌는지** 즉시 알려 주는 **판정(validation)** 기능을 제공한다.

### 1.2 배경 (Mom Test)

- **페르소나:** 4×4 격자, 빈 칸 2개(`0`), 1~16, 합 34를 맞추는 학습자.
- **진짜 문제:** 틀린 행·열·대각선을 즉시 짚지 못해 반복 계산·확신 없는 중단이 발생한다.
- **증거 요약:** 종이 35분 후 3행 실패 미발견; 코드 두 실행(7·8 vs 7·15) 혼동; 대각선은 사후에야 발견.

---

## 2. 목표 및 비목표

### 2.1 목표 (In Scope — v0.1)

| ID | 목표 |
|----|------|
| G1 | 4×4 격자에 대해 **10선** 합 34 검증 |
| G2 | 실패 시 **위반 선 ID** 목록 반환 (`row:*`, `col:*`, `diag:*`) |
| G3 | 동일 입력에 대해 **결과 재현** (도구·재실행 동일) |
| G4 | Mom Test S1~S3를 **자동 테스트**로 고정 |

### 2.2 비목표 (Out of Scope — v0.1)

| ID | 비목표 | 이유 |
|----|--------|------|
| O1 | 빈 칸 **자동 채우기 (Solver)** | Mom Test 표면 문제 — “대신 풀기” |
| O2 | **GUI** / GridUI / 데모 앱 | 판정 불편과 무관, 후속 |
| O3 | 난이도 생성·공유·계정 | 증거 무연결 |
| O4 | TDD/ECB **교육 설득**만을 위한 산출 | PRD 요구 아님 |

---

## 3. 사용자

### 3.1 Primary User

- **학습자:** 4×4 부분 마방진을 손·코드로 채우고, 합 34·10선을 스스로 확인하는 사람 (SW 전공 2학년 실습 맥락 포함).

### 3.2 사용자 스토리

| ID | 스토리 | 수용 기준 |
|----|--------|-----------|
| US1 | 학습자로서, 채운 격자를 넣으면 **몇 번째 행/열/대각선이 34가 아닌지** 알고 싶다 | S1, S3 |
| US2 | 학습자로서, 어제 종이 풀이와 오늘 코드 결과가 **같은지** 확인하고 싶다 | S2 |
| US3 | 학습자로서, “맞는 것 같다”만이 아니라 **pass/fail**을 받고 싶다 | G2 |

---

## 4. 기능 요구사항

### 4.1 도메인 규칙 (Rule)

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| R1 | 입력은 4×4 정수 배열 | P0 |
| R2 | `0`은 정확히 2개 (빈 칸) | P0 |
| R3 | `0`이 아닌 값은 1~16 (완성 검증 시 중복 없음) | P0 |
| R4 | **10선** 각각 합 = 34 (완성·부분 모두 해당 선에 대해 검사) | P0 |

**10선 정의:** `row:0..3`, `col:0..3`, `diag:main`, `diag:anti`.

### 4.2 판정 API (Command)

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| C1 | `validate(grid, target_sum=34)` → `{ ok: bool, violations: string[] }` | P0 |
| C2 | `ok === true` iff `violations` empty | P0 |
| C3 | 각 violation은 깨진 선 ID 하나 (예: `row:2`) | P0 |
| C4 | 빈 칸이 2개가 아니면 `ok: false` + 전제 위반 코드/메시지 | P0 |

### 4.3 Skill (선택, v0.1)

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| SK1 | `listViolations(grid)` — C1 결과의 `violations`만 반환 | P1 |

### 4.4 Test Loop

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| T1 | **Fixture:** 슬라이드 예제 기반 4×4 (빈 칸 2) | P0 |
| T2 | **S1:** 3행만 깨진 격자 → `row:2` 포함 | P0 |
| T3 | **S3:** 행 통과·주대각선만 깨진 격자 → `diag:main` 포함, 행만 검사 시 실패하도록 회귀 방지 | P0 |
| T4 | **S2:** 동일 `grid` 두 번 호출 시 `violations` 동일 | P0 |

---

## 5. 성공 기준 (Mom Test → PRD)

| ID | 기준 | Mom Test 증거 |
|----|------|----------------|
| S1 | 3행 합 ≠ 34 → `row:2` (또는 해당 행) 반환 | “3행 합이 34가 안 됐다” |
| S2 | 동일 격자 재검증 시 동일 `violations` | 엑셀·코드로 다시 확인 (25+15분) |
| S3 | 대각선만 실패 시 `diag:*` 반환 | “대각선은 끝에서야 알았다” |

---

## 6. 입출력 명세

### 6.1 Input

```text
grid: int[4][4]   # 0 = empty (exactly 2), else 1..16 when validating filled cells
target_sum: int   # default 34
```

### 6.2 Output

```text
{
  "ok": boolean,
  "violations": ["row:2", "diag:main", ...],  # empty if ok
  "error"?: "INVALID_EMPTY_COUNT" | "INVALID_RANGE" | ...
}
```

### 6.3 예시 격자 (참고)

| 16 | 3 | 2 | 13 |
| 5 | 10 | 11 | 0 |
| 9 | 6 | 0 | 12 |
| 4 | 15 | 14 | 1 |

---

## 7. 8계층 — 이번 릴리스 범위

| 계층 | v0.1 | 비고 |
|------|------|------|
| Rule | ✅ | §4.1 |
| Command | ✅ | §4.2 |
| Skill | △ | §4.3 |
| Test Loop | ✅ | §4.4 |
| Entity / Boundary / Policy / … | ❌ | PRD 후속 버전 |

---

## 8. ECB 로드맵 (참고, v0.1 미포함)

| 컴포넌트 | v0.1 | v0.2+ |
|----------|------|-------|
| `SquareValidator` | ✅ (Command) | — |
| `MissingFinder` | ❌ | 검토 |
| `Solver` | ❌ | 검토 |
| `MagicSquare`, `Cell`, `SolveResult` | fixture 수준 | Entity |
| `GridUI`, `InputHandler`, `ResultDisplay` | ❌ | Boundary |

---

## 9. 품질·제약

| 항목 | 요구 |
|------|------|
| 결정성 | 동일 `grid` → 동일 `violations` (S2) |
| 명확성 | “거의 맞음” 금지 — `ok` 이진 |
| 성능 | 4×4 — 체감 지연 없음 (학습용) |
| 플랫폼 | Python CLI 우선 (학습자 VS Code 맥락) |

---

## 10. 마일스톤 (초안)

| 단계 | 산출 | 완료 조건 |
|------|------|-----------|
| M1 | Rule + Command + Test Loop | S1~S3 테스트 Green |
| M2 | Skill + 문서 | `listViolations` |
| M3 | Entity + MissingFinder (검토) | PRD v0.2 |
| M4 | Boundary UI (검토) | PRD v0.3 |

---

## 11. 리스크

| 리스크 | 영향 | 대응 |
|--------|------|------|
| Mom Test 합성 증거 | 잘못된 우선순위 | 실인터뷰 후 §5 갱신 |
| 행만 검사하는 구현 | S3 실패 | T3 회귀 테스트 필수 |
| Solver scope creep | 일정 지연 | §2.2 비목표 고수 |

---

## 12. 참고 문서

- `Report/01.MagicSquare_ProblemDefinition_Report.md`
- `Report/STEP1-Mom-Test-Report.md`

---

## 13. 변경 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 0.1 | 2026-06-04 | Mom Test·세션 3 초안 기반 최초 작성 |
