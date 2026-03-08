# Evaluating Deep Agents: Our Learnings

- 구분: 블로그/아티클
- 발행일: 2025-12-03
- 저자: LangChain
- 출처: LangChain
- 원문: https://blog.langchain.com/evaluating-deep-agents-our-learnings/
- 관련성: 기반

## 한줄 요약
Deep Agents를 실제 제품에 적용하면서 eval을 어떻게 설계했는지 정리한 글로, harness 개선 루프를 평가 인프라 관점에서 구체적으로 설명한다.

## 왜 중요한가
harness engineering이 단순 prompt 튜닝이 아니라 **평가 인프라를 동반한 운영 문제**라는 점을 실무 사례로 보여준다. Anthropic의 eval 원칙 글과 함께 eval harness의 양대 기준 문서다.

## 원문 기준 핵심 흐름

### Deep Agent의 평가 문제
- LangChain이 "deep agent"라 부르는 것은 단순 QA가 아니라, 여러 tool을 호출하고 여러 단계를 거쳐 복합적인 task를 수행하는 agent다.
- 이런 agent의 eval은 전통적인 benchmark와 근본적으로 다르다. 같은 task라도 agent마다 다른 경로로 도달하고, 성공의 기준도 단순 정답 매칭이 아니다.

### Bespoke Test Logic
- datapoint마다 성공 조건이 달라 **bespoke test logic**이 필요하다.
- 예: 파일 수정 task에서는 파일 내용 비교, API 호출 task에서는 호출 순서와 파라미터 검증, 분석 task에서는 결론의 논리적 타당성 검증.
- 이는 eval harness가 범용 grader만으로는 부족하고, **task-specific verifier**를 함께 설계해야 함을 뜻한다.

### 평가 수준의 계층
- **Single-step eval**: 한 번의 tool call이나 한 번의 의사결정을 평가. agent가 올바른 tool을 선택했는지, 올바른 argument를 넣었는지를 본다. 국소적 의사결정의 품질 측정.
- **Full-turn eval**: 한 번의 완결된 실행을 시작부터 끝까지 평가. task 성공 여부와 최종 결과물의 품질을 본다.
- **Multi-turn eval**: 실제 사용자와의 여러 번 상호작용에 걸친 지속성을 평가. context 유지, 이전 결정과의 일관성, 장기 작업의 안정성을 본다.
- 세 수준은 상호 보완적이다. single-step이 좋아도 full-turn이 나쁠 수 있고, full-turn이 좋아도 multi-turn에서 무너질 수 있다.

### Environment가 Grader보다 중요하다
- 가장 핵심적인 학습: **grader보다 environment**가 더 중요하다.
- 환경이 지저분하거나 재현 가능하지 않으면, 모델 변화보다 **환경 편차가 결과를 지배**한다.
- 동일한 task를 동일한 agent로 실행해도, 환경 설정이 미묘하게 다르면(의존성 버전, 파일 시스템 상태, 네트워크 조건) 결과가 달라진다.
- 따라서 eval 환경의 **결정론적 재현 가능성**이 eval 품질의 가장 기본적인 조건이다. Docker container, snapshot, deterministic seed 등이 필요하다.

### Eval을 운영 시스템으로
- eval은 `답안 채점`이 아니라 **특정 harness 변경이 실제 behavior를 개선했는지 측정하는 운영 시스템**이다.
- 평가 데이터포인트 하나하나에 **작업 맥락**을 심는 방식이 실제 production harness 설계와 닮아 있다.
- LangSmith trace 데이터와 연결해, harness 변경 전후의 behavior 차이를 정량적으로 비교할 수 있다.
- 이 접근은 이후 LangChain의 "Improving Deep Agents with Harness Engineering" 글에서 trace-based 개선 루프로 발전한다.

## Harness Engineering 관점
- 이 글은 harness engineering의 **검증 레이어**를 설명한다. 좋은 harness는 agent를 실행하는 것만이 아니라, 바뀐 harness가 실제로 개선됐는지 측정해야 한다.
- "environment > grader"라는 교훈은 harness 설계에서도 직접 적용된다. harness의 실행 환경(sandbox, dependency, file system)이 불안정하면 harness 개선의 효과를 정확히 측정할 수 없다.
- eval의 3단계 계층(single-step, full-turn, multi-turn)은 harness 검증의 체크리스트로 활용 가능하다.

## 한계와 주의점
- LangChain의 deep agent 전제와 LangSmith 기반 워크플로우가 강하게 반영된다. LangSmith 없이 동일한 eval loop를 구축하려면 대안적 tracing 인프라가 필요하다.
- 직접적인 harness 정의보다는 eval practice에 무게가 있다. harness의 실행 레이어(prompt, tool, middleware)는 후속 글에서 다룬다.
- 구체적인 eval metric이나 threshold 기준은 제시되지 않는다.
