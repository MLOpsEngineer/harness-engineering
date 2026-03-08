# 07. Source Crosswalk and Coverage Audit

이 문서는 수집한 31개 자료 전체가 심화 리비전된 본문에 어떻게 반영되었는지 감사하기 위한 crosswalk다. 목적은 세 가지다.

- `누락 자료 0건`을 확인한다.
- 각 자료가 어떤 핵심 주장군의 근거로 쓰였는지 추적한다.
- 자료 간 상충 논점이 어디에서 다뤄졌는지 확인한다.

## 태그 범례

- 정의: harness의 개념과 경계
- 중요성: 왜 harness가 중요한지, ROI와 병목 설명
- context: prompt, memory, files, compaction, retrieval
- tool: 도구 계약, tool surface, MCP, virtualization
- runtime: loop, orchestration, execution semantics
- durability: checkpoints, handoff, retry, persistence
- safety: guardrail, approval, legality filtering
- eval: benchmark, grader, verifier, regression
- observability: trace, monitoring, analysis
- human loop: humans in/on the loop, approval, review
- 조직: repo legibility, merge, operating model
- 정량: 수치와 empirical evidence
- 한계: 적용 범위, 반례, trade-off

## 블로그/아티클 소스 매트릭스

| 자료 | 성격 | 핵심 기여 문장 | 주요 기여 태그 | 핵심 주장군 | 본문 반영 위치 | 충돌 / 주의점 |
|------|------|---------------|----------------|------------|---------------|---------------|
| Anthropic `How we built our multi-agent research system` | 기반 | 병렬 subagent와 context compression이 path-dependent research task에서 큰 lift를 만들 수 있음을 보여준다. | 중요성, context, tool, runtime, durability, eval, observability, 정량, 한계 | 왜 중요한가, 패턴 선택, eval | 02, 04, 05 | coding task에는 병렬화 이점이 제한적일 수 있음 |
| Manus `Context Engineering for AI Agents` | 기반 | 대화 히스토리 대신 files, todo, artifacts로 상태를 외재화해야 long-running agent가 안정화된다. | context, durability, runtime, 한계 | 정의와 경계, 개발 수명주기, 설계 패턴 | 01, 03, 04 | file-native 접근이 모든 모델에 항상 유리한 것은 아님 |
| Anthropic `Writing effective tools for AI agents` | 기반 | tool 이름, schema, 반환값 계약이 agent 성능을 직접 좌우하는 input surface다. | tool, eval, 한계 | 설계 패턴, eval | 04, 05 | tool-centric라 조직 운영 논의는 약함 |
| Anthropic `Effective context engineering for AI agents` | 기반 | prompt engineering보다 넓은 context lifecycle 관리가 agent behavior를 결정한다. | 정의, context, 한계 | 정의와 경계, 개발 수명주기 | 01, 03 | 실행/조직 레이어는 직접 다루지 않음 |
| Anthropic `Code execution with MCP` | 기반 | large tool universe는 virtualization과 lazy loading 없이는 context budget을 잠식한다. | tool, runtime, context, 한계 | 설계 패턴 | 04 | code execution abstraction이 새 복잡성을 만듦 |
| Anthropic `Effective harnesses for long-running agents` | 직접 | long-running coding agent의 본질 문제는 세션 간 handoff 실패이며, initializer/coding 분리와 checkpoint가 핵심 해법이다. | 정의, runtime, durability, human loop, 한계 | 정의, 중요성, 개발 수명주기, 설계 패턴 | 01, 02, 03, 04, 06 | 작은 작업에는 overhead가 될 수 있음 |
| LangChain `Evaluating Deep Agents: Our Learnings` | 기반 | agent eval에서는 grader보다 재현 가능한 environment가 더 중요하다. | eval, observability, 한계 | eval/observability | 05 | LangSmith 의존도가 높음 |
| Anthropic `Demystifying evals for AI agents` | 기반 | trajectory, final response, environment state, grader logic을 함께 봐야 agent eval이 성립한다. | eval, observability, 정의 | 정의, eval/observability | 01, 05 | 구체 구현보다 프레임 중심 |
| OpenAI `Unrolling the Codex agent loop` | 기반 | prompt assembly, tool dispatch, observation formatting, termination이 agent quality를 결정하는 runtime semantics다. | 정의, runtime, 한계 | 정의와 경계, 개발 수명주기, 설계 패턴 | 01, 03, 04 | 상위 조직 운영 문제는 직접 다루지 않음 |
| OpenAI `Unlocking the Codex harness` | 직접 | harness는 개별 UI 내부 로직이 아니라 여러 surface가 공유하는 runtime service가 될 수 있다. | runtime, 조직, human loop, 정의 | 정의와 경계, 설계 패턴, 운영 모델 | 01, 04, 06 | 소규모 팀에는 과한 투자일 수 있음 |
| Mitchell Hashimoto `My AI Adoption Journey` | 직접 | 가치의 원천이 모델 품질에서 repo와 feedback environment 정비로 이동하는 시점을 `Engineer the Harness`로 설명한다. | 중요성, human loop, 조직, 한계 | 왜 중요한가, 운영 모델 | 02, 06 | 개인 실무 관찰 중심 |
| OpenAI `Harness engineering` | 직접 | 사람의 역할은 코드 작성보다 intent specification, feedback loop design, environment shaping으로 이동한다. | 정의, 중요성, human loop, 조직, 한계 | 정의, 중요성, 개발 수명주기, 운영 모델 | 01, 02, 03, 06 | 정량적 공개 데이터는 제한적 |
| LangChain `On Agent Frameworks and Agent Observability` | 기반 | agent system은 framework와 독립 observability가 필요한 모델 바깥의 시스템이다. | 정의, observability, 조직, 한계 | 정의와 경계, eval/observability | 01, 05 | framework defense 성격이 강함 |
| LangChain `Improving Deep Agents with harness engineering` | 직접 | 같은 모델에서 middleware와 trace-based 개선만으로 큰 benchmark lift를 만들 수 있다. | 중요성, runtime, eval, observability, 정량 | 왜 중요한가, 개발 수명주기, 설계 패턴, eval | 02, 03, 04, 05 | 특정 benchmark 최적화 가능성 |
| ignorance.ai `The Emerging Harness Engineering Playbook` | 직접 | background agent, parallel fleet, async workflow, human checkpoint 재배치가 반복되는 팀 패턴이다. | 중요성, human loop, 조직, 한계 | 왜 중요한가, 운영 모델 | 02, 06 | 2차 분석이라 원전 대비 해석 개입이 있음 |
| DEV `The Agent Harness Is the Architecture` | 직접 | production bottleneck은 model IQ보다 operational substrate라는 대중적 프레이밍을 제공한다. | 중요성, 정의, 조직 | 왜 중요한가, 운영 모델 | 02, 06 | 2차 해설 성격이 강함 |
| Martin Fowler `Context Engineering for Coding Agents` | 기반 | tools, MCP, skills, rules, specs를 통해 coding agent 입력면을 artifact network로 봐야 한다. | 정의, context, 조직, 한계 | 정의와 경계, 개발 수명주기 | 01, 03 | taxonomy는 강하지만 계량 근거는 적음 |
| DEV `Building the Agent Harness` | 직접 | LLM, agent, system prompt, harness 중 팀이 가장 크게 통제할 수 있는 것은 harness다. | 중요성, 조직, human loop | 왜 중요한가, 개발 수명주기, 운영 모델 | 02, 03, 06 | field note 성격이 강함 |
| Inngest `Your Agent Needs a Harness, Not a Framework` | 직접 | retry, persistence, concurrency, event routing을 흡수하는 durable substrate가 agent 운영의 핵심이다. | 정의, runtime, durability, observability, human loop, 한계 | 정의, 중요성, 설계 패턴, eval, 운영 모델 | 01, 02, 04, 05, 06 | event-driven 구조가 아닌 팀에는 과할 수 있음 |
| Martin Fowler `Humans and Agents in Software Engineering Loops` | 기반 | humans on the loop로 이동해야 throughput mismatch를 피하고 harness를 반복 개선할 수 있다. | human loop, 조직, eval, 정의 | 정의, eval, 운영 모델 | 01, 05, 06 | 규범적 프레임이 강하고 구현 레시피는 적음 |
| Martin Fowler `Harness Engineering` | 직접 | harness는 context engineering, deterministic constraints, garbage collection을 함께 묶는 상위 discipline이다. | 정의, 중요성, runtime, 조직, 한계 | 정의, 중요성, 설계 패턴, 운영 모델 | 01, 02, 04, 06 | 2차 개념화 문헌이며 대안 구현은 제한적 |

