# Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned

- 구분: 논문
- 발행일: 2026-03-05
- 저자: Nghi D. Q. Bui
- 출처: arXiv
- 원문: https://arxiv.org/abs/2603.05344
- 관련성: 직접

## 한줄 요약
CLI 기반 코딩 에이전트 `OpenDev`를 소개하며, terminal-native coding agent에서 scaffolding, harness, context engineering, safety, memory를 하나의 compound system으로 다룬 시의성 높은 논문이다.

## 문제 설정
terminal-native coding agent는 IDE assistant보다 더 큰 자율성을 주지만, **long-horizon context bloat, destructive shell action, tool explosion, instruction fade-out, persistent memory** 문제가 훨씬 심하다. 이 문제들을 개별적으로 다루는 연구는 있었지만, 하나의 통합 시스템으로 다루는 문서는 드물었다.

## 제안 방법

### Scaffolding vs Harness 구분
- 논문은 먼저 `scaffolding`과 `harness`를 명시적으로 분리한다.
- **Scaffolding**: 첫 prompt 전에 일어나는 agent assembly. model 선택, tool registry 구성, system prompt 조립, 초기 context 설정.
- **Harness**: runtime의 tool dispatch, context management, safety enforcement. agent가 실행되는 동안 작동하는 모든 것.
- 이 구분은 Fowler의 harness engineering 정의와 일치한다. scaffolding은 "준비", harness는 "운영"이다.

### Compound AI System 설계
- OpenDev는 **compound AI system**으로 설계된다.
- workflow별로 다른 LLM을 바인딩하는 **per-workflow model binding**을 채택한다. 예: planning은 더 강한 모델, execution은 더 빠른 모델.
- agent core는 **planning과 execution을 분리**한 구조. Extended ReAct loop 안에 optional thinking/self-critique phase를 넣는다.

### Tool Layer
- tool layer는 **registry 기반**이며 MCP tool을 **lazy discovery**로 불러와 prompt budget을 절약한다.
- 모든 tool을 처음부터 context에 넣지 않고, 필요할 때 동적으로 발견해 등록한다.
- 이는 tool explosion 문제(tool이 많아지면 context를 차지하고 agent의 tool 선택 정확도가 떨어지는 현상)에 대한 해법이다.

### Context Layer
- **Adaptive Context Compaction**: context가 길어지면 자동으로 요약·압축. 단순 truncation이 아니라 의미를 보존하는 compaction.
- **Event-driven System Reminders**: 특정 이벤트(실패, 방향 전환 등)가 발생하면 관련 instruction을 context에 다시 주입. instruction fade-out 방지.
- **Experience-driven Memory Pipeline**: 과거 작업 경험에서 학습한 패턴을 저장하고 유사 상황에서 재활용.
- **Dual-memory**: 단기 기억(현재 세션)과 장기 기억(프로젝트 레벨)을 분리해 관리.

### Safety Layer
- prompt guardrail, schema-level restriction, runtime approval, tool-level validation, lifecycle hooks의 **five-layer defense-in-depth**로 설계된다.
- 각 layer는 독립적으로 작동해, 하나가 뚫려도 다른 layer가 방어한다.
- 특히 terminal agent는 destructive shell command(`rm -rf`, `git push --force` 등)를 실행할 수 있으므로 safety가 더 중요하다.

## 결과와 시사점
- 논문의 핵심 기여는 새로운 benchmark score보다 **production-grade terminal agent를 어떻게 조립했는지를 공개적으로 문서화**한 점이다.
- 저자는 OpenDev를 OpenHands처럼 browser UI 기반이 아닌, **진짜 terminal-native interactive agent**의 기술 보고서로 포지셔닝한다.
- terminal-bench류 결과를 인용하며, 단순 모델 업그레이드보다 **context efficiency와 runtime control이 결정적**이라는 메시지를 반복한다.
- context를 secondary optimization이 아니라 **first-class engineering concern**으로 다루어야 한다는 주장이 강하다.

## Harness Engineering 관점
- 현재 시점의 학술 문헌 중 harness engineering의 실무 감각을 **가장 직접적으로 흡수한 논문**이다.
- OpenAI/Anthropic/LangChain 글에서 논의되던 개념을 연구 형식과 시스템 아키텍처 문서 사이 어딘가의 형태로 정리했다.
- **per-workflow LLM binding, adaptive compaction, event-driven reminders, five-layer safety, lazy MCP**는 모두 harness를 **runtime OS처럼 다루는 설계**다.
- scaffolding/harness 분리는 harness engineering의 범위를 명확히 하는 데 유용한 프레임이다.

## 한계와 주의점
- 아직 최신 preprint라 외부 검증이 충분하지 않다.
- 자체 시스템 설명 비중이 크고, 경쟁 시스템과의 엄밀한 head-to-head 실험은 제한적이다.
- 논문도 스스로 밝히듯 algorithmic novelty보다 engineering report 성격이 강하다.
- terminal-native라는 제약이 있어, GUI 기반 agent와의 직접 비교는 어렵다.
