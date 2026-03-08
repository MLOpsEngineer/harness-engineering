# AutoHarness: improving LLM agents by automatically synthesizing a code harness

- 구분: 논문
- 발행일: 2026-02-10
- 저자: Xinghua Lou 외 5명
- 출처: arXiv
- 원문: https://arxiv.org/abs/2603.03329
- 관련성: 직접

## 한줄 요약
불법·금지 행동을 줄이기 위해 task-specific code harness를 자동 합성하는, 현재 문헌 중 가장 직접적으로 harness engineering을 다루는 논문이다.

## 문제 설정
LLM agent는 환경 제약을 자주 어기고 illegal move를 낸다. 사람은 이를 막으려고 수작업 harness를 쓰지만, 게임이나 task마다 새로 작성해야 해 확장성이 낮다.

## 제안 방법
- 논문은 이를 `code as harness`라고 부른다. LLM이 직접 자신의 harness code를 생성해 agent를 완성하는 방식이다.
- 가장 단순한 형태는 `propose_action()`과 `is_legal_action()`을 가진 rejection-sampling style harness다.
- harness 생성은 단순 iterative prompting이 아니라 `tree search + Thompson sampling`으로 수행한다.
- 환경이 illegal move, reward, execution failure를 critic으로 제공하고, refiner LLM이 코드를 반복 수정한다.
- 세 가지 harness 형태를 구분한다: `harness-as-action-filter`, `harness-as-action-verifier`, `harness-as-policy`. 마지막은 inference time에 LLM 호출 없이 code만으로 행동까지 결정한다.

## 결과와 시사점
- 출발점으로 논문은 Kaggle GameArena chess에서 Gemini-2.5-Flash 패배의 `78%`가 illegal move 때문이었다고 든다.
- 실험은 free-form dialog game을 제외한 `145`개 TextArena 게임에서 진행한다.
- training은 평균 `14.5` tree-search iteration 후 끝났고, `32`개 게임 중 `19`개는 10 iteration 미만으로 수렴했다고 적는다.
- learned harness는 test rollout에서 `145`개 게임 모두에 대해 `100%` legal action success rate를 달성했다고 주장한다.
- 실제 game play 평가에서는 Gemini-2.5-Flash + Harness가 더 큰 모델인 Gemini-2.5-Pro를 능가한다고 보고한다.
- 더 나아가 code-policy까지 밀어붙였을 때, `16`개 TextArena 1P 게임에서 Gemini-2.5-Pro와 GPT-5.2-High보다 높은 평균 reward를 얻었다고 한다.

## Harness Engineering 관점
- 현재 시점에서 가장 직접적으로 harness engineering을 논문 제목 수준에서 다루는 문헌이다.
- 실무의 `guardrail code`를 자동 생성 대상으로 본다는 점이 특히 중요하다.
- 핵심 통찰은 모델 reasoning을 더 키우는 것보다, task-specific 외부 constraint layer를 잘 합성하는 편이 더 효과적일 수 있다는 것이다.

## 한계와 주의점
- 특정 환경 제약 문제에서 강점을 보이는 만큼, 일반적인 소프트웨어 개발 harness 전체를 포괄하지는 않는다.
- TextArena game이라는 제한된 action-validity setting에 최적화되어 있다.
- generated harness가 장기적으로 얼마나 readable하고 maintainable한지, 실무 코드베이스에서 어떻게 versioning할지는 추가 검증이 필요하다.
