# 06. Humans, Organizations, and the Operating Model

Harness engineering은 도구 설계만이 아니라 `사람이 agent와 어떤 루프를 구성할 것인가`를 다시 정의한다. 이 문서는 human checkpoint, repo legibility, merge/review 재설계, background agent, async workflow를 `개인 -> 소규모 팀 -> 플랫폼 팀` 단계별 operating model로 정리한다.

## 핵심 주장

- agent-first 환경에서 사람의 역할은 직접 작성자에서 loop 설계자, 기준 관리자, 예외 승인자로 이동한다.
- review와 merge 방식을 바꾸지 않으면 agent throughput은 금방 인간 병목에 막힌다.
- repo legibility, approval policy, background agent, cleanup 루프도 모두 harness의 일부다.

## 전체 코퍼스 종합

### humans outside / in / on the loop

Martin Fowler의 분류는 조직적 harness를 이해하는 가장 좋은 프레임이다.

| 위치 | 인간 역할 | 장점 | 병목 |
|------|----------|------|------|
| Outside the loop | 결과만 요청하고 구현은 agent에 맡김 | 빠른 실험, 높은 자율성 | 내부 품질과 장기 유지보수성 통제 약함 |
| In the loop | 생성 결과를 매번 직접 검토하고 교정 | 통제력 큼 | agent throughput이 커질수록 review 병목 심화 |
| On the loop | 산출물보다 specs, checks, workflow guidance를 고침 | 재발 방지, 복리 효과 | 초기 설계와 품질 신호 구축이 필요 |

### 자료 비교

- Fowler는 이 구분을 delivery model 전체의 재편으로 본다.
- OpenAI는 같은 전환을 `intent specification, feedback loop design, environment shaping`으로 표현한다.
- Mitchell Hashimoto는 개인 워크플로 관점에서 같은 결론에 도달한다. 코드를 직접 쓰는 시간이 줄고 agent가 일할 환경을 정비하는 시간이 늘어난다.
- ignorance.ai는 이를 팀 운영 playbook으로 번역해 background agent, async workflow, human checkpoint 재배치로 정리한다.

핵심 공통점은 `사람이 최종 산출물을 끝없이 손으로 고치는 위치`에서 빠져나와야 한다는 것이다.

### repo legibility는 왜 조직 자산인가

- OpenAI는 `agent legibility`를 핵심 개념으로 제시한다.
- DEV와 Fowler는 rules, specs, README, CONTRIBUTING, CI 설정까지 모두 agent에게는 행동을 유도하는 정보 표면이라고 본다.
- Mitchell은 이런 정비가 한번 해두면 모든 후속 agent run에 재사용되는 복리 자산이라고 본다.
- GitTaskBench는 environment setup이 주요 실패 원인임을 보여주며, repo legibility 부족이 실제 성능 병목임을 간접적으로 뒷받침한다.

### 자료 비교

- OpenAI는 repo legibility를 조직 운영과 연결한다. merge/review/entropy control과 함께 본다.
- DEV는 이를 더 소박하게 풀어, 팀이 완전히 통제 가능한 레이어가 harness라고 말한다.
- Fowler는 같은 현상을 context configuration 경쟁이라고 부른다.

실무적으로 repo legibility는 `좋은 문서`가 아니라 `agent가 실패하지 않기 위한 실행 환경`이다.

### review와 merge는 왜 다시 설계해야 하나

- OpenAI는 agent throughput이 늘어나면 merge philosophy, garbage collection, review 방식이 같이 바뀌어야 한다고 본다.
- Fowler는 humans-in-the-loop 구조를 유지하면 throughput mismatch가 생긴다고 말한다.
- ignorance.ai는 작은 작업 배치, async workflow, 핵심 승인 지점만 남기는 human checkpoint 재배치를 playbook으로 정리한다.

### 자료 비교

