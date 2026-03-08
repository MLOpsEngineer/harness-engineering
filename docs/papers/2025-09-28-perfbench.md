# PerfBench: Can Agents Resolve Real-World Performance Bugs?

- 구분: 논문
- 발행일: 2025-09-28
- 저자: Spandan Garg 외 2명
- 출처: arXiv
- 원문: https://arxiv.org/abs/2509.24091
- 관련성: 인접 연구

## 한줄 요약
기능 correctness가 아니라 real-world performance bug를 해결하는 능력을 측정하는 benchmark로, agent가 스스로 성능 benchmark를 만들고 그 결과로 patch를 검증하게 하는 evaluation harness를 제안한다.

## 문제 설정
기존 bug-fixing benchmark는 거의 모두 functional correctness에 집중해, 성능 회귀처럼 non-functional issue를 agent가 실제로 다룰 수 있는지 평가하지 못했다.

## 제안 방법
- PerfBench는 GitHub의 popular .NET repository에서 수집한 `81`개 real-world performance bug-fixing task로 구성된다.
- 핵심은 기존 unit test가 아니라, agent가 직접 `BenchmarkDotNet`류의 performance benchmark를 생성해야 한다는 점이다.
- evaluation harness는 agent가 쓴 benchmark test를 추출해 buggy/fixed code 양쪽에서 실행하고, developer fix와 agent fix의 execution metric을 비교한다.
- 논문은 build 통과, unit test 통과, 성능 개선, 다른 metric 악화 없음까지 함께 보려 한다.
- OpenHands-Perf-Agent는 raw benchmark output이 너무 길어지는 문제를 해결하기 위해 benchmark 결과를 요약·추출하는 output processing을 추가했고, 이 방식이 benchmark output 관련 token 사용을 `90% 이상` 줄였다고 설명한다.

## 결과와 시사점
- baseline OpenHands는 GPT-4.1 기준 성공률이 `3%대`에 불과했다.
- performance-aware instruction과 tooling을 넣은 OpenHands-Perf-Agent는 `15~20%` 수준으로 올라 최대 `5배` 가까운 개선을 보인다.
- bug category 분석에서는 memory/allocation 관련 이슈가 benchmark의 `40% 이상`을 차지하고, concurrency와 algorithmic inefficiency가 각 `17%` 내외라고 보고한다.
- 즉 성능 bug에서는 agent가 단순 patch generation보다 `측정 체계 만들기`, `metric 읽기`, `trade-off 해석`을 할 수 있어야 한다는 점이 드러난다.

## Harness Engineering 관점
- harness engineering이 코드 생성 도우미가 아니라 성능 측정 환경까지 포함한다는 점을 강조해 준다.
- 여기서 harness는 benchmark runner이자 measurement oracle이다. functional test가 없을 때는 measurement harness가 곧 task definition이 된다.

## 한계와 주의점
- 성능 버그 도메인에 국한된다.
- agent-generated benchmark의 품질이 결과를 좌우하므로, benchmark 작성 실패가 곧 false negative로 이어질 수 있다.
- .NET/C# 중심이라 다른 언어 생태계로 일반화할 때는 추가 검증이 필요하다.
