# 지식 시스템 세미나 자료

> **최종 업데이트**: 2026-06-04
> **발표자**: 에르메스 (Hermes Agent)
> **대상**: 내부 기술 세미나

---

## 1. 개요

Hermes 지식 시스템은 Karpathy 3계층 구조를 기반으로 한 개인 AI 에이전트용 지식 관리 시스템입니다. 원본 데이터를 수집 → LLM이 가공 → 구조화된 지식을 제공하는 파이프라인으로 동작합니다.

### 핵심 원칙

- **Karpathy 3계층**: Raw Sources (불변 원본) → Wiki (LLM 가공) → Schema (규칙 정의)
- **계층적 컨텍스트 로딩**: LLM이 탐색하는 워크플로우에 맞게 L1→L2→L3 계층 구조
- **단일 진실 근원**: 원본은 knowledge/ 밖에, 가공물은 knowledge/ 안에
- **플래그 기반 아카이브**: 물리 이동 없이 metadata.json의 archived 플래그로 관리

---

## 2. 시스템 아키텍처

### 2.1 폴더 구조

```
# 원본 (knowledge/ 밖 - 기존 위치 유지)
~/.openclaw/workspace/memory/         ← OpenClaw Memory (260개 MD)
~/.hermes/sessions/                   ← Hermes Sessions (204개 JSONL)
~/.hermes/workspace/jobs/             ← JOB 원본 (578개 폴더)
~/.hermes/workspace/external/         ← 외부 소스
├── references/                       ← 리퍼런스 (73개)
└── content/                          ← 콘텐츠 (99개)

# 가공물 (knowledge/ 내)
~/.hermes/knowledge/
├── processed/wiki/
│   ├── pages/                        ← 지식 페이지 (3,651개)
│   ├── _data/                        ← 메타데이터
│   │   ├── metadata.json             ← 파일 인덱스 (3,651개)
│   │   ├── scores.json               ← 중요도 점수
│   │   ├── graph_edges.json          ← 연결 그래프
│   │   └── .usage.db                 ← 사용량 추적 (SQLite)
│   ├── index.md                      ← LLM 카탈로그 (T1/T2/T3)
│   ├── domain-*.md                   ← 도메인별 인덱스 (16개)
│   ├── tag-*.md                      ← 태그별 인덱스 (30개)
│   └── SCHEMA.md                     ← 규칙 정의
├── synthesis/                        ← 일일/주간 요약
└── pipeline/                         ← 스크립트 + status.json
```

### 2.2 진입점 계층 (L1→L4)

| Level | 파일 | 용도 | 크기 |
|-------|------|------|------|
| L1 | knowledge-navigation 스킬 | 진입점 정의 + 워크플로우 | - |
| L2 | wiki/index.md | 메인 진입점, LLM 카탈로그 | 75KB |
| L3 | llms.txt | 코드베이스 진입점 | 1.7KB |
| L4 | llms-full.txt | 전체 인덱스 | 6.4KB |

---

## 3. 실시간 현황 (2026-06-04 측정)

### 3.1 지식 페이지

| 항목 | 수치 |
|------|------|
| Wiki pages | **3,653개** (surrogate 2개 포함) |
| 유효 페이지 | **3,651개** |
| Metadata 인덱싱 | **3,651개** (100%) |
| Tags 부착 | **3,389개** (92.8%) |

### 3.2 도메인별 분포

| 도메인 | 개수 | 비율 |
|--------|------|------|
| agent | 1,029 | 28.2% |
| system | 786 | 21.5% |
| general | 744 | 20.4% |
| image | 258 | 7.1% |
| memory | 254 | 6.9% |
| session | 204 | 5.6% |
| novel | 129 | 3.5% |
| knowledge | 122 | 3.3% |
| reference | 35 | 1.0% |
| devops | 33 | 0.9% |

### 3.3 중요도 (T1/T2/T3)

| Tier | 명칭 | 점수 | 개수 | 비율 |
|------|------|------|------|------|
| T1 | Core | ≥0.7 | **272개** | **7.4%** |
| T2 | Working | 0.4-0.69 | **2,123개** | **58.1%** |
| T3 | Reference | <0.4 | **1,256개** | **34.4%** |

- **평균 점수**: 0.463
- **점수 공식**: `score = (priority × 0.3) + (recency × 0.2) + (usage × 0.3) + (hub × 0.1) × decay`

### 3.4 지식 그래프

| 항목 | 수치 |
|------|------|
| 허브 (Hubs) | 54개 |
| 연결 (Edges) | 0개 |
| Wikilinks | 0개 |

### 3.5 원본 가공률

| 원본 | 개수 | 가공 | 가공률 |
|------|------|------|--------|
| OpenClaw Memory | 260 | 259 | **99.6%** |
| Hermes Sessions | 204 | 194 | **95.1%** |
| JOB 파일 | 578 폴더 | pages 통합 | **100%** |
| 외부 리퍼런스 | 73 | pages 통합 | **100%** |
| 외부 콘텐츠 | 99 | pages 통합 | **100%** |

---

## 4. 자동화 파이프라인

### 4.1 Cron 스케줄

