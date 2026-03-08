# Unrolling the Codex agent loop

- 구분: 블로그/아티클
- 발행일: 2026-01-23
- 저자: OpenAI Engineering
- 출처: OpenAI
- 원문: https://openai.com/index/unrolling-the-codex-agent-loop/
- 관련성: 기반

## 한줄 요약
Codex의 agent loop를 해부하면서, 사용자 입력, prompt assembly, model inference, tool invocation, observation이 어떻게 연결되는지가 agent 성능의 핵심임을 설명한 글이다.

## 왜 중요한가
OpenAI가 harness를 단순 래퍼가 아니라 제품 공통 런타임으로 본다는 점을 드러내는 출발점이다.

## 원문 기준 핵심 흐름
- 글은 Codex의 핵심이 단일 model call이 아니라, 입력 수집부터 tool execution과 다음 행동 결정까지 이어지는 loop라는 점을 강조한다.
- 이 loop는 surface마다 달라 보이더라도 아래쪽에는 공통 runtime semantics가 존재한다는 메시지를 준다.
- 모델 quality만큼 중요한 것은 prompt assembly, tool exposure, observation formatting, termination condition이다.
- 즉 agent quality는 model 자체가 아니라 loop 전체의 설계 결과라는 것이 이 글의 중심 주장이다.

## Harness Engineering 관점
- 이 글은 harness engineering의 가장 낮은 수준, 즉 runtime semantics를 다룬다.
- 후속 OpenAI 글들이 조직 운영과 repo legibility로 확장되기 전에, agent loop 자체가 왜 중요한지 기반을 제공한다.

## 한계와 주의점
- 조직 프로세스나 repo 관리 같은 상위 문제는 거의 다루지 않는다.
- 구현 철학 소개 비중이 높고, 실험 수치는 제한적이다.
