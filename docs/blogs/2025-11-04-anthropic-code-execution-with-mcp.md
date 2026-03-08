# Code execution with MCP: building more efficient AI agents

- 구분: 블로그/아티클
- 발행일: 2025-11-04
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/code-execution-with-mcp
- 관련성: 기반

## 한줄 요약
MCP 서버 수가 많아질 때 tool definition과 intermediate result가 context를 잠식하는 문제를, code execution layer를 통해 우회하는 방법을 다룬 글이다.

## 왜 중요한가
large tool universe를 다뤄야 하는 harness에서 token economy와 tool virtualization이 얼마나 중요한지 보여준다.

## 원문 기준 핵심 흐름
- 글은 MCP server가 많아질수록 tool definition을 전부 upfront로 주는 방식이 token budget과 latency를 빠르게 잠식한다고 본다.
- 또 tool 실행의 intermediate result를 매번 자연어로 모델에 되돌려주는 패턴 역시 비효율적이라고 지적한다.
- 해결 방향은 `모델이 봐야 하는 것`과 `런타임이 대신 처리할 것`을 분리하는 것이다. code execution layer에서 계산과 변환을 처리하고, 모델에는 필요한 결과만 전달한다.
- MCP는 여기서 표준 연결 계층 역할을 한다. 중요한 것은 MCP 자체보다, tool universe를 context에 어떻게 가상화해 노출할 것인가다.
- 따라서 이 글의 실제 메시지는 `tool을 더 붙이자`가 아니라 `tool exposure를 virtualize하자`에 가깝다.

## Harness Engineering 관점
- 이 글은 harness engineering이 곧 ‘컨텍스트 예산 관리’이기도 하다는 점을 보여준다.
- 도구를 더 많이 붙이는 것이 아니라, 모델이 봐야 할 것과 런타임이 대신 처리할 것을 분리하는 설계가 중요하다.

## 한계와 주의점
- MCP와 code execution 환경을 전제로 해 범용성에 한계가 있다.
- 장기 메모리나 사람-에이전트 협업 루프는 중심 주제가 아니다.
