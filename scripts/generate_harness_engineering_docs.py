from __future__ import annotations

from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BLOG_DIR = DOCS / "blogs"
PAPER_DIR = DOCS / "papers"


BLOGS = [
    {
        "slug": "2025-06-13-anthropic-multi-agent-research-system",
        "title": "How we built our multi-agent research system",
        "date": "2025-06-13",
        "author": "Anthropic Engineering",
        "source": "Anthropic",
        "url": "https://www.anthropic.com/engineering/multi-agent-research-system",
        "relation": "기반",
        "one_liner": "Anthropic의 Research 기능을 사례로, 병렬 서브에이전트와 컨텍스트 압축이 왜 long-horizon 작업에서 필요한지 설명한 초기 핵심 글이다.",
        "importance": "harness engineering이라는 용어가 정착되기 전, 멀티에이전트 orchestration과 agent coordination을 실제 제품에 얹으면서 무엇이 어려운지 보여준 출발점이다.",
        "key_points": [
            "리드 에이전트가 전체 연구 과정을 계획하고, 서브에이전트가 병렬로 검색과 정리를 수행한 뒤 다시 압축된 결과를 상위 컨텍스트로 올리는 구조를 제시한다.",
            "오픈엔디드 연구 문제는 고정 파이프라인보다 경로의존적 탐색이 필요하므로, 단일 에이전트보다 컨텍스트 분리와 병렬화가 성능에 유리하다고 본다.",
            "멀티에이전트 시스템이 늘어날수록 prompt 설계보다 coordination, evaluation, tool design, failure handling이 더 중요한 엔지니어링 문제로 떠오른다.",
        ],
        "harness_view": [
            "이 글의 핵심은 모델 자체보다도 상위 orchestration layer가 각 에이전트의 역할, 컨텍스트 경계, 결과 합성 규칙을 정해야 한다는 점이다.",
            "즉 harness engineering의 초기 형태를 ‘멀티에이전트 작업 분해와 압축 메커니즘 설계’로 보여준다.",
        ],
        "limits": [
            "사례 중심 글이라 정량 비교는 제한적이다.",
            "연구 작업에 초점이 있어 코딩 에이전트나 일반 업무용 agent harness로 옮길 때 추가 해석이 필요하다.",
        ],
    },
    {
        "slug": "2025-07-18-manus-context-engineering-for-ai-agents",
        "title": "Context Engineering for AI Agents: Lessons from Building Manus",
        "date": "2025-07-18",
        "author": "Yichao 'Peak' Ji",
        "source": "Manus",
        "url": "https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus",
        "relation": "기반",
        "one_liner": "Manus 팀이 실제 에이전트 제품을 만들며 정리한 context engineering 실전 메모로, long-running agent에서 외부 상태를 어떻게 다뤄야 하는지 설명한다.",
        "importance": "2025년 하반기 harness engineering 담론의 바탕이 된 글 중 하나로, 프롬프트보다 더 넓은 의미의 상태 설계를 강조한다.",
        "key_points": [
            "컨텍스트는 단지 system prompt가 아니라 계획, 파일, 메모리, 도구 결과, 실행 기록, 중간 산출물까지 포함하는 외부 상태라고 본다.",
            "긴 작업에서는 모든 것을 대화 히스토리에 밀어 넣기보다, 파일과 구조화된 아티팩트로 외부화하고 필요한 것만 다시 주입하는 방식이 더 안정적이라고 주장한다.",
            "에이전트가 다음 세션을 위해 읽기 쉬운 흔적을 남기도록 설계해야 하며, 이 흔적 자체가 생산성을 좌우하는 기억 장치가 된다.",
        ],
        "harness_view": [
            "harness engineering 관점에서 보면 Manus는 ‘컨텍스트를 운영체제처럼 관리하는 방법’을 설명한다.",
            "모델 안쪽보다 바깥쪽에서 어떤 파일 구조, 요약 규칙, 리트리벌 경로를 만들 것인지가 핵심이라는 점을 분명히 한다.",
        ],
        "limits": [
            "정량 성능 실험보다 제품 경험을 바탕으로 한 설계 원칙 중심이다.",
            "특정 구현 세부가 충분히 공개되지는 않아 재현성은 제한적이다.",
        ],
    },
    {
        "slug": "2025-09-11-anthropic-writing-effective-tools-for-ai-agents",
        "title": "Writing effective tools for AI agents—using AI agents",
        "date": "2025-09-11",
        "author": "Anthropic Engineering",
        "source": "Anthropic",
        "url": "https://www.anthropic.com/engineering/writing-tools-for-agents",
        "relation": "기반",
        "one_liner": "도구 인터페이스를 어떻게 설계해야 에이전트가 덜 헷갈리고 더 싸게, 더 안정적으로 일하는지를 정리한 tool-design 중심 글이다.",
        "importance": "harness engineering에서 tool surface는 가장 중요한 레버 중 하나인데, 이 글은 그 레버를 어떻게 다듬는지 가장 구체적으로 다룬다.",
        "key_points": [
            "좋은 tool은 기능이 많은 tool이 아니라, 경계가 분명하고 이름이 명확하며 필요한 맥락을 적절히 반환하는 tool이라고 정리한다.",
            "tool description과 parameter schema도 prompt의 일부이므로, token cost와 agent 이해 가능성을 함께 최적화해야 한다고 본다.",
            "도구 품질은 감으로 개선하지 말고 eval을 붙인 뒤, 에이전트를 이용해 도구 자체를 반복 개선하는 루프를 만들 것을 권한다.",
        ],
        "harness_view": [
            "tool selection과 tool contract는 모델 능력을 실제 업무 성능으로 바꾸는 핵심 harness 요소라는 점을 잘 보여준다.",
            "즉 harness engineering은 ‘어떤 tool을 붙일까’보다 ‘tool을 어떤 계약으로 expose할까’에 더 가깝다.",
        ],
        "limits": [
            "tool-centric 글이라 조직 운영, 병렬화, merge 철학 같은 상위 주제는 다루지 않는다.",
            "Anthropic 스택과 MCP 친화적 관점이 강하다.",
        ],
    },
    {
        "slug": "2025-09-29-anthropic-effective-context-engineering-for-ai-agents",
        "title": "Effective context engineering for AI agents",
        "date": "2025-09-29",
        "author": "Anthropic Engineering",
        "source": "Anthropic",
        "url": "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents",
        "relation": "기반",
        "one_liner": "프롬프트 엔지니어링에서 context engineering으로 무게중심이 이동하고 있음을 선언하고, 에이전트 컨텍스트 전체를 어떻게 다뤄야 하는지 정리한 글이다.",
        "importance": "harness engineering의 내부 면을 담당하는 가장 중요한 이론적 기반 문서다.",
        "key_points": [
            "컨텍스트는 시스템 지시문뿐 아니라 tool schema, MCP, 외부 데이터, message history, 메모리까지 포함하는 전체 토큰 상태라고 정의한다.",
            "에이전트가 여러 턴을 돌수록 관련 없는 정보가 축적되므로, 무엇을 유지하고 무엇을 버릴지 설계하는 일이 prompt 작성보다 중요해진다고 본다.",
            "좋은 결과를 위해서는 ‘thinking in context’, 즉 현재 상태가 어떤 행동을 유도할지 역으로 설계하는 관점이 필요하다고 말한다.",
        ],
        "harness_view": [
            "이 글은 harness engineering 전체의 절반을 설명한다. 모델 안으로 무엇을 넣을지 정하는 내부 레이어가 context engineering이다.",
            "후속 harness engineering 담론은 여기서 한 단계 더 나아가, 모델 바깥의 실행 환경과 검증 루프까지 포함한다.",
        ],
        "limits": [
            "실행 환경이나 CI/merge 같은 바깥쪽 문제는 거의 다루지 않는다.",
            "정성적 원칙이 많고 재현 가능한 실험 수치는 적다.",
        ],
    },
    {
        "slug": "2025-11-04-anthropic-code-execution-with-mcp",
        "title": "Code execution with MCP: building more efficient AI agents",
        "date": "2025-11-04",
        "author": "Anthropic Engineering",
        "source": "Anthropic",
        "url": "https://www.anthropic.com/engineering/code-execution-with-mcp",
        "relation": "기반",
        "one_liner": "MCP 서버 수가 많아질 때 tool definition과 intermediate result가 컨텍스트를 잠식하는 문제를, code execution 레이어로 우회하는 방법을 다룬 글이다.",
        "importance": "large tool universe를 다뤄야 하는 harness에서 token economy와 tool virtualization이 얼마나 중요한지 보여준다.",
        "key_points": [
            "모든 tool definition을 upfront로 모델에 노출하면 컨텍스트 창을 소모하고 latency와 비용을 키운다고 지적한다.",
            "중간 결과를 매번 natural-language 토큰으로 다시 넣는 방식 역시 비효율적이므로, 코드 실행 환경에서 처리하고 필요한 결과만 전달하는 방식을 제안한다.",
            "MCP를 표준 연결 계층으로 두고, harness는 어떤 정보를 모델에게 직접 보여줄지와 어떤 처리를 외부 런타임으로 숨길지를 설계해야 한다고 본다.",
        ],
        "harness_view": [
            "이 글은 harness engineering이 곧 ‘컨텍스트 예산 관리’이기도 하다는 점을 보여준다.",
            "도구를 더 많이 붙이는 것이 아니라, 모델이 봐야 할 것과 런타임이 대신 처리할 것을 분리하는 설계가 중요하다.",
        ],
        "limits": [
            "MCP와 code execution 환경을 전제로 해 범용성에 한계가 있다.",
            "장기 메모리나 사람-에이전트 협업 루프는 중심 주제가 아니다.",
        ],
    },
    {
        "slug": "2025-11-26-anthropic-effective-harnesses-for-long-running-agents",
        "title": "Effective harnesses for long-running agents",
        "date": "2025-11-26",
        "author": "Anthropic Engineering",
        "source": "Anthropic",
        "url": "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents",
        "relation": "직접",
        "one_liner": "여러 컨텍스트 윈도우를 넘나들며 오래 일하는 코딩 에이전트에 필요한 harness를 직접적으로 다룬 핵심 기술 글이다.",
        "importance": "‘long-running agent harness’라는 문제 설정을 명확히 하고, initializer agent와 coding agent 분리라는 실제 패턴을 제시한다.",
        "key_points": [
            "compaction만으로는 충분하지 않고, 초기 환경을 세팅하는 initializer와 점진적 진전을 만드는 coding agent를 분리해야 한다고 주장한다.",
            "각 세션은 다음 세션이 쉽게 이어받을 수 있는 깨끗한 상태를 남겨야 하며, 그 상태는 main branch에 올릴 수 있을 정도의 정돈된 코드여야 한다고 본다.",
            "에이전트가 한 번에 전체 앱을 one-shot 하려는 경향을 억제하고, feature-by-feature로 진행하게 만드는 것이 안정성에 중요하다고 설명한다.",
        ],
        "harness_view": [
            "harness engineering을 가장 직접적으로 설명하는 Anthropic 글이다. 모델 루프 바깥에서 역할 분해, 환경 세팅, handoff artifact 설계를 수행한다.",
            "장기 작업에서 ‘다음 턴을 위한 배려’를 시스템에 강제하는 것이 핵심이라는 점이 중요하다.",
        ],
        "limits": [
            "Claude Agent SDK와 코딩 태스크 중심의 사례라 다른 도메인에 그대로 이식하기는 어렵다.",
            "정량 비교보다는 설계 원칙과 실패 패턴 공유에 가깝다.",
        ],
    },
    {
        "slug": "2025-12-03-langchain-evaluating-deep-agents-our-learnings",
        "title": "Evaluating Deep Agents: Our Learnings",
        "date": "2025-12-03",
        "author": "LangChain",
        "source": "LangChain",
        "url": "https://blog.langchain.com/evaluating-deep-agents-our-learnings/",
        "relation": "기반",
        "one_liner": "Deep Agents를 실제 제품에 적용하면서 eval을 어떻게 설계했는지 정리한 글로, harness의 개선 루프를 평가 쪽에서 설명한다.",
        "importance": "harness engineering이 단순 prompt 튜닝이 아니라 평가 인프라를 동반한 운영 문제라는 점을 잘 보여준다.",
        "key_points": [
            "deep agent는 datapoint마다 성공 조건이 다르기 때문에, 정적 QA보다 bespoke test logic이 필요하다고 주장한다.",
            "single-step, full-turn, multi-turn eval을 구분해 의사결정, 최종 상태, 현실적 상호작용을 서로 다른 수준에서 측정한다.",
            "환경 세팅이 깨끗하고 재현 가능해야 eval이 의미를 가지며, 그렇지 않으면 모델보다 환경 편차가 결과를 지배한다고 본다.",
        ],
        "harness_view": [
            "이 글은 harness engineering의 검증 레이어를 설명한다. 좋은 harness는 agent를 실행하는 것만이 아니라, 바뀐 harness가 실제로 개선됐는지 측정해야 한다.",
            "평가 데이터포인트 하나하나에 작업 맥락을 심는 방식은 실제 production harness 설계와 닮아 있다.",
        ],
        "limits": [
            "LangChain의 deep agent 전제와 LangSmith 기반 워크플로우가 강하게 반영된다.",
            "직접적인 harness 정의보다는 eval practice에 무게가 있다.",
        ],
    },
    {
        "slug": "2026-01-09-anthropic-demystifying-evals-for-ai-agents",
        "title": "Demystifying evals for AI agents",
        "date": "2026-01-09",
        "author": "Anthropic Engineering",
        "source": "Anthropic",
        "url": "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents",
        "relation": "기반",
        "one_liner": "에이전트 평가를 single-turn QA에서 multi-turn, stateful, tool-using 시스템 평가로 확장해 설명한 방법론 글이다.",
        "importance": "harness engineering에서 observability와 eval은 선택이 아니라 필수라는 점을 구조적으로 설명한다.",
        "key_points": [
            "에이전트는 도구를 호출하고 환경을 바꾸며 state를 누적하므로, 출력 문자열만 보는 eval은 충분하지 않다고 지적한다.",
            "trajectory, final response, environment state, grader logic을 함께 설계해야 실제 동작 변화를 포착할 수 있다고 말한다.",
            "자동 eval은 production에 문제가 드러나기 전에 regression을 잡는 장치이며, agent lifecycle 전체에서 가치가 누적된다고 본다.",
        ],
        "harness_view": [
            "harness engineering은 agent loop를 짜는 일만이 아니라, loop를 어떻게 관찰하고 자동 채점할지 설계하는 일까지 포함한다.",
            "이 글은 ‘좋은 harness는 좋은 eval과 함께 자란다’는 점을 명확히 한다.",
        ],
        "limits": [
            "구체 구현보다는 평가 원칙과 프레임이 중심이다.",
            "오픈 벤치마크보다는 실무 general guidance 성격이 강하다.",
        ],
    },
    {
        "slug": "2026-01-23-openai-unrolling-the-codex-agent-loop",
        "title": "Unrolling the Codex agent loop",
        "date": "2026-01-23",
        "author": "OpenAI Engineering",
        "source": "OpenAI",
        "url": "https://openai.com/index/unrolling-the-codex-agent-loop/",
        "relation": "기반",
        "one_liner": "Codex의 agent loop를 해부하면서, 모델과 도구, 사용자 사이를 실제로 어떻게 연결하는지가 agent 성능의 핵심임을 설명한 글이다.",
        "importance": "OpenAI가 harness를 단순 래퍼가 아니라 제품 공통 런타임으로 본다는 점을 드러내는 출발점이다.",
        "key_points": [
            "agent loop는 사용자 입력 수집, prompt assembly, model inference, tool invocation, 결과 해석, 다음 행동 결정으로 이어지는 반복 구조라고 설명한다.",
            "Codex CLI뿐 아니라 여러 Codex surface 아래에 공통 harness가 존재하며, 이 loop가 실제 품질과 안전성을 좌우한다고 본다.",
            "좋은 코딩 에이전트는 모델만 좋아서가 아니라, 어떤 도구를 어떤 순서와 제약 아래 노출하느냐에 달려 있다고 강조한다.",
        ],
        "harness_view": [
            "이 글은 harness engineering의 가장 낮은 수준, 즉 runtime semantics를 다룬다.",
            "후속 OpenAI 글들이 조직 운영과 repo legibility로 확장되기 전에, agent loop 자체가 왜 중요한지 기반을 제공한다.",
        ],
        "limits": [
            "조직 프로세스나 repo 관리 같은 상위 문제는 거의 다루지 않는다.",
            "구현 철학 소개 비중이 높고, 실험 수치는 제한적이다.",
        ],
    },
    {
        "slug": "2026-02-04-openai-unlocking-the-codex-harness",
        "title": "Unlocking the Codex harness: how we built the App Server",
        "date": "2026-02-04",
        "author": "Celia Chen",
        "source": "OpenAI",
        "url": "https://openai.com/index/unlocking-the-codex-harness/",
        "relation": "직접",
        "one_liner": "Codex의 공통 App Server를 통해, 여러 클라이언트 위에 같은 harness를 재사용하는 아키텍처를 설명한 OpenAI의 인프라 글이다.",
        "importance": "harness를 product surface별 UI가 아니라 공통 agent runtime 서비스로 본다는 점에서 매우 중요하다.",
        "key_points": [
            "웹 앱, CLI, IDE extension, macOS 앱 등 여러 surface가 동일한 Codex harness를 공유하도록 App Server를 설계했다고 설명한다.",
            "conversation primitives, protocol 선택, client integration 계층을 분리해 공통 로직과 채널별 표현을 나눈다.",
            "핵심 가치는 재사용성보다도 일관성이다. 동일한 agent behavior를 여러 접점에서 보장하기 위해 공통 실행 엔진을 만든 셈이다.",
        ],
        "harness_view": [
            "harness engineering을 애플리케이션 아키텍처 문제로 확장한 글이다.",
            "좋은 harness는 한 제품의 wrapper가 아니라, 여러 UI와 상호작용 방식을 통합하는 shared runtime이 될 수 있음을 보여준다.",
        ],
        "limits": [
            "Codex 내부 아키텍처 사례이므로 일반 팀이 그대로 재현하기 어렵다.",
            "context curation보다 protocol/integration 설계에 초점이 있다.",
        ],
    },
    {
        "slug": "2026-02-05-mitchellh-my-ai-adoption-journey",
        "title": "My AI Adoption Journey",
        "date": "2026-02-05",
        "author": "Mitchell Hashimoto",
        "source": "Mitchell Hashimoto",
        "url": "https://mitchellh.com/writing/my-ai-adoption-journey",
        "relation": "직접",
        "one_liner": "‘Step 5: Engineer the Harness’로 유명한 글로, 개인 개발자의 AI 활용이 채팅 보조에서 지속적으로 돌아가는 agent workflow로 바뀌는 과정을 설명한다.",
        "importance": "실무 현장에서 harness engineering이 왜 모델 선택보다 큰 차이를 만드는지 체감적으로 설명한 대표적 practitioner essay다.",
        "key_points": [
            "가치 있는 AI 활용은 챗봇 사용이 아니라, 자신의 작업을 재현시키고 에이전트가 독립적으로 돌 수 있는 환경을 만드는 데서 나온다고 본다.",
            "repo 구조, 테스트, 스크립트, 문서, task framing이 갖춰져야 agent가 useful work를 안정적으로 수행할 수 있다고 말한다.",
            "‘항상 에이전트 하나는 돌고 있게 하라’는 조언은, 인간이 코드를 직접 쓰는 시간을 agent orchestration 시간으로 바꾸는 사고방식을 보여준다.",
        ],
        "harness_view": [
            "OpenAI가 용어를 대중화하기 직전, 현업 개발자가 자발적으로 같은 결론에 도달했다는 점이 중요하다.",
            "harness를 agent가 일하기 좋은 repo/feedback environment로 본다는 점에서 이후 논의를 예고한다.",
        ],
        "limits": [
            "개인 경험을 바탕으로 하므로 통제된 비교는 없다.",
            "대규모 팀 운영보다는 solo/small-team workflow에 가까운 관점이다.",
        ],
    },
    {
        "slug": "2026-02-11-openai-harness-engineering",
        "title": "Harness engineering: leveraging Codex in an agent-first world",
        "date": "2026-02-11",
        "author": "Ryan Lopopolo",
        "source": "OpenAI",
        "url": "https://openai.com/index/harness-engineering/",
        "relation": "직접",
        "one_liner": "OpenAI가 0줄 수기 코드 제약으로 내부 제품을 만들며 얻은 교훈을 통해, 인간의 역할이 코드 작성에서 환경 설계로 이동했다고 선언한 핵심 글이다.",
        "importance": "현재 harness engineering 담론의 기준점이 되는 문서다.",
        "key_points": [
            "팀은 수작업 코드 없이 Codex만으로 제품, 테스트, CI, 문서, 툴링을 만들었고, 사람이 하는 일은 intent specification과 feedback loop 설계라고 설명한다.",
            "repository knowledge를 system of record로 삼고, architecture와 taste를 agent가 읽을 수 있는 형태로 외부화해야 한다고 주장한다.",
            "throughput이 급증하면 merge philosophy, entropy 관리, garbage collection, autonomy 수준 설정 같은 운영 원칙도 함께 바뀐다고 본다.",
            "핵심 목표는 application legibility가 아니라 agent legibility이며, 코드는 인간과 에이전트 둘 모두에게 읽혀야 한다고 말한다.",
        ],
        "harness_view": [
            "harness engineering을 조직 운영, repo 구조, CI, docs, observability, code review 방식 전체를 재편하는 discipline으로 끌어올린 글이다.",
            "이 문서 이후 harness engineering은 단순 agent wrapper가 아니라 소프트웨어 팀의 operating model을 뜻하게 된다.",
        ],
        "limits": [
            "매우 강한 내부 사례이지만 재현 가능한 외부 benchmark는 아니다.",
            "OpenAI 내부 환경과 Codex 전제의 영향이 크다.",
        ],
    },
    {
        "slug": "2026-02-13-langchain-agent-frameworks-and-observability",
        "title": "On Agent Frameworks and Agent Observability",
        "date": "2026-02-13",
        "author": "LangChain",
        "source": "LangChain",
        "url": "https://blog.langchain.com/on-agent-frameworks-and-agent-observability/",
        "relation": "기반",
        "one_liner": "모델이 좋아질수록 agent framework가 필요 없어진다는 주장에 반박하며, 에이전트는 본질적으로 모델 바깥의 시스템이라고 정리한 글이다.",
        "importance": "harness engineering을 framework/observability 관점에서 정당화하는 글이다.",
        "key_points": [
            "agent framework의 역할은 boilerplate 감소가 아니라, 빠르게 변하는 best practice를 시스템 차원에서 encode하는 것이라고 본다.",
            "agent architecture는 chaining에서 orchestration, 다시 tool-calling loop와 filesystem/memory 중심 구조로 진화했다고 설명한다.",
            "observability는 특정 framework와 독립적으로 제공돼야 하며, 그래야 실제 production failure mode를 추적할 수 있다고 주장한다.",
        ],
        "harness_view": [
            "이 글은 harness engineering의 ‘왜 framework가 아직 필요한가’에 대한 답이다.",
            "모델 성능이 높아질수록 wrapper가 사라지는 것이 아니라, 오히려 더 얇고 더 중요한 system layer로 남는다는 관점을 준다.",
        ],
        "limits": [
            "LangChain의 제품 관점이 강하게 반영된다.",
            "direct harness definition보다 broader framework defense에 가깝다.",
        ],
    },
    {
        "slug": "2026-02-17-langchain-improving-deep-agents-with-harness-engineering",
        "title": "Improving Deep Agents with harness engineering",
        "date": "2026-02-17",
        "author": "LangChain",
        "source": "LangChain",
        "url": "https://blog.langchain.com/improving-deep-agents-with-harness-engineering/",
        "relation": "직접",
        "one_liner": "같은 모델을 유지한 채 harness만 바꿔 Terminal Bench 2.0 점수를 크게 끌어올린, 현재 가장 실증적인 harness engineering 사례다.",
        "importance": "‘모델보다 harness가 더 큰 성능 레버’라는 주장을 정량 데이터로 뒷받침한다.",
        "key_points": [
            "deepagents-cli는 GPT-5.2-codex를 그대로 둔 채 system prompt, tools, middleware만 바꿔 52.8에서 66.5로 올랐다고 보고한다.",
            "LangSmith trace를 대규모로 분석해 실패 패턴을 찾고, 이를 Agent Skill 형태의 trace analyzer로 자동화해 개선 루프를 만들었다.",
            "self-verification, tracing, error-focused iteration이 harness 개선의 핵심 레버로 제시된다.",
        ],
        "harness_view": [
            "이 글은 harness engineering을 추상 개념이 아니라 measurable optimization space로 보여준다.",
            "시스템 프롬프트, 도구, middleware를 ‘knobs’로 보고 실험하는 태도가 이후 실무 패턴의 표준에 가깝다.",
        ],
        "limits": [
            "Terminal Bench라는 특정 benchmark에 최적화된 결과라 일반화에는 주의가 필요하다.",
            "LangChain 관측 인프라 전제가 강하다.",
        ],
    },
    {
        "slug": "2026-02-22-ignorance-ai-emerging-harness-engineering-playbook",
        "title": "The Emerging \"Harness Engineering\" Playbook",
        "date": "2026-02-22",
        "author": "Charlie Guo",
        "source": "ignorance.ai",
        "url": "https://www.ignorance.ai/p/the-emerging-harness-engineering",
        "relation": "직접",
        "one_liner": "OpenAI, Stripe, Peter Steinberger 등 여러 사례를 엮어, 팀이 agent-first 방식으로 재조직될 때 반복적으로 나타나는 패턴을 정리한 분석 글이다.",
        "importance": "원문 사례를 한데 묶어 ‘playbook’ 수준으로 정리한 대표적인 2차 분석 문서다.",
        "key_points": [
            "에이전트 성능 향상은 모델 진화만이 아니라, 팀 구조와 프로세스가 agent throughput에 맞게 바뀌면서 가속된다고 본다.",
            "배경 에이전트, 병렬 agent fleet, async workflow, 사람의 승인/검토 포인트 재배치가 공통 패턴으로 제시된다.",
            "agent를 잘 쓰는 팀은 코드를 직접 많이 쓰지 않고, task batching과 intent specification, repo legibility에 시간을 더 쓴다고 정리한다.",
        ],
        "harness_view": [
            "harness engineering을 개별 repo 문제에서 벗어나 조직 운영 playbook으로 해석한다.",
            "실행 환경뿐 아니라 작업 배분과 merge 흐름까지 harness의 일부로 본다는 점이 중요하다.",
        ],
        "limits": [
            "대부분 외부 사례를 재구성한 분석 글이라 1차 데이터는 제한적이다.",
            "낙관적 해석이 강하고 부정 사례는 상대적으로 적다.",
        ],
    },
    {
        "slug": "2026-02-24-devto-agent-harness-is-the-architecture",
        "title": "The Agent Harness Is the Architecture (and Your Model Is Not the Bottleneck)",
        "date": "2026-02-24",
        "author": "Evangelos Pappas",
        "source": "DEV Community",
        "url": "https://dev.to/epappas/the-agent-harness-is-the-architecture-and-your-model-is-not-the-bottleneck-3bjd",
        "relation": "직접",
        "one_liner": "모델 경쟁보다 harness 설계가 production reliability를 좌우한다는 가설을 여러 공개 사례와 논문으로 방어하는 장문 글이다.",
        "importance": "실무자 관점에서 harness engineering 개념을 더 넓은 audience에게 번역해 준 글이다.",
        "key_points": [
            "모델이 일정 capability threshold를 넘으면, reliability 차이는 context management, tool selection, state persistence, error recovery에서 난다고 주장한다.",
            "OpenAI, LangChain, benchmark 논문 등을 끌어와 harness가 실제 성능 레버라는 근거를 제시한다.",
            "agent architecture를 논할 때 model choice보다 environment design을 먼저 봐야 한다는 메시지를 강하게 밀어붙인다.",
        ],
        "harness_view": [
            "이 글은 harness engineering을 ‘아키텍처 레벨의 병목’으로 재명명한다.",
            "원전은 아니지만 다양한 근거를 한 방향으로 엮어 주기 때문에 빠른 개념 파악에 유용하다.",
        ],
        "limits": [
            "2차 문헌 의존도가 높고, 사례 해석이 약간 강한 편이다.",
            "새로운 기술 패턴을 제안하기보다는 기존 자료를 해설하는 성격이 강하다.",
        ],
    },
    {
        "slug": "2026-02-24-martinfowler-context-engineering-for-coding-agents",
        "title": "Context Engineering for Coding Agents",
        "date": "2026-02-24",
        "author": "Birgitta Böckeler",
        "source": "Martin Fowler",
        "url": "https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html",
        "relation": "기반",
        "one_liner": "코딩 에이전트의 컨텍스트를 구성하는 요소를 taxonomy로 정리하고, tools/MCP/skills/rules/specs 같은 용어를 명확히 해 주는 primer다.",
        "importance": "harness engineering을 이해하기 전에 내부 레이어를 정리하는 데 가장 유용한 글 중 하나다.",
        "key_points": [
            "reusable prompts, context interfaces, tools, MCP servers, skills, rules, specs를 구분해 coding agent context의 구성 요소를 체계화한다.",
            "Claude Code를 예시로 들어, 최근 DX 경쟁이 사실상 context configuration 경쟁으로 변하고 있다고 설명한다.",
            "‘Everything is context’라는 넓은 정의를 바탕으로, 컨텍스트를 파일과 규칙의 네트워크로 다루는 감각을 전달한다.",
        ],
        "harness_view": [
            "harness engineering이 모델 바깥을 다룬다면, 이 글은 그 바깥 레이어 중에서도 모델 안으로 넣을 입력면을 정교하게 분해한다.",
            "후속 Martin Fowler의 harness engineering 글을 이해하기 위한 전제 문서로 읽으면 가장 좋다.",
        ],
        "limits": [
            "경험 기반 primer라 정량 실험은 없다.",
            "Claude Code 중심 예시가 많아 특정 도구 편향이 있다.",
        ],
    },
    {
        "slug": "2026-03-02-devto-building-the-agent-harness",
        "title": "Building the Agent Harness: Why the Environment Matters More Than the Model",
        "date": "2026-03-02",
        "author": "Shreyas Khandelwal",
        "source": "DEV Community",
        "url": "https://dev.to/skhandelwal/building-the-agent-harness-why-the-environment-matters-more-than-the-model-39ie",
        "relation": "직접",
        "one_liner": "LLM, agent, system prompt, harness를 층위별로 구분하며, 실제로 팀이 통제할 수 있는 레버는 harness뿐이라고 정리한 현장 노트다.",
        "importance": "repo owner 관점에서 harness engineering의 실무 감각을 설명하는 글이다.",
        "key_points": [
            "LLM은 brain, agent는 loop, system prompt는 behavior definition, harness는 코드베이스 주변의 문서/제약/피드백 루프라고 층위를 나눈다.",
            "개발팀은 모델도 툴 내부도 직접 고치기 어렵지만, repo의 규칙과 환경은 직접 설계할 수 있으며 이 부분이 시간이 갈수록 복리 효과를 낸다고 주장한다.",
            "따라서 경쟁력은 ‘어떤 툴을 쓰느냐’보다 ‘어떤 환경을 소유하고 다듬느냐’에서 나온다고 본다.",
        ],
        "harness_view": [
            "실무자에게 harness engineering을 가장 소박하고 명확하게 설명하는 글 중 하나다.",
            "repo documents, constraints, tests, conventions가 모두 harness 자산이라는 점을 강조한다.",
        ],
        "limits": [
            "한 달 정도의 실험에서 나온 field note라 일반화에는 주의가 필요하다.",
            "새로운 benchmark나 구현 공개는 없다.",
        ],
    },
    {
        "slug": "2026-03-03-inngest-your-agent-needs-a-harness-not-a-framework",
        "title": "Your Agent Needs a Harness, Not a Framework",
        "date": "2026-03-03",
        "author": "Inngest",
        "source": "Inngest",
        "url": "https://www.inngest.com/blog/your-agent-needs-a-harness-not-a-framework",
        "relation": "직접",
        "one_liner": "agent harness를 event routing, retries, durability, concurrency control, tracing까지 포함하는 인프라 계층으로 정의한 글이다.",
        "importance": "harness engineering을 애플리케이션 코드 바깥의 durable runtime 관점에서 해석해 준다.",
        "key_points": [
            "wire harness, test harness, safety harness 비유를 통해 agent harness는 component를 연결하고 보호하고 오케스트레이션하는 계층이라고 정의한다.",
            "모든 LLM call과 tool call을 independently retryable step으로 다루고, 이벤트 기반으로 트리거와 worker를 분리해야 한다고 주장한다.",
            "Utah 예제를 통해 Slack/Telegram/cron/sub-agent 호출을 동일한 event fabric 위에 올리는 방식을 보여준다.",
        ],
        "harness_view": [
            "이 글은 harness engineering의 infra/runtime 면을 가장 강하게 강조한다.",
            "모델의 추론력보다도 job queue, persistence, tracing, concurrency guard가 실제 운영 안정성을 만든다는 관점이 분명하다.",
        ],
        "limits": [
            "Inngest 제품 관점이 강하고, 코딩 에이전트보다는 event-driven agent runtime 쪽에 무게가 있다.",
            "조직 운영보다 인프라 메커니즘에 초점이 있다.",
        ],
    },
    {
        "slug": "2026-03-04-martinfowler-humans-and-agents-in-software-engineering-loops",
        "title": "Humans and Agents in Software Engineering Loops",
        "date": "2026-03-04",
        "author": "Kief Morris",
        "source": "Martin Fowler",
        "url": "https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html",
        "relation": "기반",
        "one_liner": "사람과 에이전트가 소프트웨어 작업 루프 안에서 어떤 식으로 역할을 나누는지를 분류해, harness를 인간 감독까지 포함한 루프로 보게 만든 글이다.",
        "importance": "harness engineering을 순수 기술 계층이 아니라 socio-technical loop로 확장해 준다.",
        "key_points": [
            "사람이 프롬프트만 던지고 기다리는 구조, 사람과 agent가 번갈아 협업하는 구조, agent가 background에서 길게 도는 구조 등 여러 loop를 구분한다.",
            "문제는 agent autonomy가 아니라, 어느 지점에서 사람이 개입하고 승인하고 방향을 수정할지를 설계하는 것이라고 본다.",
            "도구 선택만큼이나 handoff, review, escalation, merge 타이밍이 중요하다고 설명한다.",
        ],
        "harness_view": [
            "harness engineering이 repo와 도구만의 문제가 아니라, 인간-에이전트 협업 loop 설계라는 점을 잘 보여준다.",
            "OpenAI 글의 ‘humans steer, agents execute’를 더 일반적인 소프트웨어 팀 모델로 풀어낸 셈이다.",
        ],
        "limits": [
            "경험적 taxonomy 중심이라 계량 데이터는 없다.",
            "운영 예시는 다양하지만 구현 디테일은 상대적으로 적다.",
        ],
    },
    {
        "slug": "2026-03-05-martinfowler-harness-engineering",
        "title": "Harness Engineering",
        "date": "2026-03-05",
        "author": "Birgitta Böckeler",
        "source": "Martin Fowler",
        "url": "https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html",
        "relation": "직접",
        "one_liner": "context engineering 바깥의 환경, 검증, 실행, 워크플로우를 다루는 discipline으로 harness engineering을 명시적으로 정의한 글이다.",
        "importance": "현재 개념 정의 측면에서는 OpenAI 글과 함께 가장 중요한 문서다.",
        "key_points": [
            "context engineering이 모델 안으로 무엇을 넣을지 다룬다면, harness engineering은 모델 바깥에서 결과를 안정화하는 모든 장치를 뜻한다고 설명한다.",
            "여기에는 test/eval, run loop, repo 규칙, artifacts, observability, human checkpoints, execution environment가 모두 포함된다.",
            "모델이 좋아질수록 중요한 것은 더 큰 prompt가 아니라, 외부 시스템이 agent의 불안정성을 흡수하고 productive behavior로 유도하는 방식이라고 본다.",
        ],
        "harness_view": [
            "이 글은 개념 경계를 가장 잘 긋는다. context engineering과 harness engineering을 분리해 이후 논의를 훨씬 선명하게 만든다.",
            "실무적으로는 ‘프롬프트를 고칠까?’보다 ‘환경을 바꿀까?’를 먼저 묻게 만든다.",
        ],
        "limits": [
            "개념 정리 성격이 강해 구체 구현 패턴은 다른 글과 함께 읽어야 한다.",
            "정량 benchmark보다는 사고 틀 제공에 가깝다.",
        ],
    },
]


