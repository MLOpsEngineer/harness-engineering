# 03. Harnesses in Agent Development

이 문서는 agent를 실제로 개발할 때 harness가 어디에서 쓰이는지를 `repo 준비 -> task framing -> context assembly -> execution -> validation -> handoff -> review -> 지속 개선` 순서로 정리한다. 목표는 요약이 아니라, coding/terminal agent를 만드는 팀이 `지금 어느 단계에 있고 다음에 무엇을 붙여야 하는지` 판단할 수 있게 만드는 것이다.

## 핵심 주장

- agent 개발에서 harness는 프롬프트 뒤의 보조 장치가 아니라 개발 수명주기 전체를 조정하는 환경이다.
- 좋은 harness는 agent가 코드를 더 많이 쓰게 하는 것이 아니라, 의도 오해, 반복 실패, 검증 없는 완료 선언, handoff 비용을 줄인다.
- 따라서 agent 개발의 핵심 일은 loop를 한 번 구현하는 것이 아니라, 각 단계의 artifacts와 feedback channels를 설계하는 것이다.

## 전체 코퍼스 종합

### 개발 수명주기에서의 사용 지점

| 단계 | harness가 담당하는 것 | 대표 자료 |
|------|----------------------|----------|
| 1. Repo 준비 | 문서, 규칙, 테스트, 구조를 agent-readable하게 정비 | OpenAI, Mitchell Hashimoto, DEV, Fowler |
| 2. Task framing | spec, feature list, acceptance criteria, boundaries 정의 | Anthropic long-running, Fowler context eng., OpenAI |
| 3. Context assembly | local context, rules, files, memory, tool schema 조합 | Manus, Anthropic context eng., LangChain LocalContext |
| 4. Execution loop | think-act-observe, tool dispatch, retries, loop detection | OpenAI unrolling, Inngest, OpenDev |
| 5. Validation | tests, static analysis, checklist, benchmark, verifier | LangChain checklist, Meta repair, PerfBench, Anthropic evals |
| 6. Handoff | artifacts, todo, checkpoints, session resume | Anthropic long-running, Manus, Inngest |
| 7. Review/merge | human checkpoints, approval, entropy control | Fowler humans-and-agents, OpenAI, ignorance.ai |
| 8. 지속 개선 | trace analysis, regression eval, cleanup agent | LangChain, Anthropic evals, Fowler harness eng. |

### 1. Repo 준비 단계

- OpenAI는 repository knowledge를 `system of record`로 두고 architecture, constraints, taste를 agent-readable form으로 외부화해야 한다고 본다.
- Mitchell Hashimoto는 이 단계를 `Engineer the Harness`라고 부르며, 테스트와 문서가 없으면 agent가 자기 작업을 검증하고 이해할 수 없다고 말한다.
- DEV와 Fowler는 README, rules 파일, specs, directory conventions, CI 설정이 모두 context이자 harness 자산이라고 본다.

### 자료 비교

- OpenAI는 이 단계를 조직 운영 변화와 연결한다. repo legibility가 곧 merge/review 변화의 출발점이라는 시각이다.
- Mitchell은 더 개인적이고 실무적인 언어를 쓴다. 시간을 코드 작성보다 repo 정비에 쓰는 전환이 복리 효과를 만든다고 본다.
- Fowler는 이 repo 자산을 tools, skills, rules, specs의 네트워크로 설명한다.
- GitTaskBench는 이 주장에 empirical backing을 준다. 실제 실패의 큰 비율이 environment setup과 dependency resolution에서 났다.

### coding/terminal agent 예시 artifact

- `README.md`: setup, test, run 명령
- `AGENTS.md` 또는 rules 파일: 수정 금지 영역, preferred workflow
- `CONTRIBUTING.md`: lint/type/test 기준
- `scripts/verify.sh`: 최소 acceptance runner
- `docs/architecture.md`: 구조와 boundary 설명

### 전형적 failure mode와 대응

