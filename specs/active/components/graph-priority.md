# Spec: 그래프 및 중요도 (Graph & Priority)

---
spec_id: SPEC-B4
version: v1.0
status: active
priority: P1
category: 그래프/우선순위
related_specs: ["SPEC-O1", "SPEC-B2", "SPEC-B3"]
code_refs:
  - "~/.hermes/scripts/build-graph.sh"
  - "~/.hermes/scripts/build-scores.sh"
  - "~/.hermes/scripts/update-usage-scores.sh"
  - "~/.hermes/scripts/extract-wikilinks.sh"
test_refs: []
job_refs:
  - "JOB-1439"
  - "JOB-1453"
  - "JOB-1460"
created: 2026-06-04
updated: 2026-06-04
---

### [SPEC-B4] 그래프 및 중요도

**설명**: wikilinks 기반 그래프 연결 생성, 4요인+decay 기반 중요도 점수 계산, 사용량 추적.

## SBE: 구체적 예시

```yaml
examples:
  - name: "wikilinks 추출"
    input:
      file: "pages/JOB-1453-architecture.md"
      content: "[[workflow-nine-steps]] 참조"
    expected:
      edge:
        source: "JOB-1453-architecture"
        target: "workflow-nine-steps"
  - name: "점수 계산"
    input:
      priority: "core"
      recency: "3일 전"
      usage: 50
      hub_count: 5
    expected:
      score: 0.74
      tier: "T1 Core"
  - name: "recency decay 적용"
    input:
      base_score: 0.6
      days_since_modified: 120
      usage: 0
    expected:
      decay: 0.3
      final_score: 0.18
```

## DbC: 계약 조건

```yaml
contract:
  preconditions:
    - "metadata.json 존재"
    - "scores.json 존재 (또는 생성)"
  postconditions:
    - "scores.json에 'entries' 키 포함"
    - "각 entry에 score/priority/recency/usage_count/domain 필드"
    - "graph_edges.json에 hubs/edges/wikilinks 필드"
  invariants:
    - "scores.json 구조: {version, updated, entries, summary}"
    - "점수 범위: 0.0 - 1.0"
    - "T1/T2/T3 분류 명확: ≥0.7 / 0.4-0.69 / <0.4"
```

## 점수 공식

```
score = (priority_weight × 0.3) + (recency_score × 0.2)
      + (usage_score × 0.3) + (hub_score × 0.1)
score = score × recency_decay

priority: core=1.0, working=0.6, reference=0.2
recency: 오늘=1.0, 7일=0.8, 30일=0.5, 90일=0.3, 180일=0.15
usage: 100+=1.0, 50-99=0.8, 20-49=0.6, 10-19=0.4, 0=0.0
hub: hub_count / 10.0 (최대 1.0)
decay: 90일+ & usage=0 → 0.3, 그 외 → 1.0
```

## BDD: 수락 기준

```gherkin
Given pages/에 wikilinks ([[Link]]) 포함 파일 존재
When build-graph.sh 실행
Then graph_edges.json에 edges 생성
And hubs 자동 식별

Given metadata.json에 priority/tags/domain 정보 존재
When build-scores.sh 실행
Then scores.json 점수 계산
And T1/T2/T3 분류 적용
And index.md 재생성

Given 90일 이상 수정 안되고 usage=0인 파일 존재
When scores 재계산
Then recency_decay 적용 (0.3)
```

## 검증 기준

| 항목 | 기준 | 상태 |
|------|------|------|
| 기능 | 점수 공식 정확성 | ✅ |
| 기능 | T1/T2/T3 분류 | ✅ |
| 기능 | recency decay 적용 | ✅ |
| 기능 | hubs 자동 식별 | ✅ 54개 |
| 개선 | edges 생성 (wikilinks 기반) | 🔴 0개 |
| 개선 | usage_count 추적 | 🔴 0회 |
