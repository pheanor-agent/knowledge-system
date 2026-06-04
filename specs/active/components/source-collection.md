# Spec: 원본 수집 (Raw Source Collection)

---
spec_id: SPEC-B1
version: v1.0
status: active
priority: P0
category: 원본 수집
related_specs: ["SPEC-O1"]
code_refs:
  - "~/.hermes/scripts/fetch.sh"
test_refs: []
job_refs:
  - "JOB-1434"
  - "JOB-1442"
  - "JOB-1497"
created: 2026-06-04
updated: 2026-06-04
---

### [SPEC-B1] 원본 수집

**설명**: 외부 피드(HN, GeekNews, AI Frontier) 및 내부 세션/Memory를 수집하여 원본 계층에 저장.

## SBE: 구체적 예시

```yaml
examples:
  - name: "HN 피드 수집"
    input:
      source: "hacker-news"
      cron: "0 6,18 * * *"
    expected:
      output: "~/.hermes/knowledge/feeds/2026-06-04.md"
      status: "success"
      articles: 10-20
  - name: "중복 URL 필터링"
    input:
      url: "https://example.com/already-seen"
    expected:
      action: "skip"
      reason: "url-history.txt에 존재"
  - name: "세션 가공"
    input:
      session: "~/.hermes/sessions/session-xxx.jsonl"
      role_filter: ["user", "assistant"]
    expected:
      output: "pages/session-xxx.md"
      format: "entity with frontmatter"
```

## DbC: 계약 조건

```yaml
contract:
  preconditions:
    - "원본 폴더 존재 확인"
    - "중복 URL history 파일 존재"
  postconditions:
    - "feeds/ 일일 파일 생성"
    - "url-history.txt 갱신"
    - "세션 → pages/ 인덱싱"
  invariants:
    - "원본 파일은 절대 수정하지 않음 (append-only)"
    - "url-history.txt는 중복 URL만 포함"
```

## BDD: 수락 기준

```gherkin
Given 외부 피드 소스가 존재
When fetch.sh가 cron 스케줄에 실행
Then feeds/{date}.md 파일 생성
And 중복 URL은 url-history.txt에 기록

Given 새로운 Hermes 세션 파일 존재
When sync-all.sh 실행 시 세션 가공 단계 진입
Then pages/에 wiki entity 생성
And metadata.json에 인덱싱
```

## 인터페이스

- **Input**: 외부 API (HN, GeekNews, AI Frontier) + 로컬 세션/Memory
- **Output**: `feeds/{date}.md`, `pages/session-*.md`
- **Side Effects**: url-history.txt 갱신, metadata.json 업데이트

## 내부 구조

- **fetch.sh**: 외부 피드 수집 + 중복 필터링
- **process-hermes-sessions.sh**: 세션 JSONL → wiki entities
- **process-openclaw-memory.sh**: Memory MD → wiki entities

## 검증 기준

| 항목 | 기준 | 상태 |
|------|------|------|
| 기능 | fetch.sh 06:00/18:00 정상 실행 | ✅ |
| 기능 | 세션 95%+ 가공률 | ✅ 95.1% |
| 기능 | Memory 99%+ 가공률 | ✅ 99.6% |
| 안정성 | 중복 URL skip | ✅ |
| 안정성 | surrogate 문자 파일 skip | ✅ |
