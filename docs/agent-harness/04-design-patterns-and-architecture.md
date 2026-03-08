# 04. Design Patterns and Architecture

이 문서는 전체 코퍼스를 바탕으로 `agent harness를 어떻게 설계해야 하는가`를 결정형 가이드로 정리한다. 목표는 패턴을 나열하는 것이 아니라, 각 패턴에 대해 `언제 쓰는가`, `언제 과한가`, `무엇과 같이 써야 하는가`, `대표 반례는 무엇인가`를 명확히 하는 것이다.

## 핵심 주장

- 좋은 harness는 하나의 거대한 프롬프트가 아니라 `context, tools, runtime, artifacts, memory, safety, orchestration`이 분리된 구조다.
- 설계의 핵심은 `무엇을 모델이 직접 보게 할지`와 `무엇을 런타임이 대신 처리할지`를 나누는 데 있다.
- 자율성을 높이려면 종종 더 큰 자유가 아니라 더 강한 구조, 더 작은 단계, 더 명시적인 검증이 필요하다.

## 전체 코퍼스 종합

### 패턴 선택용 의사결정 표

| 문제 상황 | 먼저 고려할 패턴 | 왜 이 패턴인가 | 과한 경우 |
|-----------|------------------|----------------|----------|
| 대화가 길어질수록 품질이 급락 | context externalization + compaction | history 오염을 줄이고 필요한 정보만 재주입 | 짧은 one-shot task |
| tool 수가 많고 선택이 흔들림 | tool contract 정비 + virtualization | 도구 선택 부담과 prompt budget을 동시에 줄임 | tool 수가 적고 안정적일 때 |
| 긴 작업에서 상태를 잃음 | checkpoints + handoff artifact + durability | 세션/step 간 continuity를 확보 | 짧고 순차적인 task |
| destructive action risk가 큼 | layered safety + deterministic constraints | 허용 행동 공간을 먼저 줄임 | low-risk local prototype |
| 여러 surface에서 같은 동작 필요 | shared runtime / App Server | behavior consistency와 centralized policy 확보 | 단일 surface, 단일 팀 |
| task가 탐색형이고 path-dependent | role separation + sub-agent orchestration | 병렬 탐색과 압축이 효과적 | tightly coupled coding task |

### 1. Context externalization

#### 언제 쓰는가

- long-running coding task
- 대량 tool output이 누적되는 task
- 세션 전환이 잦거나 중간 재시작이 필요한 task
- raw artifact를 대화 안에 직접 넣기 어려운 task

#### 자료 비교

- Manus는 context를 history에만 두지 말고 files, todo, artifacts로 बाह재화하라고 한다.
- Anthropic context engineering은 creation, accumulation, pruning lifecycle로 같은 문제를 설명한다.
- Inngest는 within-run pruning과 across-run compaction을 분리해 런타임 정책으로 구현한다.
- Structured Context Engineering은 file-native retrieval이 frontier model에는 유리하지만 약한 모델에는 mixed result임을 보여준다.

### 무엇과 함께 써야 하는가

- related-files artifact
- todo / checkpoint notes
- selective re-injection policy
- current-task local context injection
- observation summarization

#### coding/terminal agent 설계 형태

- 전체 diff, benchmark output, 긴 로그는 files나 structured artifacts에 저장한다.
- 대화에는 요약, 경로, 핵심 메트릭만 남긴다.
- 다음 턴에는 필요한 artifact만 다시 읽는다.

#### 언제 과한가

- 단순한 one-shot edit
- 관련 파일 수가 매우 적고 컨텍스트가 짧은 task
- weaker model이 file-native navigation을 잘 못하는 환경

#### 대표 반례와 주의

- `history를 줄이면 무조건 좋아진다`는 직관은 틀릴 수 있다. 요약 품질이 나쁘면 중요한 rationale을 잃는다.
- Structured Context Engineering의 `grep tax`는 compact format과 file-native retrieval이 runtime token을 오히려 늘릴 수 있음을 보여준다.

