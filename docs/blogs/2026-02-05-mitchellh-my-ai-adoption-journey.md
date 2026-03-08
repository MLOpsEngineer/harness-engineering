# My AI Adoption Journey

- 구분: 블로그/아티클
- 발행일: 2026-02-05
- 저자: Mitchell Hashimoto
- 출처: Mitchell Hashimoto
- 원문: https://mitchellh.com/writing/my-ai-adoption-journey
- 관련성: 직접

## 한줄 요약
`Step 5: Engineer the Harness`로 유명한 글로, 개인 개발자의 AI 활용이 chat assistant에서 지속적으로 돌아가는 agent workflow로 바뀌는 과정을 설명한다.

## 왜 중요한가
실무 현장에서 harness engineering이 왜 모델 선택보다 큰 차이를 만드는지 체감적으로 설명한 대표적 practitioner essay다.

## 원문 기준 핵심 흐름
- 글은 AI adoption을 여러 단계로 나누며, 채팅 보조를 넘어서는 순간이 `Engineer the Harness` 단계라고 말한다.
- 가치 있는 활용은 모델과 대화하는 시간이 아니라, agent가 독립적으로 useful work를 할 수 있게 repo와 feedback environment를 정비하는 데서 나온다고 본다.
- 여기에는 테스트, 문서, 스크립트, task framing, 프로젝트 구조가 모두 포함된다.
- `항상 에이전트 하나는 돌고 있게 하라`는 문장은, 인간의 역할이 코드를 직접 쓰는 것에서 agent orchestration과 supervision으로 이동한다는 감각을 잘 보여 준다.

## Harness Engineering 관점
- OpenAI가 용어를 대중화하기 직전, 현업 개발자가 자발적으로 같은 결론에 도달했다는 점이 중요하다.
- harness를 agent가 일하기 좋은 repo/feedback environment로 본다는 점에서 이후 논의를 예고한다.

## 한계와 주의점
- 개인 경험을 바탕으로 하므로 통제된 비교는 없다.
- 대규모 팀 운영보다는 solo/small-team workflow에 가까운 관점이다.
