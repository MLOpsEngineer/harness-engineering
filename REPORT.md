# Harness Engineering 종합 분석 보고서

- 작성일: 2026-03-08
- 코퍼스 규모: 블로그/아티클 21건, 논문 10건
- 분석 깊이: 원문 수준 상세 분석

---

## 1. 정의: Harness Engineering이란 무엇인가

### 1-1. 한 문장 정의

Harness engineering은 **모델 바깥에서 에이전트가 안정적으로 일하도록 만드는 모든 설계 행위**다. 여기에는 context curation, tool contract, runtime orchestration, eval, observability, human review loop, durability, state persistence가 모두 포함된다.

### 1-2. 용어의 어원과 비유

Inngest의 Dan Farrelly는 세 가지 비유를 든다:
- **Wiring harness** (자동차): 전기 신호를 올바른 컴포넌트로 라우팅한다. 일을 직접 수행하지 않지만 연결하고 보호한다.
- **Test harness** (소프트웨어): 테스트 대상을 감싸고 입력을 제어하며 결과를 수집한다.
- **Safety harness** (등반): 위험한 환경에서 작업자를 보호한다.

이 비유들의 공통점은 **harness 자체는 일을 하지 않지만, 일이 안전하고 예측 가능하게 수행되도록 만든다**는 것이다. LLM이 엔진이라면, tools는 주변장치, memory는 저장소, harness는 이들을 연결하고 보호하고 오케스트레이션하는 층이다.

### 1-3. Context Engineering과의 관계

수집된 문헌을 종합하면 가장 선명한 구분은 다음과 같다:

| 구분 | Context Engineering | Harness Engineering |
|------|-------------------|-------------------|
| 대상 | 모델 안으로 무엇을 넣을지 | 모델 바깥에서 실행, 검증, 기억, 제약, 루프를 설계 |
| 핵심 질문 | "어떤 정보를 어떤 형식으로 넣을까?" | "실패하면 어떻게 복구하고, 어떻게 측정하고, 사람은 어디서 개입하나?" |
| 조작 대상 | system prompt, tool schema, memory, history | runtime, CI, eval, observability, review loop, repo structure |

Martin Fowler의 Birgitta Böckeler는 이 경계를 가장 선명하게 긋는다: context engineering은 harness engineering의 **내부 레이어**다. Harness는 context engineering을 포함하되, architectural constraints, garbage collection, eval loop, human review까지 아우른다.

Anthropic의 2025년 9월 글은 context를 system prompt 하나로 축소하지 않는다. tool schema, MCP surface, external data, history, memory까지 모두 context라고 보며, 핵심 문제는 accumulation — 여러 턴이 지나면 관련 없는 정보와 오래된 observation이 쌓여 agent decision quality를 떨어뜨린다 — 이라고 정의한다.

### 1-4. 누가 이 용어를 만들었나

- **2025년 11월**: Anthropic이 "Effective harnesses for long-running agents"에서 harness라는 단어를 제목에 처음 사용
- **2026년 2월 5일**: Mitchell Hashimoto가 "Step 5: Engineer the Harness"로 실무 언어를 던짐
- **2026년 2월 11일**: OpenAI Ryan Lopopolo가 "Harness engineering: leveraging Codex in an agent-first world"로 개념을 대중화
- **2026년 2월 17일 이후**: LangChain, Inngest, Martin Fowler, DEV Community가 빠르게 개념을 확장

---

## 2. 시간축으로 본 흐름

### Phase 1: 기반 형성 (2025년 6월~9월)

이 시기의 핵심 문헌은 아직 "harness engineering"이라는 이름을 쓰지 않지만, 같은 문제를 각자의 언어로 발견한다.

**Anthropic multi-agent research system (2025-06-13)**은 병렬 서브에이전트, 컨텍스트 압축, coordination 문제를 가장 구체적으로 보여준다. 핵심 비유는 "search is compression" — 방대한 정보에서 중요한 토큰만 추려야 하는데, subagent들이 각자 독립된 context window에서 다른 방향을 탐색한 뒤 압축된 결과만 lead agent에 넘기면 더 효과적이다. 내부 eval에서 `Claude Opus 4 lead + Claude Sonnet 4 subagents` 구성이 단일 Opus 4보다 90.2% 더 나았다고 밝힌다. 동시에 비용도 분명히 적는다: 일반 chat보다 agent는 ~4배, multi-agent system은 ~15배 토큰을 더 쓴다.

이 글에서 이미 등장하는 harness 패턴들:
- 역할 분해 (lead agent + specialized subagents + citation agent)
- 메모리 지속 (plan persistence to survive context window truncation)
- tool-testing agent (tool description을 agent가 다시 쓰게 해 task completion time 40% 감소)
- 프롬프팅 원칙 8가지 (think like your agents, teach delegation, scale effort, tool design, let agents improve themselves, start wide then narrow, guide thinking, parallel tool calling)