### 2. Tool contract discipline

#### 언제 쓰는가

- tool 수가 5개를 넘어가며 선택 혼동이 생길 때
- 파라미터 오류와 잘못된 반환 해석이 반복될 때
- MCP server나 external API surface가 커질 때

#### 자료 비교

- Anthropic `Writing effective tools for AI agents`는 이름, description, schema, return format 모두가 prompt 일부라고 본다.
- Anthropic multi-agent는 agent-tool interface를 HCI만큼 중요하게 보며 tool-testing agent까지 도입했다.
- Meta program repair는 unified diff보다 search-and-replace가 더 agent-friendly했다고 보고한다.
- Anthropic MCP와 OpenDev는 tool universe를 lazy loading/virtualization으로 줄인다.

#### 무엇과 함께 써야 하는가

- 명확한 naming convention
- flat하고 constrained schema
- actionable error messages
- result size limit
- agent-as-tool-tester 또는 replay trace

#### coding/terminal agent 설계 형태

- `read_file`, `edit_file`, `run_tests`, `search_code`, `execute_code` 같은 명확한 action units
- 너무 많은 narrow tool 대신, 일부는 virtualization layer로 숨긴다
- 반환값은 다음 행동을 결정할 수 있을 정도의 정보만 남긴다

#### 언제 과한가

- tool 수가 적고 작업 종류가 거의 고정일 때
- agent가 실제로 잘못된 tool 선택을 거의 하지 않을 때

#### 대표 반례와 주의

- `tool을 세분화하면 무조건 좋다`는 보장이 없다. tool 수가 많아질수록 selection burden이 커진다.
- `execute_code` 하나로 모든 걸 가상화하면 token을 아끼지만, runtime 내부 가시성이 떨어질 수 있다.

### 3. Runtime durability와 checkpoints

#### 언제 쓰는가

- 작업이 여러 세션에 걸쳐 이어질 때
- tool/API failure가 잦을 때
- 같은 task를 반복 재시작하는 비용이 클 때
- human steering이나 async trigger가 필요한 task

#### 자료 비교

- Anthropic long-running harness는 initializer/coding agent 분리와 checkpoint handoff를 핵심 패턴으로 제시한다.
- Inngest는 이를 event-driven durable execution으로 풀어, iteration 3에서 실패하면 그 step만 재실행되게 한다.
- OpenDev는 planning/execution 분리, event-driven reminders, dual memory를 runtime OS처럼 조합한다.
- OpenAI unrolling loop는 이 모든 구조의 최소 단위를 runtime semantics로 보여준다.

#### 무엇과 함께 써야 하는가

- explicit checkpoint artifact
- completion criteria
- bounded retry policy
- loop detection
- failure recovery path

#### coding/terminal agent 설계 형태

- feature 또는 milestone 단위 checkpoint
- tool failure 시 full rerun 대신 step-local retry
- terminal output은 raw dump 대신 summarized observation으로 재주입

#### 언제 과한가

- 짧고 deterministic한 one-turn automation
- 실패 비용이 매우 낮은 local experiment

#### 대표 반례와 주의

- durability가 있다고 해서 자동으로 좋은 handoff가 생기지는 않는다. persisted state가 `읽기 어려우면` 다음 agent나 인간에게 도움이 안 된다.
- checkpoint granularity가 너무 크면 실패 국소화가 안 되고, 너무 작으면 관리 오버헤드가 커진다.

### 4. Layered safety와 deterministic constraints

#### 언제 쓰는가

- shell, filesystem, git, network write가 가능한 coding agent
- compliance나 production 영향이 큰 작업
- illegal action, destructive action, scope overreach가 반복될 때

#### 자료 비교

- OpenDev는 prompt guardrail, schema restriction, runtime approval, tool validation, lifecycle hooks의 5-layer defense를 제시한다.
- AutoHarness는 action filter, verifier, policy 형태의 harness를 실험해 stronger constraints가 더 높은 reward와 legality를 만들 수 있음을 보여준다.
- Fowler는 더 높은 자율성을 원할수록 오히려 solution space를 더 강하게 제한해야 할 수 있다고 말한다.
- Meta repair는 static analysis와 test execution을 통해 생성 patch를 external constraints로 수렴시킨다.

