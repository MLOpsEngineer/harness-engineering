# 01. Foundations and Boundaries

Harness engineering은 `모델 바깥에서 에이전트가 안정적으로 일하도록 만드는 설계와 운영의 묶음`이다. 그러나 수집한 31개 자료를 실제로 비교해 보면, 저자마다 `무엇을 harness라고 부르는지`의 범위가 조금씩 다르다. 이 문서는 그 차이를 분해해 `context engineering`, `scaffolding`, `framework`, `substrate`, `execution/eval/organizational harness` 사이의 경계를 실무적으로 쓸 수 있는 수준까지 정리한다.

## 핵심 주장

- harness engineering은 context engineering을 포함하지만 거기서 끝나지 않는다.
- 같은 말을 하더라도 OpenAI, Anthropic, LangChain, Inngest, Martin Fowler, 최근 논문이 각자 강조하는 층이 다르다.
- 실패 원인을 제대로 진단하려면 `입력면 문제`, `실행 문제`, `평가 문제`, `조직 운영 문제`를 구분해야 한다.

## 전체 코퍼스 종합

### 이 용어가 왜 생겼는가

- 2025년 중반 자료는 아직 `harness engineering`이라는 말을 널리 쓰지 않았지만, 이미 같은 문제를 다루고 있었다. Anthropic의 멀티에이전트 연구 시스템은 orchestration, memory persistence, tracing, evaluation을 함께 다뤘고, Manus는 context를 files, plans, artifacts, history 전체로 확장했다.
- 2025년 11월 Anthropic의 `Effective harnesses for long-running agents`는 long-running coding agent의 문제를 `세션 간 handoff 실패`로 규정하며 harness를 제목에 전면 배치했다.
- 2026년 2월 OpenAI의 `Harness engineering: leveraging Codex in an agent-first world`는 인간 역할을 `intent specification, feedback loop design, environment shaping`으로 재정의하며 용어를 대중화했다.
- Martin Fowler는 이 흐름을 받아 harness를 `context engineering + architectural constraints + garbage collection`으로 개념화했고, Inngest는 같은 문제를 `framework가 아니라 durable substrate`의 문제로 다시 설명했다.

### 자료 비교: 모두 같은 말을 하나

- OpenAI는 harness를 `repo, feedback loop, merge/review, documentation까지 포함한 operating model`로 본다.
- Anthropic은 long-running agent와 eval 문헌에서 `runtime continuity, handoff, tracing, grading` 쪽에 더 집중한다.
- LangChain은 `middleware, observability, eval-driven optimization`을 통해 harness를 `개선 가능한 system layer`로 본다.
- Inngest는 `event routing, retries, concurrency, persistence` 같은 substrate 기능을 harness의 본체로 본다.
- Fowler는 이들을 하나로 묶되, context engineering과 deterministic constraints를 분리해서 보게 만든다.

결론적으로 `harness engineering`은 단일 기능을 가리키는 좁은 용어가 아니라, agent를 둘러싼 바깥층을 어떤 수준까지 시스템화하느냐를 가리키는 umbrella term으로 읽는 것이 가장 정확하다.

### context engineering vs harness engineering

- Anthropic `Effective context engineering for AI agents`와 Manus `Context Engineering for AI Agents`는 둘 다 context를 system prompt 하나가 아니라 tool schema, memory, files, histories, retrieval 결과, intermediate artifact까지 포함한 전체 정보 표면으로 본다.
- Martin Fowler의 `Context Engineering for Coding Agents`는 이를 reusable prompts, tools, MCP servers, skills, rules, specs라는 artifact taxonomy로 정리한다.
- 여기까지는 모두 `모델 안으로 무엇을 넣을 것인가`에 집중한다. context engineering의 중심 질문은 `어떤 정보가 다음 행동을 가장 잘 유도하는가`다.
- 반면 OpenAI, Anthropic long-running harness, Inngest, VeRO, OpenDev는 여기서 더 나아가 `실행 상태를 어떻게 이어붙일지`, `실패를 어떻게 재시도할지`, `무엇을 측정할지`, `누가 승인할지`를 묻는다.

### 자료 비교: context engineering은 harness engineering의 하위 집합인가

- Anthropic과 Manus는 명시적으로 harness engineering이라는 말을 덜 쓰지만, 그들이 다루는 file-based state, compaction, tool surface는 이미 harness의 내부 레이어다.
- Fowler는 이 관계를 가장 명확히 정리한다. context engineering은 harness engineering의 일부이며, harness는 여기에 deterministic constraints와 cleanup/garbage collection을 더 얹는다.
- OpenDev 논문도 비슷한 구분을 택한다. `scaffolding`과 `context layer`를 준비 단계로 보고, runtime harness는 dispatch, safety, compaction, approval을 담당한다.

