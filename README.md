# 지식 시스템

## 개요

지식 시스템 프로젝트

## 구조

```
specs/                  # Spec 중앙 관리
├── active/             # 현재 유효한 Spec
├── history/            # 변경 이력
├── templates/          # 템플릿
├── _index.yaml         # Spec 인덱스
└── _matrix.json        # Traceability Matrix
src/                    # 소스 코드
tests/                  # 테스트
docs/                   # 보조 문서
scripts/spec/           # Spec 도구
```

## 진입점

### Spec 생성
```bash
bash ~/.hermes/scripts/spec/spec-create.sh knowledge-system <type> <title>
```

### 구조 검증
```bash
bash ~/.hermes/scripts/project/validate-project.sh knowledge-system
```

### 영향 분석
```bash
bash ~/.hermes/scripts/spec/spec-impact.sh knowledge-system <spec-id>
```
