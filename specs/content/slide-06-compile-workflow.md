---
slide_number: 6
label: 컴파일 워크플로우
title: 지식을 파일로 저장하는 3 단계 과정
popup_trigger: True
---

## 본문
대화가 종료되면 의미 있는 정보를 식별하여 분리하고, 연관성을 찾아 묶어준 뒤, 규칙에 맞게 다듬습니다.

## 다이어그램
Ingest(지식 추출) → Link(관계 연결) → Lint(무결성 검증)

## 팝업
<h4>Knowledge Compile Workflow</h4>
<p><strong>1. Ingest:</strong> 대화 세션 종료 후 Background Prompt 를 통해 핵심 정보를 JSON 이나 Markdown 포맷으로 적출합니다.<br>
<strong>2. Link:</strong> 기존 Index 를 스캔하여 교차 참조가 필요한 키워드에 [[문서명]] 형태의 Wiki-links 를 자동 생성합니다.<br>
<strong>3. Lint:</strong> 신규 지식이 기존 Schema 규칙과 Hallucination 모순을 일으키지 않는지 검증하고 버전을 병합합니다.</p>