- Fowler는 이 문제를 `사람의 attention을 어디에 둘 것인가`로 본다.
- OpenAI는 `throughput 증가 -> review redesign 필요`라는 운영 문제로 본다.
- ignorance.ai는 `background agent fleet + async workflow + human checkpoint`라는 팀 패턴으로 정리한다.

결론은 같다. review는 마지막에 더 많이 하는 것이 아니라, 더 앞단에서 더 구조적으로 해야 한다.

### background agent와 async workflow

- Mitchell Hashimoto는 항상 하나 이상의 agent가 백그라운드에서 돌고 있는 상태를 새로운 기본값으로 본다.
- ignorance.ai는 이를 parallel agent fleet과 async workflow로 일반화한다.
- Inngest는 이러한 background execution을 durable event substrate가 흡수해야 한다고 본다.
- Fowler harness engineering은 cleanup/garbage collection agent를 예로 들어, 문서 불일치나 규칙 위반을 주기적으로 찾아내는 loop도 harness에 포함한다.

### 자료 비교

- Mitchell의 배경 agent는 개인 생산성 감각에 가깝다.
- ignorance.ai는 그것을 팀 처리량 패턴으로 설명한다.
- Inngest는 실제 운영 substrate를 제시한다.
- Fowler는 그 결과를 entropy control과 maintenance loop로 개념화한다.

### 운영 모델을 팀 규모별로 보면

#### 1. 개인 개발자 단계

- 중심 패턴: repo legibility, rules 파일, background agent 1개, 명시적 verification
- 인간 역할: spec 제시, 결과 검토, 반복 실패 유형 파악
- 주요 위험: agent output은 많아졌는데 verification과 cleanup이 수동인 채로 남는 것

#### 자료 비교

- Mitchell과 DEV는 이 단계의 감각을 가장 잘 보여준다.
- OpenAI는 같은 패턴을 조직 수준 언어로 말하지만, 개인 개발자에게도 그대로 적용된다.

#### 2. 소규모 팀 단계

- 중심 패턴: shared rules, acceptance criteria, review checklist, 작은 PR, checkpointed approval
- 인간 역할: individual edit보다 exception approval과 scope control
- 주요 위험: agent-generated code가 PR queue를 밀어 review 병목이 생기는 것

#### 자료 비교

- Fowler humans-on-the-loop와 ignorance.ai playbook이 이 단계의 운영 모델을 가장 잘 설명한다.
- Anthropic long-running harness의 checkpoint와 handoff artifact도 팀 내 협업 비용을 낮추는 데 직접 연결된다.

#### 3. 플랫폼 팀 / 제품군 단계

- 중심 패턴: shared runtime, centralized execution backend, common safety policy, experiment store
- 인간 역할: platform guardrails, org-wide policies, reusable harness template 관리
- 주요 위험: 중앙 runtime이 단일 장애점이 되거나, 팀별 특성을 무시한 일괄 정책이 되는 것

#### 자료 비교

- OpenAI App Server가 가장 직접적인 shared runtime 사례다.
- Inngest는 shared substrate 관점에서 비슷한 문제를 푼다.
- Fowler는 장기적으로 harness가 golden path/service template처럼 수렴할 수 있다고 본다.

### 조직 관점에서의 harness 구성 요소

| 구성 요소 | 핵심 질문 | 대표 자료 | 빠진 경우의 증상 |
|----------|-----------|----------|------------------|
| Repo legibility | agent가 repo를 쉽게 읽고 바꿀 수 있는가 | OpenAI, DEV, Mitchell, Fowler | setup 재탐색, 규칙 위반 반복 |
| Human checkpoints | 사람은 어디에서 승인하고 어디에서 빠질 것인가 | Fowler, OpenAI, ignorance.ai | review overload 또는 무통제 자동화 |
| Merge/review policy | agent output throughput을 조직이 감당할 수 있는가 | OpenAI, Fowler | PR queue 병목, entropy 증가 |
| Background loops | cleanup, docs sync, regression scan을 누가 계속 돌릴 것인가 | Fowler, ignorance.ai, Inngest | 산출물 누적, 문서-코드 불일치 |
| Shared behavior | surface와 팀이 달라도 같은 semantics를 유지하는가 | OpenAI App Server | tool/safety semantics drift |

