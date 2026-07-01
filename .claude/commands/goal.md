---
description: "code-reviewer와 refactorer 서브에이전트를 오케스트레이션해서 CLAUDE.md의 8개 품질 기준을 모두 만족할 때까지 반복 수정"
argument-hint: [목표 설명 (생략 가능, 기본은 CLAUDE.md 전체 기준 충족)]
---

# /goal — 리뷰↔리팩토링 자기수정 루프

목표: $ARGUMENTS (비어있으면 "CLAUDE.md의 8개 품질 기준을 전부 만족시켜라"로 간주)

## 절차

1. **완료 조건 명시화**: `CLAUDE.md`의 8개 품질 기준을 그대로 체크리스트로 만들어 `docs/DONE_CRITERIA.md`에 기록하라.

2. **1차 진단**: `code-reviewer` 서브에이전트를 호출해 현재 상태를 진단하라. 결과를 저장해 둬라.

3. **자기수정 루프** (최대 5회 반복):
   a. `refactorer` 서브에이전트를 호출해 code-reviewer가 찾은 BLOCKER 이슈들을 고치게 하라.
   b. `code-reviewer` 서브에이전트를 다시 호출해 재검증하라.
   c. BLOCKER가 0개면 루프 종료. 남아있으면 (a)로 돌아가되, 이번엔 "이전 시도에서 왜 안 고쳐졌는지"를 refactorer에게 명시적으로 알려줘라.
   d. 5회를 다 돌았는데도 BLOCKER가 남으면 루프를 멈추고 사람에게 보고하라 (무한반복 금지).

4. **최종 보고**:
   - `docs/DONE_CRITERIA.md`의 8개 기준 중 몇 개 통과했는지
   - 리팩토링 전/후 characterization test 결과 (동작이 정말 안 바뀌었는지)
   - 사람이 직접 확인해야 할 부분 (예: mypy strict가 통과했다고 타입이 실제로 의미론적으로 맞는다는 뜻은 아님)

완료 조건이 전부 충족되기 전까지는 작업이 끝났다고 선언하지 마라. hooks가 자동으로 lint/test를 실행하니 그 결과도 관찰하라.