**Manus context engineering (2025-07-18)**은 context를 단순 system prompt가 아니라 계획, 파일, 메모리, tool result, 실행 기록, intermediate artifact 전체로 정의한다. 핵심 교훈: long-running task에서 대화 히스토리만으로 상태를 유지하면 context가 금방 붕괴한다. 정보를 외부 file/artifact로 옮기고 필요한 시점에 필요한 조각만 다시 읽게 하는 방식이 더 안정적이다.

**Anthropic writing effective tools (2025-09-11)**은 tool surface를 harness의 핵심 레버로 설명한다. 좋은 tool은 기능이 많은 tool이 아니라, 이름과 경계가 명확하고 호출 계약이 예측 가능하며 반환값이 후속 reasoning에 바로 쓰일 수 있는 tool이다. 더 나아가 agent를 써서 tool 자체를 테스트하고 설명을 고치는 loop를 권한다.

**Anthropic effective context engineering (2025-09-29)**은 핵심 전환을 선언한다: prompt engineering에서 context engineering으로. 중요한 관점은 "thinking in context" — 현재 context shape가 agent에게 어떤 행동을 유도하는지를 역으로 보며 설계해야 한다.

같은 시기 **benchmark 논문들**은 환경 의존적 태스크 평가를 시작한다:
- **SEC-bench**: 200개 실제 CVE로 보안 agent를 평가. 핵심 오라클은 memory safety sanitizer. benchmark 자체가 Dockerized environment + harness다.
- **Agentic Program Repair**: Meta 내부에서 test failure → repair agent → static analysis/test feedback → LLM judge → human review의 다층 production loop. 3개월간 생성 fix 중 25.5% landed.
- **GitTaskBench**: 54개 현실 태스크, 18개 GitHub 프로젝트. 실패의 **절반 이상이 environment setup과 dependency resolution**에서 발생.

### Phase 2: Long-running agent와 eval로 확장 (2025년 11월~2026년 1월)

**Anthropic effective harnesses for long-running agents (2025-11-26)**은 harness라는 단어를 제목에 처음 쓴 핵심 기술 글이다. long-running coding agent의 실패 원인을 단순 context overflow가 아니라 **세션 간 handoff 실패**로 본다. 해결책:
- compaction만으로는 부족하고, **initializer agent** (환경과 방향 설정)와 **coding agent** (구현 진행)를 분리해야 한다
- 각 세션은 다음 세션이 바로 이어받을 수 있도록 legible한 state를 남겨야 한다 (코드 상태, 문서, TODO, 남은 위험)
- one-shot 대신 feature-by-feature, checkpoint-by-checkpoint로 진행하도록 harness가 유도
- 핵심: **다음 턴을 위한 배려를 시스템에 강제하는 것**. 현재 작업만이 아니라 미래 세션의 재시작 비용까지 관리

**Anthropic code execution with MCP (2025-11-04)**은 tool universe 확장의 실제 문제를 다룬다. MCP server가 많아질수록 tool definition을 전부 upfront로 주는 방식이 token budget과 latency를 빠르게 잠식한다. 해결 방향: "모델이 봐야 하는 것"과 "런타임이 대신 처리할 것"을 분리. 핵심 메시지는 "tool을 더 붙이자"가 아니라 **"tool exposure를 virtualize하자"**.

**LangChain evaluating deep agents (2025-12-03)**은 eval 인프라의 실무 교훈을 정리한다. datapoint마다 성공 조건이 달라 bespoke test logic이 필요하고, 환경이 지저분하면 모델 변화보다 환경 편차가 결과를 지배한다. eval은 "답안 채점"이 아니라 **"특정 harness 변경이 실제 behavior를 개선했는지" 측정하는 운영 시스템**이 된다.

**Anthropic demystifying evals (2026-01-09)**은 agent eval이 model eval과 다른 이유를 구조적으로 설명한다. agent는 tool을 호출하고 environment state를 바꾸며 trajectory를 남기므로, 최종 문자열만 비교하면 실제 능력 변화를 잡지 못한다. eval = trajectory + final response + environment state + grader logic을 함께 설계해야 한다.

### Phase 3: 개념의 명명과 정식화 (2026년 2월~3월)

**OpenAI unrolling the Codex agent loop (2026-01-23)**은 Codex의 핵심이 단일 model call이 아니라 입력 수집 → tool execution → 다음 행동 결정까지의 **loop**라는 점을 강조한다. surface마다 달라 보여도 아래에는 공통 runtime semantics가 존재한다.

**OpenAI unlocking the Codex harness (2026-02-04)**은 harness를 **공통 agent runtime service**로 본다. 웹 앱, CLI, IDE extension, macOS app이 같은 conversation primitive와 execution backend를 공유하도록 계층을 나눈다. 핵심 가치는 코드 재사용이 아니라 **behavioral consistency** — 어디서 Codex를 부르든 비슷한 agent semantics를 보장.

**Mitchell Hashimoto "My AI Adoption Journey" (2026-02-05)**는 AI adoption을 여러 단계로 나누며, 채팅 보조를 넘어서는 순간이 "Engineer the Harness" 단계라고 말한다. 가치 있는 활용은 모델과 대화하는 시간이 아니라, agent가 독립적으로 useful work을 할 수 있게 repo와 feedback environment를 정비하는 데서 나온다. "항상 에이전트 하나는 돌고 있게 하라"는 문장이 인간 역할의 이동을 상징한다.

