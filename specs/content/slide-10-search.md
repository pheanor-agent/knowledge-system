---
slide_number: 10
label: 계층적 탐색
title: AI 가 지식을 찾는 4 단계 과정
---

## 본문
전체 자료를 무분별하게 읽어오지 않고, 지도 역할을 하는 최상위 파일부터 상세 문서까지 단계적으로 좁혀갑니다.
Navigation → Index Scan → Domain Filter → Detail Read

## 다이어그램
Navigation(탐색 도구 실행) → Index Scan(전체 맵 확인) → Domain Filter(범위 좁히기) → Detail Read(상세 내용 로드)

## 팝업
- **Hierarchical Search Protocol**: 대용량 DB 쿼리를 대체하는 토큰 최적화 탐색 기법입니다. 최상위 Index 만 먼저 로드하여 도메인을 파악한 후, 수 KB 내외의 최종 페이지만 정밀 판독합니다.