실무적으로는 `context engineering은 모델 안쪽`, `harness engineering은 모델 안쪽과 바깥 운영층을 함께 보는 상위 개념`으로 두는 것이 가장 쓸모 있다.

### scaffolding vs runtime harness

- `Building AI Coding Agents for the Terminal`은 이 둘을 가장 또렷하게 가른다. scaffolding은 첫 prompt 전에 일어나는 조립이고, harness는 실행 중 작동하는 dispatch, context management, safety enforcement다.
- OpenAI `Unrolling the Codex agent loop`를 같은 틀로 보면 input collection과 prompt assembly는 scaffolding 성격이 강하고, observation formatting, termination, tool dispatch는 runtime harness에 가깝다.
- Anthropic long-running harness의 initializer agent도 넓게 보면 scaffolding에 가깝다. 반대로 coding agent의 checkpoints, handoff, validation은 runtime harness다.

### 자료 비교: 왜 이 구분이 중요한가

- 같은 팀이 `prompt를 어떻게 조립할지`와 `실행 중 실패를 어떻게 흡수할지`를 한 덩어리로 보면, preparation 문제와 runtime 문제를 혼동하기 쉽다.
- 예를 들어 rules/specs가 빈약한 문제는 scaffolding 또는 context assembly의 문제다.
- 반면 이미 좋은 spec이 있는데 세션 전환마다 상태를 잃는 것은 runtime durability 문제다.
- 이 구분이 없으면 `더 긴 system prompt`나 `더 강한 모델`로 runtime failure를 해결하려는 잘못된 대응이 나오기 쉽다.

### framework vs harness vs substrate

- LangChain은 framework가 사라지지 않는다고 본다. 모델이 좋아질수록 wrapper code는 얇아질 수 있어도, agent loop, middleware, memory, observability를 encode하는 reusable layer는 여전히 필요하다는 주장이다.
- Inngest는 다른 결론에 더 가깝다. 중요한 것은 think-act-observe loop를 감싸는 프레임워크 API가 아니라, retries, persistence, concurrency, event routing을 흡수하는 `durable substrate`라는 입장이다.
- OpenAI App Server 패턴은 또 다른 층을 보여준다. 여기서는 harness가 개별 framework보다 더 큰 `shared runtime service`로 등장한다.

### 자료 비교: 누가 무엇을 강조하는가

| 관점 | 핵심 질문 | 대표 자료 | 실무 해석 |
|------|-----------|----------|----------|
| Framework 관점 | best practice를 어떤 reusable abstraction으로 굳힐까 | LangChain | 여러 agent workflow를 빠르게 조립할 팀에 유리 |
| Harness 관점 | agent를 어떻게 실행, 제약, 측정, 운영할까 | OpenAI, Anthropic, Fowler | 제품 성능과 품질 레버를 보는 관점 |
| Substrate 관점 | retry, persistence, scheduling을 누가 흡수할까 | Inngest | long-running / async / multi-channel agent에 중요 |
| Shared runtime 관점 | 여러 surface가 같은 semantics를 공유하게 할까 | OpenAI App Server | 제품군이 여러 개인 플랫폼 팀에 중요 |

이 네 관점은 서로 배타적이지 않다. 실무에서는 `framework를 사용할 수 있고`, 그 위에 `harness를 설계하고`, 그 아래에 `durable substrate`를 두며, 조직 규모가 커지면 `shared runtime`까지 도입할 수 있다.

### execution harness, eval harness, organizational harness

수집 문헌을 실제로 비교하면 harness는 최소 세 개의 독립된 층으로 반복된다.

1. `Execution harness`
   - tool dispatch, retries, checkpoints, context compaction, safety, persistence
   - 대표 자료: OpenAI unrolling loop, Anthropic long-running harness, Inngest, OpenDev
2. `Evaluation harness`
   - trajectory capture, environment state verification, reproducible runner, grader logic
   - 대표 자료: Anthropic evals, LangChain eval 글, VeRO, SEC-bench, GitTaskBench, PerfBench
3. `Organizational harness`
   - repo legibility, human checkpoints, merge philosophy, background agent, cleanup loop
   - 대표 자료: OpenAI harness engineering, Mitchell Hashimoto, Fowler humans-and-agents, ignorance.ai

### 자료 비교: 왜 eval harness를 따로 떼어야 하나

- Anthropic과 LangChain은 좋은 실행 loop가 있어도 평가 루프가 없으면 개선이 불가능하다고 본다.
- VeRO는 optimizer agent를 평가하려면 target agent보다 먼저 evaluation harness를 설계해야 한다고 본다.
- SEC-bench와 PerfBench는 benchmark 그 자체가 일종의 harness construction problem임을 보여준다.

즉 `agent를 굴리는 시스템`과 `agent를 측정하는 시스템`은 서로 연결되지만 별도로 설계해야 한다.

### 경계 구분이 실무에서 중요한 이유

