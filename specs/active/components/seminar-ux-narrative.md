# Seminar UX & Narrative Specification

---
spec_id: SPEC-B8
version: v1.0
status: active
priority: P1
category: 세미나 UX/서사
related_specs:
  - "SPEC-B7"  # 슬라이드 구성 규격
code_refs: []
test_refs: []
job_refs:
  - "JOB-1538"
  - "JOB-1539"
  - "JOB-1543"
---

## 1. Narrative Arc (서사 구조)

본 세미나 자료는 기술적 구현 나열이 아닌, **"왜 이 시스템이 필요한가"**에서 시작하여 **"어떤 가치를 제공하는가"**로 끝나는 서사 구조를 따릅니다.

| 단계 | 슬라이드 | 목적 | 핵심 메시지 | UX 전략 |
|:---:|:---:|---|---|---|
| **Problem** | 1-2 | 공감대 형성 | LLM의 Context Bloat와 망각 문제 | 문제의 심각성 강조 (팝업으로 기술적 근거 제시) |
| **Analogy** | 3-4 | 개념 전이 | 인간의 학습 방식 $\rightarrow$ AI의 기억 구조 | 익숙한 비유를 통해 진입 장벽 완화 |
| **Solution** | 5-6 | 해결책 제시 | 경험 $\rightarrow$ 가공 $\rightarrow$ 구조화된 지식 | 시각적 흐름도 중심의 단순한 설명 |
| **Detail** | 7-9 | 시스템 신뢰성 | 주기적 관리와 동적 우선순위 | 카드 레이아웃과 색상 코딩으로 체계성 강조 |
| **Value** | 10-11 | 실무적 이득 | 토큰 최적화 및 정밀 탐색 (Funnel) | 결과물의 효율성(Speed/Accuracy) 강조 |

---

## 2. UX & Interaction Design

### 2.1 Contextual Popups (맥락적 팝업)
- **원칙**: 팝업 트리거는 사용자가 "이게 정확히 뭐지?"라고 느끼는 **최초의 지점**에 배치한다.
- **배치 금지**: 페이지 제목(`h2`)에 일괄 배치하는 것을 금지함.
- **배치 권장**:
  - 다이어그램 내의 특정 노드 (예: `Assess` 노드 $\rightarrow$ 점수 계산 공식 팝업)
  - 카드 내의 핵심 기술 용어 (예: `RAG` $\rightarrow$ RAG 정의 팝업)
  - 복잡한 수식의 변수 (예: `λ` $\rightarrow$ Decay constant 설명 팝업)

### 2.2 Visual Metaphors (시각적 은유)
- **Hierarchical Search (Funnel)**:
  - 단순한 화살표 나열이 아닌, 위에서 아래로 갈수록 폭이 좁아지는 **역삼각형(Funnel)** 구조로 시각화.
  - `Global Index` (가장 넓음) $\rightarrow$ `Domain Filter` $\rightarrow$ `Detail Document` (가장 좁음).
- **Priority Coding**:
  - 중요도에 따른 색상 고정: `Rose (T1)` $\rightarrow$ `Amber (T2)` $\rightarrow$ `Green (T3)`.

---

## 3. Logical Pipeline Specification

### 3.1 Synchronous: Knowledge Storage (저장 시점)
사용자가 정보를 입력하거나 세션이 종료되어 지식을 저장하는 **동기적 흐름**입니다.

**흐름**: `Ingest` $\rightarrow$ `Link` $\rightarrow$ `Assess`
1. **Ingest (추출)**: Raw 데이터에서 핵심 정보 추출.
2. **Link (연결)**: 기존 지식과의 관계 생성 (Wiki-links).
3. **Assess (중요도 판정)**: **[Critical]** 저장 즉시 해당 지식의 초기 중요도(Priority)를 판정하여 저장.

### 3.2 Asynchronous: Knowledge Maintenance (유지보수 시점)
시스템이 백그라운드에서 지식의 무결성을 유지하는 **비동기적/주기적 흐름**입니다.

**흐름**: `Sync` $\rightarrow$ `Lint` $\rightarrow$ `Decay`
1. **Sync (동기화)**: 원본 소스와 위키 간의 상태 동기화.
2. **Lint (검증)**: **[Critical]** 지식 간의 모순, 중복, SCHEMA 위반 사항을 전수 조사하여 수정.
3. **Decay (감가상각)**: 사용 빈도와 경과 시간에 따라 점수를 갱신하여 불필요한 지식의 우선순위를 하향 조정.

---

## 4. Content Constraints (청중 중심)

- **Language**: 기술 용어는 영어, 설명은 한글.
- **Density**: 슬라이드당 1개 핵심 개념, 텍스트 400자 미만.
- **Instruction**: "해야 한다" 등의 명령형 배제, 시스템의 동작 원리를 설명하는 서술형 사용.
