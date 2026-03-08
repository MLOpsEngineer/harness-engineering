# Context Engineering for AI Agents: Lessons from Building Manus

- 구분: 블로그/아티클
- 발행일: 2025-07-18
- 저자: Yichao ‘Peak’ Ji
- 출처: Manus
- 원문: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- 관련성: 기반

## 한줄 요약
Manus 팀이 실제 agent product를 만들며 정리한 context engineering 실전 메모로, KV-cache 적중률, context 오염 방지, 파일 기반 상태 관리, todo-list 주도 실행 등 구체적 기법을 통해 긴 작업을 안정적으로 지속시키는 방법을 설명한다.

## 왜 중요한가
2025년 하반기 harness engineering 담론의 바탕이 된 글 중 하나로, 프롬프트보다 더 넓은 의미의 상태 설계를 강조한다. 특히 KV-cache라는 인프라 레벨의 고려사항까지 context 설계에 포함시킨 최초의 실전 문서 중 하나이다.

## 원문 기준 핵심 흐름

### 1. Context Engineering의 정의 확장
- Manus는 context를 단순 system prompt가 아니라, 계획(plan), 파일(files), 메모리(memory), tool result, 실행 기록(action history), intermediate artifact 전체로 정의한다.
- 핵심 전제: LLM은 context window 안에 있는 것만 "알 수 있다." 따라서 agent의 능력은 context 안에 무엇이 있는지에 의해 결정된다.
- context engineering은 "모델에 무엇을 말할까"가 아니라 "모델이 매 턴마다 보는 전체 정보 표면을 어떻게 설계할까"라는 문제다.

### 2. KV-Cache 인식 설계 (KV-Cache-Aware Design)
- Manus의 가장 독특한 기여 중 하나는 KV-cache 적중률을 context 설계의 핵심 지표로 삼은 것이다.
- LLM 추론 시 이전 턴의 KV-cache를 재사용하면 비용과 지연 시간이 대폭 줄어든다. 그러나 context 중간에 내용이 삽입되거나 이전 턴의 내용이 변경되면 cache가 무효화(invalidation)된다.
- 따라서 Manus는 context를 "append-only"에 가깝게 설계한다: system prompt와 tool definition은 고정(stable prefix), 대화 히스토리는 중간 삽입 없이 순차 추가, 동적 정보는 가능한 한 context 끝부분에 배치한다.
- 이 원칙을 위반하면 매 턴마다 전체 context를 재계산해야 하므로 비용이 수배로 증가한다. Manus는 이를 "context 구조의 cache-friendliness"라고 부른다.
- 구체적 규칙: system prompt를 자주 바꾸지 않기, tool definition 순서를 고정하기, 이전 메시지를 수정하지 않기(retroactive editing 금지).

### 3. Context 오염 문제 (Context Pollution)
- long-running task에서 대화 히스토리만으로 상태를 유지하려 하면 context가 금방 "오염"된다.
- 오염의 유형: (1) 이미 완료된 과거 단계의 상세 정보가 계속 남아 있는 stale information, (2) 실패한 시도의 에러 메시지와 디버깅 로그가 누적되는 noise accumulation, (3) tool result에 포함된 대량의 raw data가 후속 추론을 방해하는 observation bloat.
- 오염된 context는 agent를 이전 실패에 anchoring시키거나, 이미 완료된 작업을 반복하게 만들거나, 관련 없는 정보에 주의를 빼앗기게 만든다.
- Manus의 해결책: 정보를 대화 안에 두지 않고, 외부 파일/artifact로 옮기는 것이다.

### 4. 파일 기반 상태 관리 (File-Based State Management)
- Manus는 agent의 상태를 대화 히스토리가 아니라 파일 시스템에 저장한다.
- 구체적으로: 작업 계획은 `todo.md` 같은 마크다운 파일로 유지, 수집한 데이터는 구조화된 파일(JSON, CSV 등)로 저장, 중간 산출물(코드, 문서 초안 등)은 별도 파일로 externalize.
- agent가 다음 턴에서 필요한 정보는 파일을 읽어서(re-read) 가져온다. 대화에 모든 것을 담아두지 않는다.
- 이 접근의 핵심 이점: (1) context window를 절약, (2) 정보를 최신 상태로 유지(파일은 업데이트 가능하지만 대화 히스토리는 immutable), (3) 세션 간 상태 전달이 자연스러움.

