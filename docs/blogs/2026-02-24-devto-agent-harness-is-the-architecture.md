# The Agent Harness Is the Architecture (and Your Model Is Not the Bottleneck)

- 구분: 블로그/아티클
- 발행일: 2026-02-24
- 저자: Evangelos Pappas
- 출처: DEV Community
- 원문: https://dev.to/epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-3bjd
- 관련성: 직접

## 한줄 요약
모델 경쟁보다 harness 설계가 production reliability를 좌우한다는 가설을 여러 공개 사례와 논문으로 방어하며, harness를 아키텍처 레벨의 1등 시민으로 격상시킨 장문 글이다.

## 왜 중요한가
실무자 관점에서 harness engineering 개념을 더 넓은 개발자 audience에게 번역해 준 글이다. 다양한 출처의 근거를 하나의 논지로 엮어 접근 장벽을 낮춘다.

## 원문 기준 핵심 흐름

### 핵심 가설: Model ≠ Bottleneck
- 모델이 일정 capability threshold를 넘으면, reliability 차이는 **context management, tool selection, state persistence, error recovery**에서 난다.
- 모델 leaderboard에서 몇 점 차이보다 harness의 질이 production 결과에 더 큰 영향을 미친다는 주장이다.

### 근거 구성
- **OpenAI harness engineering 글**: 인간 역할이 코드 작성에서 환경 설계로 이동한다는 사례.
- **LangChain Terminal Bench**: 같은 모델에서 harness만 바꿔 `52.8 → 66.5`를 달성한 정량 데이터.
- **AutoHarness 논문**: 작은 모델 + 좋은 harness가 큰 모델을 이긴 학술 사례.
- **Anthropic long-running harness**: initializer/coding agent 분리와 checkpoint 패턴.
- 이 근거들을 종합해 "production bottleneck은 model IQ가 아니라 operational substrate"라는 결론을 이끈다.

### Harness = Architecture
- agent architecture 논의의 출발점이 model leaderboard가 아니라 **context, state, error recovery, observability**가 되어야 한다.
- harness를 "agent를 감싸는 유틸리티"가 아니라 **시스템 아키텍처의 핵심 계층**으로 봐야 한다는 제안이다.
- 비유: 운영체제가 CPU보다 사용자 경험을 더 많이 결정하듯, harness가 모델보다 agent 경험을 더 많이 결정한다.

### 실무 함의
- 팀이 agent 시스템을 설계할 때 model selection에 쓰는 시간과 harness 설계에 쓰는 시간의 비율을 재고해야 한다.
- 모델 교체는 API key 하나 바꾸면 되지만, harness 재설계는 시스템 아키텍처 변경이다. 투자 우선순위를 harness 쪽으로 옮기는 것이 합리적이다.

## Harness Engineering 관점
- 이 글은 harness engineering을 **아키텍처 레벨의 병목**으로 재명명한다.
- 원전(original source)은 아니지만, 다양한 근거를 하나의 방향으로 엮어 주기 때문에 harness engineering 개념의 빠른 파악에 유용한 입문 문서다.
- "model ≠ bottleneck" 가설은 LangChain의 정량 데이터와 AutoHarness의 학술 결과로 뒷받침된다.

## 한계와 주의점
- 2차 문헌 의존도가 높고, 사례 해석이 약간 강한 편이다. 원전을 직접 읽고 비교할 필요가 있다.
- 새로운 기술 패턴을 제안하기보다는 기존 자료를 해설하는 성격이 강하다.
- "model is not the bottleneck"이라는 주장이 절대적인 것은 아니다. 모델 능력이 threshold 이하인 경우에는 여전히 모델이 병목이다.
