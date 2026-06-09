---
spec_id: SPEC-B7
version: v2.0
status: active
priority: P1
category: 슬라이드 구성
related_specs: []
code_refs: []
test_refs: []
job_refs:
  - "JOB-1553"
created: 2026-06-04
updated: 2026-06-09
---

# 슬라이드 구성 규격 v2.0

## 디자인 토큰 (Stripe/Linear 스타일)

```css
:root {
  --bg: #ffffff;
  --bg-card: #f9fafb;
  --border: #e5e7eb;
  --text: #1a1a1a;
  --text-dim: #666666;
  --text-bright: #000000;
  --accent: #2563eb;
  --accent-dim: rgba(37,99,235,0.1);
  --gradient-start: #6366f1;
  --gradient-end: #8b5cf6;
}
```

## 슬라이드 목록

| # | 제목 | 라벨 | 레이아웃 |
|---|------|------|----------|
| 1 | AI 에게 기억을 선물하다 | 에이전트 메모리 시스템 | Cover |
| 2 | 왜 AI 에게 파일이 필요한가요? | 문제 | Diagram+Cards |
| 3 | 신입사원이 배우는 3 가지 지식 관리 방법 | 비유 | 3-Card Grid |
| 4 | 신입사원이 배우듯, AI 도 3 가지 방식을 활용합니다 | AI 의 3 층 기억 | Hierarchy Diagram |
| 5 | 에이전트 메모리 시스템 | 시스템 개요 | Flow Chart |
| 6 | 지식을 파일로 저장하는 3 단계 과정 | 컴파일 워크플로우 | 3-Step Diagram |
| 7 | 자동으로 파일을 정리하는 과정 | 자동화 | Pipeline Diagram |
| 8 | 동적 점수에 따른 3 단계 분류 | 중요도 | Tier Cards (T1/T2/T3) |
| 9 | 지식을 주제별로 분류하는 체계 | 주제 분류 | Tag Cloud+Tree |
| 10 | AI 가 지식을 찾는 4 단계 과정 | 계층적 탐색 | Tree Diagram |
| 11 | 세미나 완료 | Thank You | Closing |

## 다이어그램 규칙

### 필수 사용
- **순차적 동작**: 화살표 플로우 (Step 1 → Step 2 → Step 3)
- **분류적 동작**: 컬러 코딩 카드 (T1/T2/T3)
- **계층적 구조**: 트리 다이어그램 (L1→L2→L3)

### 옵션 사용
- 단순 설명: 텍스트+아이콘

## 팝업 규칙

### 확장 내용
- **코드 예시**: 실제 명령어, JSON 구조
- **파일 구조**: 디렉토리 트리 시각화
- **수식/알고리즘**: 점수 계산, 감가상각 로직

### 트리거
- 본문 내 키워드 최초 등장 지점에 `?` 아이콘
- 슬라이드당 동일 키워드 1회만

## 내용 작성 규칙

### 슬라이드당 분량
- **최소**: 200자
- **최대**: 800자 (다이어그램 제외)
- **팝업**: 400-800자

### Tip 배지
- 💡Tip: 기술 용어 평어 설명
- 슬라이드 하단 배치
- 본문과 중복 금지

## 검증 기준
- **자동**: 텍스트 유사도 80% 이상 → 경고
- **수동**: 작성자/리뷰어 확인
- **일관성**: Spec ↔ HTML 일치
