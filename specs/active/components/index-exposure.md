# Spec: 인덱스 및 노출 구조 (Index & Exposure)

---
spec_id: SPEC-B5
version: v1.0
status: active
priority: P0
category: 인덱스/노출
related_specs: ["SPEC-O1", "SPEC-B2", "SPEC-B4"]
code_refs:
  - "~/.hermes/scripts/build-scores.sh"
test_refs: []
job_refs:
  - "JOB-1460"
  - "JOB-1470"
  - "JOB-1471"
created: 2026-06-04
updated: 2026-06-04
---

### [SPEC-B5] 인덱스 및 노출 구조

**설명**: LLM이 지식 시스템을 탐색할 수 있는 계층적 인덱스 구조. index.md를 메인 진입점으로, domain/tag indexes를 필터링용으로 제공.

## SBE: 구체적 예시

```yaml
examples:
  - name: "LLM 탐색 - hook 개발 지식"
    input:
      query: "Hermes Gateway hook 개발"
    expected:
      step1: "index.md 읽기 → T1 Core 확인"
      step2: "domain-system.md 또는 tag-workflow.md 참조"
      step3: "pages/hermes-gateway-hooks.md 상세 읽기"
      result: "발견 성공"
  - name: "index.md 생성"
    input:
      core_pages: 764
      working_pages: 500
      reference_pages: 500
    expected:
      total_exposed: 1764
      exposure_rate: "48.5%"
```

## DbC: 계약 조건

```yaml
contract:
  preconditions:
    - "scores.json 존재"
    - "metadata.json 존재"
  postconditions:
    - "index.md 생성 (T1/T2/T3 섹션)"
    - "domain-*.md 생성 (각 도메인별)"
    - "tag-*.md 생성 (각 태그별)"
  invariants:
    - "index.md: Core 전량 노출, Working 500개, Reference 500개"
    - "domain 파일: 해당 domain의 pages 목록"
    - "tag 파일: 해당 tag의 pages 목록"
```

## BDD: 수락 기준

```gherkin
Given scores.json에 점수 계산된 pages 존재
When build-scores.sh 실행
Then index.md 재생성
And T1 Core는 전량 노출
And T2 Working은 Top 500 노출
And T3 Reference는 Top 500 노출

Given metadata.json에 domain 정보가 있는 pages 존재
When build-scores.sh 실행
Then domain-{name}.md 파일 생성
And 해당 도메인의 page 링크 목록 포함

Given metadata.json에 tag 정보가 있는 pages 존재
When build-scores.sh 실행
Then tag-{name}.md 파일 생성
```

## 진입점 계층

| Level | 파일 | 용도 | 크기 |
|-------|------|------|------|
| L1 | knowledge-navigation 스킬 | 진입점 정의 + 워크플로우 | — |
| L2 | wiki/index.md | 메인 진입점, LLM 카탈로그 | 75KB |
| L3 | llms.txt | 코드베이스 진입점 | 1.7KB |
| L4 | llms-full.txt | 전체 인덱스 | 6.4KB |

## LLM 탐색 워크플로우

```
1. 진입점 읽기 (wiki/index.md)
   ↓
2. T1 Core 확인 (작업 필수 지식)
   ↓
3. 도메인별 인덱스 (domain-*.md) 또는 태그별 (tag-*.md)
   ↓
4. 상세 페이지 (pages/*.md)
```

## 검증 기준

| 항목 | 기준 | 상태 |
|------|------|------|
| 기능 | index.md 생성 | ✅ |
| 기능 | Core 전량 노출 | ✅ 764개 |
| 기능 | domain indexes 생성 | ✅ 16개 |
| 기능 | tag indexes 생성 | ✅ 30개 |
| 기능 | 노출률 45%+ | ✅ 48.5% |