| failure mode | 증상 | 대응 harness |
|--------------|------|-------------|
| setup ambiguity | agent가 프로젝트를 못 띄움 | bootstrap script, explicit run/test docs |
| hidden conventions | naming/structure를 반복 위반 | rules/specs 파일, example PR |
| unverifiable edits | 수정은 했지만 확인 불가 | smoke test, lint, type check |

### 최소 도입 vs 고도화

- 최소 도입: README, 실행 가능한 테스트, 명시적 규칙 파일
- 고도화: 구조 문서, examples, agent-readable style guide, repo-specific verifier scripts

### 2. Task framing 단계

- Anthropic long-running harness는 initializer agent가 feature list JSON을 만들고 이를 coding agent에 넘긴다. 이 artifact에는 범위, 관련 파일, acceptance criteria, dependency가 들어간다.
- OpenAI는 intent specification을 인간 역할의 핵심으로 본다. vague한 요청을 바로 loop에 넣지 않고 작업 명세로 바꾸는 것이 harness engineering이다.
- Fowler context engineering에서 specs와 rules는 단순 참고 문서가 아니라 `에이전트 행동의 경계`다.

### 자료 비교

- Anthropic은 structured artifact handoff에 더 강하게 기울어 있다. feature list JSON과 checkpoint 중심이다.
- OpenAI는 조직 단위에서 intent specification을 강조한다. 자연어 요구를 repo 안의 explicit knowledge로 바꾸는 쪽이다.
- Fowler는 specs를 context taxonomy의 일부로 다루면서도, 실무상 agent behavior를 프로그래밍하는 표면으로 본다.

### coding/terminal agent 예시 artifact

- `feature-list.json`
- `task-spec.md`
- `acceptance-criteria.md`
- `related-files.txt`
- `non-goals.md`

### 전형적 failure mode와 대응

| failure mode | 증상 | 대응 harness |
|--------------|------|-------------|
| scope creep | agent가 주변 리팩터링으로 새어감 | non-goals 명시, 파일 범위 제한 |
| premature completion | edge case 빠진 채 완료 선언 | explicit acceptance criteria, checklist |
| lost rationale | 왜 이 방향으로 갔는지 남지 않음 | structured spec + checkpoint notes |

### 최소 도입 vs 고도화

- 최소 도입: 짧은 task spec + acceptance criteria
- 고도화: feature list JSON, dependency graph, file scope, checkpoint contract

### 3. Context assembly 단계

- Manus는 context를 대화 히스토리로만 유지하면 stale information, noise accumulation, observation bloat가 생긴다고 본다.
- Anthropic context engineering은 이를 `creation -> accumulation -> pruning` lifecycle로 정리한다.
- LangChain의 LocalContext는 agent가 현재 작업 파일과 디렉토리를 잊지 않도록 매 턴 relevant context를 주입한다.
- Structured Context Engineering은 file-native retrieval이 frontier model에는 유리하지만 weaker model에는 mixed result라고 보고한다.

### 자료 비교

- Manus와 Anthropic은 모두 `모든 걸 계속 넣지 말라`고 말하지만 구현 감각이 다르다. Manus는 file-based state와 KV-cache 친화성, Anthropic은 lifecycle과 pruning heuristics를 강조한다.
- LangChain은 이를 middleware 형태로 operationalize한다. 필요한 로컬 컨텍스트를 자동 주입하는 식이다.
- Structured Context Engineering은 practitioner intuition에 중요한 반례를 준다. file-native retrieval이 항상 정답은 아니며 모델 tier에 따라 다르게 설계해야 한다.

### coding/terminal agent 예시 artifact

- 현재 작업 파일 목록
- 최근 에러 요약
- open diff summary
- rules/specs snippet
- todo status
- 필요 시 파일 경로 reference만 남기고 본문은 on-demand read

### 전형적 failure mode와 대응

| failure mode | 증상 | 대응 harness |
|--------------|------|-------------|
| context pollution | 옛 실패 로그에 계속 끌려감 | compaction, selective re-injection |
| file disorientation | 작업 파일을 반복 탐색 | LocalContext, related-files artifact |
| grep tax / retrieval overhead | 필요한 정보 찾느라 token 낭비 | model-specific retrieval policy |

