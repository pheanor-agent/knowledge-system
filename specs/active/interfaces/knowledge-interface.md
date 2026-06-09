# Spec: 지식 시스템 인터페이스 (Knowledge System Interface)

---
spec_id: SPEC-C1
version: v1.0
status: active
priority: P1
category: 인터페이스
related_specs: ["SPEC-O1", "SPEC-B5"]
code_refs: []
test_refs: []
job_refs:
  - "JOB-1470"
  - "JOB-1471"
created: 2026-06-04
updated: 2026-06-04
---

### [SPEC-C1] 지식 시스템 인터페이스

**설명**: LLM(Agent)이 지식 시스템과 상호작용하는 인터페이스 정의. 진입점, 탐색 워크플로우, 검색 방법.

## SBE: 구체적 예시

```yaml
examples:
  - name: "LLM 진입점 탐색"
    input:
      agent_action: "지식 시스템 탐색 시작"
    expected:
      step1: "knowledge-navigation 스킬 로드"
      step2: "wiki/index.md 읽기"
      step3: "T1 Core → T2 Working → T3 Reference 순서 확인"
  - name: "도메인별 필터링"
    input:
      query: "에이전트 관련 지식"
    expected:
      step1: "domain-agent.md 읽기"
      step2: " 관련 page 링크 확인"
  - name: "Spec 기반 검색"
    input:
      spec_id: "SPEC-C001"
    expected:
      step1: "knowledge/index.md에서 Spec 참조 확인"
      step2: "wiki 도메인 파일에서 매칭"
      step3: "_matrix.json에서 code_refs/test_refs 조회"
```

## DbC: 계약 조건

```yaml
contract:
  preconditions:
    - "knowledge-navigation 스킬 존재"
    - "wiki/index.md 존재"
    - "domain-*.md / tag-*.md 존재"
  postconditions:
    - "LLM이 진입점에서 지식 탐색 가능"
    - "도메인/태그 필터링 동작"
  invariants:
    - "진입점은 L1→L4 계층 구조 준수"
    - "LLM이 한 번에 1-2KB 컨텍스트만 로드"
    - "지식 시스템 전체 구조 파악 후 진입점 판단"
```

## BDD: 수락 기준

```gherkin
Given LLM Agent가 지식 탐색 필요
When knowledge-navigation 스킬 로드
Then 진입점 정의 확인
And wiki/index.md 로드

Given LLM이 특정 도메인 지식 필요
When domain-*.md 참조
Then 해당 도메인 pages 목록 확인
And 상세 페이지 읽기

Given LLM이 Spec 관련 지식 검색
When knowledge/index.md grep + wiki 도메인 파일 grep
Then Spec ID 매칭 결과 반환
```

## 인터페이스

- **Input**: LLM Agent 요청 (query, domain, tag, spec_id)
- **Output**: 관련 pages 목록 + 상세 내용
- **Side Effects**: .usage.db에 접근 기록

## 검증 기준

| 항목 | 기준 | 상태 |
|------|------|------|
| 기능 | knowledge-navigation 스킬 존재 | ✅ |
| 기능 | index.md 진입점 동작 | ✅ |
| 기능 | domain/tag 필터링 | ✅ |
| 기능 | Spec 기반 검색 | ✅ |
