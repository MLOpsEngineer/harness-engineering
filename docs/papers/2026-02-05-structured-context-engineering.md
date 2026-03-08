# Structured Context Engineering for File-Native Agentic Systems: Evaluating Schema Accuracy, Format Effectiveness, and Multi-File Navigation at Scale

- 구분: 논문
- 발행일: 2026-02-05
- 저자: Damon McMillan
- 출처: arXiv
- 원문: https://arxiv.org/abs/2602.05447
- 관련성: 인접 연구

## 한줄 요약
대규모 file-native agent 환경에서 schema를 어떤 형식과 retrieval architecture로 제공해야 하는지 `9,649`회 실험으로 비교한 empirical context engineering 연구다.

## 문제 설정
대형 schema나 file structure를 agent에게 어떻게 보여줘야 하는지 practitioner lore는 많지만, format·architecture·model tier·scale을 함께 비교한 실증 연구는 거의 없었다.

## 제안 방법
- 논문은 SQL generation을 structured system actuation의 proxy task로 사용한다.
- `11`개 모델, `4`개 포맷(YAML, Markdown, JSON, TOON), `2`개 architecture, schema scale `10`~`10,000` tables를 대상으로 실험한다.
- 연구 질문도 명시적이다: file-native context가 prompt engineering보다 나은가, format이 정확도에 영향을 주는가, model tier가 중요한가, scale이 어떻게 바뀌는가, format이 효율성에 영향을 주는가.
- file-native architecture는 agent가 grep/read 같은 native file tool로 schema file을 읽는 방식이고, 비교 대상으로 prompt-inlined schema 방식이 있다.

## 결과와 시사점
- aggregate 수준에서 format 효과는 통계적으로 크지 않았다. 논문은 `chi-squared=2.45, p=0.484`로 요약한다.
- 하지만 architecture 효과는 model tier에 따라 갈린다. file-native retrieval은 frontier-tier model에 `+2.7%` 정확도 향상을 주지만, open-source model에는 aggregate `-7.7%`의 mixed result를 보인다.
- 가장 큰 변수는 model capability 자체였다. frontier와 open-source tier 사이에 `21 percentage point` accuracy gap이 있다고 보고한다.
- schema scale은 partitioning으로 해결 가능했다. file-native agent는 `10,000` tables까지 navigation accuracy를 유지할 수 있었다고 주장한다.
- 효율성 측면에서는 `grep tax`가 핵심 발견이다. compact하거나 novel한 format이 파일 크기는 작아도 grep output density나 unfamiliarity 때문에 runtime token 사용량을 늘릴 수 있다고 한다.

## Harness Engineering 관점
- harness engineering의 내부 레이어를 실험적으로 다룬 논문이다.
- repo/file-native 환경에서 어떤 serialization과 retrieval architecture가 agent-friendly한지 고민할 때 직접 참고할 만하다.
- 특히 `frontier model에는 file-native가 유리하지만 open-source에는 아닐 수 있다`는 결과는 harness를 model-specific하게 설계해야 함을 시사한다.

## 한계와 주의점
- SQL generation proxy task라 일반 코딩 작업 전체를 대표하지는 않는다.
- file-native structured system에 특화된 연구라 CLI coding agent 전체로 일반화하면 과해질 수 있다.
- format 효과가 aggregate로는 약하므로, 결과를 `YAML이 항상 최고` 같은 단순 규칙으로 읽으면 안 된다.
