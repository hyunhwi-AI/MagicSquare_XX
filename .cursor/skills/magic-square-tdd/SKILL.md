---
name: magic-square-tdd
description: MagicSquare_XX Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. MagicSquare, 마방진, ECB, Dual-Track, test_d_, test_u_, RED/GREEN/REFACTOR, SquareValidator, entity/control/boundary 구현·테스트 요청 시 적용.
---

# MagicSquare Dual-Track TDD

근거: `.cursorrules`, `docs/PRD.md`, `Report/01.*`, `Report/02.*`.  
테스트 ID 목록: [reference.md](reference.md)

## 언제 이 Skill을 켜는지

다음 **하나 이상**이면 본 Skill을 따른다.

- MagicSquare / MagicSquare_XX **기능·테스트·리팩터** 요청
- `entity` / `control` / `boundary` 레이어 코드 작성
- `test_d_*` / `test_u_*` / `D-*` / `U-*` 테스트 추가
- TDD, RED, GREEN, REFACTOR, Dual-Track, ECB 언급
- `SquareValidator`, `MagicConstant`, `validate()`, Solver 관련 구현

**Skill을 끄는 경우:** README·Report 문서만 수정, git push만, Harness 구조 변경 없는 일반 질문.

---

## 작업 선언 (매 사이클 필수)

```
Phase: RED|GREEN|REFACTOR | Layer: entity|control|boundary | Track: Logic|UI — {테스트 ID} {한 줄 목표}
```

---

## RED (5~7단계)

1. **범위 고정** — PRD·Report에서 요구 1건 + 테스트 ID(`D-*`/`U-*`) 확정.
2. **레이어·트랙 결정** — Logic(entity/control) vs UI(boundary). Mock 규칙 확인(아래 표).
3. **선언** — Phase/Layer/Track 한 줄 출력.
4. **테스트 파일** — `tests/{layer}/test_d_*.py` 또는 `test_u_*.py`에 **실패할 assert**만 작성. 구현 코드는 아직 없거나 stub.
5. **금지 확인** — skip, xfail, assert 완화, `34`/`16` 리터럴 직접 사용 없음(`MagicConstant`만).
6. **실행** — 대상 파일만 pytest → **반드시 FAIL** 확인.
7. **RED 보고** — 실패 메시지·대상 ID·다음 GREEN 범위를 3줄 이내로 기록.

---

## GREEN (5~7단계)

1. **선언** — 동일 테스트 ID로 GREEN 시작.
2. **최소 구현** — 해당 테스트를 통과하는 **가장 작은** 코드만 추가. 다른 레이어 침범 금지.
3. **ECB 준수** — entity는 E001~E005 처리·import 금지. boundary→control→entity 방향만.
4. **MagicConstant** — 합·크기 상수는 SSOT에서만 참조.
5. **실행** — 신규 테스트 파일 → 해당 레이어 디렉터리 순으로 pytest.
6. **전체 Logic smoke** — `pytest tests/entity tests/control -q` (UI 미포함) Green 확인.
7. **GREEN 보고** — 통과한 ID, 변경 파일 목록, 남은 RED 후보.

---

## REFACTOR (5~7단계)

1. **선언** — REFACTOR + 동일 Layer/Track.
2. **Green 유지** — 리팩터 전 현재 테스트 전부 Green 상태 확인.
3. **범위 제한** — 동작 변경 없음. 이름·중복·구조만 정리.
4. **금지** — assert 변경, 테스트 삭제, skip/xfail, 요구 없는 public API 추가.
5. **실행** — `pytest tests/entity tests/control tests/boundary -q` (또는 이번 스프린트 범위).
6. **ECB 재검** — entity→* import, 역방향 호출, Logic Track Mock 유입 없음.
7. **REFACTOR 보고** — 정리 내용 + 회귀 없음 확인.

---

## Logic Track vs UI Track

