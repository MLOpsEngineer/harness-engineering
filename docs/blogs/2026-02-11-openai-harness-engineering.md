# Harness engineering: leveraging Codex in an agent-first world

- 구분: 블로그/아티클
- 발행일: 2026-02-11
- 저자: Ryan Lopopolo
- 출처: OpenAI
- 원문: https://openai.com/index/harness-engineering/
- 관련성: 직접

## 한줄 요약
OpenAI가 `0 lines of hand-written code` 제약으로 내부 제품을 만들며 얻은 교훈을 통해, 인간의 역할이 코드 작성에서 환경 설계로 이동했다고 선언한 핵심 글이다. "harness engineering"이라는 용어를 업계에 정착시킨 문서.

## 왜 중요한가
현재 harness engineering 담론의 기준점이 되는 문서다. 이 글 이후 harness engineering은 단순 agent wrapper가 아니라 소프트웨어 팀의 operating model을 뜻하는 용어가 되었다.

## 원문 기준 핵심 흐름

### "0 Lines of Hand-Written Code" 실험
- OpenAI 팀이 Codex를 사용해 `수기 코드 0줄` 제약 아래 실제 제품과 운영 artifact를 만들어 본 사례에서 출발한다.
- 이 제약은 극단적이지만 의도적이다. agent가 실제로 일할 수 있으려면 무엇이 필요한지를 드러내기 위한 실험이다.
- 결과: 코드를 직접 쓰지 않아도 제품이 만들어졌지만, 그 대신 **환경 설계에 들어가는 노력이 크게 증가**했다.

### 인간 역할의 이동
- 핵심 메시지: 사람은 코드를 직접 쓰기보다 **intent specification, feedback loop design, environment shaping**을 담당하게 된다.
- Intent specification: "무엇을 만들지"를 agent가 이해할 수 있는 형태로 명세하는 작업. 자연어 요구사항을 구조화된 spec으로 변환한다.
- Feedback loop design: agent의 출력을 검증하고 교정하는 루프를 설계한다. 테스트, lint, CI, human review가 모두 feedback loop의 구성 요소다.
- Environment shaping: repo 구조, 문서, 규칙 파일, 예시 코드를 agent-friendly하게 정비한다.

### Repository를 System of Record로
- architecture, constraints, taste를 **agent-readable form**으로 외부화해야 한다고 강조한다.
- repository knowledge가 system of record가 된다. agent는 이 knowledge를 읽고 작업하므로, repo에 명시되지 않은 것은 agent에게 존재하지 않는 것이다.
- 이는 암묵지(tacit knowledge)를 명시지(explicit knowledge)로 전환하는 과정이기도 하다. 팀의 컨벤션, 아키텍처 결정, 코딩 스타일이 모두 문서화되어야 한다.

### Agent Legibility
- 가장 유명한 개념: `application legibility`를 넘어 `agent legibility`를 추구해야 한다.
- 코드베이스는 인간뿐 아니라 **agent에게도 읽히고 수정되기 쉬워야** 한다.
- agent legibility가 높은 codebase의 특징: 명확한 디렉토리 구조, 일관된 네이밍, 충분한 테스트 커버리지, 잘 정리된 README와 CONTRIBUTING 문서, 명시적 의존성 관리.
- 이는 인간 가독성과 대부분 겹치지만, agent 특유의 요구사항도 있다. 예: grep으로 찾기 쉬운 이름, 자기 설명적인 파일 경로, 독립적으로 실행 가능한 테스트.

### Throughput 증가의 파급 효과
- agent throughput이 늘어나면 **merge philosophy, garbage collection, entropy control, review 방식**까지 같이 바뀌어야 한다.
- 더 많은 코드가 더 빨리 생성되면, merge conflict 빈도가 올라가고, 코드베이스 entropy가 증가하며, review 부하가 커진다.
- 이에 대한 대응: 더 작은 PR, 더 자주 merge, 자동화된 quality gate, agent-generated code에 대한 차별화된 review 기준.
- garbage collection: agent가 생성한 임시 파일, 실험적 코드, 사용하지 않는 브랜치를 체계적으로 정리하는 프로세스가 필요하다.

### Organizational Harness
- harness engineering을 repo 수준을 넘어 **조직 운영 전체를 재편하는 discipline**으로 확장한다.
- CI/CD, documentation, observability, code review, merge policy, team structure가 모두 harness의 구성 요소다.
- 이 글 이후 harness engineering은 "agent runtime을 감싸는 코드"가 아니라 "agent-first 시대의 소프트웨어 개발 방법론"을 뜻하게 된다.

## Harness Engineering 관점
- "harness engineering"이라는 용어를 업계에 정착시킨 원점 문서다.
- agent legibility, repo as system of record, organizational harness 같은 개념은 이후 Fowler, Inngest, LangChain의 글에서 반복적으로 인용된다.
- Hashimoto의 "Engineer the Harness" 단계와 정확히 같은 결론에 도달하지만, OpenAI는 조직 수준의 변화까지 명시적으로 다룬다는 점이 다르다.
- 이 글의 "throughput 증가 → merge/review 재설계 필요"라는 관찰은 이후 Fowler의 "agentic flywheel" 개념의 기반이 된다.

## 한계와 주의점
- 매우 강력한 내부 사례이지만 재현 가능한 외부 benchmark는 아니다. OpenAI 내부 환경과 Codex의 특수한 조건이 전제된다.
- "0 lines of hand-written code"는 교훈을 극대화하기 위한 실험적 제약이므로, 모든 팀이 이 방식을 따라야 한다는 주장은 아니다.
- 정량 데이터(성능 수치, 비용 비교)는 제한적이다. 주로 정성적 교훈과 원칙을 공유하는 글이다.
