# Agent Harness 문서 묶음

이 디렉터리는 `docs/blogs`와 `docs/papers`에 있는 원문 분석 아카이브를 다시 종합해, agent harness를 실무적으로 이해하고 설계하는 데 필요한 문서만 따로 묶은 synthesis layer다. 개별 자료 소개가 아니라 `왜 중요한가`, `agent 개발에서 어떻게 쓰이는가`, `어떻게 설계하고 검증하는가`, `사람과 조직은 어떻게 바뀌는가`를 답하도록 구성했다.

## 이 디렉터리만 읽으면 얻는 것

- harness engineering의 정의와 경계
- context engineering, scaffolding, framework, substrate와의 차이
- agent 개발 수명주기에서 harness가 개입하는 실제 지점
- context, tool, runtime, durability, eval, observability, human loop의 설계 패턴
- 조직과 repo를 agent-first 방식으로 바꾸는 운영 모델
- 31개 자료 전체가 어디에 반영되었는지 확인하는 커버리지 감사표

## 대상 독자

- coding agent나 terminal agent를 실제로 만들거나 운영하는 엔지니어
- repo를 agent-friendly하게 정비하려는 팀 리드
- eval harness, tracing, benchmark 인프라를 설계하는 연구자 및 플랫폼 엔지니어
- OpenAI, Anthropic, LangChain, Inngest, Martin Fowler, 최근 논문 흐름을 한 번에 정리하고 싶은 독자

## 문서 맵

| 문서 | 핵심 질문 | 읽는 시점 |
|------|-----------|----------|
| [01-foundations-and-boundaries.md](01-foundations-and-boundaries.md) | harness engineering은 무엇이고, 어디까지를 포함하는가 | 처음 |
| [02-why-harnesses-matter.md](02-why-harnesses-matter.md) | 왜 모델보다 harness가 더 큰 레버가 될 수 있는가 | 정의를 읽은 직후 |
| [03-harnesses-in-agent-development.md](03-harnesses-in-agent-development.md) | agent를 개발할 때 harness는 구체적으로 어디에서 쓰이는가 | 실무 적용 전 |
| [04-design-patterns-and-architecture.md](04-design-patterns-and-architecture.md) | 어떤 패턴으로 harness를 설계해야 하는가 | 구현 설계 시 |
| [05-evals-observability-and-improvement.md](05-evals-observability-and-improvement.md) | harness를 어떻게 측정하고 개선하는가 | 운영 및 회귀 방지 설계 시 |
| [06-humans-org-and-operating-model.md](06-humans-org-and-operating-model.md) | 사람, 리뷰, merge, background agent는 어떻게 재배치되는가 | 팀 운영 논의 시 |
| [07-source-crosswalk-and-coverage-audit.md](07-source-crosswalk-and-coverage-audit.md) | 전체 31개 자료가 어디에 반영됐는가 | 검토 및 감사 시 |

## 권장 읽기 순서

### 빠른 이해

1. [01-foundations-and-boundaries.md](01-foundations-and-boundaries.md)
2. [02-why-harnesses-matter.md](02-why-harnesses-matter.md)
3. [03-harnesses-in-agent-development.md](03-harnesses-in-agent-development.md)

### 구현 관점

1. [04-design-patterns-and-architecture.md](04-design-patterns-and-architecture.md)
2. [05-evals-observability-and-improvement.md](05-evals-observability-and-improvement.md)

### 운영 관점

1. [06-humans-org-and-operating-model.md](06-humans-org-and-operating-model.md)
2. [07-source-crosswalk-and-coverage-audit.md](07-source-crosswalk-and-coverage-audit.md)

## 자료 범위

- 블로그/아티클 21건
- 논문 10건
- 수집 기준일: 2026-03-08
- 주된 초점: coding/terminal/repo agent
- 보조 근거: research agent, data science agent, security benchmark, agent optimizer, benchmark harness

## 이 아카이브를 읽는 방법

- 원전 흐름을 보고 싶다면 루트 [README.md](../../README.md)의 자료 목록에서 출발한다.
- 장문 단일 요약이 필요하면 루트 [REPORT.md](../../REPORT.md)를 먼저 읽는다.
- 실무 적용과 설계를 빠르게 파악하려면 이 디렉터리 문서만 순서대로 읽는다.
- 특정 주장에 대한 근거를 추적하려면 [07-source-crosswalk-and-coverage-audit.md](07-source-crosswalk-and-coverage-audit.md)에서 해당 자료가 반영된 문서를 찾는다.