### 최소 도입 vs 고도화

- 최소 도입: 관련 파일, 규칙, 현재 diff 요약을 매 턴 재주입
- 고도화: file-based state, dynamic compaction, lazy retrieval, model-tier별 retrieval strategy

### 4. Execution 단계

- OpenAI의 Codex loop 문헌은 input collection, prompt assembly, model inference, tool invocation, observation formatting, termination을 공통 runtime semantics로 본다.
- Inngest는 이를 durable execution 위에 올려 step-level retry, concurrency control, event routing으로 감싼다.
- OpenDev는 planning과 execution을 분리하고, lazy MCP discovery, event-driven reminders, dual memory를 더한다.
- Anthropic multi-agent는 task가 path-dependent할 때 orchestrator-worker와 parallel subagent를 사용한다.

### 자료 비교

- OpenAI는 execution harness의 뼈대를 `loop semantics`로 설명한다.
- Inngest는 같은 loop를 `durable substrate` 위에서 다루며 실패 복구와 async orchestration을 전면에 둔다.
- OpenDev는 terminal-native 제약 때문에 safety와 context efficiency를 함께 풀려 한다.
- Anthropic multi-agent는 execution harness를 단일 loop가 아니라 여러 agent 사이의 orchestration으로 확장한다.

### coding/terminal agent 예시 artifact

- loop state
- iteration budget
- tool registry
- active task checkpoint
- step result cache
- termination checklist

### 전형적 failure mode와 대응

| failure mode | 증상 | 대응 harness |
|--------------|------|-------------|
| loop thrashing | 같은 검색/수정 반복 | loop detection, bounded retry |
| abrupt termination | 덜 끝났는데 종료 | pre-completion checklist, explicit termination policy |
| tool explosion | 도구가 많아 선택이 흔들림 | tool grouping, lazy discovery, virtualization |
| async race | 새 입력과 기존 run 충돌 | singleton / cancellation policy, durable step resume |

### 최소 도입 vs 고도화

- 최소 도입: loop detection, completion checklist, basic retry
- 고도화: step-level durability, concurrency control, multi-agent orchestration, shared runtime

### 5. Validation 단계

- LangChain의 PreCompletionChecklist는 완료 전에 테스트, 저장, 디버그 코드 제거를 강제한다.
- Meta program repair는 static analysis, test execution, LLM judge, human review를 계층적으로 쌓는다.
- PerfBench는 agent가 benchmark를 만들고 harness가 buggy/fixed 양쪽에서 실행해 효과를 비교한다.
- Anthropic eval 문헌은 trajectory, final response, environment state, grader logic을 함께 평가해야 한다고 본다.

### 자료 비교

- LangChain은 runtime middleware로 self-verification을 강제한다.
- Meta는 production 시스템에서 verifier stack을 다층 구조로 배치한다.
- PerfBench는 non-functional issue에서 validation harness가 곧 task definition이 될 수 있음을 보여준다.
- Anthropic은 eval을 운영 장치로 설명하며, 소수의 high-quality case부터 시작하는 현실적 접근을 제안한다.

### coding/terminal agent 예시 artifact

- `verify.sh`
- `pytest -q` 또는 domain-specific runner output summary
- static analysis result
- performance benchmark delta
- acceptance checklist result

### 전형적 failure mode와 대응

| failure mode | 증상 | 대응 harness |
|--------------|------|-------------|
| unverifiable completion | 완료라는데 근거 없음 | mandatory verifier step |
| partially correct fix | 일부만 맞고 회귀 유발 | layered verifier stack |
| metric blindness | 성능/비기능 품질이 안 보임 | benchmark-based validation |

### 최소 도입 vs 고도화

- 최소 도입: smoke test + completion checklist
- 고도화: static analysis, benchmark runner, LLM judge, human approval

### 6. Handoff 단계

