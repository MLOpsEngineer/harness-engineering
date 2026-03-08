# Harness Engineering 종합 보고서

- 작성일: 2026-03-08
- 코퍼스 규모: 블로그/아티클 21건, 논문 10건

## 1. 한 문장 정의

Harness engineering은 모델 바깥에서 에이전트가 안정적으로 일하도록 만드는 모든 설계 행위다. 여기에는 context curation, tool contract, runtime orchestration, eval, observability, human review loop, durability, state persistence가 모두 포함된다.

## 2. 수집 기준과 방법

- 정확한 용어인 `harness engineering`을 기준으로 웹 검색을 수행했다.
- 여기에 2025년 하반기부터 2026년 3월 초까지의 `context engineering`, `effective harnesses`, `agent loop`, `evaluation harness`, `terminal coding agents` 문헌을 추가로 묶었다.
- 단순 뉴스 재인용과 짧은 소셜 포스트는 제외하고, 원저자 기술 글·실무 분석 글·논문 위주로 남겼다.

## 3. 시간축으로 본 흐름

### 2025년 6월~9월: 기반 형성

- Anthropic의 multi-agent research system 글은 병렬 서브에이전트, 컨텍스트 압축, coordination 문제를 먼저 드러냈다.
- Manus와 Anthropic의 context engineering 글들은 프롬프트보다 넓은 상태 관리가 중요하다는 인식을 확립했다.
- 같은 시기 benchmark 논문들은 실제 저장소, 보안, 프로그램 수리처럼 환경 의존적인 태스크를 평가하기 시작했다.

### 2025년 11월~2026년 1월: long-running agent와 eval로 확장

- Anthropic은 long-running agent harness, MCP 기반 code execution, eval methodology를 차례로 정리했다.
- LangChain은 deep agent eval과 observability를 통해, 에이전트 시스템 바깥의 측정 체계를 실무 문맥으로 끌고 왔다.
- 여기서부터 이미 `좋은 모델`보다 `좋은 시스템`이 더 중요하다는 메시지가 선명해진다.

### 2026년 2월~3월: 개념의 명명과 정식화

- Mitchell Hashimoto가 `engineer the harness`라는 실무 언어를 던졌고,
- OpenAI가 `Harness engineering: leveraging Codex in an agent-first world`로 개념을 대중화했다.
- LangChain, Inngest, Martin Fowler, DEV 커뮤니티 글들이 이 개념을 성능 향상, 인프라, 인간-에이전트 루프, 개념 정의 차원에서 빠르게 정리했다.
- 학술 쪽에서는 AutoHarness, VeRO, OPENDEV 논문이 거의 동시기에 등장하면서 용어와 연구 문제가 연결되기 시작했다.

## 4. 핵심 테마

### 4-1. 모델보다 환경이 중요해진다

거의 모든 핵심 글이 같은 결론으로 모인다. 일정 수준 이상의 모델 능력이 확보되면, 실제 차이는 다음에서 난다.

- 어떤 컨텍스트를 넣고 뺄지
- 어떤 도구를 어떤 계약으로 노출할지
- 장기 작업에서 상태를 어떻게 남길지
- 실패했을 때 어떤 피드백을 줄지
- 사람의 승인/검토 지점을 어디에 둘지

LangChain의 Terminal Bench 사례는 이 주장을 수치로 보여주고, OpenAI와 Anthropic은 제품 사례로 뒷받침한다.

### 4-2. Context engineering은 harness engineering의 일부다

수집된 문헌을 종합하면 다음처럼 구분하는 것이 가장 명확하다.

- Context engineering: 모델 안에 무엇을 넣을지 설계하는 일
- Harness engineering: 모델 바깥에서 실행, 검증, 기억, 제약, 루프를 설계하는 일

Martin Fowler의 2026년 3월 글이 이 경계를 가장 선명하게 정리해 준다.

### 4-3. 좋은 harness는 긴 작업을 작은 진전으로 분해한다

Anthropic의 long-running agent 글, OpenAI의 Codex 글, Inngest의 event-driven 글은 모두 같은 패턴을 보여준다.

- 한 번에 끝내려 하지 않는다.
- 세션 사이를 잇는 artifact를 남긴다.
- 각 step을 재시도 가능하고 관측 가능하게 만든다.
- 깨끗한 상태와 다음 단계 handoff를 중시한다.

### 4-4. Eval과 observability는 부가 기능이 아니다

Anthropic, LangChain, VeRO, GitTaskBench, PerfBench 모두 평가 harness 없이는 agent improvement가 불가능하다는 점을 강조한다.

- trajectory를 봐야 한다.
- 최종 응답만 보면 안 된다.
- 환경 상태와 실행 결과를 함께 봐야 한다.
- benchmark 자체가 현실적이어야 한다.

## 5. 학술 문헌의 상태

학술 쪽은 아직 `harness engineering`이라는 exact phrase보다 인접 개념이 더 많다.

- 직접 관련: AutoHarness, VeRO, Building AI Coding Agents for the Terminal
- 가까운 기반 연구: Structured Context Engineering, Meta Context Engineering, CEDAR
- 평가/검증 인프라 연구: SEC-bench, GitTaskBench, PerfBench, Agentic Program Repair

즉 실무 담론이 먼저 폭발했고, 논문은 그 주변의 부분문제들을 따라잡는 단계에 가깝다.

## 6. 실무적으로 가장 많이 반복된 패턴

- Repo를 사람이 아니라 agent도 읽기 쉬운 구조로 만든다.
- 규칙, 스펙, 실행 방법, 테스트 방식을 파일로 외부화한다.
- 도구는 많이 주는 것보다 명확한 계약으로 준다.
- 긴 작업은 initializer / planner / executor / reviewer 같은 역할로 쪼갠다.
- 실패를 자동으로 관찰하고, trace에서 개선 포인트를 추출한다.
- 사람은 코드를 직접 쓰기보다 intent, review, merge, exception handling에 집중한다.

## 7. 남아 있는 공백

- 정확한 ROI를 보여주는 공개 데이터가 아직 적다.
- org design과 merge/ownership 변화에 대한 체계적 연구가 부족하다.
- 벤치마크는 늘고 있지만 production drift를 완전히 대변하진 못한다.
- harness 자동 합성은 막 시작 단계이며, 장기 유지보수성 검증이 필요하다.

## 8. 추천 읽기 순서

1. Manus / Anthropic의 context engineering 글로 내부 레이어를 이해한다.
2. Anthropic long-running harness와 LangChain eval 글로 loop와 measurement를 본다.
3. OpenAI의 `Unrolling`, `Unlocking`, `Harness engineering` 3종으로 runtime과 조직 운영을 본다.
4. Martin Fowler의 `Context Engineering`, `Humans and Agents`, `Harness Engineering`으로 개념 경계를 정리한다.
5. AutoHarness, VeRO, OPENDEV 논문으로 학술 흐름을 확인한다.

## 9. 최종 판단

2025년 6월 이후의 문헌을 종합하면, harness engineering은 유행어가 아니라 에이전트 실전 배치에서 생겨난 설계 discipline으로 보는 편이 타당하다. 2025년 하반기에는 context engineering, eval harness, long-running agent design이 각각 따로 발전했고, 2026년 2월 이후 이들이 `harness engineering`이라는 이름 아래 하나의 실무 패턴으로 묶이기 시작했다.
