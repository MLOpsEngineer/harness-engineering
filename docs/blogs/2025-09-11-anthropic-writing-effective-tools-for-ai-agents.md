# Writing effective tools for AI agents—using AI agents

- 구분: 블로그/아티클
- 발행일: 2025-09-11
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/writing-tools-for-agents
- 관련성: 기반

## 한줄 요약
도구 인터페이스를 어떻게 설계해야 agent가 덜 헷갈리고 더 싸게, 더 안정적으로 일하는지를, 구체적 예시와 eval-driven 개선 루프와 함께 정리한 tool-design 중심 글이다.

## 왜 중요한가
harness engineering에서 tool surface는 가장 중요한 레버 중 하나인데, 이 글은 그 레버를 어떻게 다듬는지 가장 구체적으로 다룬다. tool은 prompt의 일부이며, tool 설계 품질이 agent 성능을 좌우한다는 핵심 통찰을 제공한다.

## 원문 기준 핵심 흐름

### 1. Tool이 중요한 이유: Tool Surface가 Agent 성능을 결정한다
- agent 성능은 모델 능력보다 tool surface 품질에 더 크게 좌우된다.
- tool definition(이름, 설명, 파라미터 스키마, 반환값)은 system prompt와 함께 매 턴마다 모델에 전달되므로, 사실상 prompt의 일부이다.
- 나쁜 tool 설계는 agent를 혼란시키고, 불필요한 tool 호출을 유발하고, 잘못된 파라미터를 전달하게 만든다.

### 2. Tool 이름 설계 원칙 (Naming Principles)
- tool 이름은 agent가 어떤 tool을 호출할지 결정하는 첫 번째 신호다.
- 좋은 이름의 원칙: (1) 동사+명사 구조로 행동을 명확히 한다(예: `create_customer`, `search_orders`), (2) 비슷한 도구끼리 일관된 명명 패턴을 사용한다, (3) 모호한 이름을 피한다.
- 나쁜 예시: `process_data`(무엇을 어떻게 처리하는지 불명확), `handle_request`(어떤 요청인지 알 수 없음), `do_thing`.
- 좋은 예시: `search_customers_by_email`, `create_support_ticket`, `get_order_status`.
- agent가 10개 이상의 tool 중에서 선택해야 할 때, 이름만으로 올바른 tool을 고를 수 있어야 한다.

### 3. Tool Description 설계
- description은 이름만으로 부족한 정보를 보충한다. 그러나 길게 늘이는 것이 좋은 것이 아니다.
- 핵심 원칙: agent가 실제로 "이 tool을 호출할지 말지"를 결정하는 데 필요한 정보만 넣어야 한다.
- 포함해야 할 것: (1) 이 tool이 하는 일의 한 줄 요약, (2) 언제 이 tool을 사용하고 언제 사용하지 말아야 하는지, (3) 중요한 제약 조건이나 부작용.
- 포함하지 말아야 할 것: 내부 구현 세부, 사용자가 아닌 개발자를 위한 기술적 노트, 다른 tool과의 비교.
- 인간 개발자를 위한 API 문서와 agent를 위한 tool description은 다르다. agent는 "이 tool을 써야 하나?"라는 결정을 내려야 하므로, decision-relevant 정보 위주로 작성한다.

### 4. Parameter Schema 설계 (Parameter Design)
- 파라미터는 agent가 실제로 채워야 하는 값이므로, 명확하고 제한적이어야 한다.
- 핵심 원칙들:
  - **필수 vs 선택 구분을 명확히**: 필수 파라미터만 required로 표시. 선택 파라미터에는 합리적인 기본값을 설정.
  - **enum 활용**: 가능한 값이 제한적이면 자유 텍스트 대신 enum을 사용. 예: `status`를 string으로 두지 않고 `["open", "closed", "pending"]`으로 제한.
  - **타입을 엄격하게**: string 대신 number, boolean 등 구체적 타입을 사용. "날짜를 string으로" 받지 않고 ISO 8601 형식을 명시.
  - **중첩 최소화**: 깊이 중첩된 object 파라미터는 agent를 혼란시킨다. 가능한 한 flat하게 설계.
  - **파라미터 이름도 설명적으로**: `q` 대신 `search_query`, `id` 대신 `customer_id`.
- 나쁜 예시: `{"data": object}` -- agent가 어떤 구조의 object를 전달해야 하는지 알 수 없다.
- 좋은 예시: `{"customer_email": string (required), "issue_type": enum["billing","technical","general"], "priority": enum["low","medium","high"]}`.