## agent 개발에서의 사용 방식

### 개인 -> 팀 -> 플랫폼으로 올라갈 때 먼저 합의할 것

1. 어떤 종류의 작업을 agent에게 맡길 것인가
2. 어떤 작업은 항상 human approval이 필요한가
3. 어떤 품질 신호를 자동화하고 어떤 판단은 사람에게 남길 것인가
4. rules와 specs는 어디에 저장하고 누가 갱신할 것인가
5. background agent가 만든 산출물을 누가 어떤 기준으로 merge할 것인가

### 실무 적용 순서

#### 1. repo를 system of record로 만든다

- rules, architecture, setup, test, conventions를 file로 남긴다.

#### 2. review를 산출물 중심에서 기준 중심으로 옮긴다

- acceptance criteria, tests, trace, checklist를 함께 본다.

#### 3. 작은 PR과 자주 merge를 기본값으로 둔다

- throughput을 review 용량에 맞춘다.

#### 4. background agent에 안전한 반복 작업부터 맡긴다

- docs sync, lint cleanup, stale artifact 정리, trace triage부터 시작한다.

#### 5. 점차 humans-on-the-loop로 이동한다

- 사람이 직접 손보는 대신 rules, checks, workflow guidance를 바꾼다.

### 조직이 흔히 놓치는 부분

- agent-generated code의 garbage collection
- 중간 산출물과 임시 브랜치 정리
- 사람이 읽는 문서와 agent가 읽는 문서를 따로 두지 않도록 하는 규칙
- agent 실패에서 나온 교훈을 repo rules와 eval suite에 다시 반영하는 루프
- background agent의 ownership과 rollback 책임

### high-risk domain에서의 기본값

- security, compliance, infra migration, data deletion, privileged shell access에서는 humans-on-the-loop로 가더라도 approval gate를 유지한다.
- low-risk cleanup, docs sync, trace triage, lint fix처럼 rollback cost가 낮은 작업부터 background automation을 늘린다.

## 설계 원칙

- 사람의 시간을 코드 작성보다 `의도 명세`, `기준 설정`, `예외 승인`, `loop 개선`에 쓴다.
- review는 더 늦게 더 많이 하는 것이 아니라 더 앞단에서 더 구조적으로 한다.
- repo는 인간 문서이면서 동시에 agent configuration surface라는 전제를 둔다.
- background agent는 merge 권한보다 cleanup, triage, suggestion 역할로 먼저 도입한다.
- organizational harness도 측정한다. PR 크기, review latency, rework rate, regression rate를 함께 본다.
- humans-on-the-loop로 가더라도 high-risk domain의 human gate는 유지한다.

## 반론/한계

- 이 영역은 공개 정량 연구가 가장 부족하다. 많은 주장이 강한 실무 직관과 사례 기반이다.
- agent legibility와 human legibility가 완전히 일치하는지는 아직 검증이 부족하다.
- 조직마다 compliance, security, change management 요구가 달라 동일한 operating model을 강요하기 어렵다.
- background agent와 async workflow는 편리하지만 ownership이 흐려지면 오히려 entropy를 키울 수 있다.

## 관련 자료 묶음

- 직접 문헌: OpenAI `Harness engineering`, Mitchell Hashimoto `My AI Adoption Journey`, ignorance.ai `The Emerging Harness Engineering Playbook`, Martin Fowler `Harness Engineering`
- 기반 문헌: Martin Fowler `Humans and Agents in Software Engineering Loops`, DEV `Building the Agent Harness`, DEV `The Agent Harness Is the Architecture`, OpenAI `Unlocking the Codex harness`
- 보조 근거: Inngest `Your Agent Needs a Harness, Not a Framework`, Anthropic `Effective harnesses for long-running agents`, `Building AI Coding Agents for the Terminal`