#### 무엇과 함께 써야 하는가

- allow/deny rules
- risk-tiered approval
- verifier stack
- retry with correction
- explicit non-goals

#### coding/terminal agent 설계 형태

- destructive command approval
- branch protection
- structural tests
- format/type/test gate
- risky file path restriction

#### 언제 과한가

- throwaway prototype
- sandboxed read-only analysis agent

#### 대표 반례와 주의

- safety를 prompt only로 두면 강도가 약하다.
- 반대로 approval을 너무 많이 두면 humans-in-the-loop bottleneck이 생긴다.
- 핵심은 `위험이 큰 행동만 강하게 제한하고, 저위험 반복 작업은 자동화`하는 것이다.

### 5. Shared runtime / App Server

#### 언제 쓰는가

- 웹, CLI, IDE, background worker 등 여러 surface가 있을 때
- behavior consistency와 centralized policy가 중요할 때
- tool execution, sandbox, state management를 중복 구현하기 싫을 때

#### 자료 비교

- OpenAI App Server는 harness를 각 UI 내부 로직이 아니라 shared runtime service로 둔다.
- Inngest는 shared service라기보다 durable substrate 쪽에 가깝지만, 동일한 event fabric 위에 여러 trigger와 workers를 올리는 구조를 제시한다.
- LangChain의 framework 관점은 이보다 높은 추상화 레벨에서 reusable agent architecture를 제공한다.

#### 무엇과 함께 써야 하는가

- shared conversation primitives
- centralized execution backend
- common safety policy
- trace and experiment store

#### coding/terminal agent 설계 형태

- CLI와 IDE가 동일한 loop semantics를 공유
- sandbox/terminal/tool access 정책을 중앙 서비스에서 통제
- trace, eval, config를 한 곳에 모은다

#### 언제 과한가

- 단일 surface, 소규모 팀, 짧은 프로젝트

#### 대표 반례와 주의

- shared runtime은 재사용성과 일관성을 주지만 중앙 장애점이 된다.
- 개별 surface별로 필요한 UX 차이를 runtime에 과도하게 밀어 넣으면 오히려 복잡성이 커진다.

### 6. Multi-agent 분업과 병렬화

#### 언제 쓰는가

- path-dependent 탐색이 길고 병렬화 가치가 큰 task
- 검색, 조사, 데이터 수집, artifact compression이 핵심인 task
- 역할 분리로 context를 깨끗하게 유지할 수 있는 task

#### 자료 비교

- Anthropic research system은 lead agent, subagents, citation agent를 통해 병렬 탐색과 압축을 수행한다.
- CEDAR는 orchestrator, text generator, code generator로 역할을 나눠 transparency를 높인다.
- Anthropic long-running harness의 initializer/coding agent 분리도 넓게 보면 role separation의 한 형태다.
- 그러나 Anthropic은 코딩 task는 research task보다 agent dependency가 커서 멀티에이전트가 항상 유리하지 않다고 직접 인정한다.

#### 무엇과 함께 써야 하는가

- clear role boundary
- handoff artifact
- coordination protocol
- cost budget
- evaluator that can judge multi-path execution

#### coding/terminal agent 설계 형태

- planner / implementer / reviewer 정도의 느슨한 역할 분리
- 조사형 sub-task만 병렬화
- code-writing core loop는 가능한 한 일관된 단일 작업 흐름으로 유지

#### 언제 과한가

- tightly coupled refactor
- 작은 bug fix
- compile-test-debug loop가 핵심인 task

#### 대표 반례와 주의

- 멀티에이전트는 데모는 화려하지만 coordination overhead, token cost, debugging complexity가 크다.
- 병렬성이 task 구조에서 자연스럽게 나오지 않으면 오히려 성능이 떨어질 수 있다.