PAPERS = [
    {
        "slug": "2025-06-13-sec-bench",
        "title": "SEC-bench: Automated Benchmarking of LLM Agents on Real-World Software Security Tasks",
        "date": "2025-06-13",
        "author": "Hwiwon Lee 외 3명",
        "source": "arXiv",
        "url": "https://arxiv.org/abs/2506.11791",
        "relation": "인접 연구",
        "one_liner": "실제 소프트웨어 보안 작업으로 LLM agent를 평가하는 자동 benchmark를 제안한 논문으로, eval harness 설계의 초기 기준점이다.",
        "problem": "기존 software-agent benchmark는 보안 실무 작업과 보안 도메인 특수성을 충분히 반영하지 못했다.",
        "approach": [
            "실제 보안 태스크를 기반으로 자동 채점 가능한 benchmark 세트를 만들고, 에이전트가 환경 안에서 작업을 수행한 결과를 harness로 평가한다.",
            "보안 업무 특성상 단순 정답 비교보다 실행 가능성과 task completion을 함께 보려는 관점을 도입한다.",
        ],
        "results": [
            "보안 도메인에서 agent의 실제 역량을 재는 재현 가능한 평가 기반을 제공했다는 점이 핵심 기여다.",
            "일반 코딩 benchmark와 다른 failure mode를 노출해, domain-specific harness가 필요함을 보여준다.",
        ],
        "harness_view": [
            "harness engineering 관점에서 이 논문은 ‘좋은 agent를 만들려면 먼저 좋은 평가 환경이 필요하다’는 사실을 보안 영역에서 보여준다.",
        ],
        "limits": [
            "직접적으로 harness engineering을 정의하지는 않는다.",
            "benchmark 논문이므로 실행 환경 개선 패턴보다는 평가 인프라가 중심이다.",
        ],
    },
    {
        "slug": "2025-07-24-agentic-program-repair-from-test-failures",
        "title": "Agentic Program Repair from Test Failures at Scale: A Neuro-symbolic approach with static analysis and test execution feedback",
        "date": "2025-07-24",
        "author": "Chandra Maddila 외 23명",
        "source": "arXiv",
        "url": "https://arxiv.org/abs/2507.18755",
        "relation": "인접 연구",
        "one_liner": "대규모 코드베이스에서 테스트 실패를 입력으로 받아 수정안을 만드는 엔지니어링 에이전트를 설명한 논문으로, test-execute-feedback loop의 중요성을 보여준다.",
        "problem": "대규모 조직의 실제 코드베이스에서는 단순 코드 생성보다 실패 테스트 해석, 정적 분석, 재실행 피드백 통합이 더 어렵다.",
        "approach": [
            "LLM 기반 agent에 정적 분석과 테스트 실행 결과를 결합한 neuro-symbolic repair loop를 구성한다.",
            "test failure를 기반으로 후보 수정안을 만들고, 실행 결과를 다시 받아 loop를 돌리는 방식으로 품질을 높인다.",
        ],
        "results": [
            "실제 조직 규모의 코드베이스에서 agentic repair가 가능함을 보였고, test feedback이 핵심 신호임을 강조한다.",
            "코드 생성보다 verification harness가 program repair 성능에 큰 영향을 미친다는 점을 드러낸다.",
        ],
        "harness_view": [
            "테스트 실패와 재실행 결과를 loop 안에 넣는 방식은 harness engineering의 전형적 패턴이다.",
            "모델이 직접 정답을 아는 것이 아니라, 환경이 피드백을 주며 agent를 점진적으로 수렴시킨다.",
        ],
        "limits": [
            "용어상 harness engineering을 직접 다루지는 않는다.",
            "상용/대규모 환경 전제가 강해 외부 재현성은 제한적이다.",
        ],
    },
    {
        "slug": "2025-08-26-gittaskbench",
        "title": "GitTaskBench: A Benchmark for Code Agents Solving Real-World Tasks Through Code Repository Leveraging",
        "date": "2025-08-26",
        "author": "Ziyi Ni 외 17명",
        "source": "arXiv",
        "url": "https://arxiv.org/abs/2508.18993",
        "relation": "인접 연구",
        "one_liner": "코드 저장소를 활용해 현실적 작업을 해결하는 agent를 평가하는 benchmark로, repo-level harness와 environment setup의 중요성을 보여준다.",
        "problem": "실제 개발 업무는 빈 파일에 코드 쓰기가 아니라, 기존 저장소를 탐색하고 환경을 세팅하며 성공 기준을 충족하는 일인데 이를 측정하는 benchmark가 부족했다.",
        "approach": [
            "54개의 현실적 태스크를 저장소와 함께 제공하고, 각 태스크마다 human-curated evaluation harness를 붙였다.",
            "task success뿐 아니라 경제적 효용(alpha-value)까지 측정해 실제 사용 가치를 보려 했다.",
        ],
        "results": [
            "최고 성능 시스템도 완전 해결률이 높지 않았고, 실패의 절반 이상이 environment setup과 dependency resolution 같은 mundane step에서 발생했다고 보고한다.",
            "즉 모델 reasoning보다 workflow management가 병목이 되는 경우가 많음을 보여준다.",
        ],
        "harness_view": [
            "repo leveraging이라는 현실 문제는 harness engineering의 핵심 과제와 거의 동일하다.",
            "좋은 모델보다 좋은 environment preparation과 practical success criteria가 더 중요하다는 근거를 준다.",
        ],
        "limits": [
            "benchmark이므로 개선 방법론보다는 문제 제시가 중심이다.",
            "직접적인 harness 설계 제안은 제한적이다.",
        ],
    },
    {
        "slug": "2025-09-28-perfbench",
        "title": "PerfBench: Can Agents Resolve Real-World Performance Bugs?",
        "date": "2025-09-28",
        "author": "Spandan Garg 외 2명",
        "source": "arXiv",
        "url": "https://arxiv.org/abs/2509.24091",
        "relation": "인접 연구",
        "one_liner": "기능적 correctness가 아니라 성능 버그 해결 능력을 측정하는 benchmark로, 성능 benchmark 자체를 생성하는 evaluation harness를 제안한다.",
        "problem": "기존 bug-fixing benchmark는 기능적 오류를 중심으로 설계되어, 성능 회귀와 같은 non-functional 문제를 평가하지 못했다.",
        "approach": [
            "실제 .NET 저장소의 성능 버그 81개를 수집하고, 에이전트가 직접 performance benchmark를 만들고 검증할 수 있는 novel evaluation harness를 설계했다.",
            "테스트 스위트가 이미 존재하지 않는 상황을 전제로, agent가 측정 도구를 스스로 구성해야 하는 문제를 포함시켰다.",
        ],
        "results": [
            "non-functional bug는 기존 benchmark보다 훨씬 어렵고, 에이전트가 스스로 측정 체계를 만드는 능력이 성패를 좌우함을 보여준다.",
            "즉 harness 자체가 task의 일부가 되는 영역이 존재함을 드러낸다.",
        ],
        "harness_view": [
            "harness engineering이 코드 생성 도우미가 아니라 성능 측정 환경까지 포함한다는 점을 강조해 준다.",
        ],
        "limits": [
            "성능 버그 도메인에 국한된다.",
            "일반 agent harness 전반을 설명하는 논문은 아니다.",
        ],
    },
    {
        "slug": "2026-01-10-cedar",
        "title": "CEDAR: Context Engineering for Agentic Data Science",
        "date": "2026-01-10",
        "author": "Rishiraj Saha Roy 외 3명",
        "source": "arXiv",
        "url": "https://arxiv.org/abs/2601.06606",
        "relation": "인접 연구",
        "one_liner": "데이터사이언스 태스크를 위해 구조화된 입력, 분리된 plan/code generation, 함수 호출을 결합한 context engineering 시스템을 제안한 논문이다.",
        "problem": "데이터사이언스 문제는 데이터 크기, 계산 제약, task complexity 때문에 일반 coding agent보다 context restriction의 영향을 더 크게 받는다.",
        "approach": [
            "DS-specific input field로 초기 프롬프트에 구조를 주고, 별도 agent가 interleaved plan/code block을 생성하도록 설계한다.",
            "function call을 활용해 데이터는 로컬에 두고 필요한 정보만 전달함으로써 token budget을 절약한다.",
        ],
        "results": [
            "효과적인 context engineering이 agentic DS workflow를 실용화할 수 있음을 시연했다.",
            "계획과 코드 생성의 역할 분리, 로컬 데이터 유지가 성능과 가독성에 중요하다고 주장한다.",
        ],
        "harness_view": [
            "도메인이 달라도 핵심은 같다. 무엇을 context로 올리고 무엇을 외부 런타임에 남길지 설계하는 것이 성능을 결정한다.",
        ],
        "limits": [
            "데이터사이언스 특화 구조라 일반 소프트웨어 작업으로 바로 확장하기는 어렵다.",
            "주로 context engineering에 초점이 있다.",
        ],
    },
    {
        "slug": "2026-01-29-meta-context-engineering",
        "title": "Meta Context Engineering via Agentic Skill Evolution",
        "date": "2026-01-29",
        "author": "Haoran Ye 외 4명",
        "source": "arXiv",
        "url": "https://arxiv.org/abs/2601.21557",
        "relation": "인접 연구",
        "one_liner": "수작업으로 만든 고정 harness 대신, meta-level agent가 context engineering skill과 artifact를 공진화시키는 프레임워크를 제안한 논문이다.",
        "problem": "현재 context engineering은 사람이 만든 rigid workflow와 schema에 묶여 있어, 탐색 공간이 좁고 구조적 편향이 크다.",
        "approach": [
            "Meta Context Engineering(MCE)이라는 bi-level framework를 도입해, meta-agent가 engineering skill과 context artifact를 함께 개선하도록 한다.",
            "정적 heuristic 대신 evolution loop를 통해 더 나은 context construction 방식을 찾으려 한다.",
        ],
        "results": [
            "context engineering 자체를 또 하나의 최적화 대상으로 본다는 점이 핵심 기여다.",
            "향후 harness engineering 자동화 가능성을 여는 아이디어로 읽을 수 있다.",
        ],
        "harness_view": [
            "사람이 직접 harness를 설계하는 단계를 넘어, harness 설계 기술 자체를 agent가 탐색하게 하려는 시도다.",
        ],
        "limits": [
            "개념적 야심이 큰 반면, 실무 재현성과 검증 폭은 아직 제한적이다.",
            "직접적인 production 사례보다는 연구 프레임워크에 가깝다.",
        ],
    },
    {
        "slug": "2026-02-05-structured-context-engineering",
        "title": "Structured Context Engineering for File-Native Agentic Systems: Evaluating Schema Accuracy, Format Effectiveness, and Multi-File Navigation at Scale",
        "date": "2026-02-05",
        "author": "Damon McMillan",
        "source": "arXiv",
        "url": "https://arxiv.org/abs/2602.05447",
        "relation": "인접 연구",
        "one_liner": "대규모 파일/스키마 환경에서 어떤 형식과 구조가 agent 성능을 높이는지 9,649회 실험으로 비교한 empirical context engineering 연구다.",
        "problem": "대형 스키마나 파일 구조를 agent에게 어떻게 보여줘야 하는지 실무 가이드는 많지만 실증 연구는 부족했다.",
        "approach": [
            "11개 모델, 4개 포맷(YAML, Markdown, JSON, TOON), 10~10,000개 스키마 범위를 대상으로 대규모 실험을 수행했다.",
            "SQL generation을 대리 과제로 써서 structured data context를 어떻게 구성할 때 agent가 더 잘 탐색하는지 측정했다.",
        ],
        "results": [
            "컨텍스트 형식과 스키마 구조가 성능에 실질적 영향을 미치며, 포맷 선택은 단순 취향 문제가 아니라는 점을 보였다.",
            "large-scale file-native agentic system에서 context schema 자체가 성능 변수임을 실증적으로 뒷받침한다.",
        ],
        "harness_view": [
            "harness engineering의 내부 레이어를 실험적으로 다룬 논문이다.",
            "repo/file-native 환경에서 어떤 serialization이 더 agent-friendly한지 고민할 때 직접 참고할 만하다.",
        ],
        "limits": [
            "SQL generation proxy task라 일반 코딩 작업 전체를 대표하지는 않는다.",
            "context engineering의 일부 면만 다룬다.",
        ],
    },
    {
        "slug": "2026-02-10-autoharness",
        "title": "AutoHarness: improving LLM agents by automatically synthesizing a code harness",
        "date": "2026-02-10",
        "author": "Xinghua Lou 외 5명",
        "source": "arXiv",
        "url": "https://arxiv.org/abs/2603.03329",
        "relation": "직접",
        "one_liner": "금지된 행동이나 비합법적 행동을 줄이기 위해, task마다 code harness를 자동 합성하는 가장 직접적인 harness engineering 논문이다.",
        "problem": "LLM agent는 외부 환경 제약을 자주 어기며, 이를 막기 위해 사람들은 수작업 harness를 작성하지만 이는 확장성이 낮다.",
        "approach": [
            "agent가 illegal move나 금지된 행동을 하지 못하도록 task-specific code harness를 자동으로 합성한다.",
            "사람이 hand-write하던 constraint layer를 자동 생성함으로써 scaling bottleneck을 줄이려 한다.",
        ],
        "results": [
            "수작업 harness 없이도 agent failure mode를 크게 줄일 수 있음을 보이며, harness synthesis 자체를 연구 대상으로 끌어올렸다.",
            "정확한 reasoning 개선보다 외부 constraint enforcement가 성능을 좌우하는 경우가 많음을 시사한다.",
        ],
        "harness_view": [
            "현재 시점에서 가장 직접적으로 harness engineering을 논문 제목 수준에서 다루는 문헌이다.",
            "실무의 ‘guardrail code’를 자동 생성 대상으로 본다는 점이 특히 중요하다.",
        ],
        "limits": [
            "특정 환경 제약 문제에서 강점을 보이는 만큼, 일반적인 소프트웨어 개발 harness 전체를 포괄하지는 않는다.",
            "자동 합성된 harness의 유지보수성 문제는 추가 검증이 필요하다.",
        ],
    },
    {
        "slug": "2026-02-25-vero",
        "title": "VeRO: An Evaluation Harness for Agents to Optimize Agents",
        "date": "2026-02-25",
        "author": "Varun Ursekar 외 4명",
        "source": "arXiv",
        "url": "https://arxiv.org/abs/2602.22480",
        "relation": "직접",
        "one_liner": "에이전트가 다른 에이전트를 개선하는 task를 위해 reproducible evaluation harness를 설계한 연구로, ‘agent optimization’ 자체를 벤치마킹한다.",
        "problem": "에이전트가 타깃 에이전트를 edit-execute-evaluate loop로 개선하는 작업은 중요하지만, 이를 체계적으로 평가하는 방법이 부족했다.",
        "approach": [
            "VERO는 versioned agent snapshot, reward, observation capture를 포함한 reproducible evaluation harness를 제공한다.",
            "stochastic LLM completion과 deterministic code execution이 섞인 특수한 최적화 문제를 다룬다.",
        ],
        "results": [
            "agent optimization task가 일반 소프트웨어 태스크와 다르며, 중간 reasoning과 실행 결과를 구조화해 포착해야 함을 보여준다.",
            "향후 self-improving agent research에 필요한 공통 실험 기반을 제시한다.",
        ],
        "harness_view": [
            "harness engineering이 agent를 개선하는 대상일 뿐 아니라, 개선 과정을 측정하는 harness도 필요하다는 점을 잘 보여준다.",
        ],
        "limits": [
            "평가 프레임워크 논문이라 직접적인 product harness recipe는 제한적이다.",
            "실제 production coding workflow와는 다소 다른 연구 설정이다.",
        ],
    },
    {
        "slug": "2026-03-05-building-ai-coding-agents-for-the-terminal",
        "title": "Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned",
        "date": "2026-03-05",
        "author": "Nghi D. Q. Bui",
        "source": "arXiv",
        "url": "https://arxiv.org/abs/2603.05344",
        "relation": "직접",
        "one_liner": "CLI 기반 코딩 에이전트 OPENDEV를 소개하며, scaffolding, harness, context engineering을 하나의 복합 시스템으로 다룬 시의성 높은 논문이다.",
        "problem": "terminal-native coding agent는 높은 자율성을 주는 대신 safety control, context bloat, reasoning degradation, long-horizon execution 문제가 크다.",
        "approach": [
            "OPENDEV는 workload-specialized model routing, planner/executor를 나눈 dual-agent architecture, safety control을 갖춘 compound AI system으로 설계된다.",
            "CLI 환경에서 실제 빌드/실행/배포 맥락을 다루기 위해 scaffolding과 harness를 동등한 1급 설계 요소로 둔다.",
        ],
        "results": [
            "IDE plugin에서 terminal-native agent로 이동하는 흐름 속에서 어떤 시스템 구성이 필요한지 체계적으로 정리했다.",
            "context efficiency와 execution control이 코딩 agent 품질에 필수적이라는 메시지를 명확히 전달한다.",
        ],
        "harness_view": [
            "현재 시점의 학술 문헌 중 harness engineering의 실무 감각을 가장 직접적으로 흡수한 논문이다.",
            "OpenAI/Anthropic/LangChain 글에서 논의되던 개념을 연구 형식으로 정리한 문서로 읽기 좋다.",
        ],
        "limits": [
            "아직 최신 preprint라 외부 검증이 충분하지 않다.",
            "자체 시스템 중심 설명이라 독립적 비교는 제한적이다.",
        ],
    },
]


