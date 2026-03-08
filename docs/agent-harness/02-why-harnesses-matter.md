# 02. Why Harnesses Matter

이 문서는 `왜 harness가 agent 개발의 핵심 레버가 되는가`를 정량 근거, 운영 근거, 비용 한계까지 함께 묶어 설명한다. 핵심 메시지는 단순하지만 오해하기 쉽다. `모델이 중요하지 않다`가 아니라, `일정 수준 이상의 모델 능력이 확보되면 실제 차이는 점점 harness에서 난다`는 것이다.

## 핵심 주장

- 좋은 모델만으로는 production-grade agent가 되지 않는다. 실행 환경, 검증 루프, context 관리, tool surface가 결과를 좌우한다.
- harness는 성능 향상뿐 아니라 실패 비용 감소, 회귀 방지, 인간 검토 부담 감소, 조직 처리량 증가를 만든다.
- 다만 harness가 만능은 아니다. reasoning-heavy task나 낮은 모델 capability 구간에서는 모델 자체가 여전히 병목일 수 있다.

## 전체 코퍼스 종합

### 가장 강한 정량 근거는 무엇인가

| 근거 | 수치 | 왜 중요한가 |
|------|------|-------------|
| LangChain `Improving Deep Agents with harness engineering` | Terminal Bench 2.0 `52.8 -> 66.5` | 같은 모델을 유지한 채 harness만 바꿔 큰 성능 향상을 얻은 대표 사례 |
| `AutoHarness` | 작은 모델 + learned harness가 더 큰 모델을 능가 | constraint layer가 모델 크기보다 강한 레버가 될 수 있음을 보여줌 |
| `PerfBench` | baseline 대비 최대 약 `5x` 개선 | 비기능 품질 task에서 harness가 측정 체계와 함께 성능을 좌우함 |
| `GitTaskBench` | 실패의 절반 이상이 environment setup / dependency resolution | 모델보다 environment preparation이 병목이 되는 현실을 보여줌 |
| Meta `Agentic Program Repair` | 생성 fix 중 `25.5%` landed | production에서도 verifier stack과 human gate가 실질 가치를 만듦 |

### 자료 비교: 같은 모델에서 무엇이 바뀌었나

- LangChain 사례에서 바뀐 것은 모델이 아니라 `middleware, LocalContext, completion checklist, loop detection, trace-based optimization`이었다.
- AutoHarness에서는 모델 reasoning 자체보다 `illegal action을 막는 외부 code harness`가 결과를 바꿨다.
- Anthropic multi-agent는 같은 모델 계열 안에서도 role separation, delegation heuristics, parallel tool calling, citation step 분리가 결과를 바꾼다고 보여줬다.

즉 공개 사례들이 공통으로 보여주는 것은 `모델 그대로 + harness 변경 = 큰 성능 차이`다.

### 왜 모델보다 harness가 더 큰 레버가 되나

- OpenAI는 agent-first 환경에서 인간 역할이 `코드 작성`보다 `환경 설계`로 이동한다고 봤다. 이는 차별화 포인트가 모델 API보다 repo legibility, feedback loop, review structure로 이동한다는 뜻이다.
- DEV와 ignorance.ai는 이를 `model is not the bottleneck`라는 문장으로 번역한다. leaderboard 차이보다 context, state persistence, observability, human checkpoint 설계가 production reliability를 더 많이 좌우한다는 주장이다.
- Anthropic의 멀티에이전트 연구 시스템은 model IQ보다 orchestration과 compression 전략이 path-dependent task 결과를 크게 바꿀 수 있음을 보여준다.
- Inngest는 한 걸음 더 내려가, 실제 실패는 모델 reasoning보다 `retry, persistence, concurrency, steering` 같은 runtime substrate에서 더 많이 난다고 주장한다.

### 자료 비교: repo와 environment가 병목이라는 근거

