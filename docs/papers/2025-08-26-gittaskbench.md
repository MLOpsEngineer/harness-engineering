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
실제 개발 업무는 scratch coding보다 기존 repository 탐색, README/코드 이해, dependency setup, task-specific execution을 포함하는데, 기존 benchmark는 이 현실을 충분히 반영하지 못했다.

## 제안 방법
- GitTaskBench는 `54`개 현실적 태스크를 `18`개 GitHub 프로젝트, `7`개 modality, `7`개 domain, `24`개 subdomain에 걸쳐 구성한다.
- 각 태스크는 repository와 함께 `human-curated automated evaluation harness`를 제공해 practical success criteria를 자동 평가한다.
- 논문은 benchmark를 네 단계로 만들었다고 설명한다: task/repository selection, completeness verification, execution framework design, evaluation framework development.
- 단순 success 외에 `alpha value`를 제안한다. 이는 success quality, token cost, developer salary를 결합해 agent의 경제적 효용을 추정하려는 지표다.

## 결과와 시사점
- 실험 결과 최고 성능은 `OpenHands + Claude 3.7`의 `48.15%` task solve rate였다. 논문 초반에는 이후 `RepoMaster + Claude 3.5`가 `62.96%`로 frontier를 올렸다고도 적는다.
- 실패 분석에서 `절반 이상`이 environment setup과 dependency resolution 같은 seemingly mundane step에서 발생했다고 보고한다.
- multimodal task는 pure textual task보다 어렵고, practical deployment 관점에서는 environment configuration과 dependency management가 agent 성능의 핵심 병목이라고 결론짓는다.
- alpha metric 분석을 통해, 성능이 높아도 항상 human 대비 비용 효율적이지는 않다고 본다. 즉 실제 현업 적용에서는 solve rate와 비용을 함께 봐야 한다.

## Harness Engineering 관점
- repo leveraging이라는 현실 문제는 harness engineering의 핵심 과제와 거의 동일하다.
- 좋은 모델보다 좋은 environment preparation, timeout budget, dependency handling, practical success criteria가 더 중요하다는 근거를 준다.
- 이 benchmark의 평가 harness가 바로 repository-aware harness의 축소판처럼 작동한다는 점이 중요하다.

## 한계와 주의점
- benchmark이므로 개선 방법론보다는 문제 제시가 중심이다.
- benchmark이라 어떤 harness 전략이 항상 최적인지까지는 제시하지 않는다.
- alpha metric은 흥미롭지만 salary와 token cost 가정에 민감할 수 있다.