def render_blog(entry: dict) -> str:
    lines = [
        f"# {entry['title']}",
        "",
        f"- 구분: 블로그/아티클",
        f"- 발행일: {entry['date']}",
        f"- 저자: {entry['author']}",
        f"- 출처: {entry['source']}",
        f"- 원문: {entry['url']}",
        f"- 관련성: {entry['relation']}",
        "",
        "## 한줄 요약",
        entry["one_liner"],
        "",
        "## 왜 중요한가",
        entry["importance"],
        "",
        "## 핵심 내용",
    ]
    lines.extend(f"- {item}" for item in entry["key_points"])
    lines.extend(
        [
            "",
            "## Harness Engineering 관점",
        ]
    )
    lines.extend(f"- {item}" for item in entry["harness_view"])
    lines.extend(
        [
            "",
            "## 한계와 주의점",
        ]
    )
    lines.extend(f"- {item}" for item in entry["limits"])
    lines.append("")
    return "\n".join(lines)


def render_paper(entry: dict) -> str:
    lines = [
        f"# {entry['title']}",
        "",
        f"- 구분: 논문",
        f"- 발행일: {entry['date']}",
        f"- 저자: {entry['author']}",
        f"- 출처: {entry['source']}",
        f"- 원문: {entry['url']}",
        f"- 관련성: {entry['relation']}",
        "",
        "## 한줄 요약",
        entry["one_liner"],
        "",
        "## 문제 설정",
        entry["problem"],
        "",
        "## 제안 방법",
    ]
    lines.extend(f"- {item}" for item in entry["approach"])
    lines.extend(
        [
            "",
            "## 결과와 시사점",
        ]
    )
    lines.extend(f"- {item}" for item in entry["results"])
    lines.extend(
        [
            "",
            "## Harness Engineering 관점",
        ]
    )
    lines.extend(f"- {item}" for item in entry["harness_view"])
    lines.extend(
        [
            "",
            "## 한계와 주의점",
        ]
    )
    lines.extend(f"- {item}" for item in entry["limits"])
    lines.append("")
    return "\n".join(lines)


