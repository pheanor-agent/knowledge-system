# Spec: 지식 가공 파이프라인 (Knowledge Processing Pipeline)

---
spec_id: SPEC-B2
version: v1.0
status: active
priority: P0
category: 가공 파이프라인
related_specs: ["SPEC-O1", "SPEC-B1"]
code_refs:
  - "~/.hermes/scripts/sync-all.sh"
  - "~/.hermes/scripts/build-metadata.sh"
  - "~/.hermes/scripts/build-graph.sh"
  - "~/.hermes/scripts/build-scores.sh"
test_refs: []
job_refs:
  - "JOB-1451"
  - "JOB-1453"
  - "JOB-1459"
  - "JOB-1497"
created: 2026-06-04
updated: 2026-06-04
---

### [SPEC-B2] 지식 가공 파이프라인

**설명**: 원본 데이터를 wiki 페이지로 변환하고 metadata/scores/graph를 자동화하는 일일 파이프라인.

## SBE: 구체적 예시

```yaml
examples:
  - name: "sync-all.sh 실행"
    input:
      schedule: "0 4 * * *"
      timeout: 3600
    expected:
      steps:
        - "build-metadata.sh 완료"
        - "build-graph.sh 완료"
        - "build-scores.sh 완료"
        - "index.md 재생성"
      status: "success"
  - name: "metadata.json 인덱싱"
    input:
      pages: 3651
    expected:
      metadata_entries: 3651
      tags_attached: 3389
      coverage: "92.8%"
  - name: "scores.json 점수 계산"
    input:
      priority_weights: {core: 1.0, working: 0.6, reference: 0.2}
      decay_applied: true
    expected:
      t1_core: 272
      t2_working: 2123
      t3_reference: 1256
      avg_score: 0.463
```

## DbC: 계약 조건

```yaml
contract:
  preconditions:
    - "pages/ 폴더 존재"
    - "surrogate 문자 파일 skip 로직 구현"
  postconditions:
    - "metadata.json 파일 수 = pages/ 파일 수"
    - "scores.json entries = metadata.json entries"
    - "index.md 재생성"
    - "domain-*.md / tag-*.md 생성"
  invariants:
    - "의존성 순서: metadata → graph → scores (변경 불가)"
    - "scores.json entries에 'entries' 키 필수"
    - "scores.json 손상 시 빈 dict 폴백"
```

## BDD: 수락 기준

```gherkin
Given 변경된 원본 파일 존재
When sync-all.sh 실행
Then metadata.json 전량 인덱싱
And scores.json 점수 재계산
And index.md + domain/tag indexes 재생성

Given surrogate 문자 포함 파일 존재
When metadata/scores 계산 실행
Then 해당 파일 skip
And 스크립트 중단 없이 계속 진행

Given scores.json이 손상됨
When build-scores.sh 실행
Then 빈 dict로 폴백 후 재시작
```

## 인터페이스

- **Input**: pages/ (지식 페이지), feeds/ (수집 결과)
- **Output**: metadata.json, scores.json, graph_edges.json, index.md
- **Side Effects**: .usage.db, feeds/ 일일 파일

## 내부 구조

| 스크립트 | 역할 | 순서 |
|----------|------|------|
| build-metadata.sh | pages/ 스캔 → metadata.json | 1 |
| build-graph.sh | wikilinks 파싱 → graph_edges.json | 2 |
| build-scores.sh | 점수 계산 + index.md 재생성 | 3 |

## 검증 기준

| 항목 | 기준 | 상태 |
|------|------|------|
| 기능 | metadata.json 100% 인덱싱 | ✅ |
| 기능 | scores.json entries 일치 | ✅ |
| 기능 | index.md 재생성 | ✅ |
| 기능 | domain/tag indexes 생성 | ✅ |
| 안정성 | surrogate 문자 skip | ✅ |
| 안정성 | scores.json 손상 시 폴백 | ✅ |
| 성능 | 실행 시간 < 5분 | ✅ |
