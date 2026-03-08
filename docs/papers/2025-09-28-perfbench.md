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
기존 bug-fixing benchmark는 거의 모두 functional correctness에 집중해, 성능 회귀처럼 non-functional issue를 agent가 실제로 다룰 수 있는지 평가하지 못했다. 성능 버그는 기능 테스트를 통과하면서도 시스템을 느리게 만들기 때문에, 전통적 test oracle로는 잡아내기 어렵다.

## 제안 방법

### Benchmark 구성
- PerfBench는 GitHub의 popular .NET repository에서 수집한 `81`개 real-world performance bug-fixing task로 구성된다.
- 각 task는 실제 개발자가 performance regression을 발견하고 고친 PR에서 추출한 것이다.
- bug category 분포: memory/allocation 관련 이슈가 `40% 이상`, concurrency 이슈가 `~17%`, algorithmic inefficiency가 `~17%`, 나머지는 I/O, caching, data structure 관련이다.

### Agent-Generated Benchmark
- 핵심 혁신: 기존 unit test가 아니라, **agent가 직접 `BenchmarkDotNet`류의 performance benchmark를 생성**해야 한다.
- 즉 agent는 버그를 고치기만 하는 것이 아니라, 자기 patch의 효과를 **측정할 수 있는 도구까지 만들어야** 한다.
- 이것이 PerfBench의 핵심 난이도 원천이다. functional test는 "맞다/틀리다"를 판단하면 되지만, performance benchmark는 "얼마나 빨라졌는지"를 정량적으로 측정해야 한다.

### Evaluation Harness
- evaluation harness는 agent가 작성한 benchmark test를 추출해 **buggy code와 fixed code 양쪽에서 실행**하고, developer fix와 agent fix의 execution metric을 비교한다.
- 평가 기준: (1) build 통과, (2) unit test 통과, (3) 성능 개선 확인, (4) 다른 metric 악화 없음을 함께 본다.
- 즉 harness는 **multi-criteria evaluator** 역할을 한다. 기능이 깨지면서 빨라지는 것은 성공이 아니다.

### Output Processing
- OpenHands-Perf-Agent는 raw benchmark output이 너무 길어지는 문제를 해결하기 위해 benchmark 결과를 **요약·추출하는 output processing**을 추가했다.
- 이 방식이 benchmark output 관련 token 사용을 `90% 이상` 줄였다고 설명한다.
- 이는 harness engineering의 핵심 문제 중 하나인 **observation size 관리**의 구체적 해결 사례다.

## 결과와 시사점
- baseline OpenHands는 GPT-4.1 기준 성공률이 `3%대`에 불과했다.
- performance-aware instruction과 tooling을 넣은 OpenHands-Perf-Agent는 `15~20%` 수준으로 올라 최대 `5배` 가까운 개선을 보인다.
- 성능 bug에서는 agent가 단순 patch generation보다 **측정 체계 만들기, metric 읽기, trade-off 해석**을 할 수 있어야 한다는 점이 드러난다.
- output processing 하나만으로 token 효율이 극적으로 개선된다는 점은 harness의 observation formatting이 얼마나 중요한지를 보여준다.

## Harness Engineering 관점
- harness engineering이 코드 생성 도우미가 아니라 **성능 측정 환경까지 포함**한다는 점을 강조해 준다.
- 여기서 harness는 benchmark runner이자 measurement oracle이다. functional test가 없을 때는 **measurement harness가 곧 task definition**이 된다.
- output processing을 통한 token 절감(`90%+`)은 Structured Context Engineering 논문의 "grep tax" 개념과 직접 연결된다. observation을 그대로 context에 넣으면 token이 폭발하고, 요약하면 효율이 올라가지만 정보 손실 위험이 있다.
- agent가 benchmark를 "작성"하고 harness가 그것을 "실행·비교"하는 구조는, agent와 harness의 역할 분리를 잘 보여준다.

## 한계와 주의점
- 성능 버그 도메인에 국한된다. functional bug-fixing과는 평가 체계가 다르므로 직접 비교가 어렵다.
- agent-generated benchmark의 품질이 결과를 좌우하므로, **benchmark 작성 실패가 곧 false negative**로 이어질 수 있다.
- .NET/C# 중심이라 다른 언어 생태계로 일반화할 때는 추가 검증이 필요하다.
- `81`개 task는 비교적 소규모이며, 통계적 유의성에는 한계가 있을 수 있다.