def render_index() -> str:
    lines = [
        "# Harness Engineering 자료 모음",
        "",
        f"- 수집 기준일: 2026-03-08",
        f"- 블로그/아티클 수: {len(BLOGS)}",
        f"- 논문 수: {len(PAPERS)}",
        "- 수집 범위: 2025년 6월 이후 발표된 harness engineering 직접 문헌과, 이를 형성한 context engineering / eval harness / coding-agent scaffolding 관련 핵심 문헌",
        "- 제외 범위: 단순 뉴스 재인용, 짧은 소셜 포스트, 번역 복제본, 제품 랜딩 페이지",
        "",
        "## 디렉터리 구조",
        "- `docs/blogs`: 블로그/아티클 개별 문서",
        "- `docs/papers`: 논문 개별 문서",
        "- `REPORT.md`: 전체 종합 보고서",
        "",
        "## 블로그/아티클",
    ]
    for entry in sorted(BLOGS, key=lambda x: (x["date"], x["slug"])):
        lines.append(
            f"- [{entry['date']}] [{entry['title']}](docs/blogs/{entry['slug']}.md) - {entry['source']}, {entry['relation']}"
        )
    lines.extend(["", "## 논문"])
    for entry in sorted(PAPERS, key=lambda x: (x["date"], x["slug"])):
        lines.append(
            f"- [{entry['date']}] [{entry['title']}](docs/papers/{entry['slug']}.md) - {entry['source']}, {entry['relation']}"
        )
    lines.append("")
    return "\n".join(lines)


