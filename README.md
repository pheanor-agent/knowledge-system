# 지식 시스템 (Knowledge System)

Karpathy 3계층 구조 기반 개인 AI 에이전트 지식 관리 시스템.

## 프로젝트 구조

```
knowledge-system/
├── specs/                  # Spec (단일 진실 근원)
│   ├── active/             # 현재 유효한 Spec
│   │   ├── architecture.md # SPEC-O1: 전체 아키텍처
│   │   ├── components/     # SPEC-B1~B5: 컴포넌트
│   │   └── interfaces/     # SPEC-C1: 인터페이스
│   ├── _index.yaml         # Spec 인덱스
│   ├── _matrix.json        # Traceability Matrix
│   └── history/            # 변경 이력
├── docs/                   # 문서
│   ├── README.md           # 기존 기술 문서
│   ├── seminar.md          # 세미나 자료 (Markdown)
│   ├── architecture.html   # 아키텍처 다이어그램
│   └── slides.html         # 슬라이드 프레젠테이션
├── src/                    # 소스 코드
├── tests/                  # 테스트
└── site/                   # GitHub Pages 배포용
    └── index.html → ../docs/slides.html
```

## Spec 목록

| Spec ID | 유형 | 제목 | 상태 |
|---------|------|------|------|
| SPEC-O1 | architecture | 지식 시스템 아키텍처 | ✅ |
| SPEC-B1 | component | 원본 수집 | ✅ |
| SPEC-B2 | component | 지식 가공 파이프라인 | ✅ |
| SPEC-B3 | component | 메타데이터 관리 | ✅ |
| SPEC-B4 | component | 그래프 및 중요도 | ✅ |
| SPEC-B5 | component | 인덱스 및 노출 구조 | ✅ |
| SPEC-C1 | interface | 지식 시스템 인터페이스 | ✅ |

## 문서

- **세미나 자료**: [docs/seminar.md](docs/seminar.md)
- **아키텍처 다이어그램**: [docs/architecture.html](docs/architecture.html)
- **슬라이드 프레젠테이션**: [docs/slides.html](docs/slides.html)

## GitHub Pages 배포

```bash
# site/ 브랜치로 푸시
git checkout --orphan gh-pages
git rm -rf .
cp -r site/* .
git add .
git commit -m "gh-pages: 세미나 슬라이드"
git push origin gh-pages
```

배포 URL: `https://<username>.github.io/knowledge-system/`

## runtime 위치

실제 지식 시스템은 아래 위치에서 동작:

```
~/.hermes/knowledge/
├── processed/wiki/     # Wiki 페이지 (3,651개)
├── pipeline/           # 스크립트 + status.json
└── synthesis/          # 일일/주간 요약
```