- OpenAI는 repository를 system of record로 삼고 architecture, constraints, taste를 agent-readable form으로 외부화해야 한다고 본다.
- Mitchell Hashimoto는 테스트, 문서, project structure를 정비하는 시간이 결국 가장 큰 복리 효과를 만든다고 말한다.
- GitTaskBench는 이것을 benchmark 차원에서 확인한다. 실패의 절반 이상이 코드 생성이 아니라 environment setup과 dependency resolution에서 발생했다.
- DEV 문헌들은 이를 실무자 언어로 다시 설명한다. 팀이 직접 통제할 수 있는 가장 큰 레버는 모델이 아니라 harness/environment라고 본다.

### harness가 만드는 네 가지 가치

### 1. 성능 향상

- LocalContext, tool contract 개선, completion checklist, better observation formatting은 같은 모델에서 더 높은 solve rate를 만든다.
- LangChain, Anthropic multi-agent, AutoHarness, PerfBench는 각기 다른 task에서 동일한 결론에 도달한다.

### 2. 안정성 향상

- Anthropic long-running harness는 작은 실패가 compound error가 되어 전체 trajectory를 무너뜨릴 수 있다고 본다.
- Inngest는 step-level retry와 durable execution으로 실패를 국소화한다.
- OpenDev는 layered safety와 event-driven reminders로 destructive terminal action과 long-horizon fade-out을 막으려 한다.

### 3. 측정 가능성

- Anthropic과 LangChain은 eval 없는 harness는 좋아졌는지 나빠졌는지 판단할 수 없다고 본다.
- VeRO는 optimizer agent조차 versioned snapshot과 budgeted evaluator 없이는 공정 비교가 어렵다고 본다.
- trace는 단순 로그가 아니라 `어떤 레버가 실제로 lift를 만들었는지` 보여주는 optimization signal이 된다.

### 4. 조직 처리량

- OpenAI, Mitchell Hashimoto, ignorance.ai는 agent throughput이 늘면 merge/review/cleanup 방식까지 같이 바뀌어야 한다고 본다.
- harness는 단순 실행 보조가 아니라 `더 많은 agent output을 조직이 소화할 수 있게 만드는 운영 장치`다.

### 경제성 한계도 함께 봐야 한다

- Anthropic multi-agent 문헌은 agent가 일반 chat보다 약 4배, multi-agent system은 약 15배 토큰을 더 쓴다고 적는다.
- GitTaskBench는 alpha value를 통해 solve rate만이 아니라 token cost, 개발자 비용, 성공 품질을 함께 봐야 한다고 주장한다.
- LangChain과 AutoHarness가 보여준 큰 개선도, 결국 가치가 큰 task에 투입될 때 의미가 커진다.

### 자료 비교: 깊은 harness가 항상 좋은가

- Anthropic multi-agent는 high-value research task에는 유리하지만, 코딩 task에서는 병렬화 이점이 더 작다고 인정한다.
- Inngest식 durable substrate는 long-running async agent에는 강력하지만, 짧은 one-shot CLI edit에는 과할 수 있다.
- shared runtime/App Server는 여러 product surface가 있을 때 큰 가치를 내지만, 단일 팀/단일 surface에서는 구현 비용이 더 커질 수 있다.

따라서 `최고로 깊은 harness`보다 `task 가치와 실패 비용에 맞는 harness 깊이`가 더 중요하다.

### 언제 harness가 병목이고 언제 모델이 병목인가

이 구분은 실제 투자 우선순위를 정할 때 가장 중요하다.

| 상황 | 더 자주 병목이 되는 것 | 근거 |
|------|----------------------|------|
| repo 탐색, dependency setup, long-running implementation | harness | GitTaskBench, OpenAI, Anthropic long-running |
| tool-rich workflow, async orchestration, background agent | harness | Inngest, LangChain, Anthropic multi-agent |
| legality filtering, safety enforcement, deterministic constraints | harness | AutoHarness, OpenDev, Fowler |
| deep reasoning-heavy academic/problem-solving task | 모델 | VeRO의 reasoning-heavy task 분석 |
| weaker/open-source model에서 file-native retrieval | 모델 + harness 둘 다 | Structured Context Engineering의 mixed result |

