# On Agent Frameworks and Agent Observability

- 구분: 블로그/아티클
- 발행일: 2026-02-13
- 저자: LangChain
- 출처: LangChain
- 원문: https://blog.langchain.com/on-agent-frameworks-and-agent-observability/
- 관련성: 기반

## 한줄 요약
모델이 좋아질수록 agent framework가 필요 없어진다는 주장에 반박하며, agent는 본질적으로 모델 바깥의 시스템이고, framework와 observability는 그 시스템의 핵심 인프라라고 정리한 글이다.

## 왜 중요한가
harness engineering을 framework/observability 관점에서 정당화하는 글이다. "모델만 좋으면 된다"는 환원주의에 대한 체계적 반론을 제공한다.

## 원문 기준 핵심 흐름

### "모델이 좋아지면 Framework가 사라진다"에 대한 반박
- 업계 일각에서 모델 성능이 올라가면 orchestration framework가 불필요해진다는 관측이 있었다.
- LangChain은 이에 정면으로 반대한다. 모델은 추론 엔진이지만, agent는 **tool orchestration, memory, execution state, tracing**을 포함하는 복합 시스템이다.
- 모델이 아무리 좋아도 tool을 호출하고, 결과를 받아들이고, 상태를 관리하고, 실패에서 복구하는 로직은 모델 바깥에 있어야 한다.
- 따라서 framework는 사라지는 것이 아니라, **더 얇고 더 중요한 system layer**로 남는다.

### Framework의 진정한 역할
- framework의 역할은 boilerplate 감소가 아니다. **빠르게 변하는 best practice를 시스템 차원에서 encode**하는 것이다.
- agent architecture의 진화 과정: chaining → orchestration → tool-calling loop → filesystem/memory 중심 구조.
- 이 진화가 빠르기 때문에, 개별 팀이 매번 처음부터 구현하는 것보다 **검증된 패턴을 재사용**하는 것이 효율적이다.
- framework는 이런 패턴의 저장소이자 배포 메커니즘이다. agent loop, tool dispatch, memory management, error handling의 표준 구현을 제공한다.

### Observability의 독립성
- observability는 특정 framework와 **독립적으로** 제공돼야 한다.
- framework 종속적인 관측은 해당 framework 밖에서 일어나는 문제를 포착하지 못한다. 예: framework가 관리하지 않는 external API 호출의 지연, 사용자 측 입력 패턴.
- 독립적 observability가 있어야 실제 production failure mode를 추적할 수 있다.
- LangSmith는 이 원칙에 따라 LangChain framework 외부의 agent 시스템도 관측할 수 있도록 설계되었다고 한다.

### Agent System의 본질
- agent system은 단순히 "모델 + 프롬프트"가 아니라 다음을 포함하는 복합 시스템이다:
  - **Tool orchestration**: 어떤 도구를 언제 호출할지 결정하는 로직
  - **Memory management**: 단기/장기 기억의 저장과 검색
  - **Execution state**: 현재 작업의 진행 상태 관리
  - **Error handling**: 실패 시 복구, 재시도, fallback
  - **Tracing**: 전체 실행 경로의 기록과 분석
- 이 모든 것이 모델 바깥에 존재하며, 이것이 바로 harness다.

## Harness Engineering 관점
- 이 글은 harness engineering의 **왜 framework가 아직 필요한가**에 대한 답이다.
- 모델 성능이 높아질수록 wrapper가 사라지는 것이 아니라, 오히려 **더 얇고 더 중요한 system layer**로 남는다는 관점은 Inngest의 "harness not framework" 주장과 흥미롭게 대비된다.
- Inngest는 framework를 넘어서야 한다고 하고, LangChain은 framework가 여전히 필요하다고 한다. 하지만 둘 다 "모델 바깥의 시스템이 중요하다"는 점에서는 일치한다. 차이는 그 시스템을 뭐라고 부르느냐에 있다.
- observability의 독립성 주장은 harness 설계에서 tracing/logging을 harness의 일부로 포함해야 한다는 원칙과 일치한다.

## 한계와 주의점
- LangChain의 제품 관점이 강하게 반영된다. framework 불필요론을 반박하는 것이 LangChain의 비즈니스 이해와 일치한다는 점은 인지해야 한다.
- direct harness definition보다 broader framework defense에 가까워, harness engineering의 구체적 레시피는 제한적이다.
- observability 도구로 LangSmith를 전제하는 부분이 있어, 다른 observability stack과의 비교는 부족하다.
