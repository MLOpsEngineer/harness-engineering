# Effective harnesses for long-running agents

- 구분: 블로그/아티클
- 발행일: 2025-11-26
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 관련성: 직접

## 한줄 요약
여러 context window를 넘나들며 오래 일하는 coding agent에 필요한 harness를 직접적으로 다룬 핵심 기술 글로, initializer/coding agent 분리와 checkpoint 기반 handoff 패턴을 제시한다.

## 왜 중요한가
'long-running agent harness'라는 문제 설정을 명확히 한 최초의 공식 기술 문서 중 하나다. 단순 context management가 아니라 **다중 세션에 걸친 작업 연속성**을 harness의 핵심 과제로 정의한다.

## 원문 기준 핵심 흐름

### 문제 정의: 세션 간 handoff 실패
- long-running coding agent의 실패 원인을 단순 context overflow가 아니라 **세션 간 handoff 실패**로 본다.
- context compaction만으로는 부족한 이유: compaction은 현재 세션의 정보를 압축할 수 있지만, 다음 세션이 이전 세션의 의도와 결정을 이해하게 만들지는 못한다.
- 핵심 문제는 `다음 턴이 현재 턴의 결과를 바로 이어받을 수 있는가`이다.

### Initializer Agent와 Coding Agent 분리
- **Initializer Agent**: 작업 시작 시 환경을 세팅하고 방향을 잡는다. 코드베이스 탐색, 관련 파일 식별, 작업 계획 수립, 필요한 context 수집을 담당한다.
- **Coding Agent**: 실제 구현을 수행한다. initializer가 준비한 환경과 계획을 받아 코드를 작성하고 테스트한다.
- 이 분리가 필요한 이유: 하나의 agent가 탐색과 구현을 동시에 하면 context가 탐색 과정의 noise로 오염된다. 분리하면 coding agent는 깨끗한 context에서 출발할 수 있다.

### Feature List JSON 구조
- initializer agent가 작업을 구조화하는 핵심 artifact가 **feature list JSON**이다.
- 각 feature는 `이름`, `설명`, `관련 파일 목록`, `수락 기준`, `의존성`을 포함한다.
- 이 JSON은 coding agent에게 전달되는 작업 명세이자, 진행 상황을 추적하는 체크리스트이기도 하다.
- feature-by-feature, checkpoint-by-checkpoint로 진행하도록 harness가 agent를 유도한다. one-shot으로 큰 작업을 밀어붙이는 방식을 명시적으로 피한다.

### 5가지 주요 실패 모드

| 실패 모드 | 설명 | harness 대응 |
|-----------|------|-------------|
| Context drift | 긴 작업 중 초기 목표와 점점 멀어짐 | Feature list를 매 세션마다 재주입 |
| Premature completion | 완료되지 않았는데 완료 선언 | Checkpoint 기반 검증 강제 |
| Lost state | 세션 전환 시 이전 작업 상태 유실 | Structured artifact handoff |
| Scope creep | 원래 범위를 넘어서는 작업 진행 | Feature list로 범위 고정 |
| Regression | 이전에 완료한 feature를 새 작업이 깨뜨림 | 테스트 기반 regression guard |

#### 실패 모드 상세 분석
- **Context drift**: agent가 이전 실패 로그에 anchoring되거나, 중간 탐색 과정에서 원래 목표를 잃어버린다. feature list를 매 세션 시작 시 재주입하면, agent가 항상 전체 목표를 인식한 채로 작업할 수 있다.
- **Premature completion**: agent가 "완료"를 선언했지만 실제로는 edge case 처리가 빠져 있거나 테스트가 통과하지 않는 경우. checkpoint에서 테스트 실행을 강제하면 이를 방지한다.
- **Lost state**: compaction이 핵심 설계 결정의 이유(why)를 손실시키는 것이 주원인. 구조화된 handoff artifact에 "왜 이 방식을 선택했는가"를 명시적으로 포함해야 한다.
- **Scope creep**: coding agent가 현재 feature와 관련 없는 리팩토링이나 코드 정리를 시작하는 경우. initializer가 각 feature의 범위를 파일 단위까지 명시하면 방지 가능하다.
- **Regression**: feature B 구현이 feature A의 동작을 깨뜨리는 경우. 각 checkpoint에서 전체 테스트 suite를 실행하는 것이 가장 확실한 방어책이다.

### 5가지 설계 원칙
1. **Legible State**: 각 세션은 다음 세션이 바로 이어받을 수 있도록 읽기 쉬운 상태를 남겨야 한다. 코드 상태, 문서, 해야 할 일, 남은 위험이 포함된다.
2. **Checkpoint Granularity**: 작업을 작은 단위로 나누고 각 단위의 완료를 명시적으로 확인한다. `commit = checkpoint`가 가장 자연스러운 패턴이다.
3. **Artifact-based Handoff**: 세션 간 전달은 자연어 요약이 아니라 구조화된 artifact(JSON, 파일 목록, 테스트 결과)를 통해 이루어져야 한다.
4. **Progressive Disclosure**: agent에게 전체 작업을 한 번에 보여주지 않고, 현재 단계에 필요한 정보만 점진적으로 제공한다.
5. **Fail-safe Defaults**: agent가 불확실한 상황에서 어떻게 행동할지를 harness가 사전에 정의해야 한다. 기본값은 항상 안전한 방향이어야 한다.

### "다음 턴을 위한 배려"
- 글의 가장 핵심적인 메시지: long-running harness는 현재 작업만이 아니라 **미래 세션의 재시작 비용까지 관리**한다.
- `다음 턴을 위한 배려를 시스템에 강제`하는 것이 long-running harness의 본질이다.
- 이는 단순히 state를 저장하는 것이 아니라, 다음 agent가 해당 state를 **이해하고 활용할 수 있는 형태**로 남기는 것까지 포함한다.

## Harness Engineering 관점
- harness engineering을 가장 직접적으로 설명하는 Anthropic 기술 글이다. 모델 루프 바깥에서 역할 분해, 환경 세팅, handoff artifact 설계를 수행한다.
- initializer/coding agent 분리는 Fowler가 말하는 `role separation` 패턴의 가장 구체적인 구현이다.
- feature list JSON은 `deterministic constraint`의 전형적 사례다. agent의 행동 범위를 구조화된 데이터로 고정한다.
- checkpoint 패턴은 Inngest의 `durable execution`과 같은 문제 — 장기 실행의 안정성 — 를 다른 추상화 수준에서 풀고 있다.
- 5가지 실패 모드 분류는 다른 agent 시스템의 harness를 설계할 때 체크리스트로 활용할 수 있다.

## 한계와 주의점
- Claude Agent SDK와 코딩 태스크 중심의 사례라 다른 도메인(데이터 분석, 고객 응대 등)에 그대로 이식하기는 어렵다.
- 정량 비교보다는 설계 원칙과 실패 패턴 공유에 가깝다. 각 원칙이 어느 정도의 성능 개선을 가져왔는지 수치는 제시되지 않는다.
- initializer/coding agent 분리가 모든 상황에 최적인지는 불분명하다. 작은 작업에서는 오히려 overhead가 될 수 있다.
