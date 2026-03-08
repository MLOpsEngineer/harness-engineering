# On Agent Frameworks and Agent Observability

- 구분: 블로그/아티클
- 발행일: 2026-02-13
- 저자: LangChain
- 출처: LangChain
- 원문: https://blog.langchain.com/on-agent-frameworks-and-agent-observability/
- 관련성: 기반

## 한줄 요약
모델이 좋아질수록 agent framework가 필요 없어진다는 주장에 반박하며, 에이전트는 본질적으로 모델 바깥의 시스템이라고 정리한 글이다.

## 왜 중요한가
harness engineering을 framework/observability 관점에서 정당화하는 글이다.

## 핵심 내용
- agent framework의 역할은 boilerplate 감소가 아니라, 빠르게 변하는 best practice를 시스템 차원에서 encode하는 것이라고 본다.
- agent architecture는 chaining에서 orchestration, 다시 tool-calling loop와 filesystem/memory 중심 구조로 진화했다고 설명한다.
- observability는 특정 framework와 독립적으로 제공돼야 하며, 그래야 실제 production failure mode를 추적할 수 있다고 주장한다.

## 원문 기준 핵심 흐름
- 글은 `모델이 좋아질수록 framework가 사라진다`는 관측에 반대한다.
- framework는 단순 편의 기능이 아니라 evolving best practice를 재사용 가능한 system primitive로 굳히는 층이라고 본다.
- 또 agent system은 본질적으로 tool orchestration, memory, execution state, tracing을 포함하므로 모델 밖의 시스템일 수밖에 없다고 주장한다.
- observability를 framework와 분리해 생각하는 것도 중요한데, 그래야 프레임워크 종속 없이 실제 failure mode와 bottleneck을 잡을 수 있다고 본다.

## Harness Engineering 관점
- 이 글은 harness engineering의 ‘왜 framework가 아직 필요한가’에 대한 답이다.
- 모델 성능이 높아질수록 wrapper가 사라지는 것이 아니라, 오히려 더 얇고 더 중요한 system layer로 남는다는 관점을 준다.

## 한계와 주의점
- LangChain의 제품 관점이 강하게 반영된다.
- direct harness definition보다 broader framework defense에 가깝다.
