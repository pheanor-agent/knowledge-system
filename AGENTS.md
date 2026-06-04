# 프로젝트 운영 규칙

## Spec 연동

### Spec 위치
- `specs/active/` — 현재 유효한 Spec
- `specs/history/` — 변경 이력
- `specs/_index.yaml` — Spec 인덱스
- `specs/_matrix.json` — Traceability Matrix

### Spec 생성
```bash
bash ~/.hermes/skills/software-development/spec-driven-dev/scripts/spec-create.sh <slug> <type> <title>
```

### 구조 검증
```bash
bash ~/.hermes/skills/software-development/spec-driven-dev/scripts/validate-project.sh <slug>
```

## Git 정책

### 브랜치 전략
- `main` — 안정 버전 (보호 브랜치)
- `feature/SPEC-XXX` —新功能 개발
- `fix/SPEC-XXX` — 버그 수정
- `spec/SPEC-XXX` — Spec 변경 전용

### Commit 컨벤션
```
<type>(SPEC-XXX): <message>
```

| Type | 용도 |
|------|------|
| `spec` | Spec 추가/수정 |
| `feat` |新功能 구현 |
| `fix` | 버그 수정 |
| `test` | 테스트 추가/수정 |
| `refactor` | 코드 리팩토링 |

## Hermes Workflow 연동

JOB-XXXX/request.md → specs/ 참조
JOB-XXXX/execution.md → Spec ID 기반 작업 기록
