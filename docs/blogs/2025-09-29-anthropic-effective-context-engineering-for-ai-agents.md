# Effective context engineering for AI agents

- 구분: 블로그/아티클
- 발행일: 2025-09-29
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 관련성: 기반

## 한줄 요약
프롬프트 엔지니어링에서 context engineering으로 무게중심이 이동하고 있음을 선언하고, agent가 실제로 보는 전체 context surface를 어떻게 설계할지를 정리한 기준 글이다.

## 왜 중요한가
harness engineering의 내부 면을 담당하는 가장 중요한 이론적 기반 문서다.

## 원문 기준 핵심 흐름
- 글은 context를 system prompt 하나로 축소하지 않는다. tool schema, MCP surface, external data, history, memory까지 모두 context라고 본다.
- 핵심 문제는 accumulation이다. 여러 턴이 지나면 관련 없는 정보와 오래된 observation이 쌓여 agent decision quality를 떨어뜨린다.
- 그래서 좋은 context engineering은 `무엇을 넣을까`보다 `무엇을 빼고, 언제 다시 불러오고, 어떤 형식으로 요약할까`를 다루는 작업이 된다.
- 글이 말하는 중요한 관점은 `thinking in context`다. 즉 현재 context shape가 agent에게 어떤 행동을 유도하는지를 역으로 보며 설계해야 한다는 것이다.
- 이 글은 context engineering을 agent behavior design의 핵심 레버로 끌어올린다. prompt copywriting보다 context lifecycle management가 더 중요하다는 주장이다.

## Harness Engineering 관점
- 이 글은 harness engineering 전체의 절반을 설명한다. 모델 안으로 무엇을 넣을지 정하는 내부 레이어가 context engineering이다.
- 후속 harness engineering 담론은 여기서 한 단계 더 나아가, 모델 바깥의 실행 환경과 검증 루프까지 포함한다.

## 한계와 주의점
- 실행 환경이나 CI/merge 같은 바깥쪽 문제는 거의 다루지 않는다.
- 정성적 원칙이 많고 재현 가능한 실험 수치는 적다.
