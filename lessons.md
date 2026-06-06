

### [Infra] GitHub Pages 정적 배포 시 Jekyll 빌드 충돌 해결 (2026-06-05)
- **현상**: HTML 푸시 후 배포가 반영되지 않고 구버전이 서빙됨.
- **원인**: GitHub Pages의 기본 Jekyll 빌더가 프로젝트 내 특정 폴더 구조와 충돌하여 빌드 실패 $ightarrow$ 구버전 롤백 서빙.
- **해결**: 프로젝트 루트에 `.nojekyll` 파일 추가 $ightarrow$ Jekyll 빌드 단계 스킵 $ightarrow$ 순수 정적 파일 서빙 강제.
- **교훈**: 
    1. 순수 HTML/CSS/JS 배포 시 반드시 `.nojekyll` 파일을 기본으로 포함할 것.
    2. 배포 반영이 안 될 경우, 단순히 푸시 확인만 하지 말고 `gh run list`를 통해 GitHub Actions의 빌드 성공 여부를 확인할 것.
