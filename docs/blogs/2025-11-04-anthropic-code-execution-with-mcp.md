# Code execution with MCP: building more efficient AI agents

- 구분: 블로그/아티클
- 발행일: 2025-11-04
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/code-execution-with-mcp
- 관련성: 기반

## 한줄 요약
MCP 서버 수가 많아질 때 tool definition과 intermediate result가 context를 잠식하는 문제를, code execution layer를 가상화 계층으로 도입하여 해결하는 방법을 다룬 글이다.

## 왜 중요한가
large tool universe를 다뤄야 하는 harness에서 token economy와 tool virtualization이 얼마나 중요한지를 구체적 아키텍처로 보여준다. "도구를 더 붙이는 것"이 아니라 "도구 노출을 가상화하는 것"이 harness의 핵심이라는 인식 전환을 제공한다.

## 원문 기준 핵심 흐름

### 1. Tool Definition Bloat 문제
- MCP(Model Context Protocol)를 통해 agent에 연결할 수 있는 tool/server가 늘어나면서, tool definition 자체가 context의 상당 부분을 차지하는 문제가 발생한다.
- 각 tool definition에는 이름, 설명, 파라미터 스키마, 반환값 설명이 포함되며, 하나의 tool definition이 수백 토큰을 소비할 수 있다.
- MCP 서버가 10개이고 각 서버가 평균 5개의 tool을 제공하면, 50개의 tool definition만으로 수천~수만 토큰을 소비한다.
- 이 토큰은 매 턴마다 반복 전송된다. 대화가 길어질수록 tool definition의 누적 비용은 기하급수적으로 늘어난다.
- 실제 사용되는 tool은 전체의 일부인데, 사용하지 않는 tool의 definition까지 매번 전송하는 것은 순수한 낭비다.

### 2. Intermediate Result Overhead
- agent가 tool을 호출할 때마다 그 결과가 context에 추가된다.
- 문제: 많은 tool 결과는 agent의 최종 추론에 직접 필요하지 않은 중간 데이터를 포함한다. 예를 들어 파일 목록을 조회한 결과, API 응답의 전체 JSON, 데이터베이스 쿼리의 raw 결과 등.
- 이런 intermediate result가 매 턴 축적되면, 실제 의사결정에 필요한 정보가 무관한 데이터 속에 묻힌다.
- 특히 multi-step 작업에서 agent가 5-10개의 tool을 순차 호출하면, 중간 결과의 총량이 context window의 상당 부분을 차지한다.

### 3. Code Execution Layer: 가상화(Virtualization) 개념
- Anthropic의 해결 방향은 "모델이 봐야 하는 것"과 "런타임이 대신 처리할 것"을 분리하는 것이다.
- code execution layer는 일종의 가상화 계층(virtualization layer)이다. 운영체제가 하드웨어를 추상화하듯, code execution layer가 tool universe를 추상화한다.
- 구체적 작동 방식:
  - agent가 직접 개별 tool을 호출하는 대신, code execution 환경(예: Python sandbox)에서 코드를 작성하고 실행한다.
  - 코드 안에서 여러 tool/API를 호출하고, 데이터를 변환하고, 조건 분기를 수행한다.
  - 모델에는 코드의 최종 결과만 반환된다. 중간 단계의 raw data는 모델의 context에 들어가지 않는다.
- 이 접근의 핵심 이점: (1) tool definition 수를 대폭 줄일 수 있다(개별 tool 대신 "execute_code" 하나로 대체 가능), (2) 중간 결과가 context를 오염시키지 않는다, (3) agent가 복잡한 데이터 변환을 프로그래밍적으로 수행할 수 있다.

### 4. Token 절약 효과
- tool definition bloat 해소: 50개의 개별 tool definition 대신 code execution tool 1개 + 사용 가능한 라이브러리 목록으로 대체하면, tool definition 토큰을 60-80% 절약할 수 있다.
- intermediate result 절약: agent가 10단계의 데이터 처리를 코드로 수행하면, 중간 9단계의 결과가 context에 포함되지 않는다. 최종 결과만 포함되므로 토큰 절약이 크다.
- 복합 효과: 한 번의 code execution 호출로 여러 tool 호출을 대체하면, tool 호출 횟수 자체가 줄어들어 전체 대화 턴 수도 감소한다.

### 5. MCP의 역할: 표준 연결 계층
- MCP는 이 아키텍처에서 표준 연결 계층(standard connection layer)으로 기능한다.
- MCP가 하는 일: 다양한 외부 서비스(데이터베이스, API, 파일 시스템 등)를 일관된 인터페이스로 agent에 노출한다.
- MCP가 하지 않는 일: context 관리, token 최적화, 결과 필터링. 이것은 harness의 역할이다.
- 따라서 중요한 것은 MCP 자체가 아니라, MCP 위에 어떤 가상화 계층을 두고 tool universe를 context에 어떻게 노출할 것인가다.
- MCP는 "파이프"이고, code execution layer는 "밸브"다. 어떤 정보가 모델에 도달하고 어떤 정보가 런타임에서 처리되는지를 결정하는 것은 밸브의 역할이다.

### 6. 아키텍처 패턴
- **Lazy Loading**: 모든 tool definition을 upfront로 주지 않고, agent가 특정 도메인의 작업을 시작할 때 관련 tool만 동적으로 로드한다.
- **Tool Grouping**: 관련 tool을 그룹으로 묶고, 그룹 수준에서 선택하게 한 뒤 세부 tool은 코드 레벨에서 접근한다.
- **Result Streaming**: tool 결과를 전체 반환하지 않고, agent가 필요한 부분만 선택적으로 접근할 수 있게 한다.
- **Sandbox Isolation**: code execution 환경을 격리하여 보안을 유지하면서도, 그 안에서 자유로운 데이터 처리를 가능하게 한다.

## Harness Engineering 관점
- 이 글은 harness engineering이 곧 ‘컨텍스트 예산 관리’이기도 하다는 점을 구체적으로 보여준다.
- tool virtualization은 harness의 핵심 기법이다. 모델에 "무엇을 보여줄까"를 능동적으로 관리하는 것이 harness의 역할이다.
- code execution layer는 harness와 모델 사이의 중간 계층으로, 복잡성을 모델로부터 숨기는 추상화 역할을 한다.
- "도구를 더 붙이는 것"에서 "도구 노출을 설계하는 것"으로의 전환은 harness engineering의 성숙을 나타낸다.

## 한계와 주의점
- MCP와 code execution 환경(sandbox)을 전제로 해 범용성에 한계가 있다. 모든 agent가 코드 실행 능력을 가진 것은 아니다.
- code execution layer를 도입하면 새로운 복잡성(보안, 에러 처리, 디버깅)이 추가된다.
- 장기 메모리나 사람-에이전트 협업 루프는 중심 주제가 아니다.
- 구체적 token 절약 수치는 시나리오에 따라 크게 달라질 수 있다.
