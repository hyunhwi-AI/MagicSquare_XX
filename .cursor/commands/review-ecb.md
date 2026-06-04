# Review ECB — 계약·아키텍처 리뷰

**MagicSquare_XX — 코드 수정 금지.**  
`src/`, `tests/` 파일을 **읽고 분석만** 한다. 위반은 표로 보고하고, **수정·리팩터·커밋은 하지 않는다.**  
근거: `.cursorrules`, `docs/PRD.md`.

---

## 필수 선언

작업 **첫 줄**:

```text
Phase: REVIEW | Scope: ECB·계약 | 대상: {브랜치/경로/커밋 범위}
```

---

## 절차

1. **범위 확정** — 사용자가 지정한 diff, PR, 디렉터리, 또는 `src/` + `tests/` 전체.
2. **파일 읽기** — `src/entity`, `src/control`, `src/boundary`, `tests/entity`, `tests/control`, `tests/boundary`.
3. **체크 5항** — 아래 표 기준으로 위반만 수집 (해당 없으면 “해당 없음”).
4. **결과 표 작성** — 위반 행만 또는 “위반 없음” 한 줄.
5. **요약** — Critical(계약 깨짐) / Warning(모호·잠재) 개수 + 한 줄 판정.

---

## 체크 항목 (5)

| # | 체크 | 계약 | 위반 예 |
|---|------|------|---------|
| 1 | **import 방향** | `boundary → control → entity`만. entity→* import 금지. control→boundary 금지. | `entity`에서 `control` import; `control`에서 `boundary` import |
| 2 | **entity E001~E005** | entity/control에서 E001~E005 catch·매핑·메시지·분기 **금지** | `if empty_count != 2: raise E002` in entity |
| 3 | **int[6] 1-index** | Solver 성공 출력 `[r1,c1,n1,r2,c2,n2]`, 행·열 **1~4** | 0-index 좌표 반환; 길이 ≠ 6 |
| 4 | **MagicConstant SSOT** | `34`, `16` 리터럴 코드·테스트 산재 금지 | `sum == 34`, `range(1, 17)` 대신 상수 미사용 |
| 5 | **Logic Track Domain Mock** | `tests/entity`, `tests/control`에서 Domain/entity Mock **금지** | `MagicMock`, `patch` on entity class in `test_d_*` |

---

## 리뷰 결과 표 (출력 형식)

**위반이 있을 때** — 행을 추가한다:

| 심각도 | 체크 | 파일:줄 | 위반 내용 | 계약 |
|--------|------|---------|-----------|------|
| Critical | import 방향 | `src/entity/foo.py:12` | `from control import …` | entity→* 금지 |
| Critical | MagicConstant SSOT | `tests/control/test_d_x.py:8` | 리터럴 `34` 사용 | SSOT만 허용 |
| Warning | Logic Domain Mock | `tests/entity/test_d_y.py:15` | `@patch("entity.Grid")` | Logic Mock 금지 |

**위반이 없을 때:**

| 심각도 | 체크 | 파일:줄 | 위반 내용 | 계약 |
|--------|------|---------|-----------|------|
| — | — | — | **위반 없음** (검사 범위: …) | — |

---

## 보고 (리뷰 종료 시)

| 항목 | 내용 |
|------|------|
| 범위 | 검사한 경로·커밋 |
| Critical | 건수 + 한 줄 요약 |
| Warning | 건수 + 한 줄 요약 |
| 판정 | **PASS** (Critical 0) / **FAIL** (Critical ≥1) |
| 변경 파일 | **없음** (리뷰만) |

---

## 금지

- **`src/`, `tests/` 코드 수정**
- 위반 “자동 수정” 제안을 코드 diff로 실행
- git commit/push (사용자 명시 요청 시만)
- pytest 실행은 **선택** — 본 command는 **정적 ECB·계약** 리뷰가 주 목적

---

## 참고 (E001~E005 — entity 금지 확인용)

| 코드 | 의미 | entity에서 금지되는 것 |
|------|------|------------------------|
| E001 | 격자 크기 ≠ 4×4 | 크기 검증·E001 반환 |
| E002 | 빈칸 ≠ 2 | `0` 개수 검증·E002 반환 |
| E003 | 값 범위 1~16 위반 | 범위 검증·E003 반환 |
| E004 | 입력 형식/타입 오류 | 파싱·E004 반환 |
| E005 | 중복·전제 위반 | E005 매핑 |

→ 위 검증·오류 코드는 **boundary**에서만.
