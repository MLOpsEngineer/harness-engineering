# Unlocking the Codex harness: how we built the App Server

- 구분: 블로그/아티클
- 발행일: 2026-02-04
- 저자: Celia Chen
- 출처: OpenAI
- 원문: https://openai.com/index/unlocking-the-codex-harness/
- 관련성: 직접

## 한줄 요약
Codex의 공통 App Server를 통해 여러 client 위에 같은 harness를 재사용하는 아키텍처를 설명한 OpenAI의 인프라 글이다.

## 왜 중요한가
harness를 product surface별 UI가 아니라 공통 agent runtime 서비스로 본다는 점에서 매우 중요하다.

## 원문 기준 핵심 흐름
- 글은 Codex harness를 특정 UI의 내부 로직이 아니라, 여러 surface가 공통으로 호출하는 App Server로 설명한다.
- 웹 앱, CLI, IDE extension, macOS app 등이 같은 conversation primitive와 execution backend를 공유하도록 계층을 나눈다.
- 핵심 가치는 코드 재사용 자체보다 behavioral consistency다. 어디서 Codex를 부르든 비슷한 agent semantics를 보장하려는 설계다.
- 이 글은 harness를 공통 runtime service로 바라보게 만든다.

## Harness Engineering 관점
- harness engineering을 애플리케이션 아키텍처 문제로 확장한 글이다.
- 좋은 harness는 한 제품의 wrapper가 아니라, 여러 UI와 상호작용 방식을 통합하는 shared runtime이 될 수 있음을 보여준다.

## 한계와 주의점
- Codex 내부 아키텍처 사례이므로 일반 팀이 그대로 재현하기 어렵다.
- context curation보다 protocol/integration 설계에 초점이 있다.
