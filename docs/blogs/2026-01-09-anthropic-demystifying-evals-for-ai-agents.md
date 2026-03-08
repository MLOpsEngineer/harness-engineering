# Demystifying evals for AI agents

- 구분: 블로그/아티클
- 발행일: 2026-01-09
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- 관련성: 기반

## 한줄 요약
agent evaluation을 single-turn QA에서 multi-turn, stateful, tool-using system 평가로 확장해 설명한 방법론 글이다.

## 왜 중요한가
harness engineering에서 observability와 eval은 선택이 아니라 필수라는 점을 구조적으로 설명한다.

## 원문 기준 핵심 흐름
- 글은 agent eval이 model eval과 다른 이유를 먼저 설명한다. agent는 tool을 호출하고 environment state를 바꾸며 trajectory를 남긴다.
- 따라서 최종 문자열만 비교하는 방식으로는 실제 능력 변화를 잘 잡지 못한다.
- eval은 `trajectory`, `final response`, `environment state`, `grader logic`을 함께 설계해야 한다.
- Anthropic은 eval을 one-off experiment가 아니라 production regression을 조기에 잡는 운영 장치로 본다.
- 즉 좋은 harness는 실행 loop와 함께 측정 loop를 동시에 가진다.

## Harness Engineering 관점
- harness engineering은 agent loop를 짜는 일만이 아니라, loop를 어떻게 관찰하고 자동 채점할지 설계하는 일까지 포함한다.
- 이 글은 ‘좋은 harness는 좋은 eval과 함께 자란다’는 점을 명확히 한다.

## 한계와 주의점
- 구체 구현보다는 평가 원칙과 프레임이 중심이다.
- 오픈 벤치마크보다는 실무 general guidance 성격이 강하다.
