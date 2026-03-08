# Writing effective tools for AI agents—using AI agents

- 구분: 블로그/아티클
- 발행일: 2025-09-11
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/writing-tools-for-agents
- 관련성: 기반

## 한줄 요약
도구 인터페이스를 어떻게 설계해야 agent가 덜 헷갈리고 더 싸게, 더 안정적으로 일하는지를, 실제 tool authoring workflow와 함께 정리한 tool-design 중심 글이다.

## 왜 중요한가
harness engineering에서 tool surface는 가장 중요한 레버 중 하나인데, 이 글은 그 레버를 어떻게 다듬는지 가장 구체적으로 다룬다.

## 원문 기준 핵심 흐름
- 글은 agent 성능이 모델보다 tool surface 품질에 크게 좌우된다고 본다.
- 좋은 tool은 단지 기능이 많은 tool이 아니라, 이름과 경계가 명확하고 호출 계약이 예측 가능하며 반환값이 후속 reasoning에 바로 쓰일 수 있어야 한다.
- tool description과 parameter schema도 prompt의 일부이므로, 설명을 길게 늘이는 것이 아니라 agent가 실제 decision을 내리는 데 필요한 정보만 명확히 넣어야 한다고 본다.
- Anthropic은 tool을 인간 문서처럼 쓰지 말고, agent가 실제로 잘 쓰는지 eval과 rollout을 붙여 개선해야 한다고 강조한다.
- 더 나아가 agent를 써서 tool 자체를 테스트하고 설명을 고치게 하는 loop를 권한다. 즉 tools도 한 번 설계하고 끝나는 artifact가 아니라 계속 개선되는 harness component다.

## Harness Engineering 관점
- tool selection과 tool contract는 모델 능력을 실제 업무 성능으로 바꾸는 핵심 harness 요소라는 점을 잘 보여준다.
- 즉 harness engineering은 ‘어떤 tool을 붙일까’보다 ‘tool을 어떤 계약으로 expose할까’에 더 가깝다.

## 한계와 주의점
- tool-centric 글이라 조직 운영, 병렬화, merge 철학 같은 상위 주제는 다루지 않는다.
- Anthropic 스택과 MCP 친화적 관점이 강하다.