**OpenAI "Harness engineering" (2026-02-11)**는 현재 담론의 기준점이다. OpenAI 팀이 "0 lines of hand-written code" 제약 아래 제품과 운영 artifact를 만들어 본 사례에서 출발한다:
- 핵심 메시지: 인간의 역할이 코드 작성에서 **intent specification, feedback loop design, environment shaping**으로 이동
- Repository knowledge를 system of record로 삼고, architecture, constraints, taste를 agent-readable form으로 외부화
- 가장 유명한 주장: **"agent legibility"** — 코드베이스는 인간뿐 아니라 agent에게도 읽히고 수정되기 쉬워야 한다
- Throughput이 늘어나면 merge philosophy, garbage collection, entropy control, review 방식까지 같이 바뀌어야 한다
- Agent가 struggle하면 **더 세게 밀지 말고 무엇이 빠졌는지 찾는다** — harness는 일회성 설정이 아니라 failure를 통해 계속 자라나는 시스템

**LangChain "Improving Deep Agents with harness engineering" (2026-02-17)**는 **가장 실증적인 harness engineering 사례**다:
- deepagents-cli는 GPT-5.2-codex를 그대로 둔 채 system prompt, tools, middleware만 바꿔 Terminal Bench 2.0 점수를 **52.8 → 66.5**로 올림
- LangSmith trace를 대규모로 분석해 실패 패턴을 찾고, Agent Skill 형태의 trace analyzer로 자동화
- 시스템 프롬프트, 도구, middleware를 'knobs'로 보고 실험하는 태도가 표준 실무 패턴에 가깝다
- 메시지: harness engineering은 추상 개념이 아니라 **measurable optimization space**

**Inngest "Your Agent Needs a Harness, Not a Framework" (2026-03-03)**는 harness engineering의 **인프라/런타임 면**을 가장 강하게 강조한다:
- Utah ("Universally Triggered Agent Harness") 참조 구현: webhook → event → worker → agent loop → reply
- 모든 LLM/tool 호출이 독립적 `step.run(...)` 단위가 됨. iteration 3에서 API 500이 나면 그 step만 재시도, 1~2 결과는 persisted state
- Token budget과 실패복구 정책까지 포함하는 운영 레이어
- "framework를 고를 것인가"보다 **"어떤 durable substrate 위에 agent loop를 올릴 것인가"**를 먼저 묻는다

**Martin Fowler "Humans and Agents in Software Engineering Loops" (2026-03-04)**는 인간-에이전트 협업 모델을 세 가지로 분류한다:
- **Humans outside the loop** (vibe coding): 인간은 결과만 제시, 구현은 agent에게. 내부 품질 문제 발생 가능
- **Humans in the loop**: 인간이 가장 안쪽 루프의 gatekeeper. **throughput mismatch** — agent가 빨라질수록 인간 검토가 병목
- **Humans on the loop** (제안 모델): 인간은 산출물을 직접 고치지 않고, **산출물을 만들어낸 specifications, checks, workflow guidance를 바꾼다**. Harness = "how loop 내부를 제어하는 specifications, checks, workflow guidance의 묶음"
- **Agentic flywheel**: agent가 harness 개선을 제안하고, 신뢰가 쌓이면 일부를 자동 승인. Harness engineering이 **자기 자신을 개선하는 meta-loop**로 발전

핵심 구분: "in the loop"에서 결과가 마음에 들지 않으면 산출물을 직접 수정한다. "on the loop"에서는 산출물을 만들어낸 **harness를 바꾼다**. 같은 유형의 문제를 다음 실행부터 덜 만들도록 **루프 자체를 교정**한다.

**Martin Fowler "Harness Engineering" (2026-03-05)**는 개념 경계를 가장 선명하게 긋는다. OpenAI 사례를 세 묶음의 메커니즘으로 재해석:
1. **Context engineering**: 코드베이스 안의 knowledge base + observability 데이터 + 동적 컨텍스트 접근
2. **Architectural constraints**: custom linters와 structural tests 같은 **deterministic checker**로 설계 경계를 강제
3. **Garbage collection**: 문서 불일치나 아키텍처 규칙 위반을 주기적으로 찾아내는 **background agent**

추가 논점:
- 기능 검증과 행동 검증이 OpenAI 글에서 상대적으로 덜 드러났다고 지적
- Harness가 미래의 **service template** 비슷한 것이 될 수 있다는 가설 — golden path template으로서의 harness
- **더 높은 AI 자율성을 얻으려면 오히려 runtime과 solution space를 더 강하게 제한해야** 할 수 있다. 자유로운 생성보다 특정 architecture, boundary, structure를 강제해야 신뢰성과 유지보수성이 생긴다.

---

## 3. Harness의 구성 요소 — 문헌 종합 Taxonomy

31개 문헌에서 반복적으로 등장하는 harness 구성 요소를 계층으로 정리하면 다음과 같다:

### Layer 1: Context Layer (모델 안으로 들어가는 것)

