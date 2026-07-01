# 완료 조건 (Definition of Done)

CLAUDE.md의 8개 품질 기준을 그대로 옮긴 체크리스트. `/goal` 루프는 이 8개가 전부 체크되기 전까지 종료를 선언하지 않는다.

- [x] 1. `ruff check src/ tests/` → 오류 0개
- [x] 2. `mypy --strict src/` → 오류 0개 (모든 public 함수/메서드에 타입힌트 필수)
- [x] 3. `pytest --cov=src --cov-report=term-missing` → 라인 커버리지 85% 이상 (실측 97%)
- [x] 4. 모든 public 함수/클래스에 docstring 필수 (한 줄 요약 + 필요 시 Args/Returns)
- [x] 5. I/O와 로직 분리: `print()`/`input()`은 CLI 엔트리포인트(`main`, `cli` 모듈)에만 존재, 비즈니스 로직 함수는 값을 반환
- [x] 6. 함수 하나당 최대 30줄 (SRP 위반 시 분리)
- [x] 7. 매직 넘버 금지 — 이름 있는 상수로 추출
- [x] 8. 전역 mutable state(`data = {}`) 금지 — 상태는 클래스나 함수 인자로 명시적으로 전달

**8/8 완료 (2026-07-02, code-reviewer 독립 재검증 통과).**

## 부가 제약 (CLAUDE.md 리팩토링 규칙)

- CLI 동작(usage 텍스트 제외)은 리팩토링 전후 동일해야 한다 — `add`/`remove`/`total`/`low`/`list` 커맨드의 입출력 결과(텍스트 포맷 포함) 동일.
- 구조 변경 전에 characterization test로 기존 동작을 먼저 고정한다.
- 작은 단위로 리팩토링하고 매 단계마다 테스트로 회귀 여부를 확인한다.

## 진행 기록

| 회차 | 시각/트리거 | BLOCKER 수 | 통과 기준 수 | 비고 |
|---|---|---|---|---|
| 1차 진단 | 이전 대화 (code-reviewer 2회 실행, 결과 일치) | 8개 이슈 그룹 (사실상 8/8 기준 FAIL) | 0/8 | ruff 1건, mypy 5건, coverage 12%, docstring 없음, I/O 미분리, 함수 37줄, 매직넘버, 전역상태 |
| 리팩토링 1회차 (refactorer) | /goal 루프 iteration 1 | — | self-report 8/8 | models.py/service.py/cli.py 분리, characterization test 작성, `src/__init__.py` 삭제(mypy 충돌 해소) |
| 재검증 1회차 (code-reviewer, 독립 실행) | /goal 루프 iteration 1 검증 | 1개 (기준 8) | 7/8 | 기준 8 FAIL: `cli.py:13` 모듈-레벨 `_service` 싱글턴 + 테스트 전용 `reset_service()` 백도어. 나머지 1~7은 self-report와 일치(ruff 0, mypy 0, coverage 97%, docstring 전수, I/O 분리, 함수 30줄 이내, 매직넘버 상수화). CLI 동작 보존도 수동 검증 완료. MINOR: `tests/test_inventory.py` 잔여 파일 정리 필요 |
| 리팩토링 2회차 (refactorer) | /goal 루프 iteration 2 | — | self-report 8/8 | `cli.py`의 모듈-레벨 `_service`/`reset_service()` 제거, `main(service: InventoryService \| None = None)`이 로컬 인스턴스를 생성해 `dispatch(service, cmd, args)`로 명시적 전달. 테스트는 per-test fixture로 전환 |
| 재검증 2회차 (code-reviewer, 독립 실행) | /goal 루프 iteration 2 검증 (최종) | 0개 | **8/8** | 전 기준 실측 재확인(ruff 0, mypy 0, coverage 97%, 26 passed). `global`/`_service`/`reset_service` grep 결과 없음. CLI 동작(add 누적, remove 부족 오류, low `<5` 경계, list/total 포맷, unknown command, usage) 수동 검증 완료 — 원본과 일치. 루프 종료 (BLOCKER 0개, 3회차 불필요) |
