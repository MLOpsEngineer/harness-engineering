# My AI Adoption Journey

- 구분: 블로그/아티클
- 발행일: 2026-02-05
- 저자: Mitchell Hashimoto
- 출처: Mitchell Hashimoto
- 원문: https://mitchellh.com/writing/my-ai-adoption-journey
- 관련성: 직접

## 한줄 요약
`Step 5: Engineer the Harness`로 유명한 글로, 개인 개발자의 AI 활용이 chat assistant에서 지속적으로 돌아가는 agent workflow로 바뀌는 과정을 6단계로 설명한다.

## 왜 중요한가
OpenAI가 "harness engineering"이라는 용어를 대중화하기 직전, 현업 개발자가 자발적으로 같은 결론에 도달했다는 점에서 harness engineering이 이론적 구성물이 아니라 실무적 필요에서 자연 발생한 개념임을 보여 준다.

## 원문 기준 핵심 흐름

### 6단계 AI adoption 여정
1. **Dismissal**: AI를 무시하거나 과소평가하는 초기 단계.
2. **Chat as Search**: ChatGPT를 구글 대신 쓰는 수준. 질문-답변 패턴에 머무른다.
3. **Chat as Pair Programmer**: 코드 생성을 대화 인터페이스에서 요청. 아직 copy-paste 중심이고 context는 수동으로 관리한다.
4. **Inline Assistant**: IDE에 통합된 Copilot류 도구 사용. autocomplete와 inline suggestion이 워크플로에 들어온다.
5. **Engineer the Harness** (핵심 단계): 모델과 대화하는 시간보다, agent가 독립적으로 유용한 작업을 할 수 있도록 **repo 환경과 feedback loop를 정비**하는 데 투자하기 시작한다. 여기에는 테스트 커버리지 확대, 문서 정비, 린트 스크립트, task framing, 프로젝트 구조 개선이 포함된다. 이 단계에서 가치의 원천이 "모델 품질"에서 "harness 품질"로 이동한다.
6. **Continuous Agent Workflow**: 항상 에이전트 하나는 돌고 있게 한다. 인간의 역할이 코드를 직접 쓰는 것에서 agent orchestration과 supervision으로 이동한다. Hashimoto는 자신의 업무 시간 중 `10~20%`를 background agent와 함께 보낸다고 언급한다.

### "Engineer the Harness"의 구체적 의미
- Hashimoto는 harness를 **agent가 일하기 좋은 repo 환경과 feedback 체계**로 정의한다.
- 핵심은 모델을 바꾸는 게 아니라 **모델이 작동하는 환경을 바꾸는 것**이다. 테스트가 없으면 agent는 자기 작업을 검증할 수 없고, 문서가 없으면 agent는 codebase를 이해할 수 없고, 구조가 엉망이면 agent는 올바른 파일을 찾지 못한다.
- 이 관점에서 harness engineering은 agent를 위한 것인 동시에 인간 개발자를 위한 것이기도 하다. 좋은 harness는 좋은 개발 환경이다.

### 실무적 전환의 감각
- 가장 큰 전환은 **시간 배분**에서 일어난다. 코드를 직접 작성하는 시간이 줄고, agent가 작업할 수 있는 조건을 만드는 시간이 늘어난다.
- Hashimoto는 이 전환이 처음에는 비생산적으로 느껴지지만, 복리 효과가 크다고 강조한다. 한번 정비한 harness는 모든 후속 agent 작업에 재사용된다.
- `항상 에이전트 하나는 돌고 있게 하라`는 문장이 글의 결론에 해당하며, 개발자의 역할 변화를 가장 함축적으로 표현한다.

## Harness Engineering 관점
- OpenAI의 공식 글보다 먼저, 실무자가 동일한 결론에 도달했다는 점에서 harness engineering이 top-down 마케팅이 아니라 bottom-up 실무 패턴임을 증명한다.
- harness를 `agent가 일하기 좋은 repo/feedback environment`로 보는 정의는 이후 Anthropic, LangChain, Inngest의 논의와 정확히 연결된다.
- 6단계 모델은 조직의 AI 성숙도를 진단하는 간편한 프레임워크로 활용할 수 있다. 대부분의 팀이 3~4단계에 머물러 있고, 5단계로의 전환이 핵심 변곡점이다.
- "항상 에이전트 하나는 돌고 있게 하라"는 조언은 이후 Fowler의 `humans on the loop` 개념과 직접 연결된다.

## 한계와 주의점
- 개인 경험을 바탕으로 하므로 통제된 비교나 정량 데이터는 없다.
- 대규모 팀 운영보다는 solo/small-team workflow에 가까운 관점이다.
- 6단계가 선형적으로 보이지만 실제로는 병행하거나 되돌아가는 경우도 많을 것이다.
