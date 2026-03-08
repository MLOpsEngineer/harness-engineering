# Humans and Agents in Software Engineering Loops

- 구분: 블로그/아티클
- 발행일: 2026-03-04
- 저자: Kief Morris
- 출처: Martin Fowler
- 원문: https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html
- 관련성: 기반

## 한줄 요약
사람과 에이전트가 소프트웨어 개발의 여러 루프에서 어디에 서 있어야 하는지를 `outside / in / on the loop`로 구분하며, harness engineering을 인간 감독 구조까지 포함한 설계 문제로 확장한 글이다.

## 왜 중요한가
harness engineering을 순수 기술 인프라가 아니라 사람의 개입 위치, 승인 방식, 피드백 경로까지 포함한 socio-technical loop 설계로 넓혀 준다.

## 원문 구조
- software engineering loop 설명
- humans outside the loop
- humans in the loop
- humans on the loop
- agentic flywheel

## 1. 원문이 먼저 정의하는 loop 프레임
- 글은 먼저 소프트웨어 개발을 `why loop`와 `how loop`로 나눈다. `why loop`는 인간이 원하는 outcome과 working software 사이를 오가고, `how loop`는 code, tests, specs, infra 같은 중간 산출물을 만들어 그 outcome을 구현하는 루프다.
- `how loop`는 단일 루프가 아니라 여러 겹의 nested loop로 구성된다. 바깥 루프는 큰 feature를, 안쪽 루프는 더 작은 작업과 코드 생성을 담당한다.
- 이 전제를 깔아 둔 뒤, 인간이 어느 루프에 개입하느냐에 따라 협업 모델이 달라진다고 설명한다.

## 2. Humans outside the loop
- `Humans outside the loop`는 흔히 말하는 vibe coding에 가깝다. 인간은 원하는 결과만 제시하고, 구현 방법은 agent에게 맡긴다.
- 저자는 이 접근이 매력적이지만, 내부 품질이 외부 결과에 미치는 영향을 과소평가하면 비용, 속도, 안정성 측면에서 문제가 커진다고 본다. 정돈된 구조의 코드베이스는 인간뿐 아니라 LLM에게도 더 빨리 이해되고 덜 spiral하게 만든다고 본다.

## 3. Humans in the loop
- `Humans in the loop`는 인간이 코드 생성이 일어나는 가장 안쪽 루프의 gatekeeper로 머무는 모델이다.
- 글의 핵심 문제 제기는 throughput mismatch다. agent가 더 빨리 더 많이 만들수록, 인간이 모든 산출물을 마지막에 직접 검토하는 방식은 병목이 된다.
- 그래서 저자는 classic shift-left 논리를 다시 꺼낸다. 마지막 검토를 늘리는 대신, agent가 더 앞단에서 스스로 quality signal을 받도록 해야 한다는 것이다.

## 4. Humans on the loop
- 여기서 제안되는 모델이 `Humans on the loop`다. 인간은 결과물을 직접 고치기보다, 그 결과물을 만들어낸 specifications, quality checks, workflow guidance를 바꾼다.
- 글이 말하는 harness는 바로 이 "how loop 내부를 제어하는 specifications, checks, workflow guidance의 묶음"이다.
- 즉 사람이 산출물 편집자가 아니라 loop 설계자, 심판 기준 제공자, 자동화 수준 조절자로 이동한다.

## in the loop와 on the loop의 차이
- 결과가 마음에 들지 않을 때 `in the loop` 접근은 산출물을 직접 수정하거나, agent에게 그 수정 자체를 지시한다.
- 반대로 `on the loop` 접근은 산출물을 만들어낸 harness를 바꾼다. 즉 같은 유형의 문제를 다음 실행부터 덜 만들도록 루프 자체를 교정한다.
- 이 차이는 harness engineering을 prompt tweaking이 아니라 재발 방지형 시스템 설계로 이해하게 만든다.

## 5. Agentic Flywheel
- 글의 마지막 확장은 `agentic flywheel`이다. 여기서는 인간이 harness를 직접 개선하는 것에서 더 나아가, agent가 harness 개선을 제안하고 나중에는 일부를 자동 적용하게 만든다.
- 출발점은 이미 존재하는 tests와 evals다. 여기에 performance 측정, failure scenario validation, production operational data, user journey logs, commercial results 같은 richer signal을 추가할수록 flywheel이 강해진다고 본다.
- 각 workflow 단계에서 agent가 결과를 검토하고, upstream harness 변경까지 포함한 개선 제안을 만들게 한다. 이후 인간이 이를 검토하거나, 충분한 신뢰가 쌓이면 risk/cost/benefit 점수에 따라 일부를 자동 승인할 수도 있다는 시나리오를 제시한다.
- 이 대목은 harness engineering이 단발성 guardrail 작업이 아니라, 자기 자신을 개선하는 meta-loop로 발전할 수 있음을 보여 준다.

## Harness Engineering 관점
- harness engineering이 repo와 도구만의 문제가 아니라, 인간-에이전트 협업에서 attention을 어디에 둘지 정하는 운영 모델이라는 점을 분명히 한다.
- OpenAI의 `humans steer, agents execute`를 더 일반적인 delivery model로 번역한 글이라고 볼 수 있다. 사람의 일은 코드를 전부 읽는 것이 아니라, loop를 정의하고 품질 신호를 공급하고 자동화 수준을 조절하는 것이다.
- 또한 eval, review, production telemetry, backlog까지 모두 harness의 일부로 묶어 본다. 즉 harness는 실행 환경만이 아니라 조직적 피드백 시스템이다.

## 한계와 주의점
- 개념 분류와 사고 틀은 강하지만, 구체적인 구현 레시피나 계량 데이터는 적다.
- `on the loop`가 실무에서 정확히 어떤 artifact, 어떤 gate, 어떤 tooling으로 구현되는지는 다른 글과 함께 봐야 한다.
- 저자의 주장은 설득력이 있지만 규범적 성격이 강하다. 따라서 실제 팀에 적용할 때는 domain risk, compliance burden, human review capacity에 맞는 loop 재설계가 추가로 필요하다.