| 요소 | 설명 | 주요 출처 |
|------|------|----------|
| System prompt | agent의 역할, 제약, 행동 규범 | Anthropic, OpenAI, LangChain |
| Tool schema | 도구 이름, 파라미터, 반환값 계약 | Anthropic tools, OpenDev |
| Dynamic context | 현재 파일, git diff, test result 등 실시간 정보 | Manus, Fowler context eng. |
| Memory/history | 이전 턴 요약, 장기 기억 | Manus, Anthropic long-running |
| Rules/specs | CLAUDE.md, cursor rules 같은 외부화된 규칙 | Fowler context eng., OpenAI |

### Layer 2: Runtime Layer (실행 환경)

| 요소 | 설명 | 주요 출처 |
|------|------|----------|
| Agent loop | think → act → observe 반복 구조 | OpenAI unrolling, Inngest |
| Step-level durability | 각 step의 결과를 persist, 실패 시 해당 step만 재시도 | Inngest Utah |
| Concurrency control | 동일 세션의 race condition 처리 (singleton 등) | Inngest |
| Role separation | initializer / planner / executor / reviewer 분리 | Anthropic long-running, multi-agent |
| Sub-agent orchestration | 병렬 subagent 생성, 결과 수집, coordination | Anthropic multi-agent |
| Context compaction | within-run pruning + across-run compaction 분리 | Inngest, Manus |
| Budget management | token budget warning, overflow recovery | Inngest, OpenDev |

### Layer 3: Constraint Layer (제약과 검증)

| 요소 | 설명 | 주요 출처 |
|------|------|----------|
| Deterministic checkers | custom linters, structural tests, type checks | Fowler harness eng. |
| Action filters/verifiers | illegal action 차단, schema-level restriction | AutoHarness, OpenDev |
| Safety layers | prompt guardrail → schema → runtime approval → tool validation → lifecycle hooks | OpenDev (5-layer) |
| Garbage collection agents | 문서 불일치, 아키텍처 위반을 주기적으로 찾는 background agent | Fowler harness eng., OpenAI |

### Layer 4: Measurement Layer (관측과 평가)

| 요소 | 설명 | 주요 출처 |
|------|------|----------|
| Tracing | 전체 trajectory 기록, decision pattern 모니터링 | Anthropic multi-agent, LangChain |
| Eval harness | trajectory + final response + env state + grader | Anthropic evals, VeRO |
| Trace analysis | failure pattern 자동 분류, 개선 후보 생성 | LangChain improving agents |
| Performance benchmarks | agent-generated benchmark로 비기능 품질 측정 | PerfBench |
| Versioned evaluation | commit 단위 versioning + budgeted eval calls | VeRO |

### Layer 5: Human-Agent Interface Layer (사람의 개입)

| 요소 | 설명 | 주요 출처 |
|------|------|----------|
| Approval points | human-in-the-loop review, merge 승인 | Fowler humans-and-agents |
| Intent specification | 코드 대신 의도, 제약, 취향을 명시 | OpenAI harness eng. |
| Review loop redesign | throughput에 맞춘 review 방식 변경 | OpenAI, ignorance.ai |
| Harness as loop control | 산출물이 아니라 loop를 교정 (on the loop) | Fowler humans-and-agents |
| Agentic flywheel | agent가 harness 개선을 제안, 일부 자동 승인 | Fowler humans-and-agents |

### Layer 6: Repository & Organization Layer (조직과 저장소)

| 요소 | 설명 | 주요 출처 |
|------|------|----------|
| Agent legibility | agent가 읽기 쉬운 repo 구조, 문서, 규칙 | OpenAI harness eng., Mitchell H. |
| Repo as system of record | architecture, constraints, taste를 agent-readable form으로 외부화 | OpenAI harness eng. |
| Merge philosophy | agent throughput에 맞춘 merge/review 방식 | OpenAI, ignorance.ai |
| Background agent fleet | 병렬로 도는 agent들, task batching | ignorance.ai playbook |
| Service template / golden path | harness를 조직 공통 template으로 | Fowler harness eng. |

---

## 4. 핵심 테마 심층 분석

### 4-1. "모델보다 환경" — 가장 강한 합의

거의 모든 핵심 글이 같은 결론으로 모인다. 일정 수준 이상의 모델 능력이 확보되면, 실제 차이는 모델 바깥에서 난다.

**가장 강한 정량적 근거**: LangChain의 Terminal Bench 2.0 사례. GPT-5.2-codex를 고정한 채 harness만 바꿔 52.8 → 66.5 (+26% 상대 향상). 이는 모델 세대를 한 단계 올리는 것과 비슷한 크기의 향상이다.

**AutoHarness 논문**: Gemini-2.5-Flash + learned harness가 더 큰 모델인 Gemini-2.5-Pro를 능가. 더 나아가 code-policy까지 밀어붙이면 GPT-5.2-High까지 넘는다.

**GitTaskBench**: 실패의 절반 이상이 environment setup과 dependency resolution에서 발생. 모델 지능이 아니라 환경 준비의 문제.

**PerfBench**: performance-aware instruction과 tooling을 넣은 OpenHands-Perf-Agent가 baseline 대비 ~5배 개선 (3% → 15-20%).

