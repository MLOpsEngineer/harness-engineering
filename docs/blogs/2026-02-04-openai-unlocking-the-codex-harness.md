# Unlocking the Codex harness: how we built the App Server

- 구분: 블로그/아티클
- 발행일: 2026-02-04
- 저자: Celia Chen
- 출처: OpenAI
- 원문: https://openai.com/index/unlocking-the-codex-harness/
- 관련성: 직접

## 한줄 요약
Codex의 공통 App Server를 통해 여러 client surface(웹, CLI, IDE, macOS) 위에 같은 harness를 재사용하는 아키텍처를 설명한 OpenAI의 인프라 글이다.

## 왜 중요한가
harness를 product surface별 UI의 내부 로직이 아니라 **공통 agent runtime 서비스**로 본다는 점에서, harness engineering을 인프라 아키텍처 문제로 확장한 핵심 문서다.

## 원문 기준 핵심 흐름

### App Server 아키텍처
- Codex harness를 특정 UI의 내부 로직이 아니라, 여러 surface가 공통으로 호출하는 **App Server**로 설명한다.
- App Server는 agent loop의 핵심 로직(prompt assembly, tool dispatch, state management, termination)을 담당하는 중앙 서비스다.
- client(웹 앱, CLI, IDE extension, macOS app)는 UI와 사용자 입력 처리만 담당하고, 실제 agent 로직은 App Server에 위임한다.

### Behavioral Consistency
- 핵심 가치는 코드 재사용 자체보다 **behavioral consistency**다.
- 어디서 Codex를 부르든 비슷한 agent semantics를 보장하려는 설계. 웹에서 물어보든, CLI에서 실행하든, IDE에서 호출하든 동일한 tool set, 동일한 prompt 구조, 동일한 safety guardrail이 적용된다.
- 이는 사용자 경험의 일관성뿐 아니라 **safety와 quality control의 단일 지점**을 만든다. 하나의 harness를 개선하면 모든 surface에 동시에 적용된다.

### Conversation Primitives
- App Server는 **conversation primitive**를 정의한다. 메시지, 턴, 세션, tool call, observation 같은 기본 단위가 표준화되어 있다.
- 이 primitive 위에서 각 client는 자신의 UX를 자유롭게 구현하되, 아래쪽의 agent semantics는 공유한다.
- 새로운 surface를 추가할 때 agent 로직을 다시 구현할 필요가 없다. conversation primitive에 맞춰 client를 만들면 된다.

### Execution Backend 공유
- tool execution, sandbox 관리, file system access, terminal command 실행 같은 **execution backend**도 App Server가 통합 관리한다.
- 이는 보안과 자원 관리의 단일 지점이기도 하다. sandbox 정책, resource limit, timeout 설정이 중앙에서 관리된다.

### Harness를 Shared Runtime Service로
- 이 글의 가장 큰 기여: harness를 **shared runtime service**로 재정의한다.
- 기존 관점: harness = 개별 agent를 감싸는 wrapper code
- 새로운 관점: harness = 여러 UI와 상호작용 방식을 통합하는 **platform-level service**
- 이는 harness engineering을 개별 팀의 agent wrapper 작업에서 **platform engineering**으로 격상시킨다.

## Harness Engineering 관점
- harness engineering을 애플리케이션 아키텍처 문제로 확장한 글이다.
- 좋은 harness는 한 제품의 wrapper가 아니라, 여러 UI와 상호작용 방식을 통합하는 **shared runtime**이 될 수 있음을 보여준다.
- App Server 패턴은 harness의 재사용성과 일관성을 높이는 구체적 아키텍처 레시피다.
- Inngest의 "harness not framework" 주장과 상호 보완적이다. Inngest는 harness의 내구성(durability)을 강조하고, 이 글은 harness의 공유성(shareability)을 강조한다.
- 이 아키텍처를 따르면 harness 개선의 영향 범위가 단일 surface에서 전체 제품 suite로 확대된다.

## 한계와 주의점
- Codex 내부 아키텍처 사례이므로 일반 팀이 이 수준의 shared runtime을 구축하기는 현실적으로 어렵다.
- context curation이나 eval 설계보다는 protocol/integration 설계에 초점이 있어, harness의 "내용"보다 "구조"를 다룬다.
- 다른 조직에서 App Server 패턴을 도입할 때의 구체적 가이드나 비용 분석은 포함되지 않는다.
