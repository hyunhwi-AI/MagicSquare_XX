# MagicSquare_XX

4×4 **부분 마방진**(빈 칸 2개, 합 **34**, **10선** 검증)을 학습할 때, 틀린 행·열·대각선을 **즉시 짚어 주는 판정(validation)** 을 목표로 하는 프로젝트입니다.

> **v0.1 상태:** 문서·Mom Test·PRD 단계입니다. 실행 코드는 아직 없으며, `docs/PRD.md`의 M1( Rule + Command + Test Loop ) 구현이 다음 단계입니다.

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
├── docs/
│   └── PRD.md                # 제품 요구사항 (v0.1)
├── Report/
│   ├── 01.MagicSquare_ProblemDefinition_Report.md  # 문제 정의
│   └── 01.REPORT.md          # STEP 1 Mom Test 보고서
└── Prompting/
    ├── 01.REPORT-prompting.md
    └── 01.MagicSquare_ProblemDefinition_Report-prompting.md
```

---

## 문서 읽는 순서

1. **[Report/01.REPORT.md](Report/01.REPORT.md)** — Mom Test 인터뷰·워크북·증거 3줄  
2. **[Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md)** — 도메인, R-G-I-O, 성공 기준 S1~S3, 8계층 범위  
3. **[docs/PRD.md](docs/PRD.md)** — 기능 요구, API 입출력, 마일스톤, 비목표  

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

## ECB 로드맵 (참고)

4교시 실습 맥락의 ECB 분류. **v0.1**에서는 `SquareValidator`(판정)만 해당합니다.

| 계층 | 컴포넌트 | v0.1 |
|------|----------|------|
| Control | `SquareValidator` | ✅ |
| Control | `MissingFinder`, `Solver` | ❌ |
| Entity | `MagicSquare`, `Cell`, `SolveResult` | fixture 수준 |
| Boundary | `GridUI`, `InputHandler`, `ResultDisplay` | ❌ |

---

## 시작하기 (구현 예정)

코드가 추가되면 예상 형태:

```bash
# (M1 이후) 예시
python -m magicsquare validate --grid examples/slide_partial.txt
```

현재는 문서만 있으므로, 구현 시 `docs/PRD.md` §4·§6과 `Report/01.MagicSquare_ProblemDefinition_Report.md` §4.3 성공 기준 S1~S3를 테스트 fixture로 고정하세요.

---

## 라이선스 / 기여

교육·실습용 프로젝트입니다. 기여·라이선스 정책은 저장소에 파일이 추가되면 명시합니다.

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-06-04 | README 초안 — Mom Test·문제 정의·PRD 반영 |
