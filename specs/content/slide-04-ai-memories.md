---
slide_number: 4
label: AI 의 3 층 기억
title: 신입사원이 배우듯, AI 도 3 가지 방식을 활용합니다
---

## 본문
1. 사전 학습 모델 (Model Training): 변경 불가한 고정 지식.
2. 에이전트 메모리 (File System): 실시간으로 추가되는 개인 메모리.
3. 문서 참조 (Retrieval-Augmented Generation): 외부 연동되는 참조 자료.

오늘은 2 번 '에이전트 메모리' 에 해당하는 파일 기반 지식 시스템을 다룹니다.

## 다이어그램
(없음)

## 팝업
- **Pre-trained Data**: 모델 학습 단계에서 습득한 지식으로, 변경이 불가능하며 전역적인 상식으로 작용합니다.
- **Agent Storage**: 에이전트가 실시간으로 기록하는 개인 메모리로, 파일 시스템 기반으로 관리됩니다.
- **Document Database**: 외부 문서 저장소로, RAG 를 통해 필요 시 검색하여 참조합니다.