**Structured Context Engineering 논문**: 가장 큰 변수는 model capability 자체 (frontier vs open-source 21pp gap)였지만, file-native retrieval architecture는 frontier model에 +2.7% 정확도 향상을 추가로 줬다. 즉 **강한 모델 + 좋은 harness가 최적 조합**.

### 4-2. Harness는 일회성 설정이 아니라 반복적으로 자라는 시스템

**OpenAI**: "agent가 struggle하면 더 세게 밀지 말고 무엇이 빠졌는지 찾는다". Harness는 failure를 통해 계속 자라나는 시스템.

**Anthropic multi-agent**: tool-testing agent가 MCP tool description을 다시 쓰게 해 task completion time 40% 감소. Agent가 harness component를 개선하는 loop.

**LangChain**: trace analyzer skill로 failure pattern을 자동 분류하고 개선 후보 생성. Eval은 one-off experiment가 아니라 continuous improvement signal.

**Fowler humans-and-agents**: agentic flywheel — agent가 harness 개선을 제안하고, 충분한 신뢰가 쌓이면 일부 자동 승인. Harness engineering이 **self-improving meta-loop**로 발전.

### 4-3. 장기 작업의 핵심은 "다음 턴을 위한 배려"

**Anthropic long-running harness**: 각 세션은 다음 세션이 바로 이어받을 수 있도록 legible한 state를 남겨야 한다. 코드 상태 + 문서 + TODO + 남은 위험.

**Manus**: agent가 미래의 자신이나 다른 agent를 위해 legible한 흔적을 남기게 만드는 것이 productivity의 핵심.

**Anthropic multi-agent**: context window가 200,000 tokens를 넘으면 잘릴 수 있기 때문에 plan persistence가 중요. 완료된 작업 단계를 요약하고 핵심 정보를 외부 memory에 저장하는 패턴.

**Inngest**: within-run pruning과 across-run compaction을 분리. 오래된 tool result를 soft trim/hard clear하고 최근 몇 턴은 보존. 남은 iteration이 적을 때 budget warning, context-too-large 오류 시 강제 compaction 후 회복.

### 4-4. Tool은 많이 주는 것보다 명확한 계약으로

**Anthropic writing tools**: tool description과 parameter schema도 prompt의 일부. 설명을 길게 늘이는 것이 아니라 agent가 실제 decision을 내리는 데 필요한 정보만 명확히.

**Anthropic multi-agent 프롬프팅 원칙**: "agent-tool interface를 human-computer interface만큼 중요하게 보라". MCP 도구가 늘어날수록 tool description 품질이 agent 성능을 직접 바꾼다.

**Anthropic MCP code execution**: tool universe가 커지면 upfront로 모든 tool을 보여주는 방식은 token budget을 잠식. 해결책: tool exposure virtualization.

**OpenDev 논문**: MCP tool을 lazy discovery로 불러와 prompt budget을 절약. Registry 기반 tool layer.

**Meta agentic program repair**: 표준 unified diff보다 search-and-replace 포맷이 agent에게 더 자연스러워 성능이 높았다. **Tool의 format 자체가 harness design decision**.

### 4-5. Eval과 observability는 부가 기능이 아니다

**Anthropic**: eval은 one-off experiment가 아니라 production regression을 조기에 잡는 운영 장치. 좋은 harness는 실행 loop와 측정 loop를 동시에 가진다.

**LangChain**: eval 수준 3단계 — single-step (국소 의사결정), full-turn (한 번의 완결된 실행), multi-turn (상호작용 지속성).

**VeRO 논문**: agent optimizer를 비교하려면 target agent보다 먼저 evaluation harness를 제대로 설계해야 한다. versioned snapshot + structured trace + budgeted evaluator.

**Anthropic multi-agent**: 초반에는 큰 eval 세트보다 약 20개 정도의 real usage query만 있어도 prompt 변경의 큰 효과를 잡아낼 수 있다. LLM-as-judge로 0.0-1.0 점수와 pass/fail을 같이.

### 4-6. Deterministic constraint가 AI 자율성을 높인다 — 역설

**Fowler harness engineering**: "더 높은 AI 자율성을 얻으려면 오히려 runtime과 solution space를 더 강하게 제한해야 할 수 있다."

**AutoHarness**: rejection-sampling style harness (propose_action + is_legal_action)가 Gemini-2.5-Flash의 illegal move를 완전히 제거하고, 더 큰 모델을 능가하게 함.

**OpenDev 5-layer safety**: prompt guardrail → schema-level restriction → runtime approval → tool-level validation → lifecycle hooks. 층위별 제약이 오히려 안전한 자율성을 가능하게 한다.

**Meta agentic program repair**: static analysis + test execution feedback의 neuro-symbolic loop. Agent 단독보다 외부 검증을 넣은 구성이 훨씬 좋았다 (42.3% solve rate).

---

## 5. 학술 문헌의 상태

학술 쪽은 아직 "harness engineering"이라는 exact phrase보다 인접 개념이 더 많다. 실무 담론이 먼저 폭발했고, 논문은 그 주변의 부분문제들을 따라잡는 단계에 가깝다.

