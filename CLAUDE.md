# CLAUDE.md — Code Review & Refactoring Agent

## 프로젝트
`src/mini_inventory/inventory.py`는 일부러 지저분하게 짠 재고관리 CLI다.
목표: 이 코드를 아래 품질 기준을 100% 만족하도록 리팩토링하되, **CLI 동작(usage 텍스트 제외)은 기존과 동일하게 유지**한다 (동작 변경은 리팩토링이 아니라 새 기능이므로 별도 승인 없이 하지 말 것).

## 품질 기준 (Definition of Done — 전부 정량적으로 측정 가능해야 함)
1. `ruff check src/ tests/` → 오류 0개
2. `mypy --strict src/` → 오류 0개 (모든 public 함수/메서드에 타입힌트 필수)
3. `pytest --cov=src --cov-report=term-missing` → **라인 커버리지 85% 이상**
4. 모든 public 함수/클래스에 docstring 필수 (한 줄 요약 + 필요 시 Args/Returns)
5. **I/O와 로직 분리**: `print()`/`input()`은 CLI 엔트리포인트(`main`, `cli` 모듈)에만 존재해야 하고, 비즈니스 로직 함수(재고 추가/제거/합계 계산 등)는 값을 **반환**해야 한다 (그래야 print 없이 단위테스트 가능)
6. 함수 하나당 최대 30줄 (SRP 위반 시 분리)
7. 매직 넘버 금지 — 예: 재고 부족 기준값(5)은 이름 있는 상수로 뺄 것
8. 전역 mutable state(`data = {}`) 금지 — 상태는 클래스나 함수 인자로 명시적으로 전달

## 리팩토링 규칙
- **기능 동작은 그대로**: `add`, `remove`, `total`, `low`, `list` 커맨드의 입출력 결과(텍스트 포맷 포함)는 리팩토링 전후로 동일해야 한다. 기존 동작을 테스트로 먼저 고정(characterization test)한 뒤에 구조를 바꿀 것.
- 리팩토링은 작은 단위로 커밋하듯 진행 — 한 번에 다 바꾸지 말고, 각 단계마다 테스트를 돌려서 회귀가 없는지 확인
- 새 모듈 구조 제안 예시(강제 아님, TRD에서 직접 결정): `models.py`(데이터 구조), `service.py`(비즈니스 로직), `cli.py`(I/O)

## 의존성
- Python 3.11+, 표준 라이브러리만 사용 (외부 런타임 의존성 없음)
- 개발 의존성: ruff, mypy, pytest, pytest-cov

## 완료 조건 참조
`/goal` 실행 시 이 파일의 8개 품질 기준을 전부 만족해야 완료다.
`.claude/agents/code-reviewer.md`는 읽기 전용으로 위반 사항만 찾아 보고하고, 실제 수정은 메인 에이전트(또는 별도 구현 subagent)가 수행한다.
