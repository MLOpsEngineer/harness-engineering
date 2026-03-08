# Improving Deep Agents with harness engineering

- 구분: 블로그/아티클
- 발행일: 2026-02-17
- 저자: LangChain
- 출처: LangChain
- 원문: https://blog.langchain.com/improving-deep-agents-with-harness-engineering/
- 관련성: 직접

## 한줄 요약
같은 모델(GPT-5.2-codex)을 유지한 채 harness만 바꿔 Terminal Bench 2.0 점수를 `52.8 → 66.5`로 끌어올린, 현재 가장 실증적인 harness engineering 사례다.

## 왜 중요한가
'모델보다 harness가 더 큰 성능 레버'라는 주장을 정량 데이터로 뒷받침한 최초의 공개 사례 중 하나다. harness engineering이 추상 개념이 아니라 measurable optimization space임을 증명한다.

## 원문 기준 핵심 흐름

### 실험 설계
- `deepagents-cli`는 GPT-5.2-codex 모델을 고정한 채, system prompt, tool behavior, middleware, trace analysis loop를 함께 변경해 Terminal Bench 2.0 점수를 개선했다.
- 개선은 prompt 한 줄 수정이 아니라 여러 harness 레이어를 동시에 다루는 compound change다.
- 핵심 점수 변화: `52.8 → 66.5` (`+13.7점`, `+26%` 상대 개선).

### 3가지 핵심 middleware
1. **PreCompletionChecklist**: agent가 작업 완료를 선언하기 전에 체크리스트를 강제한다. `테스트가 통과하는가`, `변경한 파일을 모두 저장했는가`, `불필요한 디버그 코드를 제거했는가` 등을 확인한다. 이 middleware 하나만으로 premature completion 실패를 상당히 줄였다고 보고한다.
2. **LocalContext**: agent가 현재 작업 중인 파일과 디렉토리의 context를 자동으로 수집해 매 턴마다 context window에 주입한다. agent가 `어디에 있는지`를 잊는 문제를 해결한다.
3. **LoopDetection**: agent가 같은 패턴의 행동을 반복하면(예: 같은 에러를 반복적으로 생성) 이를 감지하고 개입한다. 무한 루프와 resource 낭비를 방지하는 circuit breaker 역할이다.

### Reasoning Sandwich 전략
- system prompt 구조를 `instruction → examples → constraints → reasoning nudge` 순서로 배치하는 패턴이다.
- 핵심 아이디어: agent에게 행동을 지시하기 전에 먼저 `현재 상황을 분석하라`는 reasoning step을 끼워 넣는다.
- 이렇게 하면 agent가 반사적으로 행동하지 않고, 현재 context를 해석한 뒤에 행동을 결정한다.

### Trace-based 개선 루프
- LangSmith trace를 대규모로 분석해 실패 패턴을 찾는다. 이를 `Agent Skill` 형태의 **trace analyzer**로 자동화했다.
- trace analyzer는 실패 trace에서 공통 패턴을 추출하고, 이를 middleware나 prompt 수정으로 변환할 수 있는 개선 후보를 생성한다.
- 이 접근은 `trace를 단순 로그가 아니라 optimization signal로 본다`는 관점에서 출발한다. 관측 인프라가 곧 개선 인프라가 된다.
- 개선 루프: `trace 수집 → 실패 패턴 분류 → 개선 후보 생성 → harness 수정 → 재실행 → 재측정`.

### Self-verification 패턴
- agent가 자신의 출력을 스스로 검증하는 단계를 harness가 강제한다.
- 단순히 "확인하라"는 prompt가 아니라, middleware 수준에서 verification step을 삽입해 agent가 이를 건너뛸 수 없게 한다.
- self-verification, tracing, error-focused iteration이 harness 개선의 핵심 3대 레버로 제시된다.

## Harness Engineering 관점
- 이 글은 harness engineering을 **measurable optimization space**로 확립한 핵심 사례다. `+13.7점`이라는 숫자가 harness 변경의 가치를 직접 증명한다.
- system prompt, tool, middleware를 `knobs`로 보고 실험하는 태도가 이후 실무 패턴의 표준에 가깝다.
- trace-based 개선 루프는 harness engineering을 one-shot 설계가 아니라 **continuous optimization**으로 만드는 핵심 메커니즘이다.
- middleware 패턴(PreCompletionChecklist, LocalContext, LoopDetection)은 다른 agent 시스템에도 바로 적용 가능한 구체적 레시피다.
- Fowler가 말하는 `agentic flywheel` — trace에서 배우고, harness를 고치고, 다시 측정하는 — 의 가장 구체적인 구현 사례다.

## 한계와 주의점
- Terminal Bench라는 특정 benchmark에 최적화된 결과라 일반화에는 주의가 필요하다.
- LangChain의 관측 인프라(LangSmith)에 강하게 의존하는 사례라, 이 인프라가 없는 환경에서 동일한 개선 루프를 만들기는 어려울 수 있다.
- middleware 세 가지가 각각 얼마나 기여했는지 개별 ablation 결과는 공개되지 않았다.
- deepagents-cli는 LangChain 팀의 자체 시스템이므로, 제3자 독립 검증은 아직 이루어지지 않았다.
