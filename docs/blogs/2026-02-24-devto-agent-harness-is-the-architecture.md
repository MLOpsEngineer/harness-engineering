# The Agent Harness Is the Architecture (and Your Model Is Not the Bottleneck)

- 구분: 블로그/아티클
- 발행일: 2026-02-24
- 저자: Evangelos Pappas
- 출처: DEV Community
- 원문: https://dev.to/epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-3bjd
- 관련성: 직접

## 한줄 요약
모델 경쟁보다 harness 설계가 production reliability를 좌우한다는 가설을 여러 공개 사례와 논문으로 방어하는 장문 글이다.

## 왜 중요한가
실무자 관점에서 harness engineering 개념을 더 넓은 audience에게 번역해 준 글이다.

## 핵심 내용
- 모델이 일정 capability threshold를 넘으면, reliability 차이는 context management, tool selection, state persistence, error recovery에서 난다고 주장한다.
- OpenAI, LangChain, benchmark 논문 등을 끌어와 harness가 실제 성능 레버라는 근거를 제시한다.
- agent architecture를 논할 때 model choice보다 environment design을 먼저 봐야 한다는 메시지를 강하게 밀어붙인다.

## 원문 기준 핵심 흐름
- 글은 model capability가 어느 임계치를 넘은 뒤부터는 reliability 차이가 harness에서 나온다고 주장한다.
- 그래서 architecture discussion의 출발점도 model leaderboard가 아니라 context, state, error recovery, observability가 된다.
- 여러 공개 글과 논문을 인용하지만, 논지의 핵심은 간단하다. production bottleneck은 model IQ가 아니라 operational substrate다.

## Harness Engineering 관점
- 이 글은 harness engineering을 ‘아키텍처 레벨의 병목’으로 재명명한다.
- 원전은 아니지만 다양한 근거를 한 방향으로 엮어 주기 때문에 빠른 개념 파악에 유용하다.

## 한계와 주의점
- 2차 문헌 의존도가 높고, 사례 해석이 약간 강한 편이다.
- 새로운 기술 패턴을 제안하기보다는 기존 자료를 해설하는 성격이 강하다.