### 직접 관련 논문 3편

| 논문 | 핵심 기여 | Harness 관점 |
|------|----------|-------------|
| **AutoHarness** (2026-02) | task-specific code harness를 tree search + Thompson sampling으로 자동 합성 | guardrail code 자동 생성. 모델 reasoning을 키우는 것보다 외부 constraint layer를 합성하는 편이 효과적 |
| **VeRO** (2026-02) | agent가 다른 agent를 개선하는 과정을 reproducible하게 측정하는 eval harness | self-improving agent 연구의 기본 인프라. Versioned snapshot + budgeted evaluator |
| **OpenDev/Building AI Coding Agents** (2026-03) | terminal-native coding agent의 scaffolding, harness, context engineering을 compound system으로 문서화 | scaffolding (첫 prompt 전 assembly)과 harness (runtime dispatch/context/safety)를 명시적으로 분리 |

### 가까운 기반 연구 3편

| 논문 | 핵심 기여 | Harness 관점 |
|------|----------|-------------|
| **Meta Context Engineering** (2026-01) | bi-level optimization으로 CE skill 진화. 평균 16.9% 상대 향상 | harness 설계 기술 자체를 agent가 탐색하게 하는 시도. 장기적 harness 자동화의 전조 |
| **Structured Context Engineering** (2026-02) | 9,649 실험으로 format/architecture/scale 비교 | "grep tax" 발견: compact format이 파일은 작아도 runtime token을 늘릴 수 있다. Harness의 model-specific 설계 필요성 |
| **CEDAR** (2026-01) | DS용 structured prompt + 3-agent + local execution + history rendering | 도메인이 달라도 harness 패턴은 같다: structured input + role separation + external execution + context management |

### 평가/검증 인프라 연구 4편

| 논문 | 핵심 기여 | Harness 관점 |
|------|----------|-------------|
| **SEC-bench** (2025-06) | 200개 실제 CVE로 보안 agent 평가. Sanitizer 기반 오라클 | eval harness = benchmark construction harness. 보안에서는 production-like environment reconstruction이 필수 |
| **GitTaskBench** (2025-08) | 54 현실 태스크. 실패 50%+ environment setup 문제 | alpha metric (success quality × token cost × salary). 환경 준비가 agent 성능의 핵심 병목 |
| **PerfBench** (2025-09) | 81개 .NET 성능 버그. Agent가 직접 benchmark 생성해야 | measurement harness가 곧 task definition. 비기능 품질에서 harness의 역할 |
| **Agentic Program Repair** (2025-07) | Meta 모노레포 production repair loop. 25.5% landed | test failure bot → repair agent → verifier → judge → human의 다층 production harness |

---

## 6. 실무 패턴: 가장 많이 반복된 것들

### 패턴 1: Repo를 agent-readable하게 만든다
- 규칙, 스펙, 실행 방법, 테스트 방식을 파일로 외부화
- CLAUDE.md, .cursorrules, AGENTS.md 같은 agent-readable knowledge base
- 코드베이스가 인간뿐 아니라 agent에게도 읽히고 수정되기 쉬워야 한다 (agent legibility)

### 패턴 2: 역할을 분리한다
- Initializer + Coding agent (Anthropic long-running)
- Lead agent + Subagents + Citation agent (Anthropic multi-agent)
- Orchestrator + Text generator + Code generator (CEDAR)
- Planning + Execution 분리 (OpenDev Extended ReAct)
- Human → Intent/Review/Merge/Exception, Agent → Code/Test/Docs (OpenAI)

### 패턴 3: 도구는 명확한 계약으로 expose한다
- 이름과 경계가 명확하고 호출 계약이 예측 가능한 도구
- 도구 설명도 prompt의 일부이므로 eval로 다듬는다
- Agent가 tool을 테스트하고 description을 고치는 loop
- Large tool universe는 lazy discovery / virtualization으로 관리

### 패턴 4: 장기 작업은 checkpoint + artifact handoff로
- 한 번에 끝내려 하지 않는다. Feature-by-feature, checkpoint-by-checkpoint
- 세션 사이를 잇는 artifact를 남긴다 (코드 상태, TODO, 남은 위험)
- Within-run pruning과 across-run compaction을 분리
- Budget warning과 overflow recovery

### 패턴 5: 실패를 관찰하고 trace에서 개선 포인트를 추출한다
- Trace를 단순 로그가 아니라 optimization signal로
- Failure pattern을 자동 분류하고 개선 후보 생성
- Agent가 struggle하면 prompt가 아니라 환경을 바꾼다
- Eval은 운영 장치: regression 조기 감지

### 패턴 6: Deterministic checker로 경계를 강제한다
- Custom linters, structural tests, type checks
- Action filter/verifier (illegal action 차단)
- 5-layer defense-in-depth (OpenDev)
- Static analysis + test execution feedback loop (Meta)

### 패턴 7: 사람은 on the loop로 이동한다
- 코드를 직접 쓰기보다 intent, review, merge, exception handling에 집중
- 결과물이 아니라 결과물을 만드는 loop를 교정
- Task batching과 intent specification에 시간을 쓴다
- Agent throughput에 맞춘 merge/review 방식 재설계