## 논문 소스 매트릭스

| 자료 | 성격 | 핵심 기여 문장 | 주요 기여 태그 | 핵심 주장군 | 본문 반영 위치 | 충돌 / 주의점 |
|------|------|---------------|----------------|------------|---------------|---------------|
| `SEC-bench` | 인접 연구 | 보안 agent 평가는 Dockerized reproduction, sanitizer oracle, gold artifact를 갖춘 benchmark harness가 있어야만 성립한다. | eval, runtime, 정량, 한계 | eval/observability | 05 | security domain 특화 |
| `Agentic Program Repair from Test Failures at Scale` | 인접 연구 | production repair는 static analysis, test execution, judge, human review가 쌓인 verifier stack으로 수렴된다. | runtime, eval, human loop, 정량, 한계 | 왜 중요한가, 개발 수명주기, 설계 패턴, eval | 02, 03, 04, 05 | Meta 내부 인프라 전제가 강함 |
| `GitTaskBench` | 인접 연구 | 현실 task 실패의 큰 비율이 code generation이 아니라 environment setup과 repository leveraging에서 난다. | 중요성, eval, 정량, 한계 | 왜 중요한가, 개발 수명주기, eval | 02, 03, 05 | task 수와 domain coverage에 한계가 있음 |
| `PerfBench` | 인접 연구 | performance bug에서는 benchmark 생성과 metric comparison harness가 곧 task definition이 된다. | 중요성, eval, tool, 정량, 한계 | 왜 중요한가, 설계 패턴, eval | 02, 04, 05 | .NET 중심 도메인 |
| `CEDAR` | 인접 연구 | structured input, role separation, local execution, smart history rendering이 다른 도메인에서도 반복되는 harness pattern임을 보여준다. | context, runtime, 한계 | 정의, 설계 패턴 | 01, 04 | DS domain 특화 |
| `Meta Context Engineering via Agentic Skill Evolution` | 인접 연구 | harness-like context strategy 자체를 search space로 두는 meta-optimization이 가능함을 보여준다. | context, eval, 정량, 한계 | eval/observability | 05 | production 재현성은 낮음 |
| `Structured Context Engineering for File-Native Agentic Systems` | 인접 연구 | file-native retrieval의 효과는 model tier에 따라 달라지며 compact format도 grep tax를 낳을 수 있다. | context, 중요성, 정량, 한계 | 정의, 중요성, 설계 패턴 | 01, 02, 04 | SQL proxy task라는 한계 |
| `AutoHarness` | 직접 | stronger external constraints를 자동 합성하면 작은 모델도 큰 모델을 넘어설 수 있다. | 중요성, safety, runtime, 정량, 한계 | 왜 중요한가, 설계 패턴 | 02, 04 | TextArena setting에 제한됨 |
| `VeRO` | 직접 | optimizer agent를 비교하려면 versioning, budget enforcement, structured tracing을 갖춘 eval harness가 먼저 필요하다. | eval, observability, runtime, 정량, 한계 | 정의, eval/observability | 01, 05 | budget 정의가 token variance를 완전히 포착하지 못함 |
| `Building AI Coding Agents for the Terminal` | 직접 | scaffolding와 harness를 분리하고 terminal-native agent를 compound system으로 다뤄야 한다. | 정의, runtime, safety, 조직, 한계 | 정의, 개발 수명주기, 설계 패턴, 운영 모델 | 01, 03, 04, 06 | engineering report 성격이 강함 |