### 5. Artifact 외재화 (Artifact Externalization)
- "artifact"는 agent가 생산하는 중간/최종 산출물을 의미한다: 코드 파일, 분석 보고서, 수집된 데이터, 생성된 문서 등.
- Manus는 이런 artifact를 대화 안에 인라인으로 두지 않고, 파일 시스템에 쓴 뒤 경로만 context에 남긴다.
- 이렇게 하면 agent가 artifact를 수정할 때 대화 히스토리 전체를 오염시키지 않고, 해당 파일만 업데이트하면 된다.
- re-injection 패턴: agent가 특정 artifact가 필요한 시점에 해당 파일을 다시 읽어서 context에 주입한다. 전체 artifact를 항상 들고 다니지 않는다.

### 6. Todo-List 주도 실행 (Todo-List Driven Execution)
- Manus agent의 핵심 제어 메커니즘은 todo-list다.
- agent는 작업 시작 시 todo.md를 생성하고, 각 항목에 체크박스(`[ ]` / `[x]`)를 사용해 진행 상태를 추적한다.
- 매 턴마다 agent는 todo-list를 다시 읽어서 다음에 무엇을 할지 결정한다. 이는 대화 히스토리의 마지막 몇 턴에 의존하는 것보다 훨씬 안정적이다.
- todo-list는 (1) agent에게 방향성을 제공하고, (2) 진행 상태를 명시적으로 만들고, (3) context window를 절약하고(전체 작업 계획을 매번 대화에 포함하지 않아도 됨), (4) 세션 간 연속성을 보장한다.
- 이 패턴은 후속 Anthropic 글에서도 반복 등장하는 핵심 harness 패턴이 되었다.

### 7. "Think in Context" 접근
- context를 설계할 때, 설계자가 agent의 관점에서 현재 context를 바라봐야 한다는 원칙이다.
- 질문: "이 context를 본 agent가 다음에 어떤 행동을 할까?" -> 원하는 행동이 아니라면 context를 수정해야 한다.
- 이는 프롬프트에 "이렇게 해라"라고 지시하는 것과 다르다. context의 구조와 내용 자체가 agent의 행동을 유도하도록 설계하는 것이다.
- 예시: agent가 이전 실패에 집착하고 있다면, 실패 로그를 context에서 제거하거나 요약으로 교체한다. 명시적으로 "무시해라"라고 말하는 것보다 효과적이다.

## Harness Engineering 관점
- Manus는 ‘컨텍스트를 운영체제처럼 관리하는 방법’을 제시한다. 파일 시스템, 읽기/쓰기 연산, 캐시 관리가 모두 등장한다.
- KV-cache 인식 설계는 harness가 인프라 레벨까지 내려가야 함을 보여준다. context의 의미적 내용뿐 아니라 물리적 구조(순서, 위치, 변경 빈도)도 harness 설계의 대상이다.
- todo-list 주도 실행은 이후 Anthropic의 "feature-by-feature progression"과 직접 연결된다.
- 파일 기반 상태 + artifact 외재화는 "모델 바깥에서 상태를 관리한다"는 harness engineering의 핵심 원칙을 가장 구체적으로 구현한 사례다.

## 한계와 주의점
- 정량 성능 실험보다 제품 경험을 바탕으로 한 설계 원칙 중심이다. KV-cache 적중률의 구체적 개선 수치는 공개되지 않았다.
- Manus의 구체적 구현 세부(파일 구조, 요약 알고리즘, re-injection 타이밍 등)가 충분히 공개되지는 않아 재현성은 제한적이다.
- 범용 agent보다 Manus의 특정 제품 맥락(웹 브라우징, 코드 실행 중심)에 최적화된 교훈일 수 있다.
