# Evaluating Deep Agents: Our Learnings

- 구분: 블로그/아티클
- 발행일: 2025-12-03
- 저자: LangChain
- 출처: LangChain
- 원문: https://blog.langchain.com/evaluating-deep-agents-our-learnings/
- 관련성: 기반

## 한줄 요약
Deep Agents를 실제 제품에 적용하면서 eval을 어떻게 설계했는지 정리한 글로, harness 개선 루프를 평가 인프라 관점에서 설명한다.

## 왜 중요한가
harness engineering이 단순 prompt 튜닝이 아니라 평가 인프라를 동반한 운영 문제라는 점을 잘 보여준다.

## 원문 기준 핵심 흐름
- LangChain은 deep agent를 평가할 때 datapoint마다 성공 조건이 달라 bespoke test logic이 필요하다고 본다.
- 평가 수준도 나눈다. single-step eval은 국소 의사결정을, full-turn eval은 한 번의 완결된 실행을, multi-turn eval은 실제 상호작용 지속성을 본다.
- 중요한 것은 grader보다 environment다. 환경이 지저분하거나 재현 가능하지 않으면 모델 변화보다 환경 편차가 결과를 지배한다고 말한다.
- 결국 eval은 `답안 채점`이 아니라 `특정 harness 변경이 실제 behavior를 개선했는지` 측정하는 운영 시스템이 된다.

## Harness Engineering 관점
- 이 글은 harness engineering의 검증 레이어를 설명한다. 좋은 harness는 agent를 실행하는 것만이 아니라, 바뀐 harness가 실제로 개선됐는지 측정해야 한다.
- 평가 데이터포인트 하나하나에 작업 맥락을 심는 방식은 실제 production harness 설계와 닮아 있다.

## 한계와 주의점
- LangChain의 deep agent 전제와 LangSmith 기반 워크플로우가 강하게 반영된다.
- 직접적인 harness 정의보다는 eval practice에 무게가 있다.