## 주장군별 근거 감사

| 주장군 | 직접 문헌 근거 | 기반 문헌 근거 | 논문 근거 | 주 반영 문서 | 감사 결과 |
|--------|----------------|---------------|----------|-------------|----------|
| harness의 정의와 경계 | OpenAI, Fowler, Inngest | Anthropic context eng., OpenAI unrolling | OpenDev, VeRO | 01 | 직접/기반/논문 모두 포함 |
| 왜 중요한가 | OpenAI, LangChain improving, Mitchell, DEV | Anthropic multi-agent, Anthropic long-running | AutoHarness, GitTaskBench, PerfBench | 02 | 정량/정성 근거 모두 포함 |
| agent 개발에서의 사용 방식 | OpenAI, Anthropic long-running | Manus, Anthropic context eng., Fowler context eng. | Meta repair, OpenDev, GitTaskBench | 03 | 수명주기 전 단계 비교 포함 |
| 설계 패턴과 아키텍처 | Inngest, OpenAI unlocking, Fowler harness eng. | Anthropic tools, Anthropic MCP, Anthropic multi-agent | AutoHarness, Structured Context Engineering, CEDAR | 04 | 패턴별 사용 조건/반례 포함 |
| eval, tracing, 개선 루프 | LangChain improving, Anthropic evals | Anthropic multi-agent, LangChain observability | VeRO, SEC-bench, GitTaskBench, PerfBench, Meta repair | 05 | production/benchmark/optimizer/verifier stack 분리 완료 |
| 사람과 조직 운영 | OpenAI, Mitchell, ignorance.ai, Fowler harness eng. | Fowler humans-and-agents, DEV | OpenDev, Meta repair | 06 | 개인/소규모 팀/플랫폼 팀 단계별 정리 완료 |

