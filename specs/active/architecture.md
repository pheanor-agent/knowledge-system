# 지식 시스템 아키텍처 Spec

---
spec_id: SPEC-O1
version: v1.0
status: verified
priority: P0
category: 아키텍처 설계
related_specs: []
code_refs:
  - "~/.hermes/scripts/sync-all.sh"
  - "~/.hermes/scripts/build-metadata.sh"
  - "~/.hermes/scripts/build-graph.sh"
  - "~/.hermes/scripts/build-scores.sh"
  - "~/.hermes/scripts/process-hermes-sessions.sh"
test_refs: []
job_refs:
  - "JOB-1394"
  - "JOB-1395"
  - "JOB-1396"
  - "JOB-1409"
  - "JOB-1414"
  - "JOB-1416"
  - "JOB-1442"
  - "JOB-1451"
  - "JOB-1453"
  - "JOB-1459"
  - "JOB-1460"
  - "JOB-1490"
  - "JOB-1496"
  - "JOB-1497"
created: 2026-06-04
updated: 2026-06-04
---

### [SPEC-O1] 지식 시스템 아키텍처

**설명**: Karpathy 3계층 구조 기반 개인 AI 에이전트 지식 관리 시스템. 원본 데이터를 수집 → LLM이 가공 → 구조화된 지식을 제공하는 엔드투엔드 파이프라인.

**설계 원칙**:
1. **Karpathy 3계층**: Raw Sources (불변) → Wiki (LLM 가공) → Schema (규칙)
2. **계층적 컨텍스트 로딩**: LLM이 L1→L2→L3 순서로 필수 컨텍스트만 로드
3. **원본 직접 참조**: 복사/이동/symlink 금지, `source:` 필드에 원본 경로만 기록
4. **플래그 기반 아카이브**: 물리 이동 없이 `archived: true/false`로 관리

## 아키텍처 다이어그램

```
┌──────────────────────────────────────────────────────────────┐
│                    LAYER 1: Raw Sources                      │
│                                                              │
│  ┌──────────┐  ┌────────────┐  ┌───────┐  ┌──────────────┐ │
│  │OpenClaw  │  │Hermes      │  │JOB    │  │External      │ │
│  │Memory    │  │Sessions    │  │Files  │  │References    │ │
│  │260 MD    │  │204 JSONL   │  │578    │  │172 files     │ │
│  └──────────┘  └────────────┘  └───────┘  └──────────────┘ │
│         ↕              ↕             ↕              ↕        │
├──────────────────────────────────────────────────────────────┤
│                    LAYER 2: Processing                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              sync-all.sh (04:00 daily)                   │ │
│  │  ┌─────────────┐  ┌───────────┐  ┌──────────────────┐  │ │
│  │  │build-meta   │  │build-graph│  │build-scores      │  │ │
│  │  │.sh          │→ │.sh        │→ │.sh + index.md    │  │ │
│  │  └─────────────┘  └───────────┘  └──────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              fetch.sh (06:00, 18:00)                     │ │
│  │  HN / GeekNews / AI Frontier → feeds/                   │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│         ↕                    ↕                               │
├──────────────────────────────────────────────────────────────┤
│                    LAYER 3: Wiki + Schema                     │
│                                                              │
│  ┌─────────────────────┐  ┌────────────────────────────────┐ │
│  │ pages/              │  │ _data/                         │ │
│  │ 3,651 .md files     │  │ metadata.json  (3,651 entries) │ │
│  │ T1/T2/T3 분류       │  │ scores.json     (점수)         │ │
│  │                     │  │ graph_edges.json(54 hubs)      │ │
│  └─────────────────────┘  └────────────────────────────────┘ │
│         ↕                    ↕                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ index.md (LLM 카탈로그) + domain-*.md + tag-*.md         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│         ↕                                                    │
├──────────────────────────────────────────────────────────────┤
│                    LLM Consumer (Hermes Agent)                │
│  index.md → domain-*.md → pages/*.md                         │
└──────────────────────────────────────────────────────────────┘
```

## 구성 요소

### 1. 원본 계층 (Raw Sources)

**책임**: 불변 원본 데이터 저장. append-only, 수정/삭제 금지.

| 소스 | 위치 | 형식 | 현재 |
|------|------|------|------|
| OpenClaw Memory | `~/.openclaw/workspace/memory/` | MD | 260개 |
| Hermes Sessions | `~/.hermes/sessions/` | JSONL | 204개 |
| JOB Files | `~/.hermes/workspace/jobs/` | MD | 578 폴더 |
| External Refs | `~/.hermes/workspace/external/` | MD | 172개 |

### 2. 가공 파이프라인 (Processing)

**책임**: 원본 → Wiki 페이지 변환, metadata/scores/graph 자동화.

#### 2.1 sync-all.sh (일일 가공)
- **스케줄**: 매일 04:00
- **의존성**: 무
- **단계**:
  1. `build-metadata.sh`: pages/ 전량 스캔 → metadata.json
  2. `build-graph.sh`: wikilinks 파싱 → graph_edges.json
  3. `build-scores.sh`: 점수 계산 + index.md 재생성

#### 2.2 fetch.sh (외부 수집)
- **스케줄**: 06:00, 18:00
- **소스**: Hacker News, GeekNews, AI Frontier
- **출력**: `~/.hermes/knowledge/feeds/{date}.md`
- **중복 방지**: `url-history.txt` 기반

#### 2.3 세션 가공
- `process-hermes-sessions.sh`: JSONL → wiki entities
- `process-openclaw-memory.sh`: MD → wiki entities
- sync-all.sh에 통합 (별도 cron 없음)

