---
slide_number: 2
label: 문제
title: 왜 AI 에게 파일이 필요한가요?
popup_trigger: True
---

## 본문
에이전트에게 무조건 많은 정보를 한 번에 주입하면 부작용이 발생합니다.
자료가 방대해질수록 정작 중요한 지시 사항은 망각하게 되며 효율성이 급감합니다.
이를 해결하기 위해 물리적인 파일 형태의 선택적 기억 장치가 필요합니다.

## 다이어그램
(없음)

## 팝업
<h4>Context Bloat & Lost in the Middle</h4>
<p>LLM 은 Context Window 가 길어질수록 중앙부(Middle)의 Attention 가중치가 하락하여 핵심 지시 사항을 누락하는 <strong>Lost in the Middle</strong> 현상이 발생합니다.</p>
<p>또한 매 대화 턴마다 불필요한 과거 이력을 전부 포함하면 Token Cost Inflation 이 유발되므로, 필요한 정보만 필터링하여 로딩하는 시스템이 필수적입니다.</p>
