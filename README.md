# Harness Engineering 자료 모음

- 수집 기준일: 2026-03-08
- 블로그/아티클 수: 21
- 논문 수: 10
- 수집 범위: 2025년 6월 이후 발표된 harness engineering 직접 문헌과, 이를 형성한 context engineering / eval harness / coding-agent scaffolding 관련 핵심 문헌
- 제외 범위: 단순 뉴스 재인용, 짧은 소셜 포스트, 번역 복제본, 제품 랜딩 페이지

## 통합 문서 묶음

- [docs/agent-harness/README.md](docs/agent-harness/README.md): 새 synthesis layer의 진입점
- [docs/agent-harness/01-foundations-and-boundaries.md](docs/agent-harness/01-foundations-and-boundaries.md): 정의, 경계, 용어 구분
- [docs/agent-harness/02-why-harnesses-matter.md](docs/agent-harness/02-why-harnesses-matter.md): 왜 harness가 중요한가
- [docs/agent-harness/03-harnesses-in-agent-development.md](docs/agent-harness/03-harnesses-in-agent-development.md): agent 개발에서의 사용 방식
- [docs/agent-harness/04-design-patterns-and-architecture.md](docs/agent-harness/04-design-patterns-and-architecture.md): 설계 패턴과 아키텍처
- [docs/agent-harness/05-evals-observability-and-improvement.md](docs/agent-harness/05-evals-observability-and-improvement.md): eval, tracing, 개선 루프
- [docs/agent-harness/06-humans-org-and-operating-model.md](docs/agent-harness/06-humans-org-and-operating-model.md): 사람, 조직, 운영 모델
- [docs/agent-harness/07-source-crosswalk-and-coverage-audit.md](docs/agent-harness/07-source-crosswalk-and-coverage-audit.md): 31개 자료 커버리지 감사표
- [REPORT.md](REPORT.md): 위 문서 묶음을 빠르게 훑는 축약형 랜딩 문서

## 디렉터리 구조
- `docs/blogs`: 블로그/아티클 개별 문서
- `docs/papers`: 논문 개별 문서
- `docs/agent-harness`: 전체 코퍼스를 다시 종합한 실무 플레이북 문서 묶음
- `REPORT.md`: 새 문서 구조를 안내하는 축약형 종합 개요

