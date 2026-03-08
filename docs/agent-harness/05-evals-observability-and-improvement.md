# 05. Evals, Observability, and Improvement

Harness는 실행만 잘하면 끝나지 않는다. 이 문서는 `어떻게 측정하고`, `어디를 관찰하고`, `무엇을 바꿔야 하는지`를 판단하는 evaluation harness와 observability layer를 실전 관점으로 다시 정리한다. 핵심은 모든 eval을 한 종류로 보지 않는 것이다. production eval, benchmark eval, optimizer eval, verifier stack은 서로 다른 목적과 trade-off를 가진다.

## 핵심 주장

- 좋은 harness는 실행 루프와 함께 `측정 루프`를 가진다.
- eval은 최종 문자열 채점이 아니라 trajectory, environment state, side effect, cost, retry budget까지 포함하는 시스템 평가다.
- trace는 로그가 아니라 optimization signal이며, observability는 디버깅 도구를 넘어 harness 개선의 입력이다.

## 전체 코퍼스 종합

### agent eval이 model eval과 다른 이유

- Anthropic은 agent가 tool을 호출하고 환경 상태를 바꾸며 trajectory를 남기기 때문에, 최종 답 문자열만 비교하는 방식은 불충분하다고 본다.
- LangChain은 deep agent 평가에서 datapoint마다 bespoke test logic이 필요하다고 말한다.
- VeRO는 optimizer agent 평가조차 stochastic LLM behavior와 deterministic code execution이 섞여 있어 재현이 어렵다고 본다.

### 자료 비교

- Anthropic은 agent eval을 `trajectory + final response + environment state + grader logic`의 조합으로 설명한다.
- LangChain은 여기에 `single-step / full-turn / multi-turn`이라는 레벨 구분을 추가한다.
- VeRO는 같은 문제를 재현성, versioning, budget enforcement 요구사항으로 뒤집어 설명한다.

결국 세 접근은 같은 결론으로 모인다. `agent eval은 실행 환경을 포함한 시스템 평가`다.

### 평가 레벨의 계층

| 레벨 | 질문 | 대표 자료 | 놓치기 쉬운 것 |
|------|------|----------|---------------|
| Single-step eval | 특정 tool 선택이나 한 번의 판단이 맞았는가 | Anthropic evals, LangChain evals | 전체 task 성공 여부 |
| Full-turn eval | 한 번의 task run이 성공했는가 | LangChain evals, GitTaskBench, PerfBench | 장기 세션 continuity |
| Multi-turn eval | 긴 상호작용과 세션 전환을 견디는가 | Anthropic long-running, Inngest, VeRO | single-step의 지역적 품질 |

좋은 harness는 이 세 수준을 혼동하지 않는다. single-step이 좋아도 handoff가 깨지면 long-running coding agent는 실패한다.

### Production eval

production eval은 `실제 agent를 개선하기 위한 내부 측정 루프`다.

- Anthropic은 early stage에서는 소수의 현실적인 case로 시작하고, failure mode가 발견될 때마다 eval suite를 키우라고 한다.
- LangChain은 trace와 task-specific verifier를 연결해 harness 변경 전후를 비교한다.
- Meta repair는 triage -> repair -> static analysis/test -> LLM judge -> human review의 production verifier stack을 운영한다.

### 자료 비교

- Anthropic은 rubric과 LLM judge, 인간 평가의 조합을 강조한다.
- LangChain은 trace-based optimization을 위해 bespoke test logic과 environment control을 강조한다.
- Meta repair는 production patching 환경에서 deterministic verifier와 human gate를 계층화한다.

이 셋을 합치면 production eval의 기본 형태가 나온다. `현실 task`, `재현 가능한 환경`, `자동 검증`, `trace`, `최종 human judgment`의 조합이다.

### Benchmark eval

benchmark eval은 `모델 또는 harness variant를 비교하기 위한 공통 실험장`에 더 가깝다.

- SEC-bench는 sanitizer oracle과 Docker environment를 묶어 security task benchmark harness를 만든다.
- GitTaskBench는 repository-aware task runner와 automated evaluation harness를 제공한다.
- PerfBench는 agent가 benchmark를 생성하고, harness가 buggy/fixed 양쪽에서 실행해 비기능 품질을 측정한다.

### 자료 비교

- SEC-bench는 benchmark construction harness가 본체다. 환경을 재구성하지 않으면 보안 task 평가가 성립하지 않는다.
- GitTaskBench는 environment setup 자체를 현실 task의 일부로 드러낸다.
- PerfBench는 measurement harness가 task definition이 되는 사례다. 성능 버그는 unit test만으로 평가할 수 없기 때문이다.

benchmark eval은 production suitability를 완전히 대체하지 않지만, variant 비교와 회귀 감지에 매우 강하다.

### Optimizer eval

optimizer eval은 `agent가 다른 agent를 개선하는 과정` 자체를 평가한다.

- VeRO는 versioning, rewards, observations를 evaluation harness 핵심으로 둔다.
- budget enforcement, permission control, reproducible execution, structured tracing이 없으면 optimizer 결과를 비교할 수 없다고 본다.
- Meta Context Engineering은 CE skill 자체를 진화 대상으로 삼는다. production harness라기보다 연구용 optimization loop지만, `harness 변경을 search space로 다룬다`는 점에서 optimizer eval과 연결된다.

### 자료 비교

- VeRO는 매우 엄격한 평가 인프라를 요구한다. git worktree, experiment database, evaluator abstraction이 핵심이다.
- Meta Context Engineering은 더 연구적이지만, 사람 손 대신 agent가 harness-like skill을 탐색한다는 점에서 self-improving 방향성을 보여준다.
- Fowler의 agentic flywheel은 이 논리의 organizational version이다. production telemetry와 business outcome까지 harness 개선 입력으로 넣으려 한다.

