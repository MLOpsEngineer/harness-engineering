# Effective harnesses for long-running agents

- 구분: 블로그/아티클
- 발행일: 2025-11-26
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 관련성: 직접

## 한줄 요약
여러 context window를 넘나들며 오래 일하는 coding agent에 필요한 harness를 직접적으로 다룬 핵심 기술 글이다.

## 왜 중요한가
‘long-running agent harness’라는 문제 설정을 명확히 하고, initializer agent와 coding agent 분리라는 실제 패턴을 제시한다.

## 원문 기준 핵심 흐름
- 글은 long-running coding agent의 실패 원인을 단순 context overflow가 아니라 `세션 간 handoff 실패`로 본다.
- 그래서 compaction 하나만으로는 부족하고, 초기 환경과 방향을 잡는 `initializer agent`와 실제 구현을 진행하는 `coding agent`를 분리해야 한다고 주장한다.
- 각 세션은 다음 세션이 바로 이어받을 수 있도록 legible한 state를 남겨야 한다. 여기에는 코드 상태, 문서, 해야 할 일, 남은 위험이 포함된다.
- Anthropic은 one-shot으로 큰 작업을 밀어붙이기보다 feature-by-feature, checkpoint-by-checkpoint로 진행하도록 harness가 agent를 유도해야 한다고 본다.
- 핵심은 `다음 턴을 위한 배려를 시스템에 강제`하는 것이다. long-running harness는 현재 작업만이 아니라 미래 세션의 재시작 비용까지 관리한다.

## Harness Engineering 관점
- harness engineering을 가장 직접적으로 설명하는 Anthropic 글이다. 모델 루프 바깥에서 역할 분해, 환경 세팅, handoff artifact 설계를 수행한다.
- 장기 작업에서 ‘다음 턴을 위한 배려’를 시스템에 강제하는 것이 핵심이라는 점이 중요하다.

## 한계와 주의점
- Claude Agent SDK와 코딩 태스크 중심의 사례라 다른 도메인에 그대로 이식하기는 어렵다.
- 정량 비교보다는 설계 원칙과 실패 패턴 공유에 가깝다.
