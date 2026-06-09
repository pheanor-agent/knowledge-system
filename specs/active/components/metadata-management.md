# Spec: 메타데이터 관리 (Metadata Management)

---
spec_id: SPEC-B3
version: v1.0
status: active
priority: P1
category: 메타데이터
related_specs: ["SPEC-O1", "SPEC-B2"]
code_refs:
  - "~/.hermes/scripts/build-metadata.sh"
  - "~/.hermes/scripts/rebuild-metadata.sh"
  - "~/.hermes/scripts/index-missing.sh"
  - "~/.hermes/scripts/auto-tag.sh"
  - "~/.hermes/scripts/auto-domain.sh"
test_refs: []
job_refs:
  - "JOB-1453"
  - "JOB-1459"
created: 2026-06-04
updated: 2026-06-04
---

### [SPEC-B3] 메타데이터 관리

**설명**: pages/ 폴더의 모든 파일에 대한 metadata.json 인덱싱, tags/domain 자동 추출, 누락 파일 보정.

## SBE: 구체적 예시

```yaml
examples:
  - name: "metadata.json 전량 인덱싱"
    input:
      pages_count: 3651
    expected:
      metadata_entries: 3651
      tags_extracted: 3389
      domains_assigned: 10
  - name: "tags 자동 추출"
    input:
      filename: "JOB-1453-architecture.md"
    expected:
      tags: ["job-1453", "architecture"]
  - name: "domain 자동 할당"
    input:
      filename: "JOB-1453-architecture.md"
      content_keywords: ["agent", "workflow"]
    expected:
      domain: "agent"
  - name: "누락 파일 incremental 업데이트"
    input:
      pages: 3665
      existing_metadata: 3190
    expected:
      new_entries: 475
      method: "index-missing.sh"
```

## DbC: 계약 조건

```yaml
contract:
  preconditions:
    - "pages/ 폴더 존재"
    - "metadata.json 파일 존재 (또는 생성)"
  postconditions:
    - "metadata.files 키에 모든 page 스템 포함"
    - "각 엔트리에 tags 배열 존재"
    - "각 엔트리에 domain 문자열 존재"
  invariants:
    - "metadata.json 구조: {files: {filename: {tags, domain, ...}}}"
    - "tags 최대 5개"
    - "domain은 10개 사전 정의 값 중 하나"
```

## BDD: 수락 기준

```gherkin
Given pages/에 새 파일 추가됨
When build-metadata.sh 실행
Then metadata.json에 해당 파일 인덱싱
And tags/domain 자동 추출

Given metadata.json 일부 파일 누락
When index-missing.sh 실행
Then 누락 파일만 추가 (전체 rebuild 아님)
```

## 프론트매터 스키마

```yaml
---
type: entity | concept | synthesis
tags: [tag1, tag2, tag3]
domain: agent | system | general | image | memory | session | novel | knowledge | reference | devops
source: /원본/경로.md
job: JOB-XXXX
priority: core | working | reference
archived: false
---
```

## 검증 기준

| 항목 | 기준 | 상태 |
|------|------|------|
| 기능 | metadata.json = pages/ 파일 수 | ✅ 3,651/3,651 |
| 기능 | tags 추출률 90%+ | ✅ 92.8% |
| 기능 | domain 자동 할당 | ✅ |
| 안정성 | surrogate 파일 skip | ✅ |
| 안정성 | incremental 업데이트 | ✅ |
