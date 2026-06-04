# TDD RED — 실패 테스트 먼저

**MagicSquare_XX Dual-Track TDD — RED 단계만.**  
구현(`src/`)은 GREEN까지 건드리지 않는다. 근거: `.cursorrules`, `docs/PRD.md`.

---

## 필수 선언

작업 **첫 줄**에 반드시 출력:

```text
Phase: RED | Layer: entity|control|boundary | Track: Logic|UI — {D-* 또는 U-*} {한 줄 목표}
```

예:

```text
Phase: RED | Layer: entity | Track: Logic — D-02 빈칸 0 정확히 2개
```

---

## 절차

1. **ID 확인** — `D-*`(Logic) 또는 `U-*`(UI)를 확정. 목록은 `.cursor/skills/magic-square-tdd/reference.md` 참고.
2. **레이어·파일** — Logic: `tests/entity/test_d_*.py` 또는 `tests/control/test_d_*.py` / UI: `tests/boundary/test_u_*.py`
3. **AAA 테스트 작성** — Arrange(격자·fixture) → Act(호출) → Assert(요구사항 그대로). **아직 없는 API를 호출해도 됨** (ImportError/FAIL 기대).
4. **금지 점검** — skip, xfail, assert 완화, `34`/`16` 리터럴, Logic Track Domain Mock 없음.
5. **pytest 실행** — 대상 파일만 실행 → **반드시 FAIL** 확인.
6. **RED 불가 시** — 이미 PASS면 테스트가 잘못됐거나 구현이 선행됨. assert 강화 또는 범위 재확인. **src/ 수정으로 Green 만들지 말 것.**

---

## pytest 예시 (bash)

```bash
# Logic — entity
pytest tests/entity/test_d_magic_constant.py -v

# Logic — control
pytest tests/control/test_d_validate_s1.py -v

# UI — boundary
pytest tests/boundary/test_u_invalid_grid_e001.py -v

# RED 직후 기대: FAILED (exit code 1). no tests / PASS 는 RED 미완료.
```

---

## 보고

RED 완료 시 **한국어**로 아래만 보고:

| 항목 | 내용 |
|------|------|
| 테스트 ID | `D-*` 또는 `U-*` |
| FAIL 요약 | 실패 유형·assert 메시지 1~2줄 |
| 변경 파일 | **`tests/` 아래만** (경로 목록) |

---

## 금지

- **`src/` 수정** — RED에서는 테스트만 추가·수정
- **Logic Track Domain Mock** — entity/control 실 객체·실 규칙만
- **assert 완화** — 요구를 느슨하게 바꿔 PASS 만들기
- `@pytest.mark.skip`, `xfail`, 실패 테스트 삭제
- git commit/push (사용자 명시 요청 시만)

---

**다음 단계:** GREEN은 `/tdd-green` 또는 사용자 지시 후 `src/` 최소 구현.