### 5. 반환값 설계: 후속 Reasoning을 위한 포맷팅
- tool의 반환값은 agent의 다음 추론에 직접 사용된다. 따라서 반환값 설계는 "어떤 데이터를 돌려줄까"뿐 아니라 "agent가 이 데이터를 보고 다음에 무엇을 할 수 있는가"를 고려해야 한다.
- 핵심 원칙들:
  - **관련 정보만 반환**: 데이터베이스의 전체 행을 반환하지 않고, agent의 다음 결정에 필요한 필드만 선별.
  - **에러 메시지를 actionable하게**: `"Error: 404"`보다 `"Customer not found. Try searching by email instead of ID."`가 agent를 올바른 다음 행동으로 유도한다.
  - **구조화된 포맷**: JSON으로 반환하여 agent가 파싱하기 쉽게. 그러나 불필요하게 깊은 중첩은 피한다.
  - **결과 크기 제한**: 대량의 데이터를 반환하면 context를 잠식한다. 페이지네이션이나 요약을 사용.
- 반환값에 "다음에 할 수 있는 행동"에 대한 힌트를 포함하는 것도 효과적이다. 예: `{"result": ..., "suggested_next_action": "Use update_customer to modify this record"}`.

### 6. Eval-Driven Tool 개선 (Eval-Driven Tool Improvement)
- tool 설계는 한 번에 완성되지 않는다. 실제 agent가 tool을 사용하는 것을 관찰하고 반복 개선해야 한다.
- Anthropic이 권장하는 프로세스:
  - (1) 초기 tool definition 작성.
  - (2) agent에게 실제 시나리오를 수행하게 한다.
  - (3) agent의 tool 호출 패턴을 관찰: 잘못된 tool을 선택하는가? 파라미터를 잘못 채우는가? 반환값을 오해하는가?
  - (4) 문제 패턴에 따라 이름, 설명, 스키마, 반환값을 수정.
  - (5) 수정 후 동일 시나리오를 다시 실행하여 개선 여부 확인.
- 이 과정을 eval(평가)이라고 부른다. tool 설계에도 모델 학습처럼 "train -> eval -> iterate" 사이클이 필요하다.

### 7. Agent-as-Tool-Tester 루프 (Agent as Tool Tester)
- 더 나아가, agent 자체를 tool tester로 활용할 수 있다.
- 방법: agent에게 tool definition만 주고 "이 tool을 사용해서 X를 수행해보라"라고 요청한다. agent가 혼란을 느끼는 지점이 바로 tool 설계의 약점이다.
- agent가 tool description을 읽고도 올바른 파라미터를 추론하지 못하면, description이 불충분한 것이다.
- agent가 비슷한 이름의 두 tool 사이에서 망설이면, 이름이나 description에서 구분이 불충분한 것이다.
- 이 루프를 통해 tool을 "agent-friendly"하게 개선할 수 있다. tool도 한 번 설계하고 끝나는 artifact가 아니라 계속 개선되는 harness component다.

### 8. 도구 수와 복잡성 관리
- tool이 너무 많으면 agent의 선택 부담이 늘어나고, 잘못된 tool을 호출할 확률이 높아진다.
- 가능하면 tool 수를 줄이고, 비슷한 기능은 하나의 tool로 통합하되 파라미터로 분기한다.
- 그러나 하나의 tool에 너무 많은 기능을 넣으면 파라미터가 복잡해지고 agent가 올바른 조합을 만들기 어렵다.
- 적절한 균형: 각 tool이 하나의 명확한 행동을 수행하되, 전체 tool 수를 합리적으로 관리.

## Harness Engineering 관점
- tool selection과 tool contract는 모델 능력을 실제 업무 성능으로 바꾸는 핵심 harness 요소라는 점을 잘 보여준다.
- harness engineering은 ‘어떤 tool을 붙일까’보다 ‘tool을 어떤 계약으로 expose할까’에 더 가깝다.
- eval-driven improvement와 agent-as-tester 루프는 harness를 "계속 개선 가능한 시스템"으로 만드는 핵심 방법론이다.
- tool의 반환값 설계까지 harness의 영역이라는 점은, harness가 모델의 입력과 출력 양쪽을 모두 관리해야 함을 보여준다.

## 한계와 주의점
- tool-centric 글이라 조직 운영, 병렬화, merge 철학 같은 상위 주제는 다루지 않는다.
- Anthropic 스택과 MCP 친화적 관점이 강하다.
- 구체적 정량 결과(tool 개선 전후의 성공률 변화 등)는 공개되지 않았다.