| 항목 | Logic Track | UI Track |
|------|-------------|----------|
| **대상** | `entity`, `control` | `boundary` |
| **테스트 ID** | `D-*` | `U-*` |
| **파일명** | `test_d_*.py` | `test_u_*.py` |
| **경로** | `tests/entity/`, `tests/control/` | `tests/boundary/` |
| **Domain Mock** | **금지** | — |
| **control/IO Mock** | **금지** | **허용** |
| **검증 초점** | 도메인 규칙·유스케이스 | 입출력·E코드·포맷 |
| **RED pytest** | `pytest tests/{entity\|control}/test_d_xxx.py` | `pytest tests/boundary/test_u_xxx.py` |

---

## ECB · Mock · E001~E007

### ECB 의존

```
boundary → control → entity
```

| 규칙 | entity | control | boundary |
|------|--------|---------|----------|
| 상위 레이어 import | **금지** | entity만 | control·entity |
| E001~E005 처리 | **금지** | **금지** | **허용·전담** |
| E006~E007 | 도메인 규칙만 | 조율·전달 | 노출·변환 |
| `validate()` / CLI | — | Command | Boundary adapter |

### E001~E007 (boundary 전담 vs entity)

| 코드 | boundary | entity/control |
|------|----------|----------------|
| E001 | 격자 크기 ≠ 4×4 | **처리 금지** |
| E002 | 빈칸(`0`) 개수 ≠ 2 | **처리 금지** |
| E003 | 값 범위 위반 (1~16) | **처리 금지** |
| E004 | 입력 형식/타입 오류 | **처리 금지** |
| E005 | 중복·전제 위반 | **처리 금지** |
| E006 | 해 없음 (Solver) | 도메인 결과 |
| E007 | 해 비유일 (Solver) | 도메인 결과 |

### Mock

| Mock 대상 | Logic | UI |
|-----------|-------|-----|
| Entity/도메인 객체 | **금지** | — |
| Control 유스케이스 | **금지** | **허용** |
| stdin/stdout/파일 IO | **금지** | **허용** |

---

## Test / Review Loop

| 시점 | 명령 | 기대 |
|------|------|------|
| RED 직후 | `pytest tests/{layer}/test_d_xxx.py -v` (또는 `test_u_xxx.py`) | **FAIL** |
| GREEN 중 | 동일 파일 `-v` | **PASS** |
| GREEN 완료 | `pytest tests/entity tests/control -q` | 전부 PASS |
| boundary 작업 후 | `pytest tests/boundary -q` | 전부 PASS |
| REFACTOR / Review | `pytest tests/ -q` | 전부 PASS |
| 회귀 방지 (M1) | S1~S3 해당 `D-*` 포함 Logic 전체 | PASS 유지 |

**Review Loop (사이클 종료 시):**

1. 이번 ID 테스트 단독 PASS  
2. 해당 Track 디렉터리 PASS  
3. Logic 전체 PASS (UI 변경 없으면 boundary 생략 가능)  
4. `.cursorrules` 위반 없음(리터럴 34/16, entity import, skip/xfail)  
5. 완료 보고 작성

---

## 완료 보고 항목

사이클·기능 단위로 아래를 **한국어**로 보고한다.

1. **선언 요약** — Phase / Layer / Track / 테스트 ID  
2. **RED** — 실패했던 assert·메시지 (해당 시)  
3. **변경 파일** — `src/…`, `tests/…` 목록  
4. **pytest 결과** — 실행한 명령 + pass/fail 건수  
5. **ECB·Mock·E코드** — 위반 없음 / 해당 없음  
6. **MagicConstant** — SSOT 사용 여부  
7. **다음 RED** — 후속 테스트 ID 1~2개 (있으면)

---

## 금지 (항상)

- assert 완화, `@pytest.mark.skip`, `xfail`, 실패 테스트 삭제로 Green
- Logic Track에서 Domain·Control Mock
- entity에서 E001~E005 catch/매핑/메시지
- entity → control/boundary/* import
- 코드·테스트에 `34`, `16` 리터럴 산재 (`MagicConstant` SSOT만)
- git commit/push — **사용자 명시 요청 시만**

---

## 추가 자료

- D-* 테스트 ID: [reference.md](reference.md)
