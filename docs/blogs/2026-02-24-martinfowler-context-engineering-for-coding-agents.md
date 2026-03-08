# Context Engineering for Coding Agents

- 구분: 블로그/아티클
- 발행일: 2026-02-24
- 저자: Birgitta Böckeler
- 출처: Martin Fowler
- 원문: https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html
- 관련성: 기반

## 한줄 요약
코딩 에이전트의 컨텍스트를 구성하는 요소를 taxonomy로 정리하고, tools/MCP/skills/rules/specs 같은 용어를 명확히 해 주는 primer다.

## 왜 중요한가
harness engineering을 이해하기 전에 내부 레이어를 정리하는 데 가장 유용한 글 중 하나다.

## 핵심 내용
- reusable prompts, context interfaces, tools, MCP servers, skills, rules, specs를 구분해 coding agent context의 구성 요소를 체계화한다.
- Claude Code를 예시로 들어, 최근 DX 경쟁이 사실상 context configuration 경쟁으로 변하고 있다고 설명한다.
- ‘Everything is context’라는 넓은 정의를 바탕으로, 컨텍스트를 파일과 규칙의 네트워크로 다루는 감각을 전달한다.

## 원문 기준 핵심 흐름
- 글은 coding agent context를 taxonomy 형태로 정리한다. reusable prompts, tools, MCP servers, skills, rules, specs가 서로 다른 역할을 가진다고 본다.
- 여기서 중요한 메시지는 `everything is context`다. 즉 repo 안팎의 여러 artifact가 실제로는 agent의 행동을 결정하는 입력면이다.
- Claude Code를 예시로 들며, 최근 개발자 경험 경쟁이 모델 경쟁이 아니라 context configuration 경쟁으로 이동했다고 해석한다.

## Harness Engineering 관점
- harness engineering이 모델 바깥을 다룬다면, 이 글은 그 바깥 레이어 중에서도 모델 안으로 넣을 입력면을 정교하게 분해한다.
- 후속 Martin Fowler의 harness engineering 글을 이해하기 위한 전제 문서로 읽으면 가장 좋다.

## 한계와 주의점
- 경험 기반 primer라 정량 실험은 없다.
- Claude Code 중심 예시가 많아 특정 도구 편향이 있다.
