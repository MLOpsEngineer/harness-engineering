# Context Engineering for AI Agents: Lessons from Building Manus

- 구분: 블로그/아티클
- 발행일: 2025-07-18
- 저자: Yichao 'Peak' Ji
- 출처: Manus
- 원문: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- 관련성: 기반

## 한줄 요약
Manus 팀이 실제 agent product를 만들며 정리한 context engineering 실전 메모로, 긴 작업을 지속시키기 위해 대화 바깥의 상태를 어떻게 구조화하고 다시 주입할지를 설명한다.

## 왜 중요한가
2025년 하반기 harness engineering 담론의 바탕이 된 글 중 하나로, 프롬프트보다 더 넓은 의미의 상태 설계를 강조한다.

## 원문 기준 핵심 흐름
- 글은 context를 단순 system prompt가 아니라, 계획, 파일, 메모리, tool result, 실행 기록, intermediate artifact 전체로 정의한다.
- 핵심 문제는 long-running task에서 대화 히스토리만으로 상태를 유지하려 하면 context가 금방 붕괴한다는 점이다.
- Manus는 이를 해결하기 위해 정보를 외부 file/artifact로 옮기고, agent가 필요한 시점에 필요한 조각만 다시 읽게 하는 방식이 더 안정적이라고 본다.
- 따라서 좋은 context engineering은 `무엇을 기억할지`만이 아니라 `어떤 형식으로 남길지`, `다음 세션의 agent가 다시 읽기 쉽게 어떻게 정리할지`까지 포함한다.
- 글 전반의 메시지는, agent가 미래의 자신이나 다른 agent를 위해 legible한 흔적을 남기게 만드는 것이 productivity의 핵심이라는 것이다.

## Harness Engineering 관점
- harness engineering 관점에서 보면 Manus는 ‘컨텍스트를 운영체제처럼 관리하는 방법’을 설명한다.
- 모델 안쪽보다 바깥쪽에서 어떤 파일 구조, 요약 규칙, 리트리벌 경로를 만들 것인지가 핵심이라는 점을 분명히 한다.

## 한계와 주의점
- 정량 성능 실험보다 제품 경험을 바탕으로 한 설계 원칙 중심이다.
- 특정 구현 세부가 충분히 공개되지는 않아 재현성은 제한적이다.
