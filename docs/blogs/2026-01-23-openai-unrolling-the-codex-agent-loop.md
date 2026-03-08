# Unrolling the Codex agent loop

- 구분: 블로그/아티클
- 발행일: 2026-01-23
- 저자: OpenAI Engineering
- 출처: OpenAI
- 원문: https://openai.com/index/unrolling-the-codex-agent-loop/
- 관련성: 기반

## 한줄 요약
Codex의 agent loop를 해부하면서, 사용자 입력부터 prompt assembly, model inference, tool invocation, observation formatting, termination까지 이어지는 전체 루프가 agent 성능의 핵심임을 설명한 글이다.

## 왜 중요한가
OpenAI가 harness를 단순 래퍼가 아니라 **제품 공통 런타임**으로 본다는 점을 드러내는 출발점이다. 후속 글(Unlocking the Codex Harness, Harness Engineering)의 기반이 된다.

## 원문 기준 핵심 흐름

### Agent Loop의 구성 요소
- Codex의 핵심이 단일 model call이 아니라, 여러 단계가 반복되는 **loop**라는 점을 강조한다.
- loop의 각 단계:
  1. **Input Collection**: 사용자 요청, 대화 히스토리, 시스템 설정을 수집
  2. **Prompt Assembly**: 수집된 입력을 모델이 처리할 수 있는 형태로 조립. system prompt, tool definitions, conversation history, current task context를 결합
  3. **Model Inference**: 조립된 prompt를 모델에 전달해 다음 행동을 결정
  4. **Tool Invocation**: 모델이 선택한 tool을 실행. 파일 읽기/쓰기, 터미널 명령, 검색 등
  5. **Observation Formatting**: tool 실행 결과를 모델이 이해할 수 있는 형태로 가공
  6. **Termination Check**: 작업이 완료되었는지, 계속 반복해야 하는지 판단

### 공통 Runtime Semantics
- 웹 앱, CLI, IDE extension 등 surface마다 달라 보이지만, 아래쪽에는 **공통 runtime semantics**가 존재한다.
- 이 공통 semantics가 바로 harness다. 어떤 surface에서 호출하든 동일한 loop logic, tool dispatch, observation formatting이 적용된다.
- loop 전체가 하나의 시스템이므로, 한 단계의 변경이 다른 모든 단계에 영향을 준다. prompt assembly를 바꾸면 tool 선택이 달라지고, observation formatting을 바꾸면 다음 턴의 reasoning이 달라진다.

### Model Quality vs Loop Quality
- 모델 quality만큼 중요한 것이 **prompt assembly, tool exposure, observation formatting, termination condition**이다.
- agent quality는 model 자체가 아니라 **loop 전체의 설계 결과**라는 것이 글의 중심 주장.
- 예시: 같은 모델이라도 tool description을 바꾸면 tool 선택 패턴이 변하고, observation을 요약하면 context가 깔끔해져 이후 추론이 좋아진다.
- 이 관점은 이후 LangChain의 Terminal Bench 실험(같은 모델, 다른 harness, +13.7점)과 정확히 일치한다.

### Termination의 중요성
- loop가 언제 끝나는지를 결정하는 **termination condition**이 과소평가되고 있다고 지적한다.
- premature termination: 작업이 완료되지 않았는데 agent가 멈추는 문제. harness가 completion criteria를 명시하지 않으면 자주 발생한다.
- infinite loop: agent가 같은 행동을 반복하면서 멈추지 않는 문제. loop detection과 budget enforcement가 필요하다.
- 좋은 harness는 이 두 극단 사이에서 **적절한 종료 시점**을 판단할 수 있어야 한다.

## Harness Engineering 관점
- 이 글은 harness engineering의 가장 낮은 수준, 즉 **runtime semantics**를 다룬다.
- loop의 각 단계(prompt assembly, tool dispatch, observation formatting, termination)가 모두 harness 설계의 대상임을 보여준다.
- 후속 OpenAI 글들이 조직 운영(harness engineering)과 인프라(Unlocking the Codex Harness)로 확장되기 전에, agent loop 자체가 왜 중요한지 기반을 제공한다.
- LangChain의 middleware 패턴(PreCompletionChecklist, LoopDetection)은 이 글이 제시한 termination 문제의 구체적 해결책으로 읽을 수 있다.

## 한계와 주의점
- 조직 프로세스나 repo 관리 같은 상위 문제는 거의 다루지 않는다. runtime loop에 집중한다.
- 구현 철학 소개 비중이 높고, 실험 수치나 정량 비교는 제한적이다.
- Codex 특화 사례이므로 다른 agent 시스템의 loop와 직접 비교하기는 어렵다.