### 자료 비교: 모델이 여전히 병목인 구간

- VeRO는 tool-use-heavy task에서는 harness 최적화 lift가 잘 나오지만, reasoning-heavy task에서는 개선 폭이 더 작다고 보고한다.
- Structured Context Engineering은 frontier와 weaker model 간 capability gap이 여전히 크고, file-native retrieval의 효과도 model tier에 따라 달라진다고 말한다.
- 이는 `모델보다 harness`라는 문장을 절대화하면 안 된다는 뜻이다. 정확히는 `충분히 강한 모델 위에서 harness가 가장 큰 추가 레버가 되는 경우가 많다`가 맞다.

## agent 개발에서의 사용 방식

### 모델 교체 전에 먼저 검토할 체크리스트

1. agent가 task 범위와 완료 조건을 명확히 알고 있는가
2. repo 구조와 규칙이 agent-readable form으로 외부화되어 있는가
3. tool surface가 agent-friendly한가
4. context가 stale observation과 raw output으로 오염되고 있지 않은가
5. checkpoints, retries, validation, trace가 있는가
6. 실패를 재현하고 회귀를 감지할 eval 환경이 있는가

### harness 투자가 특히 큰 ROI를 내는 상황

- long-running coding agent를 운영할 때
- repo마다 setup과 실행 방식이 다를 때
- tool 수가 많아지고 MCP surface가 커질 때
- agent 산출물을 자동 검증할 수 있을 때
- background agent나 agent fleet을 병렬 운영하기 시작할 때
- 규제나 비용 때문에 실패 한 번의 대가가 클 때

### 최소 투자 순서

1. repo legibility와 verifier를 먼저 만든다.
2. tool contract와 local context 수집을 정리한다.
3. trace와 regression eval을 붙인다.
4. 그다음 durable execution, background agent, shared runtime, multi-agent를 검토한다.

### 자료 비교: 왜 이 순서인가

- OpenAI와 Mitchell은 repo와 feedback 환경 정비를 가장 먼저 둔다.
- LangChain과 Anthropic은 verification, checklist, trace가 없으면 반복 개선이 안 된다고 본다.
- Inngest와 OpenDev가 다루는 durability/safety/shared runtime은 고도화 단계에서 필요성이 커진다.

## 설계 원칙

- 모델 업그레이드보다 먼저 실패를 줄이는 harness 레버를 탐색한다.
- solve rate뿐 아니라 failure cost, token cost, review cost, replayability를 같이 측정한다.
- task가 tool-use-heavy한지 reasoning-heavy한지에 따라 기대 레버를 다르게 둔다.
- 값비싼 멀티에이전트 구조는 high-value task에만 배치한다.
- performance gain과 운영 안정성 gain을 구분해서 본다.
- 정량 근거가 있는 레버와 아직 사례 중심인 레버를 구분한다.

## 반론/한계

- LangChain과 AutoHarness의 결과는 강력하지만 각각 Terminal Bench, TextArena 같은 특정 환경에 최적화된 사례다.
- OpenAI와 Mitchell의 주장은 설득력 있으나 정량 데이터보다 현장 관찰에 가깝다.
- GitTaskBench와 PerfBench는 문제를 잘 보여주지만 task 분포와 생태계 편향이 있다.
- harness를 너무 넓게 정의하면 사실상 모든 엔지니어링 활동을 가리키게 될 위험이 있다.

## 관련 자료 묶음

- 직접 문헌: OpenAI `Harness engineering`, LangChain `Improving Deep Agents with harness engineering`, Mitchell Hashimoto `My AI Adoption Journey`, DEV `The Agent Harness Is the Architecture`
- 기반 문헌: Anthropic `How we built our multi-agent research system`, Anthropic `Effective harnesses for long-running agents`, Inngest `Your Agent Needs a Harness, Not a Framework`
- 인접 논문: `AutoHarness`, `GitTaskBench`, `PerfBench`, `Agentic Program Repair from Test Failures at Scale`, `VeRO`, `Structured Context Engineering`