## 상충 주장 감사

| 논점 | 상반된 입장 | 현재 처리 위치 | 감사 메모 |
|------|-------------|---------------|----------|
| Framework vs Harness vs Substrate | LangChain은 framework의 지속 필요성을 강조, Inngest는 durable substrate 우선 | 01, 04, 05 | 층위 구분으로 정리했고 어느 하나를 절대화하지 않음 |
| 모델 vs 환경 | OpenAI/DEV/ignorance는 환경 우위, Structured Context Engineering은 모델 격차도 큼 | 02 | `일정 수준 이상에서 harness가 더 자주 병목`으로 정리 |
| 자율성 vs 제약 | Fowler/AutoHarness/OpenDev는 stronger constraints를 옹호 | 04 | risk-tiered constraints로 정리 |
| file-native retrieval의 가치 | Manus/Fowler 계열은 선호, Structured Context Engineering은 model-specific mixed result 제시 | 03, 04 | model-tier별 기본값으로 정리 |
| multi-agent의 coding 적합성 | Anthropic research는 큰 효과를 보고, 동시에 coding task 한계를 인정 | 02, 04 | task-selective pattern으로 정리 |
| prompt 변경 vs broader harness 변경 | VeRO는 optimizer가 prompt에 과의존, OpenAI/Fowler는 broader harness 변경을 강조 | 01, 05 | meta-optimization의 현재 한계로 명시 |

## 미해결 질문

- harness 자동 합성 결과물을 실무 코드처럼 versioning하고 유지보수할 수 있는가
- agent legibility와 human legibility가 항상 같은 방향으로 움직이는가
- background agent가 늘어날 때 ownership과 audit trail을 어떻게 유지할 것인가
- production task의 경제성을 token cost, review cost, rollback cost까지 포함해 어떻게 계산할 것인가
- mid-run steering과 human override를 durable execution 위에서 어떻게 다룰 것인가
- reasoning-heavy task에서 harness 최적화가 실제로 얼마나 더 여지가 있는가

## 최종 감사 결과

- 수집 자료 31건 모두 이 문서에 등장한다.
- 각 자료는 `07`뿐 아니라 최소 1개 이상의 본문 문서에서 실질 비교 근거로 쓰인다.
- 사용자 요구 핵심 질문인 `왜 중요한가`, `agent 개발에서 어떻게 쓰이는가`, `어떻게 설계해야 하는가`는 각각 02, 03, 04에서 독립적으로 답한다.
- `framework vs substrate`, `모델 vs 환경`, `자율성 vs 제약`, `file-native retrieval의 모델 의존성`, `multi-agent의 coding 적합성`은 별도 충돌 표와 본문 대응 위치를 갖는다.