## 블로그/아티클
- [2025-06-13] [How we built our multi-agent research system](docs/blogs/2025-06-13-anthropic-multi-agent-research-system.md) - Anthropic, 기반
- [2025-07-18] [Context Engineering for AI Agents: Lessons from Building Manus](docs/blogs/2025-07-18-manus-context-engineering-for-ai-agents.md) - Manus, 기반
- [2025-09-11] [Writing effective tools for AI agents—using AI agents](docs/blogs/2025-09-11-anthropic-writing-effective-tools-for-ai-agents.md) - Anthropic, 기반
- [2025-09-29] [Effective context engineering for AI agents](docs/blogs/2025-09-29-anthropic-effective-context-engineering-for-ai-agents.md) - Anthropic, 기반
- [2025-11-04] [Code execution with MCP: building more efficient AI agents](docs/blogs/2025-11-04-anthropic-code-execution-with-mcp.md) - Anthropic, 기반
- [2025-11-26] [Effective harnesses for long-running agents](docs/blogs/2025-11-26-anthropic-effective-harnesses-for-long-running-agents.md) - Anthropic, 직접
- [2025-12-03] [Evaluating Deep Agents: Our Learnings](docs/blogs/2025-12-03-langchain-evaluating-deep-agents-our-learnings.md) - LangChain, 기반
- [2026-01-09] [Demystifying evals for AI agents](docs/blogs/2026-01-09-anthropic-demystifying-evals-for-ai-agents.md) - Anthropic, 기반
- [2026-01-23] [Unrolling the Codex agent loop](docs/blogs/2026-01-23-openai-unrolling-the-codex-agent-loop.md) - OpenAI, 기반
- [2026-02-04] [Unlocking the Codex harness: how we built the App Server](docs/blogs/2026-02-04-openai-unlocking-the-codex-harness.md) - OpenAI, 직접
- [2026-02-05] [My AI Adoption Journey](docs/blogs/2026-02-05-mitchellh-my-ai-adoption-journey.md) - Mitchell Hashimoto, 직접
- [2026-02-11] [Harness engineering: leveraging Codex in an agent-first world](docs/blogs/2026-02-11-openai-harness-engineering.md) - OpenAI, 직접
- [2026-02-13] [On Agent Frameworks and Agent Observability](docs/blogs/2026-02-13-langchain-agent-frameworks-and-observability.md) - LangChain, 기반
- [2026-02-17] [Improving Deep Agents with harness engineering](docs/blogs/2026-02-17-langchain-improving-deep-agents-with-harness-engineering.md) - LangChain, 직접
- [2026-02-22] [The Emerging "Harness Engineering" Playbook](docs/blogs/2026-02-22-ignorance-ai-emerging-harness-engineering-playbook.md) - ignorance.ai, 직접
- [2026-02-24] [The Agent Harness Is the Architecture (and Your Model Is Not the Bottleneck)](docs/blogs/2026-02-24-devto-agent-harness-is-the-architecture.md) - DEV Community, 직접
- [2026-02-24] [Context Engineering for Coding Agents](docs/blogs/2026-02-24-martinfowler-context-engineering-for-coding-agents.md) - Martin Fowler, 기반
- [2026-03-02] [Building the Agent Harness: Why the Environment Matters More Than the Model](docs/blogs/2026-03-02-devto-building-the-agent-harness.md) - DEV Community, 직접
- [2026-03-03] [Your Agent Needs a Harness, Not a Framework](docs/blogs/2026-03-03-inngest-your-agent-needs-a-harness-not-a-framework.md) - Inngest, 직접
- [2026-03-04] [Humans and Agents in Software Engineering Loops](docs/blogs/2026-03-04-martinfowler-humans-and-agents-in-software-engineering-loops.md) - Martin Fowler, 기반
- [2026-03-05] [Harness Engineering](docs/blogs/2026-03-05-martinfowler-harness-engineering.md) - Martin Fowler, 직접

## 논문
- [2025-06-13] [SEC-bench: Automated Benchmarking of LLM Agents on Real-World Software Security Tasks](docs/papers/2025-06-13-sec-bench.md) - arXiv, 인접 연구
- [2025-07-24] [Agentic Program Repair from Test Failures at Scale: A Neuro-symbolic approach with static analysis and test execution feedback](docs/papers/2025-07-24-agentic-program-repair-from-test-failures.md) - arXiv, 인접 연구
- [2025-08-26] [GitTaskBench: A Benchmark for Code Agents Solving Real-World Tasks Through Code Repository Leveraging](docs/papers/2025-08-26-gittaskbench.md) - arXiv, 인접 연구
- [2025-09-28] [PerfBench: Can Agents Resolve Real-World Performance Bugs?](docs/papers/2025-09-28-perfbench.md) - arXiv, 인접 연구
- [2026-01-10] [CEDAR: Context Engineering for Agentic Data Science](docs/papers/2026-01-10-cedar.md) - arXiv, 인접 연구
- [2026-01-29] [Meta Context Engineering via Agentic Skill Evolution](docs/papers/2026-01-29-meta-context-engineering.md) - arXiv, 인접 연구
- [2026-02-05] [Structured Context Engineering for File-Native Agentic Systems: Evaluating Schema Accuracy, Format Effectiveness, and Multi-File Navigation at Scale](docs/papers/2026-02-05-structured-context-engineering.md) - arXiv, 인접 연구
- [2026-02-10] [AutoHarness: improving LLM agents by automatically synthesizing a code harness](docs/papers/2026-02-10-autoharness.md) - arXiv, 직접
- [2026-02-25] [VeRO: An Evaluation Harness for Agents to Optimize Agents](docs/papers/2026-02-25-vero.md) - arXiv, 직접
- [2026-03-05] [Building AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned](docs/papers/2026-03-05-building-ai-coding-agents-for-the-terminal.md) - arXiv, 직접
