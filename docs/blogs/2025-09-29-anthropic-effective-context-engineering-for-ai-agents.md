# Effective context engineering for AI agents

- 구분: 블로그/아티클
- 발행일: 2025-09-29
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 관련성: 기반

## 한줄 요약
프롬프트 엔지니어링에서 context engineering으로 무게중심이 이동하고 있음을 선언하고, context의 생성-축적-정리 생애주기와 "thinking in context" 방법론을 체계적으로 정리한 기준 글이다.

## 왜 중요한가
harness engineering의 내부 면을 담당하는 가장 중요한 이론적 기반 문서다. "prompt engineering은 context engineering의 부분집합"이라는 프레이밍이 이후 모든 논의의 출발점이 되었다.

## 원문 기준 핵심 흐름

### 1. Prompt Engineering에서 Context Engineering으로의 전환
- Anthropic은 "prompt engineering"이라는 용어가 더 이상 agent 시대의 핵심 활동을 충분히 담지 못한다고 본다.
- prompt는 system prompt 하나를 잘 쓰는 문제이지만, context engineering은 agent가 매 추론 단계에서 보는 전체 정보 표면(total information surface)을 설계하는 문제다.
- context에 포함되는 요소: system prompt, tool schema/definition, MCP surface, 외부 데이터(RAG 결과, 파일 내용), 대화 히스토리, 이전 tool 호출의 결과, agent의 내부 메모리/scratchpad, 사용자 프로파일/설정.
- 이 모든 요소를 "하나의 통합된 정보 환경"으로 보고, 그 환경이 agent의 다음 행동을 어떻게 유도하는지를 설계하는 것이 context engineering이다.

### 2. Context 생애주기 (Context Lifecycle)
- Anthropic은 context를 세 단계의 생애주기로 나눈다:

#### 2-1. 생성(Creation)
- context의 초기 구성. system prompt, tool definition, 초기 사용자 메시지, 관련 데이터의 retrieval 등.
- 핵심 원칙: 첫 턴의 context가 agent의 전체 궤도를 결정한다. 초기 context에 방향성이 불충분하면 agent는 탐색적 행동을 시작하고, 이후 교정 비용이 크다.
- system prompt에는 (1) agent의 역할과 목표, (2) 사용 가능한 tool과 그 용도, (3) 행동 지침과 제약 조건, (4) 출력 형식 요구사항을 포함해야 한다.

#### 2-2. 축적(Accumulation)
- agent가 작업을 진행하면서 context에 정보가 쌓이는 단계.
- 축적되는 정보: tool 호출과 결과, 사용자와의 추가 대화, 중간 추론 결과, 검색/조회한 데이터.
- 핵심 문제: 관련 없는 정보, 오래된 observation, 실패한 시도의 로그가 무한정 쌓인다. 이것이 agent decision quality를 떨어뜨리는 가장 큰 원인이다.
- "context는 기본적으로 증가한다"(context grows by default). 아무것도 하지 않으면 context는 계속 커지기만 한다.

#### 2-3. 정리(Pruning/Compaction)
- 쌓인 context에서 불필요한 정보를 제거하거나 요약하는 단계.
- 기법들: (1) 오래된 tool result를 요약으로 교체, (2) 완료된 작업의 상세 로그 제거, (3) 실패한 시도의 기록을 간단한 교훈으로 압축, (4) 대량의 raw data를 핵심 수치로 요약.
- 주의: 너무 공격적으로 정리하면 agent가 이전 맥락을 잃어버린다. 정리 시 "이 정보가 향후 결정에 영향을 줄 수 있는가?"를 기준으로 판단.
- compaction은 단순 truncation이 아니다. 의미를 보존하면서 분량을 줄이는 것이다.

### 3. "Thinking in Context" 방법론
- context 설계의 핵심 원칙: 설계자가 agent의 입장에서 현재 context를 바라보는 것.
- 구체적 절차: (1) 현재 context의 snapshot을 본다, (2) "이 context를 본 agent가 다음에 무엇을 할까?"를 예측한다, (3) 원하는 행동과 다르면 context를 수정한다.
- 이것은 "agent에게 지시하기"와 다르다. "이렇게 하지 마"라고 말하는 대신, agent가 자연스럽게 올바른 행동을 하도록 context 자체를 바꾸는 것이다.
- 예시: agent가 특정 API를 잘못 사용한다면, "이 API를 이렇게 쓰지 마"라는 지시 대신, tool definition 자체를 수정하여 잘못된 사용이 불가능하게 만든다.
- 이 방법론은 UX 디자인에서의 "affordance" 개념과 유사하다. context가 올바른 행동을 "유도"(afford)하게 만드는 것이다.

### 4. 주요 안티패턴 (Anti-Patterns)
- **과다 지시(Over-instruction)**: system prompt에 모든 가능한 시나리오를 나열하는 것. agent가 정보 과부하로 핵심 지침을 놓친다.
- **Context 동결(Context Freezing)**: 초기 context를 설정하고 이후 관리하지 않는 것. context는 계속 변해야 한다.
- **Tool Result 무차별 포함**: tool이 반환한 모든 데이터를 context에 그대로 유지하는 것. 수 턴이 지나면 context가 tool result로 가득 찬다.
- **History 무한 보존**: 대화 히스토리를 절대 정리하지 않는 것. 초기 턴의 탐색적 대화가 50턴 뒤에도 context를 차지한다.
- **Implicit State 의존**: agent의 상태를 대화 흐름에서 암묵적으로 추론하게 만드는 것. 명시적 상태 관리가 없으면 agent는 자기가 어디에 있는지 혼란스러워한다.

### 5. 실전 기법들
- **Scratchpad 패턴**: agent가 중간 추론 결과를 별도 영역에 기록하게 한다. "생각의 과정"과 "최종 결과"를 분리할 수 있다.
- **Summarize-then-act**: 복잡한 tool result를 받으면, 먼저 요약한 뒤 다음 행동을 결정하게 한다.
- **Selective re-injection**: 이전 턴의 모든 정보를 유지하는 대신, 다음 행동에 관련된 정보만 선별적으로 다시 주입한다.
- **Context budget 관리**: 전체 context window 중 각 유형의 정보에 할당하는 비율을 사전에 설계한다(예: system prompt 10%, tool definitions 15%, history 40%, current task 35%).

## Harness Engineering 관점
- 이 글은 harness engineering 전체의 절반을 설명한다. 모델 안으로 무엇을 넣을지 정하는 내부 레이어가 context engineering이다.
- context lifecycle(생성-축적-정리)은 harness가 관리해야 하는 핵심 프로세스다. harness는 이 세 단계를 자동화하고 제어하는 시스템이다.
- "thinking in context"는 harness 설계 방법론의 핵심이다. harness 설계자는 모델의 관점에서 자신이 만든 context를 평가해야 한다.
- 안티패턴 목록은 harness 설계의 체크리스트로 직접 활용 가능하다.

## 한계와 주의점
- 실행 환경이나 CI/merge 같은 바깥쪽 문제는 거의 다루지 않는다. context engineering은 harness의 "내부 면"만 다룬다.
- 정성적 원칙이 많고 재현 가능한 실험 수치는 적다. context budget 비율 같은 구체적 숫자는 예시일 뿐 검증된 값이 아니다.
- 단일 agent 기준의 논의이며, multi-agent 환경에서의 context 공유/분리 문제는 다루지 않는다.
