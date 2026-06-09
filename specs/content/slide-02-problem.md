---
slide_number: 2
label: 문제
title: 왜 AI 에게 파일이 필요한가요?
---

## 본문
에이전트에게 무조건 많은 정보를 한 번에 주입하면 부작용이 발생합니다.
Context Bloat 와 Lost in the Middle 현상이 발생하여 효율성이 급감합니다.
이를 해결하기 위해 물리적인 파일 형태의 선택적 기억 장치가 필요합니다.

## 다이어그램
(없음)

## 팝업
- **Context Bloat**: 매 대화 턴마다 불필요한 과거 이력을 전부 포함하면 Token Cost Inflation 이 유발되는 현상입니다.
- **Lost in the Middle**: LLM 의 Context Window 가 길어질수록 중앙부의 Attention 가중치가 하락하여 핵심 지시 사항을 누락하는 현상입니다.
