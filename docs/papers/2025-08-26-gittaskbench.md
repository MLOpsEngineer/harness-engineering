# GitTaskBench: A Benchmark for Code Agents Solving Real-World Tasks Through Code Repository Leveraging

- 구분: 논문
- 발행일: 2025-08-26
- 저자: Ziyi Ni 외 17명
- 출처: arXiv
- 원문: https://arxiv.org/abs/2508.18993
- 관련성: 인접 연구

## 한줄 요약
오픈소스 저장소를 실제 개발자처럼 활용해 end-to-end task를 해결하는 능력을 평가하는 benchmark로, repository-aware harness와 environment provisioning의 중요성을 정면에서 보여준다.

## 문제 설정
실제 개발 업무는 scratch coding보다 **기존 repository 탐색, README/코드 이해, dependency setup, task-specific execution**을 포함하는데, 기존 benchmark(SWE-bench 등)는 이 현실을 충분히 반영하지 못했다. SWE-bench는 bug-fix에 집중하고, HumanEval은 isolated function에 집중한다.

## 제안 방법

### Benchmark 구성
- GitTaskBench는 `54`개 현실적 태스크를 `18`개 GitHub 프로젝트, `7`개 modality, `7`개 domain, `24`개 subdomain에 걸쳐 구성한다.
- task 유형이 bug-fix에 국한되지 않고, **feature implementation, configuration, data processing, visualization** 등 실제 개발자가 하는 다양한 작업을 포함한다.
- 각 태스크는 repository와 함께 `human-curated automated evaluation harness`를 제공해 practical success criteria를 자동 평가한다.

### 4단계 Benchmark 구축 프로세스
1. **Task/Repository Selection**: 다양한 domain과 modality를 커버하도록 프로젝트와 task를 선정.
2. **Completeness Verification**: 각 task가 repository 정보만으로 완료 가능한지 사람이 검증.
3. **Execution Framework Design**: agent가 task를 실행할 수 있는 환경(Docker container, dependency, timeout)을 구축.
4. **Evaluation Framework Development**: task별 성공 기준과 자동 채점 로직을 구현.

### Alpha Value: 경제적 효용 지표
- 단순 success rate 외에 `alpha value`를 제안한다. 이는 **success quality, token cost, developer salary**를 결합해 agent의 경제적 효용을 추정하려는 지표다.
- alpha > 1이면 agent가 사람보다 비용 효율적, alpha < 1이면 사람이 더 효율적.
- 이 지표는 "agent가 문제를 풀 수 있는가"를 넘어 "agent가 문제를 풀어도 경제적으로 합리적인가"를 묻는다.

## 결과와 시사점

### 성능 결과
- 최고 성능은 `OpenHands + Claude 3.7`의 `48.15%` task solve rate였다. 이후 `RepoMaster + Claude 3.5`가 `62.96%`로 frontier를 올렸다고도 적는다.
- 이 수치가 보여주는 것: 가장 좋은 agent라도 **절반 이상의 현실적 task를 해결하지 못한다**.

### 실패 분석: Environment가 핵심 병목
- 실패 분석에서 **절반 이상이 environment setup과 dependency resolution** 같은 seemingly mundane step에서 발생했다.
- 코드 생성 능력 자체는 충분하지만, **repository를 올바르게 설정하고, 의존성을 설치하고, 실행 환경을 구성하는 능력**이 부족하다.
- multimodal task는 pure textual task보다 어렵다.
- 이 결과는 harness engineering의 핵심 주장 — 모델 능력보다 환경 설계가 중요하다 — 을 benchmark 수준에서 뒷받침한다.

### 경제적 효용
- alpha metric 분석 결과, 성능이 높아도 **항상 human 대비 비용 효율적이지는 않다**. token 비용이 높은 복잡한 task에서는 사람이 더 효율적일 수 있다.
- 실제 현업 적용에서는 solve rate와 비용을 함께 봐야 한다.

## Harness Engineering 관점
- repo leveraging이라는 현실 문제는 harness engineering의 핵심 과제와 거의 동일하다. agent가 repo를 이해하고 활용하려면 repo가 **agent-friendly**해야 한다.
- 좋은 모델보다 **좋은 environment preparation, timeout budget, dependency handling, practical success criteria**가 더 중요하다는 근거를 준다.
- 이 benchmark의 evaluation harness가 바로 **repository-aware harness의 축소판**처럼 작동한다는 점이 중요하다. 평가를 위해 만든 harness가 사실상 production harness의 프로토타입이다.
- 실패 원인 분석에서 environment setup이 절반 이상이라는 결과는 OpenAI의 "agent legibility"와 직접 연결된다.

## 한계와 주의점
- benchmark이므로 개선 방법론보다는 문제 제시가 중심이다. 어떤 harness 전략이 항상 최적인지까지는 제시하지 않는다.
- `54`개 task는 비교적 소규모이며, domain별 task 수가 적어 세분화된 분석에는 한계가 있다.
- alpha metric은 흥미롭지만 salary와 token cost 가정에 민감할 수 있다.