### 3. Wiki 계층 (LLM 가공물)

**책임**: 구조화된 지식 저장, LLM이 읽을 수 있는 형식.

#### 3.1 pages/ (지식 페이지)
- **수**: 3,651개 (surrogate 2개 제외)
- **분류**: T1 Core (272), T2 Working (2,123), T3 Reference (1,256)
- **메타데이터**: tags (92.8%), domain (10개)
- **프론트매터**: `type`, `source`, `job`, `priority`, `tags`, `domain`

#### 3.2 _data/ (메타데이터)

| 파일 | 역할 | 항목 |
|------|------|------|
| metadata.json | 파일 인덱스 | tags, domain, source |
| scores.json | 중요도 점수 | score, priority, recency, usage |
| graph_edges.json | 연결 그래프 | hubs, edges, wikilinks |
| .usage.db | 사용량 추적 | SQLite, filepath/count/last_accessed |

#### 3.3 Index 계층 (노출 구조)

| 파일 | 개수 | 용도 |
|------|------|------|
| index.md | 1개 | LLM 카탈로그 (T1/T2/T3) |
| domain-*.md | 16개 | 도메인별 탐색 |
| tag-*.md | 30개 | 태그별 탐색 |

### 4. Schema 계층 (규칙 정의)

**책임**: 시스템 규칙, 프론트매터 스키마, 구조 정의. 변경 통제.

| 파일 | 용도 |
|------|------|
| SCHEMA.md | 구조 정의 + 원본 소스 |
| AGENTS.md § 지식 탐색 가이드 | 진입점 + 워크플로우 |

## 데이터 흐름

```
1. 원본 수집
   ├─ OpenClaw/Hermes 세션, JOB 파일 → daily
   ├─ 외부 피드 (HN, GeekNews) → 06:00/18:00
   └─ Signal Detector → inbox.md

2. 가공 (sync-all.sh, 04:00)
   ├─ 변경 원본 스캔 (어제 이후)
   ├─ LLM 가공 (배치, gpt-4o-mini)
   ├─ pages/ 저장
   ├─ metadata.json 갱신
   ├─ graph_edges.json 갱신
   └─ scores.json + index.md 재생성

3. LLM 노출
   ├─ index.md (T1 Core → T2 Working → T3 Reference)
   ├─ domain-*.md / tag-*.md (필터링)
   └─ pages/*.md (상세 페이지)

4. 피드백
   ├─ 사용량 추적 (.usage.db)
   ├─ 점수 갱신 (recency decay)
   └─ 아카이브 (90일 미접촉 → archived: true)
```

## 점수 계산 공식

```
score = (priority_weight × 0.3) + (recency_score × 0.2)
      + (usage_score × 0.3) + (hub_score × 0.1)
score = score × recency_decay

priority_weight: core=1.0, working=0.6, reference=0.2
recency_score: 오늘=1.0, 7일=0.8, 30일=0.5, 90일=0.3, 180일=0.15
usage_score: 100+=1.0, 50-99=0.8, 20-49=0.6, 10-19=0.4, 0=0.0
hub_score: hub_count / 10.0 (정규화, 최대 1.0)
recency_decay: 90일 이상 + usage=0 → 0.3, 그 외 → 1.0
```

## 도메인 분류

| 도메인 | 현재 개수 | 내용 |
|--------|----------|------|
| agent | 1,029 | 에이전트 동작, 통신, 브리지 |
| system | 786 | 워크플로우, 리뷰, 정책 |
| general | 744 | 일반 지식 |
| image | 258 | 이미지 생성, ComfyUI |
| memory | 254 | AI 메모리 시스템 |
| session | 204 | 세션 요약 |
| novel | 129 | 소설 작성 |
| knowledge | 122 | 지식 관리 |
| reference | 35 | 외부 참조 |
| devops | 33 | 스크립트, 설정 |

## 프론트매터 스키마

```yaml
---
type: entity | concept | synthesis
source: /원본/경로.md
job: JOB-XXXX
priority: core | working | reference
recency: YYYY-MM-DD
usage_count: 42
domain: [agent, novel, image, system, bridge, knowledge, devops]
tags: [tag1, tag2]
archived: false
---
```

## 비기능 요구사항

### 성능
- sync-all.sh 실행: < 5분 (3,651개 파일)
- index.md 크기: < 100KB
- metadata.json: < 2MB

### 확장성
- 최대 10,000 pages (현재 3,651)
- domain/tag index 자동 생성

### 안정성
- surrogate 문자 파일 skip (errors='surrogateescape')
- atomic write (tmp → mv -T)
- scores.json 손상 시 빈 dict 폴백

### 가용성
- cron 실패 시 재시도 (3회)
- 상태 파일: `pipeline/status.json`

## 검증 기준

- [x] 3계층 구조 구현 완료
- [x] 원본 → Wiki → Schema 분리가 명확함
- [x] sync-all.sh 의존성 순서 보장 (metadata → graph → scores)
- [x] metadata.json 100% 인덱싱 (3,651/3,651)
- [x] T1/T2/T3 분포: 7.4% / 58.1% / 34.4%
- [x] index.md + domain/tag indexes 생성됨
- [ ] graph_edges.json 에지 > 0 (현재 0)
- [ ] .usage.db 사용량 추적 활성화 (현재 0)

**Traceability**:
- 코드: sync-all.sh, build-metadata.sh, build-graph.sh, build-scores.sh
- 테스트: —
- JOB: JOB-1394/1395/1396/1409/1414/1416/1442/1451/1453/1459/1460/1490/1496/1497
