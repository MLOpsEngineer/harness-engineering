# Demystifying evals for AI agents

- 구분: 블로그/아티클
- 발행일: 2026-01-09
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- 관련성: 기반

## 한줄 요약
agent evaluation을 single-turn QA에서 multi-turn, stateful, tool-using system 평가로 확장해 설명한 방법론 글로, eval harness 설계의 기준 문서다.

## 왜 중요한가
harness engineering에서 observability와 eval은 선택이 아니라 필수라는 점을 구조적으로 설명한다. 좋은 harness는 실행 loop와 함께 **측정 loop**를 동시에 가져야 한다는 원칙을 확립한다.

## 원문 기준 핵심 흐름

### Agent Eval이 Model Eval과 다른 이유
- agent는 tool을 호출하고, environment state를 바꾸며, trajectory(행동 경로)를 남긴다.
- 따라서 최종 문자열만 비교하는 방식으로는 실제 능력 변화를 잡지 못한다.
- 같은 정답에 도달하더라도 경로가 다를 수 있다. 효율적인 경로와 비효율적인 경로를 구분할 수 있어야 한다.

### Eval의 4가지 구성 요소
1. **Trajectory**: agent가 어떤 순서로 어떤 tool을 호출했는지. 행동 경로 자체가 평가 대상이다.
2. **Final Response**: agent의 최종 출력. 정답 여부뿐 아니라 형식, 완결성, 정확성을 본다.
3. **Environment State**: agent 실행 후 환경이 어떤 상태인지. 파일이 올바르게 수정되었는지, 테스트가 통과하는지, 부작용은 없는지.
4. **Grader Logic**: 위 세 가지를 종합해 점수를 매기는 로직. 단순 string match부터 LLM-as-a-judge까지 다양하다.

### Eval 수준의 분류
- **Single-step eval**: 한 번의 tool call이나 한 번의 응답을 평가. 국소적 의사결정의 품질을 본다.
- **Full-turn eval**: 한 번의 완결된 실행(task 시작부터 완료까지)을 평가. 전체 작업의 성공 여부를 본다.
- **Multi-turn eval**: 여러 번의 상호작용에 걸친 지속성을 평가. 긴 대화에서 context를 유지하는지, 이전 결정과 일관되는지를 본다.

### Eval을 운영 장치로
- Anthropic은 eval을 one-off experiment가 아니라 **production regression을 조기에 잡는 운영 장치**로 본다.
- harness를 변경할 때마다 eval을 돌려서 regression이 없는지 확인한다. 이는 소프트웨어 개발의 CI test와 동일한 역할이다.
- eval suite는 harness와 함께 성장해야 한다. 새로운 failure mode가 발견되면 그에 해당하는 eval case를 추가한다.
- 즉 좋은 harness는 "agent를 실행하는 loop"과 "loop를 관찰하고 채점하는 loop"를 동시에 가진다.

### 실용적 권고
- eval 환경의 재현 가능성이 가장 중요하다. 환경이 지저분하거나 재현 불가능하면 모델 변화보다 환경 편차가 결과를 지배한다.
- 초기에는 소수의 고품질 eval case로 시작해, 실패 패턴이 발견될 때마다 점진적으로 확장하는 것이 현실적이다.
- eval 결과를 해석할 때 pass/fail 이분법보다 **trajectory 분석**이 더 유용하다. 왜 실패했는지, 어디서 잘못된 결정을 했는지를 아는 것이 harness 개선의 출발점이다.

## Harness Engineering 관점
- harness engineering은 agent loop를 짜는 일만이 아니라, **loop를 어떻게 관찰하고 자동 채점할지 설계하는 일**까지 포함한다.
- '좋은 harness는 좋은 eval과 함께 자란다'는 원칙은 LangChain의 trace-based 개선 루프와 직접 연결된다.
- eval의 4가지 구성 요소(trajectory, final response, environment state, grader logic)는 eval harness 설계의 체크리스트로 활용 가능하다.
- VeRO 논문이 제시한 evaluation harness 설계 요구사항(versioning, budget enforcement, reproducible execution)은 이 글의 원칙을 학술적으로 구체화한 것으로 읽을 수 있다.

## 한계와 주의점
- 구체 구현보다는 평가 원칙과 프레임이 중심이다. 특정 eval framework의 코드나 API는 포함되지 않는다.
- 오픈 벤치마크 결과보다는 실무 general guidance 성격이 강하다.
- multi-turn eval의 구체적 구현 방법은 아직 업계 전체에서 미성숙한 영역이며, 이 글도 원칙만 제시하고 구현 디테일은 부족하다.
