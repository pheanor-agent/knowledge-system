---
slide_number: 10
label: 계층적 탐색
title: AI 가 지식을 찾는 4 단계 과정
popup_trigger: True
---

## 본문
전체 자료를 무분별하게 읽어오지 않고, 지도 역할을 하는 최상위 파일부터 상세 문서까지 단계적으로 좁혀가며 필요한 정보만 정확히 찾아냅니다.

## 다이어그램
Navigation(탐색 도구 실행) → Index Scan(전체 맵 확인) → Domain Filter(범위 좁히기) → Detail Read(상세 내용 로드)

## 팝업
<h4>Hierarchical Search Protocol</h4>
<p>대용량 DB 쿼리를 대체하는 토큰 최적화 탐색 기법입니다.</p>
<p>최상위 <code>index.md</code> 만 먼저 Context 에 로드하여 도메인 위치를 파악하고, 관심 주제 필터(<code>domain-*.md</code>)를 거친 후, 수 KB 내외의 최종 <code>pages/*.md</code> 만 정밀 판독합니다.</p>
