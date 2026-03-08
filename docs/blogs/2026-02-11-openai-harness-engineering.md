# Harness engineering: leveraging Codex in an agent-first world

- 구분: 블로그/아티클
- 발행일: 2026-02-11
- 저자: Ryan Lopopolo
- 출처: OpenAI
- 원문: https://openai.com/index/harness-engineering/
- 관련성: 직접

## 한줄 요약
OpenAI가 0줄 수기 코드 제약으로 내부 제품을 만들며 얻은 교훈을 통해, 인간의 역할이 코드 작성에서 환경 설계로 이동했다고 선언한 핵심 글이다.

## 왜 중요한가
현재 harness engineering 담론의 기준점이 되는 문서다.

## 원문 기준 핵심 흐름
- 글은 OpenAI 팀이 `0 lines of hand-written code` 제약 아래 제품과 운영 artefact를 만들어 본 사례에서 출발한다.
- 핵심 메시지는 인간의 역할 이동이다. 사람은 코드를 직접 쓰기보다 intent specification, feedback loop design, environment shaping을 담당한다.
- repository knowledge를 system of record로 삼고, architecture, constraints, taste를 agent-readable form으로 외부화해야 한다고 강조한다.
- throughput이 늘어나면 merge philosophy, garbage collection, entropy control, review 방식까지 같이 바뀌어야 한다고 본다.
- 가장 유명한 주장은 `application legibility`보다 `agent legibility`다. 코드베이스는 인간뿐 아니라 agent에게도 읽히고 수정되기 쉬워야 한다.

## Harness Engineering 관점
- harness engineering을 조직 운영, repo 구조, CI, docs, observability, code review 방식 전체를 재편하는 discipline으로 끌어올린 글이다.
- 이 문서 이후 harness engineering은 단순 agent wrapper가 아니라 소프트웨어 팀의 operating model을 뜻하게 된다.

## 한계와 주의점
- 매우 강한 내부 사례이지만 재현 가능한 외부 benchmark는 아니다.
- OpenAI 내부 환경과 Codex 전제의 영향이 크다.
