# Improving Deep Agents with harness engineering

- 구분: 블로그/아티클
- 발행일: 2026-02-17
- 저자: LangChain
- 출처: LangChain
- 원문: https://blog.langchain.com/improving-deep-agents-with-harness-engineering/
- 관련성: 직접

## 한줄 요약
같은 모델을 유지한 채 harness만 바꿔 Terminal Bench 2.0 점수를 크게 끌어올린, 현재 가장 실증적인 harness engineering 사례다.

## 왜 중요한가
‘모델보다 harness가 더 큰 성능 레버’라는 주장을 정량 데이터로 뒷받침한다.

## 핵심 내용
- deepagents-cli는 GPT-5.2-codex를 그대로 둔 채 system prompt, tools, middleware만 바꿔 52.8에서 66.5로 올랐다고 보고한다.
- LangSmith trace를 대규모로 분석해 실패 패턴을 찾고, 이를 Agent Skill 형태의 trace analyzer로 자동화해 개선 루프를 만들었다.
- self-verification, tracing, error-focused iteration이 harness 개선의 핵심 레버로 제시된다.

## 원문 기준 핵심 흐름
- 글은 같은 모델을 고정한 채 harness만 바꿔 Terminal Bench 2.0 점수를 끌어올린 사례를 전면에 둔다.
- 개선은 prompt 한 줄 수정이 아니라 system prompt, tool behavior, middleware, trace analysis loop를 함께 다루는 식으로 이뤄진다.
- LangChain은 trace를 단순 로그가 아니라 optimization signal로 본다. trace analyzer skill을 두어 failure pattern을 자동으로 분류하고 개선 후보를 만든다.
- 메시지는 분명하다. harness engineering은 추상 개념이 아니라, measurable optimization space다.

## Harness Engineering 관점
- 이 글은 harness engineering을 추상 개념이 아니라 measurable optimization space로 보여준다.
- 시스템 프롬프트, 도구, middleware를 ‘knobs’로 보고 실험하는 태도가 이후 실무 패턴의 표준에 가깝다.

## 한계와 주의점
- Terminal Bench라는 특정 benchmark에 최적화된 결과라 일반화에는 주의가 필요하다.
- LangChain 관측 인프라 전제가 강하다.
