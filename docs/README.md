# Hermes 지식 시스템

> **작성일**: 2026-06-01  
> **버전**: v1.0  
> **작성자**: Hermes Agent (JOB-1437)

---

## 목차

1. [개요](#1-개요)
2. [지식 그래프](#2-지식-그래프)
3. [위키 구조](#3-위키-구조)
4. [지식 가공 파이프라인](#4-지식-가공-파이프라인)
5. [검색 시스템](#5-검색-시스템)
6. [중요도 관리](#6-중요도-관리)
7. [세션 → 지식 변환](#7-세션-지식-변환)
8. [Cron 자동화](#8-cron-자동화)
9. [운용 및 모니터링](#9-운용-및-모니터링)

---

## 1. 개요

### 1.1 시스템 목적

Hermes 지식 시스템은 AI 에이전트가 **장기 기억을 유지하고 지식을 구조화**하는 인프라입니다. 세션 대화, JOB 산출물, 외부 참조 등 원천 데이터를 수집 → 가공 → 그래프화하여 에이전트가 효율적으로 검색하고 활용하게 합니다.

### 1.2 핵심 원칙

- **원본 직접 참조**: 복사/이동/symlink 금지. 원본 경로를 직접 참조
- **가공본은 위키에만**: 원본은 references/, 가공된 데이터만 wiki/
- **단일 관리 포인트**: llms.txt → wiki/index.md → graph.json 계층적 참조
- **자동화 우선**: 수동 작업은 cron으로 자동화

### 1.3 핵심 지표 (2026-06-01 기준)

| 지표 | 값 |
|------|-----|
| 총 지식 파일 | 3,703개 |
| concepts (개념) | 1,384개 |
| entities (엔티티) | 1,110개 |
| sources (소스) | 932개 |
| references (리퍼런스) | 116개 |
| 총 데이터 크기 | 7.24 MB |

---

## 2. 지식 그래프

### 2.1 그래프 구조

지식 시스템은 **그래프 기반**으로 설계되었습니다. 각 지식 노드는 wikilinks([[Link]])로 연결되어 연관 지식을 탐색할 수 있습니다.

**graph.json**:

```json
{
  "nodes": [
    {
      "id": "entities/JOB-1437-request.md",
      "type": "entity",
      "title": "JOB-1437: 지식 시스템 기술 문서",
      "domain": "knowledge",
      "links": ["concepts/knowledge-graph.md", "entities/JOB-1434-request.md"]
    }
  ],
  "edges": [
    {
      "source": "entities/JOB-1437-request.md",
      "target": "concepts/knowledge-graph.md",
      "weight": 0.8
    }
  ]
}
```

### 2.2 그래프 동기화

**knowledge-graph-sync.sh** (매일 08:00):

1. 모든 wiki 파일 스캔
2. wikilinks ([[Link]]) 추출
3. graph.json 업데이트
4. 고립 노드 감지 (에지가 없는 노드)

### 2.3 고립 노드 문제

- **현재**: 85% → 30% 미만 목표 (JOB-1170)
- **해결**: 에지 자동 생성 + 백링크 부스팅

---

## 3. 위키 구조

### 3.1 디렉토리 구조

```
~/.hermes/knowledge/wiki/
├── concepts/           # 1,384개 - 추상적 개념
├── entities/           # 1,110개 - 구체적 엔티티
├── sources/            # 932개 - 원본 소스
├── syntheses/          # 9개 - 종합 문서
├── topics/             # 11개 - 주제 그룹화
├── lessons/            # 교훈
├── references/         # 24개 - 위키 내 리퍼런스
├── jobs/               # JOB 관련
├── reports/            # 리포트
├── graph.json          # 지식 그래프
├── scores.json         # 중요도 점수
├── index.md            # 위키 인덱스
└── inbox.md            # 중앙 집합소
```

### 3.2 파일 타입 정의

| 타입 | 설명 | 예시 |
|------|------|------|
| `concept` | 추상적 개념 (알고리즘, 패턴, 아키텍처) | knowledge-graph.md, dual-agent.md |
| `entity` | 구체적 엔티티 (JOB, 프로젝트, 사람, 도구) | JOB-1437-request.md, kernel-chat.md |
| `source` | 원본 소스 (세션, 로그, 설정) | session-20260601.md |
| `synthesis` | 종합 문서 (월간/주제별 종합) | knowledge-2026-05.md |
| `topic` | 주제 그룹화 (에이전트, 지식, 소설) | ai-agents.md |
| `lesson` | 교훈 (실패/성공 분석) | lessons.md |

### 3.3 Frontmatter 스키마

```yaml
---
type: entity|concept|source|reference|lesson|synthesis|topic
source: /absolute/path/to/source
job: JOB-XXXX
priority: P0|P1|P2
domain: ai|agent|knowledge|system|novel|image|workflow|general
tags: [tag1, tag2, tag3]
recency: '2026-06-01'
usage_count: 0
---
```

---

## 4. 지식 가공 파이프라인

### 4.1 3계층 구조

```
┌─────────────────────────────────────────────┐
│  Layer 1: 원본 (references/)                 │
│  - 외부 리퍼런스, 원본 문서                   │
│  - 가공되지 않은 상태                         │
└─────────────────────────────────────────────┘
              ↓ 가공
┌─────────────────────────────────────────────┐
│  Layer 2: 위키 (wiki/)                       │
│  - concepts/, entities/, sources/           │
│  - frontmatter + 구조화된 내용               │
│  - wikilinks로 연결                          │
└─────────────────────────────────────────────┘
              ↓ 그래프화
┌─────────────────────────────────────────────┐
│  Layer 3: 그래프 (graph.json)                │
│  - 노드 + 에지                              │
│  - 중요도 점수 (scores.json)                 │
│  - 사용량 추적 (.usage.db)                   │
└─────────────────────────────────────────────┘
```

### 4.2加工 흐름

```
1. 원본 수집
   ├── inbox.md (중앙 집합소)
   ├── JOB 산출물 (investigation.md, design.md, etc.)
   └── 세션 이력

2. 분류 및 구조화
   ├── 타입 판별 (concept/entity/source)
   ├── 도메인 할당 (ai/agent/knowledge/...)
   ├── frontmatter 생성
   └── wikilinks 추가

3. 위키 저장
   ├── concepts/ 또는 entities/ 또는 sources/
   ├── graph.json 업데이트
   └── scores.json 업데이트

4. 인덱싱
   ├── llms.txt 갱신
   └── wiki/index.md 갱신
```

---

## 5. 검색 시스템

### 5.1 FTS5 풀텍스트 검색

SQLite FTS5 기반 검색:

```bash
# 기본 검색
sqlite3 ~/.hermes/knowledge/wiki/.usage.db \
  "SELECT * FROM search WHERE content MATCH '지식 그래프'"

# 다중 키워드
sqlite3 ~/.hermes/knowledge/wiki/.usage.db \
  "SELECT * FROM search WHERE content MATCH 'AI AND agent'"

# 프레이즈 검색
sqlite3 ~/.hermes/knowledge/wiki/.usage.db \
  "SELECT * FROM content MATCH '\"지식 시스템\"'"
```

### 5.2 하이브리드 검색

```
FTS5 (키워드) + graph.json (그래프) + scores.json (중요도)
```

1. FTS5로 키워드 매칭
2. graph.json으로 연관 노드 확장
3. scores.json으로 중요도 정렬

### 5.3 llms.txt 계층적 인덱스

```
llms.txt (요약)
    ↓
llms-full.txt (전체)
    ↓
wiki/index.md (카탈로그)
    ↓
개별 파일 (자세한 내용)
```

---

## 6. 중요도 관리

### 6.1 scores.json

```json
{
  "entities/JOB-1437-request.md": {
    "priority": "P1",
    "usage_count": 5,
    "last_accessed": "2026-06-01T08:00:00Z",
    "domain": "knowledge"
  }
}
```

### 6.2 중요도 레벨

| 레벨 | 설명 | 처리 |
|------|------|------|
| P0 | 최우선 (시스템 핵심) | 항상 캐시, 우선 노출 |
| P1 | 중요 (자주 참조) | 정기 동기화 |
| P2 | 일반 | 필요 시 로드 |

### 6.3 자동 업데이트

**knowledge-priority.sh** (매일 07:00):

- usage_count 기반 자동 레벨 조정
- 최근 접근 시간 반영
- 도메인별 가중치 적용

---

## 7. 세션 → 지식 변환

### 7.1 자동 변환 파이프라인

```
세션 대화 → Signal Detector → inbox.md → 위키
```

**Signal Detector**는 대화에서 다음을 감지:

| 신호 | 조건 | 형식 |
|------|------|------|
| URL | 사용자가 URL 공유 | `[URL] 텍스트 — 출처, HH:MM` |
| 결정 | 명확한 선택/지시 | `[결정] 내용 — HH:MM` |
| 개념 | 처음 등장하는 기술/프로젝트 | `[개념] 이름 — 설명 — HH:MM` |
| 문제 | 버그/장애/오류 보고 | `[문제] 요약 — HH:MM` |

### 7.2 JOB 산출물 자동 등록

JOB 완료 시:

1. `on-job-complete.sh` 실행
2. AGENTS.md 업데이트
3. llms.txt 갱신
4. wiki 동기화
5. graph.json 업데이트

---

## 8. Cron 자동화

### 8.1 지식 관련 Cron 작업

| 이름 | 시간 | 설명 |
|------|------|------|
| knowledge-health | 05:00 | 건강 체크 |
| knowledge-lessons | 05:30 | 교훈 자동 등록 |
| knowledge-graph-sync | 08:00 | 그래프 동기화 |
| inbox-to-references | 07:00 | inbox → references |
| wiki-sync | 09:00 | 위키 동기화 |
| knowledge-priority | 07:00 | 중요도 업데이트 |

---

## 9. 운용 및 모니터링

### 9.1 건강 체크

**knowledge-health-report.sh** (매일 05:00):

- 파일 수 통계
- 그래프 정합성 (invalid nodes 감지)
- 고립 노드 수
- 중복 파일 감지

### 9.2 에러 모니터링

**wiki-error-monitor.sh** (매일 06:00):

- 파싱 에러
- 그래프 에러
- 동기화 실패

### 9.3 현재 문제점

- **고립 노드**: 85% → 30% 미만 목표 (진행 중)
- **usage_count 추적**: 불완전 (개선 필요)
- **scores.json 업데이트**: 간헐적 실패

---

## 부록 A: 스크립트 목록

| 스크립트 | 설명 |
|---------|------|
| knowledge-graph-sync.sh | 그래프 동기화 |
| knowledge-health-report.sh | 건강 체크 |
| wiki-sync.sh | 위키 동기화 |
| inbox-to-references.sh | inbox → references |
| knowledge-priority.sh | 중요도 업데이트 |
| update-knowledge-index.sh | 인덱스 업데이트 |
| knowledge-validate.sh | 지식 검증 |

---

## 부록 B: 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| v1.0 | 2026-06-01 | 초안 작성 (JOB-1437) |

---

*이 문서는 Hermes Agent에 의해 자동 생성되었습니다.*