def render_report() -> str:
    return dedent(
        f"""\
        # Harness Engineering 종합 보고서

        - 작성일: 2026-03-08
        - 코퍼스 규모: 블로그/아티클 {len(BLOGS)}건, 논문 {len(PAPERS)}건

        ## 1. 한 문장 정의

        Harness engineering은 모델 바깥에서 에이전트가 안정적으로 일하도록 만드는 모든 설계 행위다. 여기에는 context curation, tool contract, runtime orchestration, eval, observability, human review loop, durability, state persistence가 모두 포함된다.

        ## 2. 수집 기준과 방법

        - 정확한 용어인 `harness engineering`을 기준으로 웹 검색을 수행했다.
        - 여기에 2025년 하반기부터 2026년 3월 초까지의 `context engineering`, `effective harnesses`, `agent loop`, `evaluation harness`, `terminal coding agents` 문헌을 추가로 묶었다.
        - 단순 뉴스 재인용과 짧은 소셜 포스트는 제외하고, 원저자 기술 글·실무 분석 글·논문 위주로 남겼다.

        ## 3. 시간축으로 본 흐름

        ### 2025년 6월~9월: 기반 형성

        - Anthropic의 multi-agent research system 글은 병렬 서브에이전트, 컨텍스트 압축, coordination 문제를 먼저 드러냈다.
        - Manus와 Anthropic의 context engineering 글들은 프롬프트보다 넓은 상태 관리가 중요하다는 인식을 확립했다.
        - 같은 시기 benchmark 논문들은 실제 저장소, 보안, 프로그램 수리처럼 환경 의존적인 태스크를 평가하기 시작했다.

        ### 2025년 11월~2026년 1월: long-running agent와 eval로 확장

        - Anthropic은 long-running agent harness, MCP 기반 code execution, eval methodology를 차례로 정리했다.
        - LangChain은 deep agent eval과 observability를 통해, 에이전트 시스템 바깥의 측정 체계를 실무 문맥으로 끌고 왔다.
        - 여기서부터 이미 `좋은 모델`보다 `좋은 시스템`이 더 중요하다는 메시지가 선명해진다.

        ### 2026년 2월~3월: 개념의 명명과 정식화

        - Mitchell Hashimoto가 `engineer the harness`라는 실무 언어를 던졌고,
        - OpenAI가 `Harness engineering: leveraging Codex in an agent-first world`로 개념을 대중화했다.
        - LangChain, Inngest, Martin Fowler, DEV 커뮤니티 글들이 이 개념을 성능 향상, 인프라, 인간-에이전트 루프, 개념 정의 차원에서 빠르게 정리했다.
        - 학술 쪽에서는 AutoHarness, VeRO, OPENDEV 논문이 거의 동시기에 등장하면서 용어와 연구 문제가 연결되기 시작했다.

        ## 4. 핵심 테마

        ### 4-1. 모델보다 환경이 중요해진다

        거의 모든 핵심 글이 같은 결론으로 모인다. 일정 수준 이상의 모델 능력이 확보되면, 실제 차이는 다음에서 난다.

        - 어떤 컨텍스트를 넣고 뺄지
        - 어떤 도구를 어떤 계약으로 노출할지
        - 장기 작업에서 상태를 어떻게 남길지
        - 실패했을 때 어떤 피드백을 줄지
        - 사람의 승인/검토 지점을 어디에 둘지

        LangChain의 Terminal Bench 사례는 이 주장을 수치로 보여주고, OpenAI와 Anthropic은 제품 사례로 뒷받침한다.

        ### 4-2. Context engineering은 harness engineering의 일부다

        수집된 문헌을 종합하면 다음처럼 구분하는 것이 가장 명확하다.

        - Context engineering: 모델 안에 무엇을 넣을지 설계하는 일
        - Harness engineering: 모델 바깥에서 실행, 검증, 기억, 제약, 루프를 설계하는 일

        Martin Fowler의 2026년 3월 글이 이 경계를 가장 선명하게 정리해 준다.

        ### 4-3. 좋은 harness는 긴 작업을 작은 진전으로 분해한다

        Anthropic의 long-running agent 글, OpenAI의 Codex 글, Inngest의 event-driven 글은 모두 같은 패턴을 보여준다.

        - 한 번에 끝내려 하지 않는다.
        - 세션 사이를 잇는 artifact를 남긴다.
        - 각 step을 재시도 가능하고 관측 가능하게 만든다.
        - 깨끗한 상태와 다음 단계 handoff를 중시한다.

        ### 4-4. Eval과 observability는 부가 기능이 아니다

        Anthropic, LangChain, VeRO, GitTaskBench, PerfBench 모두 평가 harness 없이는 agent improvement가 불가능하다는 점을 강조한다.

        - trajectory를 봐야 한다.
        - 최종 응답만 보면 안 된다.
        - 환경 상태와 실행 결과를 함께 봐야 한다.
        - benchmark 자체가 현실적이어야 한다.

        ## 5. 학술 문헌의 상태

        학술 쪽은 아직 `harness engineering`이라는 exact phrase보다 인접 개념이 더 많다.

        - 직접 관련: AutoHarness, VeRO, Building AI Coding Agents for the Terminal
        - 가까운 기반 연구: Structured Context Engineering, Meta Context Engineering, CEDAR
        - 평가/검증 인프라 연구: SEC-bench, GitTaskBench, PerfBench, Agentic Program Repair

        즉 실무 담론이 먼저 폭발했고, 논문은 그 주변의 부분문제들을 따라잡는 단계에 가깝다.

        ## 6. 실무적으로 가장 많이 반복된 패턴

        - Repo를 사람이 아니라 agent도 읽기 쉬운 구조로 만든다.
        - 규칙, 스펙, 실행 방법, 테스트 방식을 파일로 외부화한다.
        - 도구는 많이 주는 것보다 명확한 계약으로 준다.
        - 긴 작업은 initializer / planner / executor / reviewer 같은 역할로 쪼갠다.
        - 실패를 자동으로 관찰하고, trace에서 개선 포인트를 추출한다.
        - 사람은 코드를 직접 쓰기보다 intent, review, merge, exception handling에 집중한다.

        ## 7. 남아 있는 공백

        - 정확한 ROI를 보여주는 공개 데이터가 아직 적다.
        - org design과 merge/ownership 변화에 대한 체계적 연구가 부족하다.
        - 벤치마크는 늘고 있지만 production drift를 완전히 대변하진 못한다.
        - harness 자동 합성은 막 시작 단계이며, 장기 유지보수성 검증이 필요하다.

        ## 8. 추천 읽기 순서

        1. Manus / Anthropic의 context engineering 글로 내부 레이어를 이해한다.
        2. Anthropic long-running harness와 LangChain eval 글로 loop와 measurement를 본다.
        3. OpenAI의 `Unrolling`, `Unlocking`, `Harness engineering` 3종으로 runtime과 조직 운영을 본다.
        4. Martin Fowler의 `Context Engineering`, `Humans and Agents`, `Harness Engineering`으로 개념 경계를 정리한다.
        5. AutoHarness, VeRO, OPENDEV 논문으로 학술 흐름을 확인한다.

        ## 9. 최종 판단

        2025년 6월 이후의 문헌을 종합하면, harness engineering은 유행어가 아니라 에이전트 실전 배치에서 생겨난 설계 discipline으로 보는 편이 타당하다. 2025년 하반기에는 context engineering, eval harness, long-running agent design이 각각 따로 발전했고, 2026년 2월 이후 이들이 `harness engineering`이라는 이름 아래 하나의 실무 패턴으로 묶이기 시작했다.
        """
    )


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    for entry in BLOGS:
        write(BLOG_DIR / f"{entry['slug']}.md", render_blog(entry))
    for entry in PAPERS:
        write(PAPER_DIR / f"{entry['slug']}.md", render_paper(entry))

    write(ROOT / "README.md", render_index())
    write(ROOT / "REPORT.md", render_report())


if __name__ == "__main__":
    main()
