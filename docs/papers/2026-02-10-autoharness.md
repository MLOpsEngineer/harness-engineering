# AutoHarness: improving LLM agents by automatically synthesizing a code harness

- 구분: 논문
- 발행일: 2026-02-10
- 저자: Xinghua Lou 외 5명
- 출처: arXiv
- 원문: https://arxiv.org/abs/2603.03329
- 관련성: 직접

## 한줄 요약
불법·금지 행동을 줄이기 위해 task-specific code harness를 자동 합성하는, 현재 문헌 중 가장 직접적으로 harness engineering을 논문 제목 수준에서 다루는 연구다.

## 문제 설정
LLM agent는 환경 제약을 자주 어기고 illegal move를 낸다. 사람은 이를 막으려고 수작업 harness(guardrail code)를 쓰지만, 게임이나 task마다 새로 작성해야 해 **확장성이 낮다**. 이 문제를 자동화할 수 있는가?

## 제안 방법

### "Code as Harness" 패러다임
- 논문은 이를 `code as harness`라고 부른다. **LLM이 직접 자신의 harness code를 생성**해 agent를 완성하는 방식이다.
- harness는 agent의 행동을 제약하거나 검증하는 코드다. 수작업으로 만들던 것을 자동 합성의 대상으로 전환한다.

### 세 가지 Harness 형태
1. **Harness-as-action-filter**: `propose_action()`과 `is_legal_action()`을 가진 rejection-sampling style. agent가 행동을 제안하면 harness가 합법성을 확인하고, 불법이면 재제안을 요구한다.
2. **Harness-as-action-verifier**: agent의 행동을 사후 검증하는 방식. filter보다 느슨하지만 구현이 간단하다.
3. **Harness-as-policy**: inference time에 **LLM 호출 없이 code만으로 행동까지 결정**한다. 가장 극단적인 형태로, harness가 곧 agent가 된다.

### 합성 방법: Tree Search + Thompson Sampling
- harness 생성은 단순 iterative prompting이 아니라 **tree search + Thompson sampling**으로 수행한다.
- 환경이 illegal move, reward, execution failure를 **critic**으로 제공하고, refiner LLM이 코드를 반복 수정한다.
- training은 평균 `14.5` tree-search iteration 후 끝났고, `32`개 게임 중 `19`개는 10 iteration 미만으로 수렴했다고 적는다.

### 실험 환경
- 출발 동기: Kaggle GameArena chess에서 **Gemini-2.5-Flash 패배의 `78%`가 illegal move** 때문이었다.
- 실험은 free-form dialog game을 제외한 **145개 TextArena 게임**에서 진행한다.

## 결과와 시사점

### Legal Action 완전 해결
- learned harness는 test rollout에서 **145개 게임 모두에 대해 `100%` legal action success rate**를 달성했다고 주장한다.
- 즉 harness가 illegal move 문제를 완전히 해결했다.

### 작은 모델이 큰 모델을 이긴다
- Gemini-2.5-Flash + Harness가 **더 큰 모델인 Gemini-2.5-Pro를 능가**한다고 보고한다.
- 더 나아가 code-policy까지 밀어붙였을 때, `16`개 TextArena 1P 게임에서 **Gemini-2.5-Pro와 GPT-5.2-High보다 높은 평균 reward**를 얻었다고 한다.
- 이는 "모델 크기보다 harness 품질이 더 중요할 수 있다"는 harness engineering의 핵심 주장을 학술적으로 뒷받침하는 결과다.

### Harness-as-Policy의 함의
- harness가 단순 guardrail을 넘어 **agent의 전략까지 결정**할 수 있다는 점은 놀라운 결과다.
- 이 경우 LLM은 harness code를 생성하는 데만 사용되고, 실행 시에는 LLM 없이 code만으로 행동한다.
- 이는 "harness는 agent의 보조 장치"라는 통념을 뒤집는다. 특정 조건에서는 **harness가 agent의 핵심**이 될 수 있다.

## Harness Engineering 관점
- 현재 시점에서 가장 직접적으로 harness engineering을 논문 제목 수준에서 다루는 문헌이다.
- 실무의 `guardrail code`를 **자동 생성 대상**으로 본다는 점이 특히 중요하다. 수작업 harness의 확장성 한계를 극복하려는 시도다.
- 핵심 통찰: **모델 reasoning을 더 키우는 것보다, task-specific 외부 constraint layer를 잘 합성하는 편이 더 효과적**일 수 있다.
- 세 가지 harness 형태(filter, verifier, policy)는 harness 설계의 스펙트럼을 잘 보여준다. filter는 가장 보수적이고, policy는 가장 극단적이다.
- LangChain의 middleware 패턴(PreCompletionChecklist 등)은 harness-as-action-filter의 실무 버전으로 읽을 수 있다.

## 한계와 주의점
- TextArena game이라는 **제한된 action-validity setting**에 최적화되어 있다. 소프트웨어 개발처럼 action space가 거의 무한한 환경에서 동일한 방식이 작동할지는 미지수다.
- generated harness가 장기적으로 얼마나 readable하고 maintainable한지, 실무 코드베이스에서 어떻게 versioning할지는 추가 검증이 필요하다.
- harness-as-policy는 인상적이지만, creative/open-ended task에서는 적용이 어려울 수 있다.
- 일반적인 소프트웨어 개발 harness 전체를 포괄하지는 않는다.
