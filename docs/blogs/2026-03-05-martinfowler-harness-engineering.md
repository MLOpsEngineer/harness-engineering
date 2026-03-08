# Harness Engineering

- 구분: 블로그/아티클
- 발행일: 2026-02-17
- 저자: Birgitta Böckeler
- 출처: Martin Fowler
- 원문: https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html
- 관련성: 직접

## 한줄 요약
OpenAI의 사례를 계기로, context engineering 바깥에서 에이전트를 제어하는 도구, 제약, 검증, 유지보수 메커니즘 전체를 harness engineering으로 묶어 해석한 개념 정리 글이다.

## 왜 중요한가
현재 harness engineering의 개념 경계를 가장 명확하게 그어 주는 문서 중 하나다.

## 원문 구조
- OpenAI 글을 읽고 느낀 문제의식
- harness를 구성하는 세 가지 요소
- 부족하다고 본 부분
- service template와의 유사성
- autonomy와 제약의 역설

## 1. 원문에서 확인한 출발점
- 글은 OpenAI의 `Harness engineering: leveraging Codex in an agent-first world`를 읽고 그 사례를 개념적으로 정리하는 응답으로 출발한다.
- 저자는 OpenAI 글에 harness 정의가 직접적으로 정리되어 있지는 않지만, 그 사례 전체를 설명하기에 가장 적절한 단어가 harness라고 본다.
- 그리고 OpenAI 사례를 세 묶음의 메커니즘으로 재해석한다.

## 2. 저자가 정리한 harness의 세 축
- 첫째는 context engineering이다. 코드베이스 안의 지속적으로 개선되는 knowledge base와 observability 데이터, browser navigation 같은 동적 컨텍스트 접근까지 포함한다.
- 둘째는 architectural constraints다. LLM의 판단에만 맡기지 않고, custom linters와 structural tests 같은 deterministic checker로 설계 경계를 강제하는 층이다.
- 셋째는 "garbage collection"이다. 문서 불일치나 아키텍처 규칙 위반을 주기적으로 찾아내는 background agent를 두어 entropy와 decay를 억제하는 메커니즘이다.
- 저자는 특히 OpenAI 팀의 "agent가 struggle하면 더 세게 밀지 말고 무엇이 빠졌는지 찾는다"는 반복적 개선 태도를 중요한 operational lesson으로 읽는다. harness는 일회성 설정이 아니라 failure를 통해 계속 자라나는 시스템이라는 뜻이다.

## 3. 원문이 별도로 짚는 논점
- 이 글이 중요한 이유는 harness를 prompt wrapper보다 훨씬 넓게 본다는 데 있다. harness는 단순히 모델 앞뒤에 붙는 얇은 제어층이 아니라, 장기 내부 품질과 유지보수성을 지탱하는 장치들의 묶음이다.
- 저자는 여기서 기능 검증과 행동 검증이 OpenAI 글에서는 상대적으로 덜 드러났다고 지적한다. 즉 maintainability를 높이는 장치들은 잘 보이지만, 원하는 사용자 동작을 어떻게 체계적으로 검증하는지는 더 보완이 필요하다고 본다.
- 이어서 harness를 미래의 service template 비슷한 것으로 상상한다. 많은 조직이 소수의 주요 tech stack 위에서 움직이는 만큼, custom linter, structural test, 기본 knowledge doc, context provider를 갖춘 harness가 golden path template가 될 수 있다는 가설이다.
- 동시에 service template가 포크와 동기화 문제를 겪듯, harness도 팀별 변형과 공통 기반 간의 긴장을 가질 것이라고 본다.
- 또 하나의 중요한 주장으로, 더 높은 AI 자율성을 얻으려면 오히려 runtime과 solution space를 더 강하게 제한해야 할 수 있다고 본다. 원하는 언어와 패턴을 무한히 생성하게 두는 것이 아니라, 특정 architecture, boundary, structure를 강제해야 장기적인 신뢰성과 유지보수성이 생긴다는 관점이다.
- 여기서 저자는 장기적으로 AI 친화적 harness가 잘 갖춰진 일부 tech stack와 application topology 쪽으로 수렴이 일어날 가능성도 제시한다.

## Harness Engineering 관점
- 이 글은 개념 경계를 가장 잘 긋는다. 무엇을 컨텍스트로 넣을지와, 어떤 외부 시스템으로 agent를 제약하고 검증할지를 분리해 이후 논의를 훨씬 선명하게 만든다.
- 특히 harness를 deterministic 장치와 agentic 장치가 섞여 있는 복합 시스템으로 보는 시각이 중요하다. lint, structural test, docs, cleanup agent, observability access가 모두 같은 묶음에 들어간다.
- 실무적으로는 `프롬프트를 고칠까?`보다 `failure를 다시 안 만들 환경을 어떻게 바꿀까?`를 먼저 묻게 만든다.

## 한계와 주의점
- 개념 정리 성격이 강해 구체 구현 패턴은 OpenAI 글이나 실전 사례와 함께 읽어야 한다.
- 원문 자체가 OpenAI 사례에 대한 해석이므로, 1차 실험 보고서라기보다 2차적 개념화에 가깝다.
- 기능 검증과 행동 검증에 대한 저자의 문제 제기는 중요하지만, 이에 대한 대안 메커니즘은 이 글 안에서 자세히 전개되지는 않는다.
