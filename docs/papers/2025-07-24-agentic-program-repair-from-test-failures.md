# Agentic Program Repair from Test Failures at Scale: A Neuro-symbolic approach with static analysis and test execution feedback

- 구분: 논문
- 발행일: 2025-07-24
- 저자: Chandra Maddila 외 23명
- 출처: arXiv
- 원문: https://arxiv.org/abs/2507.18755
- 관련성: 인접 연구

## 한줄 요약
대규모 모노레포 환경에서 test failure를 입력으로 받아 patch를 생성하고, static analysis·test execution·LLM judge·human review까지 연결하는 production repair loop를 설명한 논문이다.

## 문제 설정
대규모 조직의 실제 코드베이스에서는 단순 코드 생성보다 failing test 해석, blame/bisect 정보 결합, static analysis와 test feedback 통합, patch 품질 통제가 훨씬 어렵다.

## 제안 방법
- 입력은 rule-based `Test Failure Management Bot (TFMB)`가 triage한 failing test다.
- Engineering Agent는 개발 환경을 세팅한 뒤 ReAct harness로 `reasoning -> action -> observation` 루프를 돌며 파일 읽기, 테스트 실행, 패치 생성 등 `15`개 액션을 수행한다.
- 핵심은 neuro-symbolic loop다. agent가 생성한 patch를 static analysis와 test execution으로 검증하고, 그 피드백을 다시 agent에 넣어 반복 수정하게 만든다.
- patch가 validation을 통과하면 별도 `LLM-as-a-Judge`가 Meta 기준에 맞는 patch인지 필터링하고, 마지막에 human reviewer가 landing 여부를 결정한다.

## 결과와 시사점
- offline ablation에서 ReAct agent 단독보다 static analysis와 test feedback을 함께 넣은 구성이 훨씬 좋았다. 균형 모델은 `42.3%` solve rate, 평균 `11.8` feedback iteration을 기록한다.
- 반복 실행 시 best model은 `SR@5 61.0%`까지 오른다.
- patch format 자체도 중요했다. 표준 unified diff보다 `search-and-replace` 포맷이 agent에게 더 자연스러워 성능이 높았다고 보고한다.
- production에서는 3개월 동안 생성된 fix 중 `80%`가 human review를 받았고, review된 것 중 `31.5%`가 landed, 전체 생성 기준 `25.5%`가 landed 되었다.
- negative feedback은 flaky test, missing actions, partially-correct fix에 집중됐고, 이 피드백이 이후 production system 개선으로 이어졌다고 적는다.

## Harness Engineering 관점
- 테스트 실패와 재실행 결과를 loop 안에 넣는 방식은 harness engineering의 전형적 패턴이다.
- 모델이 직접 정답을 아는 것이 아니라, static analysis, test oracle, judge model, human review가 합쳐진 외부 harness가 agent를 점진적으로 수렴시킨다.
- 특히 이 논문은 `test failure bot -> repair agent -> verifier -> judge -> human`의 다층 loop가 production-grade harness라는 점을 잘 보여 준다.

## 한계와 주의점
- 용어상 harness engineering을 직접 다루지는 않는다.
- Meta 내부 mono repo와 TFMB 같은 사내 인프라 전제가 강하다.
- 범용 알고리즘 논문이라기보다 production case study 성격이 짙고, 외부에서 동일한 환경을 재현하기는 어렵다.
