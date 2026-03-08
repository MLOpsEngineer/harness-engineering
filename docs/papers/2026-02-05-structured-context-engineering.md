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
대형 schema나 file structure를 agent에게 어떻게 보여줘야 하는지 practitioner lore는 많지만, **format·architecture·model tier·scale을 함께 비교한 실증 연구**는 거의 없었다. "YAML이 최고", "JSON이 낫다" 같은 주장은 있지만 근거가 빈약했다.

## 제안 방법

### 실험 설계
- SQL generation을 structured system actuation의 proxy task로 사용한다.
- **11개 모델**, **4개 포맷**(YAML, Markdown, JSON, TOON), **2개 architecture**(prompt-inlined vs file-native), **schema scale 10~10,000 tables**를 대상으로 실험한다.
- 총 `9,649`회 실험이라는 대규모 empirical study다.

### 연구 질문
1. File-native context가 prompt-inlined보다 나은가?
2. Format이 정확도에 영향을 주는가?
3. Model tier가 중요한가?
4. Scale이 어떻게 영향을 미치는가?
5. Format이 효율성(token 사용량)에 영향을 주는가?

### 두 가지 Architecture
- **Prompt-inlined**: 모든 schema 정보를 system prompt에 직접 넣는 방식.
- **File-native**: agent가 grep/read 같은 native file tool로 schema file을 읽는 방식. 필요한 정보를 능동적으로 검색한다.

## 결과와 시사점

### Format 효과: 생각보다 약하다
- aggregate 수준에서 format 효과는 통계적으로 크지 않았다. `chi-squared=2.45, p=0.484`.
- 즉 "YAML이 항상 최고" 같은 단순 규칙은 성립하지 않는다. 실무에서 format 선택에 과도한 시간을 쓸 필요가 없다는 함의다.

### Architecture 효과: Model Tier에 따라 갈린다
- file-native retrieval은 **frontier-tier model에 `+2.7%` 정확도 향상**을 주지만, **open-source model에는 aggregate `-7.7%`의 mixed result**를 보인다.
- 이는 file-native architecture가 보편적 해법이 아니라, **model의 tool-use 능력에 의존하는 전략**임을 의미한다.
- frontier model은 필요한 정보를 효율적으로 검색하지만, open-source model은 검색 과정에서 오히려 혼란을 겪을 수 있다.

### Model Capability가 가장 큰 변수
- frontier와 open-source tier 사이에 **21 percentage point accuracy gap**이 있다.
- format이나 architecture보다 model 자체의 능력이 결과에 더 큰 영향을 미친다.

### Scale은 Partitioning으로 해결 가능
- file-native agent는 **10,000 tables까지 navigation accuracy를 유지**할 수 있었다.
- 핵심은 partitioning이다. 전체 schema를 한 번에 보여주지 않고, agent가 필요한 부분만 검색하게 하면 scale 문제가 완화된다.

### "Grep Tax" — 핵심 발견
- compact하거나 novel한 format이 **파일 크기는 작아도** grep output density나 unfamiliarity 때문에 **runtime token 사용량을 늘릴 수 있다**.
- 즉 format 효율성은 static file size가 아니라 **agent가 실제로 소비하는 token**으로 측정해야 한다.
- "grep tax"는 file-native architecture에서 agent가 정보를 검색할 때 발생하는 추가 token 비용을 뜻한다.
- 이 발견은 context engineering에서 **전체 비용 = 저장 비용 + 검색 비용**이라는 관점을 도입한다.

## Harness Engineering 관점
- harness engineering의 내부 레이어를 실험적으로 다룬 논문이다. **어떤 serialization과 retrieval architecture가 agent-friendly한지**를 정량적으로 비교한다.
- 특히 `frontier model에는 file-native가 유리하지만 open-source에는 아닐 수 있다`는 결과는 **harness를 model-specific하게 설계해야 함**을 시사한다. 범용 harness는 존재하지 않을 수 있다.
- "grep tax" 개념은 PerfBench의 output processing과 Anthropic의 context engineering에서 다루는 **observation size 관리**와 직접 연결된다.
- `9,649`회 실험이라는 규모는 context engineering 분야에서 가장 대규모의 empirical study 중 하나다.

## 한계와 주의점
- SQL generation proxy task라 일반 코딩 작업 전체를 대표하지는 않는다.
- file-native structured system에 특화된 연구라 CLI coding agent 전체로 일반화하면 과해질 수 있다.
- format 효과가 aggregate로는 약하므로, 결과를 "YAML이 항상 최고" 같은 단순 규칙으로 읽으면 안 된다.
- 논문의 실험 환경(SQL generation)과 실무 환경(코딩, 분석, 디버깅)의 차이를 감안해야 한다.