---

## 7. 핵심 긴장과 미해결 문제

### 7-1. Framework vs. Substrate

Inngest는 "framework를 고를 것인가"보다 "어떤 durable substrate 위에 agent loop를 올릴 것인가"를 먼저 묻는다. LangChain은 framework가 evolving best practice를 system primitive로 굳히는 층이라 사라지지 않는다고 반박한다. 이 긴장은 아직 해소되지 않았다.

### 7-2. Agent Legibility vs. Human Legibility

OpenAI의 "agent legibility" 주장은 코드가 agent에게 최적화되어야 한다고 본다. 그러나 Fowler는 정돈된 구조의 코드베이스가 LLM에게도 더 빨리 이해된다고 본다. 두 legibility가 항상 수렴하는지, 혹은 긴장이 생기는지는 아직 경험적 증거가 부족하다.

### 7-3. 자율성 vs. 제약의 최적 지점

Fowler: "더 높은 AI 자율성을 얻으려면 오히려 더 강한 제약이 필요할 수 있다." AutoHarness는 이를 실험적으로 확인했지만, 일반 소프트웨어 개발에서 제약의 정도를 어떻게 calibrate할지는 열려 있다.

### 7-4. Harness의 자동 합성과 유지보수성

AutoHarness는 harness code를 자동 생성하는 데 성공했지만, TextArena 게임이라는 제한된 환경이다. Generated harness가 장기적으로 readable하고 maintainable한지, 실무 코드베이스에서 어떻게 versioning할지는 추가 검증이 필요하다.

### 7-5. Eval의 현실성 문제

벤치마크는 늘고 있지만 production drift를 완전히 대변하진 못한다. GitTaskBench의 alpha metric처럼 경제적 효용까지 포함한 평가가 필요하지만, salary와 token cost 가정에 민감하다. VeRO의 budgeted evaluator도 evaluation call 수로만 정의해 token/API cost variance를 완전히 통제하지 못한다.

### 7-6. 조직 설계의 공백

Harness engineering이 조직 운영 모델까지 바꾼다는 주장은 설득력 있지만, 체계적인 연구는 아직 없다:
- Agent throughput 증가에 따른 merge/ownership 변화
- Code review bottleneck 해소 전략의 비교
- 팀 규모별 harness engineering 성숙도 모델
- ROI를 보여주는 공개 데이터

### 7-7. Mid-run Steering

Inngest는 "새 메시지가 오면 이전 run을 취소하고 다시 시작하는 정책"의 trade-off를 인정한다. Agent가 작업 중일 때 사람이 방향을 바꾸려 하면 어떻게 해야 하는가는 아직 설계 중인 영역이다.

---

## 8. 인사이트: 문헌을 관통하는 숨은 패턴들

### 인사이트 1: Harness engineering은 "소프트웨어 엔지니어링의 메타화"다

전통적 소프트웨어 엔지니어링에서 프로그래머는 코드를 작성하고, 코드가 시스템을 만든다. Harness engineering에서 엔지니어는 **코드를 작성하는 시스템(harness)**을 설계하고, 그 시스템이 코드를 만든다. 이는 한 단계 위의 추상화다.

이 메타화는 여러 문헌에서 다른 말로 반복된다:
- OpenAI: "인간의 역할이 코드 작성에서 environment shaping으로 이동"
- Fowler: "산출물을 직접 수정하지 않고, 산출물을 만들어낸 loop를 교정"
- Mitchell H.: "agent가 독립적으로 useful work을 할 수 있게 환경을 정비"
- DEV Community: "팀이 통제할 수 있는 레버는 harness뿐"

### 인사이트 2: 네 가지 다른 "harness"가 같은 이름을 쓰고 있다

문헌을 정밀하게 읽으면, "harness"라는 단어가 실제로는 네 가지 다른 레벨에서 사용된다:

1. **Execution harness**: agent loop의 runtime substrate. Step durability, retry, concurrency (Inngest)
2. **Context harness**: 모델에 들어가는 입력면의 설계. Prompt, tools, memory, rules (Anthropic, Manus)
3. **Eval harness**: agent 행동을 측정하고 채점하는 인프라 (VeRO, SEC-bench, LangChain)
4. **Organizational harness**: repo 구조, merge 철학, review 방식, 역할 재배치 (OpenAI, ignorance.ai)

이 네 레벨이 하나의 "harness engineering" 아래 묶여 있다는 것이 현재 담론의 강점이자 혼란의 원인이기도 하다. 실무에서는 자신이 다루는 레벨을 명확히 인식하는 것이 중요하다.

### 인사이트 3: Harness engineering은 "shift-left"의 극단적 확장이다

Fowler의 "humans on the loop"에서 핵심 논리는 classic shift-left다: 마지막 검토를 늘리는 대신, agent가 더 앞단에서 quality signal을 받도록 한다. 이를 극단까지 밀면:

- Test-first가 아니라 **constraint-first**: agent가 코드를 쓰기 전에 linter, type checker, structural test가 경계를 정한다
- Review-last가 아니라 **review-as-loop-design**: 사람이 산출물을 읽는 게 아니라 loop의 규칙을 바꾼다
- Deploy-then-monitor가 아니라 **trace-then-improve**: production observability가 harness 개선 신호를 공급한다

### 인사이트 4: "Grep tax"와 format paradox

Structured Context Engineering 논문의 발견은 실무적으로 매우 중요하다: compact하거나 novel한 format이 파일 크기는 작아도 **grep output density나 unfamiliarity 때문에 runtime token 사용량을 늘릴 수 있다**. 즉 "정보를 압축하면 agent에게 좋을 것"이라는 직관이 항상 맞지는 않다. Agent가 실제로 어떻게 정보를 탐색하는지 관찰해야 한다.

이는 Anthropic의 "thinking in context"와 같은 맥락이다: context shape가 agent 행동을 유도하는 방식을 역으로 보며 설계해야 한다.

### 인사이트 5: 수렴 가설 — AI 친화적 tech stack으로의 수렴

Fowler는 "장기적으로 AI 친화적 harness가 잘 갖춰진 일부 tech stack과 application topology 쪽으로 수렴이 일어날 가능성"을 제시한다. 이를 다른 문헌과 연결하면:

- Agent-readable repo 구조가 표준화될 수 있다
- Custom linter + structural test + knowledge doc + context provider를 갖춘 harness가 **golden path template**이 될 수 있다
- 이는 현재의 microservice template/platform engineering과 유사한 궤적을 그릴 수 있다

이 수렴은 기회이자 위험이다. Service template가 포크와 동기화 문제를 겪듯, harness template도 팀별 변형과 공통 기반 간의 긴장을 가질 것이다.

### 인사이트 6: 비용-가치 경계가 harness 설계를 제약한다

Anthropic multi-agent: agent는 ~4배, multi-agent는 ~15배 토큰을 쓴다. 가치가 높은 작업에서만 경제성이 나온다. GitTaskBench의 alpha metric은 solve rate와 비용을 함께 본다. 즉 **harness를 얼마나 정교하게 만들 것인가는 task의 경제적 가치에 의해 결정**된다. 모든 작업에 full harness를 적용하는 것은 과잉이고, 핵심 high-value task에 집중하는 것이 현실적이다.

---

## 9. 추천 읽기 순서

### 빠른 이해 (3편)
1. **Mitchell Hashimoto "My AI Adoption Journey"** — 왜 harness engineering이 필요한지 체감
2. **OpenAI "Harness engineering"** — 기준점이 되는 정의와 사례
3. **Martin Fowler "Harness Engineering"** — 개념 경계와 구성 요소 정리

### 기술적 깊이 (5편 추가)
4. **Anthropic "Effective harnesses for long-running agents"** — 장기 작업의 harness 패턴
5. **Anthropic "Effective context engineering"** → **"Context Engineering for Coding Agents"** — 내부 레이어 이해
6. **Inngest "Your Agent Needs a Harness, Not a Framework"** — runtime/infrastructure 면
7. **LangChain "Improving Deep Agents with harness engineering"** — 정량적 증거
8. **Martin Fowler "Humans and Agents in Software Engineering Loops"** — 인간-에이전트 협업 모델

### 전체 맥락 (5편 추가)
9. **Anthropic "Multi-agent research system"** — 가장 구체적인 초기 사례
10. **Anthropic "Demystifying evals"** — eval 설계 원칙
11. **OpenAI "Unrolling" → "Unlocking"** — runtime semantics에서 shared service로
12. **AutoHarness 논문** — harness 자동 합성의 가능성
13. **OpenDev 논문** — 학술적 종합 보고서

---

## 10. 최종 판단

2025년 6월 이후의 문헌을 종합하면, harness engineering은 유행어가 아니라 에이전트 실전 배치에서 생겨난 **설계 discipline**으로 보는 편이 타당하다.

**왜 유행어가 아닌가:**
- 여러 독립적인 조직(Anthropic, OpenAI, LangChain, Inngest, Meta, 개인 개발자)이 각자의 실무에서 같은 문제를 발견하고 같은 패턴에 수렴했다
- 정량적 증거가 존재한다 (Terminal Bench, AutoHarness, PerfBench)
- 학술 논문이 인접 문제를 정식화하기 시작했다

**현재 성숙도:**
- 개념 정의: 안정화 진입 (Fowler, OpenAI가 경계를 그음)
- 실무 패턴: 축적 중 (7가지 반복 패턴이 형성)
- 정량적 검증: 초기 (Terminal Bench, AutoHarness 정도)
- 학술적 정식화: 시작 단계 (직접 논문 3편)
- 조직 설계 연구: 거의 없음
- 표준화/템플릿화: 아직 없음

**앞으로 주시할 방향:**
1. Harness 자동 합성의 범용화 (AutoHarness → 일반 소프트웨어)
2. Agent가 harness를 개선하는 flywheel의 실제 사례
3. 조직 운영 모델 변화에 대한 체계적 연구
4. Harness template / golden path의 표준화
5. 비용-효과 분석 프레임워크의 성숙