- Anthropic long-running harness의 핵심 메시지는 `다음 턴을 위한 배려`다.
- Manus의 todo-list와 file-based state management는 같은 원리를 구현 중심으로 보여준다.
- Inngest는 within-run pruning과 across-run compaction을 분리하고, overflow recovery를 런타임 기능으로 둔다.

### 자료 비교

- Anthropic은 structured handoff artifact와 checkpoint를 강조한다.
- Manus는 files와 todo를 durable state 저장소로 둔다.
- Inngest는 event/step persistence로 같은 문제를 푼다.

세 접근은 표면은 다르지만 공통 목적이 같다. `다음 실행이 이전 실행의 의도와 상태를 곧바로 이해할 수 있게 한다`는 것이다.

### coding/terminal agent 예시 artifact

- `todo.md`
- `checkpoint.md`
- `handoff-notes.md`
- `known-risks.md`
- `next-steps.md`

### 전형적 failure mode와 대응

| failure mode | 증상 | 대응 harness |
|--------------|------|-------------|
| lost state | 세션 바뀌면 처음부터 다시 탐색 | explicit handoff artifact |
| rationale loss | why가 사라짐 | decision log / checkpoint notes |
| overlong session | context overflow로 품질 하락 | compaction + resume |

### 최소 도입 vs 고도화

- 최소 도입: todo + next step notes
- 고도화: feature-level checkpoint artifact, step persistence, resume-from-failure

### 7. Review와 merge 단계

- Fowler는 사람을 `in the loop`에 두면 agent throughput이 커질수록 review 병목이 생긴다고 본다.
- OpenAI와 ignorance.ai는 review를 더 앞단의 quality signal, 더 작은 PR, 더 자주 merge, 더 명시적인 approval point로 재설계해야 한다고 본다.
- Mitchell Hashimoto는 항상 background agent가 돌아가는 상황에서 인간 시간이 점점 supervision과 selection으로 이동한다고 본다.

### 자료 비교

- Fowler는 review 철학을 `humans on the loop`로 개념화한다.
- OpenAI는 그것을 merge philosophy와 entropy control 문제로 번역한다.
- ignorance.ai는 background agent, async workflow, human checkpoint 재배치를 팀 playbook으로 정리한다.

### coding/terminal agent 예시 artifact

- PR checklist
- approval-required label
- risk score
- diff summary
- trace link
- acceptance evidence bundle

### 전형적 failure mode와 대응

| failure mode | 증상 | 대응 harness |
|--------------|------|-------------|
| review overload | agent output은 빠른데 사람 검토가 막힘 | smaller PR, auto checks, checkpointed approval |
| entropy accumulation | 임시 코드/브랜치/문서 불일치 누적 | cleanup loop, background agent |
| opaque edits | 리뷰어가 의도와 검증 근거를 모름 | trace + acceptance bundle 첨부 |

### 최소 도입 vs 고도화

- 최소 도입: small PR policy, checklist, required tests
- 고도화: background cleanup agents, risk-tiered approval, async review routing

### 8. 지속 개선 단계

- LangChain은 trace analyzer를 이용해 failure pattern을 자동 분류하고, 이를 middleware나 prompt 수정 후보로 변환한다.
- Anthropic은 새로운 failure mode가 보일 때마다 eval case를 추가하라고 한다.
- Fowler는 agentic flywheel을 통해 나중에는 agent가 harness 개선 제안까지 하게 되는 meta-loop를 상상한다.

### 자료 비교

- LangChain은 실전 trace-driven optimization을 가장 구체적으로 보여준다.
- Anthropic은 eval suite를 점진적으로 키우는 운영 습관을 제시한다.
- Fowler는 이를 조직적 meta-loop로 일반화한다.

### coding/terminal agent 예시 artifact

- failure taxonomy
- trace cluster summary
- regression eval suite
- rules 업데이트 로그
- cleanup backlog

### 전형적 failure mode와 대응

