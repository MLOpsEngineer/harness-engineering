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
repo owner 관점에서 harness engineering의 실무 감각을 가장 소박하고 명확하게 설명하는 글이다. 복잡한 이론 없이 "팀이 실제로 뭘 할 수 있는가"에 초점을 맞춘다.

## 원문 기준 핵심 흐름

### 4계층 모델
- 글은 agent 시스템을 4계층으로 나눈다:
  1. **LLM (Brain)**: 추론 능력을 제공하는 모델. 팀이 직접 수정할 수 없다.
  2. **Agent (Loop)**: 모델을 반복적으로 호출하며 tool을 사용하는 루프. Claude Code, Cursor 같은 제품이 담당한다.
  3. **System Prompt (Behavior Definition)**: agent의 행동 규칙을 정의하는 instruction. CLAUDE.md 등.
  4. **Harness (Environment)**: 코드베이스 주변의 문서, 제약, 테스트, 피드백 루프, CI, 디렉토리 구조. **팀이 완전히 소유하고 직접 설계할 수 있는 유일한 레이어**.

### 통제 가능성 분석
- LLM: 통제 불가 (외부 서비스)
- Agent: 제한적 통제 (기성 도구 사용 시 설정만 가능)
- System Prompt: 높은 통제 (직접 작성)
- Harness: **완전한 통제** (repo의 모든 것이 대상)
- 따라서 가장 큰 ROI는 harness 투자에서 나온다.

### Harness의 구성 요소
- **문서**: README, CONTRIBUTING, ADR. agent가 codebase를 이해하는 기반.
- **테스트**: unit, integration, e2e test. agent가 자신의 작업을 검증하는 도구.
- **컨벤션**: naming, directory structure, import 규칙. 일관된 코드 생성을 위한 패턴.
- **피드백 루프**: CI/CD, lint, type check, code review. agent 출력을 자동 검증하는 체계.
- **제약 조건**: branch protection, PR template, merge 규칙. 위험한 행동을 방지하는 가드레일.

### 복리 효과
- 한 번 정비한 harness는 **모든 후속 agent 작업에 재사용**된다.
- 시간이 갈수록 harness 투자의 효과가 누적된다. 반면 harness 없이 agent를 쓰면 매번 같은 실수를 교정하는 데 시간을 쓴다.
- 경쟁력은 **어떤 tool을 쓰느냐**보다 **어떤 environment를 소유하고 다듬느냐**에서 나온다.

## Harness Engineering 관점
- 실무자에게 harness engineering을 가장 소박하고 명확하게 설명하는 글 중 하나다.
- 4계층 모델(LLM → Agent → System Prompt → Harness)은 harness engineering의 위치를 직관적으로 이해시킨다.
- "통제 가능성"이라는 기준으로 투자 우선순위를 정하는 프레임은 실무 의사결정에 바로 적용 가능하다.
- repo documents, constraints, tests, conventions가 모두 harness 자산이라는 관점은 OpenAI, Hashimoto, Fowler의 주장과 일치한다.

## 한계와 주의점
- 한 달 정도의 실험에서 나온 field note라 일반화에는 주의가 필요하다.
- 새로운 benchmark나 구현 공개는 없다.
- 4계층 모델이 깔끔하지만 현실에서는 경계가 모호할 수 있다.