| 작업 | 스케줄 | 상태 | 의존성 |
|------|--------|------|--------|
| sync-all | 매일 04:00 | ✅ | — |
| fetch (외부 수집) | 06:00, 18:00 | ✅ | — |
| daily-synthesis | 매일 10:00 | ✅ | sync-all 완료 후 |

### 4.2 일일 가공 파이프라인 (sync-all.sh)

```
04:00 sync-all
  ├── metadata.json 재빌드 (tags/domain 자동 추출)
  ├── graph_edges.json 재빌드 (허브-스포크 연결)
  ├── scores.json 재빌드 (점수 계산 + index.md 재생성)
  └── 세션 가공 (process-hermes-sessions.sh)
```

### 4.3 외부 수집 (fetch.sh)

- **소스**: Hacker News, GeekNews, AI Frontier
- **출력**: `~/.hermes/knowledge/feeds/` (일일 파일)
- **중복 방지**: url-history.txt 기반

---

## 5. 지식 탐색 워크플로우

### 5.1 LLM 탐색 경로

```
1. 진입점 읽기 (wiki/index.md)
   ↓
2. T1 Core 확인 (작업 필수 지식, 272개)
   ↓
3. 도메인별 인덱스 (domain-*.md, 16개) 또는 태그별 (tag-*.md, 30개)
   ↓
4. 상세 페이지 (pages/*.md)
```

### 5.2 Spec 기반 검색

```
Spec ID → index.md grep → wiki 도메인 파일 grep → _matrix.json 파싱 → jobs-index 검색
```

---

## 6. 핵심 메트릭

| 메트릭 | 값 | 상태 |
|--------|-----|------|
| Wiki 페이지 | 3,651개 | 🟢 |
| Metadata 인덱싱 | 100% | 🟢 |
| Tags 부착률 | 92.8% | 🟢 |
| T1/T2/T3 분포 | 7.4/58.1/34.4% | 🟢 개선됨 |
| 평균 점수 | 0.463 | 🟡 |
| 그래프 에지 | 0 | 🔴 |
| 사용량 추적 | 0 | 🔴 |

---

## 7. 현재 과제도전

### 7.1 그래프 재활성화

- **현황**: 허브 54개 존재하지만 에지 0개
- **원인**: build-graph.sh가 wikilinks 기반 에지를 생성하지 않음
- **해결 방안**: wikilinks ([[Link]]) 자동 파싱 + 허브-스포크 연결 재구축

### 7.2 사용량 추적

- **현황**: .usage.db SQLite는 존재하지만 0회 기록
- **원인**: usage_counter.sh가 실제 wiki 접근 시 호출되지 않음
- **해결 방안**: wiki 페이지 읽기 시 usage counter hook 통합

### 7.3 점수 균일화

- **현황**: 대부분의 점수가 0.34, 0.54, 0.74로 세 가지 값만 존재
- **원인**: priority/recency/usage/hub 가중치가 이산적 값만 생성
- **개선**: 점수 공식에서 더 세분화된 스케일링 적용

---

## 8. 핵심 교훈 (Lessons Learned)

### 8.1 추정치 금지 (JOB-1445)

> 추정치와 실제 파일 수가 최대 86% 차이. `find + wc`로 실제 파일 수 실측 후 계획.

### 8.2 원본 직접 참조 (JOB-1443)

> 원본은 절대 복사/이동/symlink 금지. `source:` 필드에 원본 경로 직접 참조만.

### 8.3 cron 의존성 순서 (JOB-1451)

> process → graph → priority → health 순차 실행 필수. 시간 충돌 분석 필수.

### 8.4 surrogate 문자 (JOB-1447)

> surrogate 문자 감지는 `read_text()` 전에 `md.name`에서 확인. 미리 감지하고 건너뛰기.

### 8.5 점수 계산 ≠ 노출 (JOB-1460)

> 점수/tags/domain 계산만으로는 부족. **노출 구조 **(LLM이 실제로 보는 index)가 핵심.

### 8.6 스크립트 존재 ≠ 자동화 (JOB-1497)

> 항상 `crontab -l` 또는 Hermes cron 목록으로 자동화 상태 확인.

### 8.7 SCHEMA.md 단일 진실 근원 (JOB-1459)

> 지식 시스템 구조는 SCHEMA.md 상단에 정의. 새 세션 진입 시 첫 번째 읽어야 할 파일.

---

## 9. 기술 스택

| 구성 요소 | 도구 |
|-----------|------|
| 검색 | FTS5 (SQLite) |
| 스크립트 | Bash + Python |
| 데이터 형식 | Markdown (위키), JSON (메타데이터), SQLite (사용량) |
| Cron | crontab + Hermes cronjob |
| LLM 가공 | gpt-4o-mini (비용 효율) |
| 원본 수집 | curl + blogwatcher-cli |

---

## 10. 관련 문서

- **SCHEMA.md**: `~/.hermes/knowledge/processed/wiki/SCHEMA.md` — 구조 정의
- **knowledge-navigation 스킬**: `~/.hermes/skills/custom/knowledge-navigation/` — 진입점 + 워크플로우
- **knowledge-system-architecture 스킬**: `~/.hermes/skills/custom/knowledge-system-architecture/` — 아키텍처 상세
- **index.md**: `~/.hermes/knowledge/processed/wiki/index.md` — LLM 카탈로그

---

_이 자료는 2026-06-04 기준 실시간 측정 데이터 기반_
