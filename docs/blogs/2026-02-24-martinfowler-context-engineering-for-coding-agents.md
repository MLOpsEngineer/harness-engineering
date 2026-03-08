# Context Engineering for Coding Agents

- 구분: 블로그/아티클
- 발행일: 2026-02-24
- 저자: Birgitta Böckeler
- 출처: Martin Fowler
- 원문: https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html
- 관련성: 기반

## 한줄 요약
코딩 에이전트의 컨텍스트를 구성하는 요소를 taxonomy로 정리하고, tools/MCP/skills/rules/specs 같은 용어를 명확히 해 주는 primer로, harness의 "내부 면"을 체계화한 글이다.

## 왜 중요한가
harness engineering을 이해하기 전에 내부 레이어(context engineering)를 정리하는 데 가장 유용한 글 중 하나다. Fowler의 harness engineering 글과 함께 읽으면 내부-외부 레이어의 관계가 명확해진다.

## 원문 기준 핵심 흐름

### Context의 구성 요소 Taxonomy
- coding agent가 사용하는 context를 체계적으로 분류한다:
  - **Reusable Prompts**: 여러 작업에 걸쳐 재사용되는 instruction. CLAUDE.md, .cursorrules 같은 파일이 해당한다.
  - **Tools**: agent가 호출할 수 있는 도구. 파일 읽기/쓰기, 터미널 실행, 검색 등.
  - **MCP Servers**: Model Context Protocol을 통해 외부 시스템과 연결하는 인터페이스. DB, API, 외부 서비스 접근을 표준화한다.
  - **Skills**: 특정 작업에 대한 복합적인 instruction + tool 조합. 예: "테스트를 작성하고 실행하라"는 단순 prompt보다 구조화된 형태.
  - **Rules**: agent 행동의 제약 조건. "절대 main 브랜치에 직접 push하지 마라" 같은 hard constraint.
  - **Specs**: 작업의 구체적 명세. 무엇을 만들지, 어떤 기준으로 완료를 판단할지를 정의한다.

### "Everything is Context"
- 넓은 정의: repo 안팎의 여러 artifact가 실제로는 agent의 행동을 결정하는 **입력면**이다.
- README, CONTRIBUTING, 테스트 파일, CI 설정, 린트 규칙, 디렉토리 구조까지 모두 agent에게는 context다.
- 이 관점에서 context engineering은 "prompt를 잘 쓰는 기술"이 아니라 **"agent에게 보이는 정보 환경 전체를 설계하는 기술"**이다.

### DX 경쟁 = Context Configuration 경쟁
- Claude Code를 예시로 들어, 최근 **개발자 경험(DX) 경쟁이 모델 경쟁이 아니라 context configuration 경쟁**으로 변하고 있다고 해석한다.
- CLAUDE.md, .cursorrules 같은 파일은 사실상 **agent의 행동을 프로그래밍하는 configuration**이다.

### Context를 파일 네트워크로 다루기
- 하나의 거대한 system prompt 대신, **여러 파일의 네트워크**로 context를 구성하는 것이 현대적 패턴이다.
- 파일별로 역할이 다르다: 전역 규칙(rules), 프로젝트별 설정(specs), 도구 정의(tools), 재사용 가능한 패턴(skills).
- 이 파일들은 버전 관리되고, 팀원 간 공유되며, 시간에 따라 진화한다. context engineering이 **코드와 같은 수준의 엔지니어링 대상**이 되는 것이다.

## Harness Engineering 관점
- harness engineering이 모델 바깥을 다룬다면, 이 글은 그 바깥 레이어 중에서도 **모델 안으로 넣을 입력면을 정교하게 분해**한다.
- Anthropic의 context engineering 글이 원칙을 제시했다면, 이 글은 그 원칙을 **구체적 artifact 유형**으로 분류한다.
- 후속 Martin Fowler의 harness engineering 글을 이해하기 위한 **전제 문서**로 읽으면 가장 좋다.
- "DX = context configuration"이라는 관찰은 harness engineering이 제품 경쟁력과 직결됨을 시사한다.

## 한계와 주의점
- 경험 기반 primer라 정량 실험은 없다.
- Claude Code 중심 예시가 많아 특정 도구 편향이 있다.
- context의 "양"보다 "질"이 중요하다는 원칙은 제시하지만, 질을 측정하는 기준은 명확하지 않다.