### Verifier stack

verifier stack은 eval과 runtime 사이에 있는 층이다. `실행 중 혹은 종료 직전 agent 결과를 외부 기준으로 검사하는 장치`를 뜻한다.

- LangChain PreCompletionChecklist는 가장 얕은 verifier stack이다.
- Meta repair의 static analysis + test execution + LLM judge + human review는 가장 두꺼운 verifier stack이다.
- OpenDev의 layered safety는 verifier stack과 action constraint가 결합된 형태다.
- PerfBench의 benchmark execution, SEC-bench의 sanitizer oracle도 domain-specific verifier다.

### 자료 비교

- LangChain은 completion quality와 premature completion 방지에 초점을 둔다.
- Meta는 patch quality와 regression 방지에 초점을 둔다.
- PerfBench/SEC-bench는 domain-specific measurable oracle을 만든다.

따라서 verifier stack은 `무엇을 성공으로 볼 것인가`에 따라 달라져야 한다.

### 환경 재현성이 왜 먼저인가

- LangChain은 `environment > grader`라고까지 말한다.
- GitTaskBench, SEC-bench, PerfBench는 모두 환경 재구성을 benchmark 본체로 다룬다.
- VeRO는 versioned snapshots와 controlled filesystem access를 평가 harness 필수 요건으로 둔다.

재현 가능한 환경이 없으면 모델 변경인지, harness 변경인지, 환경 변동인지 분리할 수 없다.

### trace와 observability는 어떻게 쓰이는가

- Anthropic multi-agent는 tracing 없이는 비결정적 long-running behavior를 이해하기 어렵다고 본다.
- LangChain은 LangSmith trace를 실패 패턴 분류와 개선 후보 도출에 직접 사용한다.
- Fowler는 나중에 agent가 harness 변경까지 제안하는 flywheel을 상상한다.

### 자료 비교

- Anthropic은 tracing을 debugging necessity로 본다.
- LangChain은 tracing을 optimization infrastructure로 끌어올린다.
- Fowler와 Meta Context Engineering은 tracing 이후의 meta-optimization까지 본다.

즉 observability는 `무엇이 일어났는지 보기 위한 눈`에서 `무엇을 바꿔야 하는지 찾는 검색 엔진`으로 진화한다.

## agent 개발에서의 사용 방식

### coding/terminal agent용 실전 eval stack

1. `Local verifier`
   - smoke test, lint, type check
2. `Task acceptance`
   - feature-specific tests, CLI scenario, output schema checks
3. `Full-turn task replay`
   - 같은 repo 상태에서 task 재실행
4. `Long-running / resume eval`
   - checkpoint 이후 이어서 성공하는지
5. `Domain-specific verifier`
   - performance benchmark, sanitizer, migration checker 등
6. `Human review`
   - high-risk change, weak oracle, business judgment

### harness 변경을 적용할 때의 기본 루프

1. trace와 실패 사례를 수집한다.
2. failure mode를 분류한다.
3. 어느 harness 레이어를 바꿀지 결정한다.
4. 같은 환경에서 재실행한다.
5. solve rate뿐 아니라 variance, cost, regression을 함께 본다.

### 초기에 무엇부터 만들까

- replay 가능한 몇 개의 현실 task
- trace와 run metadata 저장
- deterministic한 smoke verifier
- task별 acceptance check
- 실패 taxonomy를 붙인 간단한 regression suite

### 언제 benchmark가 필요한가

- variant 비교를 반복적으로 해야 할 때
- 회귀 비용이 커서 자동 비교가 필요할 때
- `좋아진 것 같다`가 아니라 score/lift로 의사결정해야 할 때
- production data만으로는 드리프트 때문에 비교가 어려울 때

### 언제 human review를 남겨야 하나

- deterministic oracle이 없을 때
- 비기능 품질이나 taste judgment가 중요할 때
- production impact가 큰 migration/security/infra change일 때
- optimizer agent가 broader harness를 바꾸는 경우

## 설계 원칙

- eval 환경을 먼저 고정하고 grader를 정교화한다.
- final answer만 보지 말고 trajectory와 environment state를 함께 저장한다.
- production eval, benchmark eval, optimizer eval을 목적별로 구분한다.
- verifier stack은 task risk와 oracle 강도에 맞춰 두껍게 혹은 얇게 만든다.
- trace는 구조화된 optimization signal로 저장한다.
- regression과 variance를 함께 본다.
- cost, latency, token budget도 평가 항목에 포함한다.

## 반론/한계

- benchmark는 현실을 축소한다. GitTaskBench, PerfBench, SEC-bench는 유용하지만 production drift를 완전히 대표하지 않는다.
- LLM judge는 편향과 불안정성이 있으며 deterministic oracle이 없을 때 보조적으로 써야 한다.
- trace가 많아질수록 분석 비용도 커진다. 수집보다 해석 체계가 더 중요하다.
- self-improving flywheel은 매력적이지만, VeRO가 지적하듯 현재 optimizer agent는 prompt modification에 과도하게 의존하는 경향이 있다.

## 관련 자료 묶음

- 직접 문헌: Anthropic `Demystifying evals for AI agents`, LangChain `Evaluating Deep Agents: Our Learnings`, LangChain `Improving Deep Agents with harness engineering`, Martin Fowler `Humans and Agents in Software Engineering Loops`
- 기반 문헌: Anthropic `How we built our multi-agent research system`, Anthropic `Effective harnesses for long-running agents`, LangChain `On Agent Frameworks and Agent Observability`
- 인접 논문: `VeRO`, `SEC-bench`, `GitTaskBench`, `PerfBench`, `Agentic Program Repair from Test Failures at Scale`, `Meta Context Engineering via Agentic Skill Evolution`
