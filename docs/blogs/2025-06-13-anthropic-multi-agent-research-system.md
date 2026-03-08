# How we built our multi-agent research system

- 구분: 블로그/아티클
- 발행일: 2025-06-13
- 저자: Anthropic Engineering
- 출처: Anthropic
- 원문: https://www.anthropic.com/engineering/multi-agent-research-system
- 관련성: 기반

## 한줄 요약
Anthropic의 Research 기능을 사례로, 멀티에이전트 시스템이 왜 필요한지, 어떻게 오케스트레이션하는지, 어떤 프롬프트/평가/운영 기법으로 프로덕션까지 끌고 갔는지를 원문 섹션별로 설명한 실전 엔지니어링 글이다.

## 왜 중요한가
harness engineering이라는 용어가 널리 굳기 전, 멀티에이전트 orchestration, evaluation, durability, observability를 실제 제품에 얹을 때 무엇이 필요한지 가장 구체적으로 보여준 초기 사례다.

## 원문 구조
- Benefits of a multi-agent system
- Architecture overview for Research
- Prompt engineering and evaluations for research agents
- Effective evaluation of agents
- Production reliability and engineering challenges
- Appendix

## 1. 왜 멀티에이전트가 필요한가
- 원문은 research 작업을 `고정 경로를 미리 정의하기 어려운, path-dependent한 탐색 문제`로 둔다. 즉 정적인 파이프라인이나 one-shot 답변으로는 대응하기 어렵다고 본다.
- 핵심 비유는 `search is compression`이다. 방대한 정보에서 중요한 토큰만 추려야 하는데, 이때 subagent들이 각자 독립된 context window 안에서 다른 방향을 탐색한 뒤 압축된 결과만 lead agent에 넘기면 더 효과적이라고 설명한다.
- Anthropic은 내부 eval에서 `Claude Opus 4 lead agent + Claude Sonnet 4 subagents` 구성이 단일 Opus 4 agent보다 90.2% 더 나았다고 밝힌다.
- 예시도 구체적이다. S&P 500 Information Technology 기업들의 board member를 모두 찾는 질의에서 멀티에이전트는 작업 분해를 통해 성공했고, 단일 agent는 느린 순차 검색으로 실패했다고 설명한다.
- 성능의 핵심 원인도 분석한다. BrowseComp 변동성의 95%를 설명하는 요인으로 token usage, tool call 수, model choice를 제시하며, 그중 token usage만으로 80%를 설명한다고 말한다.
- 반대로 비용도 분명히 적는다. 일반 chat보다 agent는 약 4배, multi-agent system은 약 15배 토큰을 더 쓴다고 하며, 그래서 가치가 높은 작업에서만 경제성이 나온다고 본다.
- 또한 모든 작업이 멀티에이전트에 맞는 것은 아니라고 선을 긋는다. 모든 agent가 동일 컨텍스트를 강하게 공유해야 하거나, agent 간 dependency가 큰 작업은 아직 적합하지 않다고 본다. 코딩 작업은 연구보다 병렬화 여지가 적고 delegation/coordination이 아직 약하다고도 적는다.

## 2. Research 아키텍처를 원문 기준으로 따라가면
- 아키텍처 패턴은 `orchestrator-worker`다. lead agent가 계획을 세우고, specialized subagent들을 병렬로 띄워 다른 측면을 조사하게 한다.
- 정적인 RAG와의 대비도 명확하다. RAG가 query와 유사한 chunk를 가져와 답변하는 정적 retrieval이라면, Research는 multi-step search로 새 정보를 계속 발견하고 경로를 수정하며 답을 형성한다.
- 흐름은 다음과 같다.
- 사용자가 질의를 넣으면 `LeadResearcher`가 진입한다.
- LeadResearcher는 먼저 접근 계획을 세우고 이를 Memory에 저장한다. 원문은 context window가 200,000 tokens를 넘으면 잘릴 수 있기 때문에 plan persistence가 중요하다고 직접 설명한다.
- 이어서 task-specific subagent들을 생성한다.
- 각 subagent는 web search를 반복 수행하고, tool result 뒤에 interleaved thinking으로 결과 품질과 공백을 점검한 뒤 다음 행동을 결정한다.
- 결과는 lead agent로 돌아가고, lead는 추가 조사 필요 여부를 판단해 subagent를 더 만들거나 전략을 조정한다.
- 충분한 정보가 모이면 마지막에 `CitationAgent`가 별도로 들어가 문서와 리포트를 보고 citation 위치를 붙인다. 즉 answer generation과 citation attachment를 분리한 구조다.
- 이 구조의 포인트는 subagent가 `intelligent filter` 역할을 한다는 점이다. 원문은 subagent가 모든 원문을 그대로 올리는 것이 아니라, 필요한 정보만 압축해서 상위 agent에 전달한다고 설명한다.

