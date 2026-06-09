# 슬라이드 버전 관리

---
spec_id: SPEC-B6
version: v1.0
status: verified
priority: P1
category: 버전 관리
related_specs: []
code_refs: []
test_refs: []
job_refs:
  - "JOB-1503"
  - "JOB-1504"
  - "JOB-1506"
  - "JOB-1510"
  - "JOB-1511"
created: 2026-06-04
updated: 2026-06-04
---

### [SPEC-B6] 슬라이드 버전 관리

**설명**: 세미나 슬라이드의 버전 이력 관리 및 배포 규격. Git + 폴더 구조 기반.

## 버전 번호링 규칙

### 포맷
```
v{주}.{부}-{설명}
```

### 예시
- `v1.0-initial`: 초안 생성
- `v1.1-redesign`: 슬라이드 리디자인
- `v1.2-popup`: 팝업 기능 도입
- `v1.3-white-bg`: 흰색 배경 디자인
- `v1.4-feedback`: 피드백 반영
- `v1.5-diagram`: 다이어그램 추가

### 주/부 버전 구분
| 버전 | 변경 유형 | 예시 |
|------|-----------|------|
| 주 버전 | 대폭 변경 | v2.0 - 전체 리뉴얼 |
| 부 버전 | 소폭 변경 | v1.1 - 슬라이드 추가/수정 |

## 저장 구조

### 폴더 구조
```
docs/
  slides.html                 (최신 버전 - gh-pages 배포용)
  versions/
    v1.0-initial.html         (버전별 파일)
    v1.1-redesign.html
    ...
    CHANGELOG.md              (변경 이력)
    FEEDBACK.md               (피드백 이력)
```

### 파일 역할
| 파일 | 역할 | 업데이트 시기 |
|------|------|---------------|
| `docs/slides.html` | 최신 버전 | 매 변경 시 |
| `docs/versions/v{주}.{부}-{설명}.html` | 버전별 파일 | 버전 생성 시 |
| `docs/versions/CHANGELOG.md` | 변경 이력 | 매 변경 시 |
| `docs/versions/FEEDBACK.md` | 피드백 이력 | 피드백 수신 시 |

## 워크플로우

### 버전 생성 프로세스
```
1. 리비전 요청
   ↓
2. docs/slides.html 수정
   ↓
3. docs/versions/v{주}.{부}-{설명}.html 생성
   ↓
4. CHANGELOG.md 갱신
   ↓
5. FEEDBACK.md 갱신 (피드백 반영 시)
   ↓
6. git add + git commit
   ↓
7. git push origin main
   ↓
8. gh-pages 업데이트
```

### Git 커밋 컨벤션
```
feat: v{주}.{부} {설명}

예시:
feat: v1.5 다이어그램 추가 + 페이지 분리 + 내용 연결
```

## 변경 이력 관리

### CHANGELOG.md 구조
```markdown
# 슬라이드 변경 이력

## v1.5-diagram (2026-06-04)
- 다이어그램 추가: 5 개 슬라이드
- 페이지 분리: 신입사원 예시와 AI 내용 분리
- 내용 연결: 점수 → 중요도 로직 연결
```

### FEEDBACK.md 구조
```markdown
# 피드백 이력

## v1.5-diagram (2026-06-04)
- 다이어그램 추가 요청
- 페이지 분리 요청
- 내용 연결 요청
```

## 배포

### gh-pages 브랜치
- `docs/slides.html` → `gh-pages/index.html`
- 최신 버전만 배포

### 배포 프로세스
```bash
# gh-pages 업데이트
git checkout gh-pages
git rm -rf .
cp docs/slides.html index.html
git add index.html
git commit -m "feat: v{주}.{부} 배포"
git push origin gh-pages --force
git checkout main
```

## 검증 기준

- [x] 버전 번호링 규칙 정의
- [x] 저장 구조 정의
- [x] 워크플로우 정의
- [x] 변경 이력 관리 정의
- [x] 배포 프로세스 정의
- [ ] 실제 버전 생성 테스트
- [ ] CHANGELOG.md 검증
- [ ] FEEDBACK.md 검증

**Traceability**:
- 코드: —
- 테스트: —
- JOB: JOB-1503/1504/1506/1510/1511
