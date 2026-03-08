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
terminal-native coding agent는 IDE assistant보다 더 큰 자율성을 주지만, long-horizon context bloat, destructive shell action, tool explosion, instruction fade-out, persistent memory 문제가 훨씬 심하다.

## 제안 방법
- 논문은 먼저 `scaffolding`과 `harness`를 분리한다. scaffolding은 첫 prompt 전 agent assembly이고, harness는 runtime의 tool dispatch, context management, safety enforcement다.
- OpenDev는 `compound AI system`으로 설계된다. workflow별로 다른 LLM을 바인딩하는 `per-workflow model binding`을 채택한다.
- agent core는 planning과 execution을 분리한 구조를 취하고, Extended ReAct loop 안에 optional thinking/self-critique phase를 넣는다.
- tool layer는 registry 기반이며 MCP tool을 `lazy discovery`로 불러와 prompt budget을 절약한다.
- context layer는 `Adaptive Context Compaction`, `event-driven system reminders`, `experience-driven memory pipeline`, `dual-memory` 구조를 사용한다.
- safety는 prompt guardrail, schema-level restriction, runtime approval, tool-level validation, lifecycle hooks의 `five-layer` defense-in-depth로 설계된다.

## 결과와 시사점
- 논문의 핵심 기여는 새로운 benchmark score보다 `production-grade terminal agent를 어떻게 조립했는지`를 공개적으로 문서화한 점에 있다.
- 저자는 OpenDev를 OpenHands처럼 browser UI 기반이 아닌, 진짜 terminal-native interactive agent의 기술 보고서로 포지셔닝한다.
- terminal-bench류 결과를 인용하며, 이런 환경에서는 단순 모델 업그레이드보다 context efficiency와 runtime control이 결정적이라는 메시지를 반복한다.
- 특히 context를 secondary optimization이 아니라 first-class engineering concern으로 다루어야 한다는 주장이 강하다.

## Harness Engineering 관점
- 현재 시점의 학술 문헌 중 harness engineering의 실무 감각을 가장 직접적으로 흡수한 논문이다.
- OpenAI/Anthropic/LangChain 글에서 논의되던 개념을 연구 형식과 시스템 아키텍처 문서 사이 어딘가의 형태로 정리한 문서다.
- `per-workflow LLM binding`, `adaptive compaction`, `event-driven reminders`, `five-layer safety`, `lazy MCP`는 모두 harness를 runtime OS처럼 다루는 설계라고 볼 수 있다.

## 한계와 주의점
- 아직 최신 preprint라 외부 검증이 충분하지 않다.
- 자체 시스템 설명 비중이 크고, 경쟁 시스템과의 엄밀한 head-to-head 실험은 제한적이다.
- 논문도 스스로 밝히듯 algorithmic novelty보다 engineering report 성격이 강하다.
