# TRD — Code Review & Refactoring Agent

> PRD를 먼저 채우고 오세요. `[TODO]`를 직접 채우세요.

## 1. 목표 모듈 구조 (제안, 확정은 직접)
```
src/mini_inventory/
├── __init__.py
├── models.py    # 재고 항목 데이터 구조 (dataclass 등)
├── service.py   # 비즈니스 로직 (add/remove/total/low) - print 없음, 값만 반환
└── cli.py       # argv 파싱 + print만 담당
```
[TODO] `inventory.py`를 그대로 두고 내부만 리팩토링할지, 위처럼 파일을 쪼갤지 결정. 쪼갠다면 `main()`의 진입점이 바뀌므로 CLAUDE.md의 "동작 동일 유지"와 어떻게 양립시킬지도 적기.

## 2. 함수 시그니처 (초안 — 직접 다듬기)
```python
[TODO] 예: def add_item(inventory: dict[str, Item], name: str, qty: int, price: float) -> dict[str, Item]: ...
[TODO] 전역 상태를 없앤다면 이 함수들이 상태를 어떻게 주고받을지 (인자로 전달? 클래스 메서드?)
```

## 3. Characterization test 전략
- [TODO] 리팩토링 전 `inventory.py`의 현재 출력을 어떻게 캡처할지 (예: `subprocess`로 실제 CLI를 실행해서 stdout을 캡처하고 스냅샷으로 저장)
- [TODO] 이 테스트가 CLAUDE.md 5번 기준(I/O 분리)과 상충되지 않는지 — I/O를 분리한 후에도 CLI 레벨 통합테스트는 여전히 필요함을 인지

## 4. Subagent 오케스트레이션 순서
- [TODO] `.claude/commands/goal.md`에 이미 초안이 있음. 이 순서(진단→수정→재진단, 최대 5회)가 실제로 합리적인지, 아니면 이슈를 심각도별로 나눠서 BLOCKER부터 순차 처리하는 게 나을지 검토하고 필요하면 goal.md 자체를 수정

## 5. 테스트 전략
- 단위 테스트: `service.py`의 각 함수 (전역상태 없이 순수함수로 테스트 가능해야 함 — 이게 리팩토링이 잘 됐는지의 증거)
- 통합 테스트: CLI 전체 실행 후 stdout 검증 (characterization test)
- [TODO] pytest-cov 85% 기준을 어떤 파일들에 적용할지 (cli.py의 argv 파싱 분기까지 다 커버해야 하는지)

## 6. 의존성 / 실행 환경
- Python 3.11+, ruff, mypy, pytest, pytest-cov (dev only)
- [TODO] pyproject.toml에 ruff/mypy 설정 (strict 레벨 등) 명시
