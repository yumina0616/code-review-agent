# Code Review & Refactoring Agent

Claude Code의 `/goal` 기반 자기수정 워크플로우와 Multi-Agent 오케스트레이션(code-reviewer ↔ refactorer)을 실습하기 위한 토이 프로젝트입니다.

일부러 품질이 낮게 짠 재고관리 CLI(`src/mini_inventory/inventory.py`)를, 두 개의 독립된 subagent가 진단→수정→재검증 루프를 돌며 `CLAUDE.md`에 정의된 8개 품질 기준을 100% 만족할 때까지 자동으로 리팩토링합니다.

## 결과

`/goal` 실행 후 **8/8 품질 기준 통과** (2026-07-02, code-reviewer 독립 재검증 완료). 상세 이력은 [`docs/DONE_CRITERIA.md`](docs/DONE_CRITERIA.md) 참고.

| 기준 | 상태 |
|---|---|
| ruff check 오류 0개 | ✅ |
| mypy --strict 오류 0개 | ✅ |
| pytest 커버리지 85%+ | ✅ (실측 97%) |
| 모든 public 함수 docstring | ✅ |
| I/O와 로직 분리 | ✅ |
| 함수당 최대 30줄 | ✅ |
| 매직 넘버 금지 | ✅ |
| 전역 mutable state 금지 | ✅ |

## 프로젝트 구조

```
code-review-agent/
├── CLAUDE.md                  # 프로젝트 컨텍스트: 용어, 품질 기준(8개), 리팩토링 규칙
├── docs/
│   ├── PRD.md                 # 제품 요구사항 (Spec Driven Development)
│   ├── TRD.md                 # 기술 요구사항
│   └── DONE_CRITERIA.md       # /goal 실행 시 자동 생성되는 완료 조건 + 진행 이력
├── .claude/
│   ├── settings.json          # hooks: 코드 수정 시 자동 ruff/mypy/pytest, 품질기준 미달 시 세션 종료 차단
│   ├── commands/goal.md       # /goal 커스텀 슬래시 커맨드 (완료조건 명시화 + 자기수정 루프)
│   └── agents/
│       ├── code-reviewer.md   # 읽기 전용 리뷰어 subagent (Read/Grep/Glob/Bash만 허용)
│       └── refactorer.md      # 실제 수정 담당 subagent
├── src/mini_inventory/        # 리팩토링 대상 소스
├── tests/                     # 단위 테스트 + characterization test
├── pyproject.toml             # ruff/mypy/pytest 설정
└── requirements-dev.txt
```

## 요구사항

- Python 3.11+
- [Claude Code](https://code.claude.com) (Pro 이상 요금제)

## 설치

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

## 사용법

```bash
claude
```

세션 안에서:

```
/agents              # code-reviewer, refactorer가 Library 탭에 등록됐는지 확인
/goal                # 자기수정 루프 실행 — 8개 기준 전부 통과할 때까지 반복 (최대 5회)
```

품질 기준을 직접 확인하고 싶다면:

```bash
ruff check src/ tests/
mypy --strict src/
pytest --cov=src --cov-report=term-missing
```

## 설계 노트

- **역할 분리**: `code-reviewer`는 `Write`/`Edit` 권한이 아예 없어서, 진단만 하고 절대 코드를 수정할 수 없습니다 (프롬프트가 아니라 도구 권한 레벨에서 강제됨).
- **재사용성**: 두 subagent 정의는 이 프로젝트의 파일명이나 경로를 하드코딩하지 않습니다. `CLAUDE.md`만 다른 프로젝트 것으로 교체하면 동일한 subagent를 재사용할 수 있도록 설계했습니다.
- **하드 게이트 vs 소프트 가이드**: `CLAUDE.md`의 품질 기준은 지침(무시될 수 있음)이지만, `.claude/settings.json`의 Stop 훅이 `pytest --cov-fail-under=85` 등을 강제로 재검사해서 실제 완료 여부를 물리적으로 검증합니다.

## 라이선스

학습 목적의 예제 프로젝트입니다.