## 3. Anthropic이 원문에서 정리한 프롬프팅 원칙 8가지
- 1) `Think like your agents`
- 프롬프트를 고치려면 먼저 실제 agent가 어떻게 실패하는지 step-by-step으로 봐야 한다고 말한다. Anthropic은 exact prompt와 tools를 넣은 simulation을 Console에서 돌리며 failure mode를 관찰했다고 적는다.
- 2) `Teach the orchestrator how to delegate`
- lead agent가 subagent에게 줄 instruction은 목적, 출력 형식, 어떤 tools/sources를 쓸지, task boundary까지 포함해야 한다고 말한다. 짧은 지시는 쉽게 중복 작업과 누락을 만든다고 한다.
- 원문 예시는 semiconductor shortage 조사다. 한 subagent는 2021 automotive chip crisis를 파고, 다른 둘은 2025 supply chain을 중복 조사해 division of labor가 실패했다.
- 3) `Scale effort to query complexity`
- 질의 복잡도에 따라 subagent 수와 tool call budget을 규칙으로 심어야 한다고 한다. 간단한 fact-finding은 1개 agent와 3-10 tool calls, direct comparison은 2-4 subagents와 각 10-15 calls, 복잡한 research는 10개 이상 subagent도 가능하다고 적는다.
- 4) `Tool design and selection are critical`
- agent-tool interface를 human-computer interface만큼 중요하게 본다. 특히 MCP 도구가 늘어날수록 tool description 품질이 agent 성능을 직접 바꾼다고 한다.
- Anthropic은 모든 툴을 먼저 훑고, intent와 맞는 tool을 선택하며, broad external exploration에는 web search를 쓰고, generic tool보다 specialized tool을 선호하라는 heuristic을 넣었다.
- 5) `Let agents improve themselves`
- Claude 4가 prompt engineering에도 유용했다고 직접 쓴다. 실패 사례와 prompt를 주면 agent가 실패 원인을 진단하고 개선안을 제시했다는 것이다.
- 더 나아가 flawed MCP tool을 실제로 여러 번 사용해 본 뒤 tool description을 다시 쓰는 `tool-testing agent`를 만들었고, 이 결과 future agents의 task completion time이 40% 줄었다고 보고한다.
- 6) `Start wide, then narrow down`
- 초기 검색을 짧고 넓게 시작한 뒤 점진적으로 좁혀 가게 했다. agent는 기본적으로 너무 길고 구체적인 query를 바로 던지는 경향이 있어 이를 프롬프트로 교정했다고 적는다.
- 7) `Guide the thinking process`
- lead agent는 extended thinking으로 접근 계획, tool 선택, query complexity, subagent count, role assignment를 정리한다.
- subagent는 tool result 이후 interleaved thinking으로 품질 점검과 gap analysis를 수행한다.
- 8) `Parallel tool calling transforms speed and performance`
- 병렬화는 두 층에서 이뤄진다. lead agent가 3-5 subagent를 병렬로 띄우고, 각 subagent도 3개 이상 도구를 병렬 호출한다.
- 원문은 이 변경으로 복잡한 query의 research time이 최대 90% 줄었다고 주장한다.
- 이 8가지를 종합하며, Anthropic은 rigid rule보다 `good heuristics`를 심는 것이 핵심이라고 정리한다.

