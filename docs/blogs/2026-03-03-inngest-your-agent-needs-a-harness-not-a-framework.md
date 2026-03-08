# Your Agent Needs a Harness, Not a Framework

- 구분: 블로그/아티클
- 발행일: 2026-03-03
- 저자: Dan Farrelly
- 출처: Inngest
- 원문: https://www.inngest.com/blog/your-agent-needs-a-harness-not-a-framework
- 관련성: 직접

## 한줄 요약
agent harness를 프레임워크 API가 아니라 이벤트 라우팅, durable execution, step-level retry, concurrency control, tracing을 제공하는 인프라 계층으로 재정의한 글이다.

## 왜 중요한가
harness engineering을 프롬프트나 에이전트 루프 내부가 아니라, 그 바깥에서 실패를 흡수하고 실행을 지속시키는 런타임 설계 문제로 해석한다.

## 원문 구조
- 왜 framework가 아니라 harness인가
- Utah 예제 소개
- Inngest 위에서 agent loop를 올리는 법
- tool wiring과 sub-agent invocation
- context compaction과 conversational state 관리
- concurrency, retries, tracing, steering 이슈

## 1. 원문에서 먼저 세우는 문제의식
- 글은 wiring harness, test harness, safety harness를 공통 비유로 사용하며, harness의 본질을 "일을 직접 수행하지 않지만 연결하고 보호하고 오케스트레이션하는 층"으로 잡는다.
- 이 관점에서 LLM은 엔진, tools는 주변장치, memory는 저장소다. 실제 운영 난제는 모델 정확도 자체보다 실패한 호출을 어떻게 복구하고, 어떤 이벤트를 어떤 핸들러로 보낼지, 동시에 들어온 메시지를 어떻게 직렬화할지에 있다고 본다.
- 그래서 agent framework가 저마다 retry, persistence, queue, event routing을 다시 구현하는 현실을 비판하고, 이미 존재하는 durable event infrastructure를 harness로 쓰는 편이 더 낫다고 주장한다.

## 2. Utah 예제로 보여주는 전체 구조
- 글의 레퍼런스 구현인 Utah는 "Universally Triggered Agent Harness"로, Telegram/Slack 같은 대화형 채널, cron, sub-agent invocation, 함수 간 이벤트를 하나의 event fabric 위에 올린다.
- 전체 흐름은 `webhook -> Inngest Cloud transform -> typed event -> local worker -> agent loop -> reply event -> channel-specific reply function` 구조다. 이 구조 덕분에 public ingress와 local execution을 느슨하게 연결할 수 있다.
- worker는 `connect()` 기반의 persistent WebSocket으로 Inngest Cloud와 연결되고, 에이전트 루프는 worker 내부에서 단순한 `think -> act -> observe` while-loop로 구현된다.
- 중요한 구분은 루프 본체와 오케스트레이션 레이어를 떼어낸다는 점이다. 루프는 LLM 호출과 tool 실행만 담당하고, 트리거 전달, 상태 지속, 재시도, 스케줄링, trace 수집은 harness가 맡는다.

## 3. 원문이 직접 보여주는 구현 메커니즘
- 모든 LLM 호출과 tool 호출은 각각 독립적인 `step.run(...)` 단위가 된다. 같은 이름의 step이 반복 호출되면 SDK가 내부적으로 인덱싱하므로 루프 코드가 상대적으로 단순하다.
- iteration 3에서 LLM API가 500을 내면 그 step만 재시도되고, iteration 1~2 결과는 persisted state로 남아 재실행되지 않는다. 글이 말하는 durable execution의 핵심이 바로 여기에 있다.
- 툴링은 직접 재구현하지 않고 `pi-coding-agent`의 `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls`를 가져오고, 여기에 `remember`, `web_fetch`, `delegate_task`만 추가한다.
- Utah는 하나의 거대한 함수가 아니라 `handleMessage`, `sendReply`, `acknowledgeMessage`, `failureHandler`, `heartbeat`, `subAgent` 같은 분리된 함수들로 구성된다. 각 함수는 별도의 retry 정책, concurrency 설정, trigger 조건을 가진다.
- `delegate_task`는 `step.invoke()`로 별도 sub-agent run을 띄운다. 부모 에이전트는 하위 실행 결과만 tool result처럼 받지만, 하위 실행은 별도 context window, 별도 retries, 별도 traces를 가진다.
- 대화형 채널의 race condition은 `singleton` 설정으로 처리한다. 동일 세션에 새 메시지가 들어오면 기존 run을 취소하고 최신 메시지를 포함한 새 run으로 다시 시작하는 식이다.

## 4. 원문이 길게 다루는 컨텍스트 관리
- 글에서 가장 노골적으로 인정하는 어려움은 모델 호출 그 자체보다 context management다.
- 장문 tool result가 누적되면 agent가 끝없이 tool call을 반복하거나 방향을 잃기 쉬우므로, within-run pruning과 across-run compaction을 분리해 적용한다.
- 오래된 tool result를 soft trim 또는 hard clear 하고, 최근 몇 턴은 보존한다. 세션 전체가 커지면 요약 기반 compaction을 수행한다.
- 남은 iteration이 적을 때 budget warning을 주고, context-too-large 오류가 나면 강제 compaction 후 같은 턴을 회복하는 overflow recovery도 둔다.
- 이 대목은 harness가 단순 실행기만이 아니라 token budget과 실패복구 정책까지 포함하는 운영 레이어임을 보여 준다.

## 5. 원문 마지막에 남겨 두는 운영 이슈
- 새 메시지가 오면 이전 run을 취소하고 다시 시작하는 정책은 UX와 steering 사이의 trade-off가 있다고 인정한다.
- 글은 human approval, streaming, multiplayer agent, memory compaction, monitoring 같은 기능을 같은 event substrate 위에서 계속 확장 가능한 항목으로 본다.
- 즉 결론은 "agent loop를 어떻게 쓸까"보다 "운영 문제를 어떤 durable substrate가 흡수하나"에 가깝다.

## Harness Engineering 관점
- 이 글은 harness engineering의 infra/runtime 면을 가장 강하게 강조한다. 모델이 더 똑똑해지는 것보다, 실패를 step 단위로 격리하고 실행 이력을 남기며 채널별 동시성을 통제하는 것이 운영 안정성에 더 중요하다는 입장이다.
- 또한 "framework를 고를 것인가"보다 "어떤 durable substrate 위에 agent loop를 올릴 것인가"를 먼저 묻는다. 이 점에서 application code 중심 논의보다 한 단계 아래의 orchestration substrate로 시야를 내린다.
- sub-agent, human approval, streaming, multiplayer orchestration 같은 기능도 동일 event system 위에서 확장 가능한 것으로 본다. 즉 harness는 매번 새 패턴을 만드는 대신 같은 실행 기반을 재활용하는 방식으로 설계된다.

## 한계와 주의점
- Inngest 제품 관점이 강하다. durable execution, event routing, tracing, singleton concurrency의 필요성은 설득력 있지만, 구현 예시는 자연스럽게 Inngest를 중심으로 전개된다.
- 코딩 에이전트 일반론보다는 event-driven conversational/runtime agent에 더 가깝다. repo legibility, documentation system, code review loop 같은 소프트웨어 팀 운영 문제는 깊게 다루지 않는다.
- `cancel on new message` 같은 steering 정책은 여전히 미해결 문제로 남겨 둔다. 즉 harness가 많은 문제를 흡수해도, mid-run steering과 streaming UX는 아직 설계 중인 영역으로 인정한다.