### 핵심 긴장 정리

#### framework vs substrate

- LangChain은 framework를 살아남는 system layer로 본다.
- Inngest는 substrate가 더 중요하다고 본다.
- 실무 기본값은 `framework와 substrate를 경쟁 개념으로 보기보다, framework는 위쪽 추상화, substrate는 아래쪽 durability layer`로 두는 것이다.

#### 자율성 vs 제약

- AutoHarness, OpenDev, Fowler는 더 강한 구조가 더 높은 자율성을 가능하게 할 수 있음을 보여준다.
- 그러나 제약이 지나치면 humans-in-the-loop bottleneck과 과소탐색이 생길 수 있다.
- 기본값은 `저위험 행동 자동화, 고위험 행동 제약`이다.

#### file-native retrieval의 모델 의존성

- Manus/Fowler 계열은 files 네트워크를 선호한다.
- Structured Context Engineering은 model tier에 따라 결과가 달라진다고 본다.
- 기본값은 `frontier model + mature tool use`면 file-native를 우선 검토하고, weaker model이면 hybrid retrieval을 쓴다.

#### multi-agent의 coding 적합성

- research, DS, 조사형 workflow에서는 role separation이 강력하다.
- compile-test-debug 중심 coding loop에서는 coordination cost가 빨리 커진다.
- 기본값은 `role separation은 쓰되, 병렬 subagent는 선택적으로만`이다.

## agent 개발에서의 사용 방식

### 패턴 선택 순서

1. context externalization과 tool contracts를 먼저 정리한다.
2. completion checks, checkpoints, loop detection을 붙인다.
3. 장기 작업이 많아지면 durability와 handoff artifacts를 도입한다.
4. risk가 높아지면 layered safety와 deterministic constraints를 강화한다.
5. surface가 늘어나면 shared runtime을 검토한다.
6. task 구조가 병렬화에 맞을 때만 multi-agent를 쓴다.

### 구현 전 자가 점검 질문

- 이 task는 history 누적형인가 artifact handoff형인가
- tool 수는 얼마나 많고 selection error가 얼마나 자주 나는가
- failure cost는 retry로 감당 가능한가, checkpoint가 필요한가
- high-risk action이 있는가
- 여러 surface에서 같은 semantics가 필요한가
- 병렬 분업으로 얻는 이득이 coordination cost보다 큰가

## 설계 원칙

- state는 history가 아니라 artifacts에 둔다.
- tool contract는 human API doc가 아니라 agent decision surface로 설계한다.
- observation은 raw dump가 아니라 다음 행동에 필요한 크기와 형태로 가공한다.
- termination은 모델의 자율 판단에만 맡기지 않는다.
- safety는 가능한 행동 공간을 줄이는 방식으로 먼저 설계한다.
- model-specific harness 차이를 인정한다.
- shared runtime과 multi-agent는 필요 조건이 충분할 때만 도입한다.

## 반론/한계

- file-based state와 compaction 전략은 구현 난도가 높고, 요약이 잘못되면 중요한 맥락을 잃는다.
- tool virtualization은 token을 아끼지만 가시성을 낮출 수 있다.
- shared runtime은 일관성을 주지만 중앙 장애점이 된다.
- multi-agent는 coding workflow에서 종종 과잉 설계가 되기 쉽다.

## 관련 자료 묶음

- 직접 문헌: Anthropic `Effective harnesses for long-running agents`, OpenAI `Unlocking the Codex harness`, Inngest `Your Agent Needs a Harness, Not a Framework`, Martin Fowler `Harness Engineering`
- 기반 문헌: Manus `Context Engineering for AI Agents`, Anthropic `Writing effective tools for AI agents`, Anthropic `Code execution with MCP`, Anthropic `How we built our multi-agent research system`
- 인접 논문: `Building AI Coding Agents for the Terminal`, `AutoHarness`, `Structured Context Engineering for File-Native Agentic Systems`, `CEDAR`, `Agentic Program Repair from Test Failures at Scale`