## 4. 평가를 어떻게 했는가
- 원문은 multi-agent 평가가 어려운 이유를 먼저 분명히 한다. 같은 입력이라도 여러 valid path가 가능하기 때문에, 고정된 정답 경로를 따라갔는지로 평가하기 어렵다는 것이다.
- 그래서 `outcome은 맞는가`와 `과정이 reasonable한가`를 함께 보는 유연한 평가가 필요하다고 본다.
- 실무 팁도 구체적이다. 초반에는 큰 eval 세트보다 약 20개 정도의 real usage query만 있어도 prompt 변경의 큰 효과를 잡아낼 수 있다고 한다.
- grading 방식은 `LLM-as-judge`다. rubric 항목은 factual accuracy, citation accuracy, completeness, source quality, tool efficiency다.
- 여러 judge를 나눠 쓰는 방식도 시험했지만, 최종적으로는 하나의 LLM call이 0.0-1.0 점수와 pass/fail을 같이 내는 방식이 인간 판단과 가장 잘 맞았다고 적는다.
- 그래도 human eval은 대체되지 않는다. 실제로 사람 평가자가 early agent가 academic PDF나 personal blog보다 SEO content farm을 선호하는 문제를 발견했고, source quality heuristic 추가로 이를 보완했다고 한다.
- appendix에서는 persistent state를 바꾸는 장기 워크플로우에 대해 `turn-by-turn`보다 `end-state evaluation`이 더 잘 맞는다고 별도로 조언한다.

## 5. 프로덕션 운영에서 나온 교훈
- `Agents are stateful and errors compound`
- 장기 실행 agent는 중간 tool call들 사이에서 상태를 유지하기 때문에, 작은 에러도 전체 궤적을 무너뜨릴 수 있다고 본다.
- 그래서 재시작보다 `resume from where the error occurred`가 중요하다고 하며, deterministic retry logic와 regular checkpoint를 두고, 동시에 model이 tool failure를 인지하고 우회하도록 만드는 적응성도 활용한다고 적는다.
- `Debugging needs tracing`
- 같은 prompt여도 비결정적이라서 "왜 obvious한 정보를 못 찾았는지"를 일반 로그로는 알기 어렵다고 말한다.
- 해결책은 full production tracing과 high-level observability다. 원문은 privacy를 위해 대화 내용 자체를 모두 감시하지 않고도 decision pattern과 interaction structure를 모니터링했다고 설명한다.
- `Deployment is hard because agents are long-lived`
- agent가 계속 실행 중일 때 새 버전을 배포하면 기존 실행을 망가뜨릴 수 있으므로 rainbow deployment를 쓴다고 직접 적는다.
- `Synchronous subagent execution is a current bottleneck`
- 현재 lead agent는 subagent 묶음이 끝날 때까지 기다리는 동기 방식이라 steering, subagent coordination, information flow에 병목이 생긴다고 한다.
- 비동기 실행이 더 많은 병렬성을 주겠지만, result coordination, state consistency, error propagation 문제가 따라온다고 적는다.

## 6. Appendix에 나온 추가 팁
- `Long-horizon conversation management`
- 수백 턴 대화를 다루려면 완료된 작업 단계를 요약하고 핵심 정보를 외부 memory에 저장하는 패턴이 필요하다고 한다.
- context 한계가 오면 fresh subagent를 새 context에서 띄우고, research plan 같은 핵심 정보는 memory에서 재가져와 continuity를 유지한다고 설명한다.
- `Subagent output to a filesystem`
- 모든 subagent 산출물을 lead agent 대화 안으로 다시 흘려보내면 "game of telephone"이 생기므로, 어떤 결과는 파일시스템 같은 외부 artifact store에 직접 쓰게 하고 coordinator에는 lightweight reference만 넘기라고 조언한다.
- 이 방식은 token overhead를 줄이고, 코드/리포트/시각화처럼 structured output의 fidelity를 높인다고 한다.

## Harness Engineering 관점
- 이 글은 harness를 단순 wrapper로 보지 않는다. 역할 분해, 메모리 지속, citation 후처리, tracing, deployment, eval rubric, context overflow 대응까지 모두 한 시스템으로 본다.
- 특히 `lead agent + subagents + citation agent + memory + tracing + evals`의 조합이 이미 하나의 harness라는 점이 중요하다.
- coding agent 맥락으로 번역하면 planner, implementer, reviewer, evaluator를 병렬 또는 계층적으로 배치하고, artifact handoff와 평가 기준을 설계하는 일이 곧 harness engineering이라는 시사점을 준다.

## 한계와 주의점
- 이 글은 research agent 사례에 최적화되어 있다. 원문도 코딩 작업은 research보다 병렬화 여지가 적고 멀티에이전트 적합성이 낮을 수 있다고 인정한다.
- 내부 eval 수치와 production 사례는 유용하지만, 공개 benchmark 재현성은 제한적이다.
- 또한 이 글은 harness engineering이라는 단어를 직접 쓰기보다, 멀티에이전트 시스템을 실제로 굴리며 필요한 운영 메커니즘을 하나씩 보여주는 문서로 읽는 편이 정확하다.
