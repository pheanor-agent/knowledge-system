---
slide_number: 8
label: 중요도
title: 동적 점수에 따른 3 단계 분류
popup_trigger: True
---

## 본문
T1: 항상 참조해야 하는 핵심 행동 규칙
T2: 특정 상황에 직면했을 때 꺼내보는 일상 지식
T3: 요청이 있을 때만 제공되는 보조 배경 정보

## 다이어그램
Score 계산(다중 변수 종합) → Tier 배정(T1/T2/T3) → Context 로딩(전략적 배치)

## 팝업
<h4>Scoring Logic & Mathematical Decay</h4>
<p><strong>Score Formula:</strong><br><code>Score = (0.3 × Priority) + (0.2 × Recency) + (0.3 × Usage) + (0.1 × Hub)</code></p>
<p><strong>Recency Decay (감가상각 알고리즘):</strong><br><code>Recency = e<sup>-λ·t</strong></code><br>(t: 마지막 접근 후 경과 시간, λ: Decay constant)</p>
<p>90일 이상 미사용 시 최하점(0.3)으로 수렴하도록 설계하여 불필요한 Context 의 메모리 점유를 수학적으로 방지합니다.</p>
