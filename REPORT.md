# Harness Engineering 종합 개요

- 작성일: 2026-03-08
- 코퍼스 규모: 블로그/아티클 21건, 논문 10건
- 목적: 수집 아카이브 전체를 `실무 플레이북 + 커버리지 감사` 구조로 다시 읽게 만드는 랜딩 문서

## 이 문서의 역할

이 파일은 더 이상 장문 단일 보고서가 아니다. 대신 새로 정리한 `docs/agent-harness/` 문서 묶음으로 들어가기 위한 개요와 읽기 순서를 제공한다. 원문 분석 아카이브는 그대로 유지하고, 이 파일은 전체 synthesis의 요약 입구 역할만 맡는다.

## 핵심 결론

- harness engineering은 프롬프트 튜닝의 별칭이 아니라 `context + runtime + eval + human loop + organizational operating model`을 함께 설계하는 discipline이다.
- 일정 수준 이상의 모델 능력이 확보되면 성능 차이는 점점 harness에서 난다. 같은 모델에서 harness만 바꿔 큰 성능 향상을 얻은 공개 사례가 이미 존재한다.
- agent를 잘 쓰는 팀은 코드를 더 많이 직접 쓰는 팀이 아니라 repo legibility, specs, tests, checklists, traces, review policy를 더 잘 정비한 팀이다.
- 좋은 harness는 실행 루프와 측정 루프를 동시에 가진다. trace, eval, reproducible environment가 없으면 개선 루프가 닫히지 않는다.
- 사람의 역할은 `직접 코드를 다 읽고 손보는 것`에서 `intent, checks, workflow guidance, approval points를 설계하는 것`으로 이동한다.

## 어디서 읽을지

### 통합 플레이북

1. [docs/agent-harness/README.md](docs/agent-harness/README.md)
2. [docs/agent-harness/01-foundations-and-boundaries.md](docs/agent-harness/01-foundations-and-boundaries.md)
3. [docs/agent-harness/02-why-harnesses-matter.md](docs/agent-harness/02-why-harnesses-matter.md)
4. [docs/agent-harness/03-harnesses-in-agent-development.md](docs/agent-harness/03-harnesses-in-agent-development.md)
5. [docs/agent-harness/04-design-patterns-and-architecture.md](docs/agent-harness/04-design-patterns-and-architecture.md)
6. [docs/agent-harness/05-evals-observability-and-improvement.md](docs/agent-harness/05-evals-observability-and-improvement.md)
7. [docs/agent-harness/06-humans-org-and-operating-model.md](docs/agent-harness/06-humans-org-and-operating-model.md)
8. [docs/agent-harness/07-source-crosswalk-and-coverage-audit.md](docs/agent-harness/07-source-crosswalk-and-coverage-audit.md)

### 원문 아카이브

- [README.md](README.md): 전체 수집 목록
- `docs/blogs/`: 블로그/아티클 개별 분석
- `docs/papers/`: 논문 개별 분석

## 문서별 역할

| 문서 | 무엇을 답하는가 |
|------|----------------|
| `01` | harness engineering의 정의, 경계, 유사 개념 구분 |
| `02` | 왜 harness가 중요한가, 모델 대비 어디서 차이가 나는가 |
| `03` | agent 개발 과정에서 harness가 어디에 쓰이는가 |
| `04` | 어떤 패턴으로 설계해야 하는가 |
| `05` | 어떻게 측정하고 개선하는가 |
| `06` | 사람과 조직은 어떻게 바뀌는가 |
| `07` | 31개 자료가 어디에 반영되었는가 |

## 정량 근거만 빠르게 보기

- LangChain: Terminal Bench 2.0 `52.8 -> 66.5`
- AutoHarness: 작은 모델 + learned harness가 더 큰 모델을 능가
- GitTaskBench: 실패의 절반 이상이 environment setup과 dependency resolution
- PerfBench: performance-aware harness로 baseline 대비 큰 폭 개선
- Meta program repair: 생성 fix 중 `25.5%` landed

## 이 묶음을 어떻게 활용할지

- 개념 정리가 필요하면 `01 -> 02`
- 실무 적용 순서가 필요하면 `03 -> 04`
- tracing, eval, benchmark 설계가 필요하면 `05`
- 팀 운영과 review/merge 재설계가 필요하면 `06`
- 전체 자료 반영 여부를 확인하려면 `07`

## 범위와 주의

- 강조점은 coding/terminal/repo agent다.
- research, data science, security, optimizer-agent 문헌은 직접적인 대상이라기보다 설계 근거와 반례를 제공하는 supporting evidence로 사용했다.
- 벤더 문헌과 논문은 서로 다른 수준의 증거를 제공하므로, `개념 정의`, `정량 근거`, `운영 사례`를 같은 무게로 읽지 않는다.