| failure mode | 증상 | 대응 harness |
|--------------|------|-------------|
| same bug, new wording | 표현만 달라졌는데 같은 실패 반복 | failure taxonomy + eval expansion |
| local fix, global regression | 한 레버는 좋아졌지만 다른 task에서 악화 | cross-task eval, variance tracking |
| static harness | 환경은 바뀌는데 rules/verification은 그대로 | trace-driven update cadence |

### 최소 도입 vs 고도화

- 최소 도입: monthly failure review + regression case 추가
- 고도화: automated trace clustering, agent-proposed harness changes, background quality loops

## agent 개발에서의 사용 방식

### 최소 실행 가능한 harness

처음부터 shared runtime service나 durable substrate가 없어도 된다. 하지만 다음은 거의 항상 필요하다.

1. agent-readable README 또는 rules/spec 파일
2. task별 acceptance criteria
3. 실행 가능한 테스트나 최소 verifier
4. tool 이름과 설명의 정리
5. 현재 작업 파일과 관련 컨텍스트를 재주입하는 장치
6. 완료 전 체크리스트와 trace
7. 간단한 handoff artifact 또는 next-step note

### 단계별 도입 로드맵

#### 초기

- repo 문서 정리
- rules/specs 외부화
- smoke test와 lint 연결
- 수동 trace 확인
- next-step note 남기기

#### 중간

- LocalContext, loop detection, completion checklist 추가
- file-based state와 todo artifact 사용
- regression eval suite 구축
- small PR / approval checklist 도입

#### 고도화

- initializer/planner/executor/reviewer 역할 분리
- durable execution과 step-level retry
- benchmark and domain-specific verifier stack
- background agent, cleanup loop, cross-surface shared runtime 도입

### harness가 없을 때 나타나는 전형적 증상

- agent가 이미 실패한 경로를 반복한다.
- task 범위를 잊고 주변 리팩터링으로 새어나간다.
- 완료 선언이 너무 이르다.
- 긴 작업 뒤에 왜 그런 결정을 했는지 남지 않는다.
- review는 많은데 재사용 가능한 개선이 쌓이지 않는다.
- repo setup이 task마다 다시 탐색 대상이 된다.

## 설계 원칙

- repo 준비를 optional nice-to-have로 보지 않는다.
- task framing artifact를 대화 히스토리 밖의 구조화된 파일로 남긴다.
- context는 대화에 누적하기보다 files, summaries, references로 재주입한다.
- validation을 프롬프트 부탁이 아니라 runtime step으로 강제한다.
- 장기 작업에서는 handoff artifact를 먼저 설계하고 loop를 짠다.
- human review는 최종 산출물만 보지 말고 acceptance criteria와 trace를 함께 본다.
- harness 성숙도를 `얼마나 자율적인가`보다 `얼마나 재시작 가능하고 검증 가능한가`로 판단한다.

## 반론/한계

- 모든 팀이 initializer agent, feature list JSON, durable runtime까지 필요로 하지는 않는다.
- file-based state나 todo artifact는 간단한 one-shot 작업에는 과할 수 있다.
- repo를 정리한다고 해서 agent가 자동으로 잘 작동하는 것은 아니다. tool 품질과 eval 부재는 별도 문제다.
- 인간 검토를 줄이는 방향은 domain risk가 높은 환경에서는 제약이 크다. security, compliance, production migration task에서는 human gate가 더 강해야 한다.

## 관련 자료 묶음

- 직접 문헌: Anthropic `Effective harnesses for long-running agents`, OpenAI `Harness engineering`, OpenDev `Building AI Coding Agents for the Terminal`
- 기반 문헌: Manus `Context Engineering for AI Agents`, Anthropic `Effective context engineering for AI agents`, OpenAI `Unrolling the Codex agent loop`, Martin Fowler `Context Engineering for Coding Agents`
- 실증/보조 근거: LangChain `Improving Deep Agents with harness engineering`, Meta `Agentic Program Repair from Test Failures at Scale`, PerfBench, GitTaskBench, Fowler `Humans and Agents in Software Engineering Loops`
