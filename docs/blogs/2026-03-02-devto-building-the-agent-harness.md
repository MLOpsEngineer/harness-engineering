# Building the Agent Harness: Why the Environment Matters More Than the Model

- 구분: 블로그/아티클
- 발행일: 2026-03-02
- 저자: Shreyas Khandelwal
- 출처: DEV Community
- 원문: https://dev.to/skhandelwal/building-the-agent-harness-why-the-environment-matters-more-than-the-model-39ie
- 관련성: 직접

## 한줄 요약
LLM, agent, system prompt, harness를 층위별로 구분하며, 실제로 팀이 통제할 수 있는 레버는 harness뿐이라고 정리한 현장 노트다.

## 왜 중요한가
repo owner 관점에서 harness engineering의 실무 감각을 설명하는 글이다.

## 핵심 내용
- LLM은 brain, agent는 loop, system prompt는 behavior definition, harness는 코드베이스 주변의 문서/제약/피드백 루프라고 층위를 나눈다.
- 개발팀은 모델도 툴 내부도 직접 고치기 어렵지만, repo의 규칙과 환경은 직접 설계할 수 있으며 이 부분이 시간이 갈수록 복리 효과를 낸다고 주장한다.
- 따라서 경쟁력은 ‘어떤 툴을 쓰느냐’보다 ‘어떤 환경을 소유하고 다듬느냐’에서 나온다고 본다.

## 원문 기준 핵심 흐름
- 글은 brain, loop, system prompt, harness를 층위별로 나누어 설명한다.
- 이 구분을 통해 팀이 실제로 통제 가능한 레버가 무엇인지 드러낸다. 모델과 툴 internals는 외부 변수지만, repo rules와 feedback environment는 팀이 직접 설계할 수 있다는 것이다.
- 따라서 장기 경쟁력은 tool choice보다 environment ownership에서 나온다고 결론짓는다.

## Harness Engineering 관점
- 실무자에게 harness engineering을 가장 소박하고 명확하게 설명하는 글 중 하나다.
- repo documents, constraints, tests, conventions가 모두 harness 자산이라는 점을 강조한다.

## 한계와 주의점
- 한 달 정도의 실험에서 나온 field note라 일반화에는 주의가 필요하다.
- 새로운 benchmark나 구현 공개는 없다.
