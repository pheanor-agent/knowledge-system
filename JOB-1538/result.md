

## 🚩 배포 트러블슈팅 (Deployment Issue)

**문제 상황**:
- `gh-pages` 브랜치에 최신 `index.html`을 푸시했음에도 브라우저에서 구버전(v1.6)이 계속 서빙됨.
- `git push`는 성공했으나 실제 반영이 되지 않는 현상 발생.

**원인 분석**:
- GitHub Pages의 기본 설정이 모든 리포지토리를 **Jekyll 사이트**로 인식하여 자동 빌드 파이프라인을 실행함.
- 빌드 과정 중 `/github/workspace/specs/templates` 경로를 찾지 못해 `Errno::ENOENT` 에러가 발생하며 빌드가 실패(`failure`)함.
- 빌드가 실패하면 GitHub Pages는 안전을 위해 **마지막으로 성공한 빌드 버전(구버전)**을 계속 서빙함.

**해결 방법**:
- 루트 경로에 `.nojekyll` 파일 생성.
- GitHub Pages에게 Jekyll 빌드 과정을 완전히 건너뛰고 정적 파일을 그대로 서빙하도록 강제함.

**결과**:
- 빌드 에러 제거 및 정적 파일 즉시 배포 성공.
