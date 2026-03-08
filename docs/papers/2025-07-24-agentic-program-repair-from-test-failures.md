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
대규모 조직의 실제 코드베이스에서는 단순 코드 생성보다 **failing test 해석, blame/bisect 정보 결합, static analysis와 test feedback 통합, patch 품질 통제**가 훨씬 어렵다. 학술 benchmark와 달리 production 환경에서는 false positive patch가 곧 regression이 되므로, **다층 검증이 필수**다.

## 제안 방법

### 전체 파이프라인
1. **Test Failure Management Bot (TFMB)**: rule-based bot이 failing test를 triage한다. 어떤 test가 왜 실패했는지, 어떤 commit이 원인인지를 분류한다.
2. **Engineering Agent**: 개발 환경을 세팅한 뒤 **ReAct harness**로 `reasoning → action → observation` 루프를 돌며 파일 읽기, 테스트 실행, 패치 생성 등 **15개 액션**을 수행한다.
3. **Neuro-symbolic Verification Loop**: agent가 생성한 patch를 **static analysis와 test execution**으로 검증하고, 그 피드백을 다시 agent에 넣어 반복 수정하게 만든다.
4. **LLM-as-a-Judge**: patch가 validation을 통과하면 별도 LLM이 Meta의 코딩 기준에 맞는 patch인지 필터링한다.
5. **Human Review**: 마지막에 human reviewer가 landing 여부를 결정한다.

### Neuro-symbolic Loop의 핵심
- 순수 neural(LLM만) 접근보다 **symbolic feedback(static analysis, test result)**을 결합하는 것이 훨씬 효과적이다.
- agent는 patch를 생성하고, static analyzer가 코드 품질을 확인하고, test runner가 기능을 확인하고, 문제가 있으면 agent에게 되돌려 수정하게 한다.
- 이 loop가 harness의 핵심이다. 모델이 정답을 아는 것이 아니라, **외부 harness가 agent를 점진적으로 수렴**시킨다.

### Patch Format의 중요성
- 표준 unified diff보다 **search-and-replace** 포맷이 agent에게 더 자연스러워 성능이 높았다.
- 이는 harness engineering에서 **tool contract 설계**의 중요성을 보여준다. 같은 기능이라도 agent-friendly한 형식으로 제공하면 성능이 달라진다.

## 결과와 시사점

### Offline 실험
- ReAct agent 단독보다 static analysis와 test feedback을 함께 넣은 구성이 훨씬 좋았다.
- 균형 모델은 **42.3% solve rate**, 평균 **11.8 feedback iteration**을 기록한다.
- 반복 실행 시 best model은 **SR@5 61.0%**까지 오른다.

### Production 결과 (3개월)
- 생성된 fix 중 **80%가 human review**를 받았고, review된 것 중 **31.5%가 landed**, 전체 생성 기준 **25.5%가 landed** 되었다.
- negative feedback은 flaky test, missing actions, partially-correct fix에 집중됐고, 이 피드백이 이후 production system 개선으로 이어졌다.
- 즉 human review가 harness 개선의 signal source로 작동한다. Fowler의 "agentic flywheel" — 실패에서 배우고, harness를 고치고, 다시 측정 — 의 실제 구현이다.

## Harness Engineering 관점
- **test failure bot → repair agent → verifier → judge → human**의 다층 loop가 production-grade harness의 전형적 구조다.
- 모델이 직접 정답을 아는 것이 아니라, static analysis, test oracle, judge model, human review가 합쳐진 **외부 harness가 agent를 점진적으로 수렴**시킨다.
- patch format의 영향(unified diff vs search-and-replace)은 harness engineering에서 **tool contract 설계**가 성능에 직접 영향을 미친다는 증거다.
- production 3개월 운영에서 나온 human feedback이 시스템 개선으로 이어지는 패턴은 harness engineering의 **continuous improvement loop**을 보여준다.

## 한계와 주의점
- 용어상 harness engineering을 직접 다루지는 않는다. 하지만 구조적으로 harness engineering의 모든 요소를 포함한다.
- Meta 내부 monorepo와 TFMB 같은 사내 인프라 전제가 강하다. 외부에서 동일한 환경을 재현하기는 어렵다.
- 범용 알고리즘 논문이라기보다 **production case study** 성격이 짙다.
- landed rate 25.5%는 인상적이지만, 나머지 74.5%의 실패 비용(리뷰 시간, 잘못된 patch에 대한 교정)도 고려해야 한다.