- tool 선택이 엉키는 문제는 대개 context/tool-contract 문제다.
- 장기 작업에서 상태를 잃는 문제는 execution/durability 문제다.
- 좋아졌는지 판단이 안 되는 문제는 evaluation harness 문제다.
- agent output은 늘었지만 조직이 감당하지 못하는 문제는 organizational harness 문제다.

이 구분이 없으면 팀은 모든 실패를 `프롬프트를 고친다`, `모델을 바꾼다`라는 한 가지 반응으로 처리하게 된다.

## agent 개발에서의 사용 방식

### 실패를 레벨별로 진단한다

| 실패 징후 | 먼저 의심할 레벨 | 왜 그 레벨인가 | 대표 대응 |
|-----------|------------------|---------------|----------|
| 같은 파일을 반복해서 잘못 읽음 | Context harness | 필요한 파일·규칙이 매 턴 명확히 보이지 않음 | LocalContext, file-native retrieval, specs 보강 |
| 작업 중간에 방향을 잃음 | Execution harness | handoff artifact와 checkpoint가 약함 | feature list, todo, checkpoint, resume policy |
| 완료 선언은 했는데 결과가 틀림 | Execution + Eval harness | 종료 조건과 verifier가 약함 | pre-completion checklist, tests, structure check |
| replay가 안 되어 개선도 못 함 | Evaluation harness | trace와 reproducible environment가 없음 | trace capture, frozen env, task runner |
| agent는 빨라졌는데 merge가 막힘 | Organizational harness | human checkpoint와 review policy가 안 바뀜 | 작은 PR, on-the-loop review, background triage |

### coding/terminal agent 예시로 보면

- `AGENTS.md`, `CLAUDE.md`, project rules 파일은 context/scaffolding 자산이다.
- `feature-list.json`, `todo.md`, `checkpoint.md`, `handoff-notes.md`는 execution harness 자산이다.
- `acceptance.sh`, benchmark runner, trace store, replay script는 evaluation harness 자산이다.
- PR template, merge policy, review checklist, background cleanup bot은 organizational harness 자산이다.

### 팀이 실제로 소유하는 것은 무엇인가

- 모델은 외부 서비스일 수 있지만 harness는 팀이 설계하고 바꿀 수 있다.
- OpenAI, DEV, Mitchell Hashimoto가 공통으로 강조하듯, repo 구조, rules 파일, test suite, CI, checklists, trace viewer, approval policy는 모두 팀의 통제 범위 안에 있다.
- 따라서 ROI는 अक्सर 가장 통제 가능한 층에서 나온다. 즉 모델보다 harness를 먼저 보게 된다.

### 우선순위를 잡는 법

1. 먼저 context/scaffolding을 본다.
   - rules, specs, acceptance criteria, local context가 충분한가
2. 다음으로 execution harness를 본다.
   - checkpoints, retries, termination, handoff가 있는가
3. 그다음 evaluation harness를 본다.
   - trace, replay, verifier, regression suite가 있는가
4. 마지막으로 organizational harness를 본다.
   - review/merge/cleanup 방식이 throughput에 맞는가

## 설계 원칙

- harness engineering은 prompt engineering의 상위 집합으로 다룬다.
- context, runtime, eval, organizational layers를 따로 진단한다.
- agent 실패를 곧바로 모델 능력 부족으로 결론내리지 않는다.
- 같은 coding task라도 repo 탐색, long-running implementation, benchmark evaluation은 다른 harness를 요구한다.
- evaluation harness가 없으면 execution harness 개선이 우연인지 실제 향상인지 알 수 없다.
- 자율성을 높일수록 종종 더 강한 구조와 더 명시적인 제약이 필요하다.

## 반론/한계

- 이 용어는 아직 완전히 표준화되지 않았다. 어떤 자료는 runtime을, 어떤 자료는 조직 운영 전체를 harness라 부른다.
- 모델 능력은 여전히 중요하다. Structured Context Engineering은 frontier와 weaker model 간 차이가 여전히 큼을 보여준다.
- 모든 팀이 organizational harness까지 당장 구축할 필요는 없다. 작은 작업에서는 context/tool/runtime 정비만으로도 충분할 수 있다.
- multi-agent, durable substrate, shared runtime은 coding task의 모든 상황에 맞는 기본값이 아니다.

## 관련 자료 묶음

- 직접 문헌: OpenAI `Harness engineering`, Anthropic `Effective harnesses for long-running agents`, Martin Fowler `Harness Engineering`, Inngest `Your Agent Needs a Harness, Not a Framework`
- 기반 문헌: Anthropic `Effective context engineering for AI agents`, Manus `Context Engineering for AI Agents`, OpenAI `Unrolling the Codex agent loop`, Martin Fowler `Context Engineering for Coding Agents`
- 인접 논문: `Building AI Coding Agents for the Terminal`, `Structured Context Engineering for File-Native Agentic Systems`, `VeRO`, `CEDAR`
