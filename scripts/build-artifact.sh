#!/bin/bash
# scripts/build-artifact.sh
# Spec 기반 HTML Artifact 빌드 스크립트

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPEC_DIR="specs/content"
OUTPUT_DIR="docs/versions"
SPEC_FILE="specs/active/components/slide-structure.md"
CHANGELOG_FILE="specs/history/CHANGELOG.md"
SKILL_DIR="$HOME/.hermes/skills/software-development/spec-driven-dev/scripts"

echo "=== Artifact 빌드 시작 ==="

# 1. Spec 버전 읽기
SPEC_VERSION=$(grep "version:" ${SPEC_FILE} | head -1 | awk '{print $2}')
if [ -z "${SPEC_VERSION}" ]; then
    echo "❌ FAIL: SPEC-B7 버전 정보 없음"
    exit 1
fi
echo "[1/5] Spec 버전: ${SPEC_VERSION}"

# 2. 검증 실행
echo "[2/5] 검증 실행..."
bash scripts/validate-specs.sh
if [ $? -ne 0 ]; then
    echo "❌ FAIL: 검증 실패 - 빌드 중단"
    exit 1
fi

# 3. HTML 생성 (메타데이터 자동 갱신 포함)
echo "[3/5] HTML 생성..."
python3 scripts/generate-slides.py --output docs/slides.html
if [ $? -ne 0 ]; then
    echo "❌ FAIL: HTML 생성 실패"
    exit 1
fi

# 버전 파일 복사 (v 중복 방지)
VERSION_SLUG=${SPEC_VERSION#v}  # 'v' 접두사 제거
mkdir -p ${OUTPUT_DIR}
cp docs/slides.html ${OUTPUT_DIR}/v${VERSION_SLUG}.html
echo "[4/5] 버전 파일 저장: ${OUTPUT_DIR}/v${VERSION_SLUG}.html"

# 5. 자동 CHANGELOG 생성
echo "[5/5] CHANGELOG 생성..."
mkdir -p specs/history

TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
BUILD_AT=$(date -Iseconds)

# 변경된 파일 수집 (최신 수정 파일 기반)
CHANGES=""
for f in $(find specs/active specs/content -name "*.md" -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -10 | awk '{print $2}'); do
    fname=$(basename "$f")
    mtime=$(date -r "$f" '+%Y-%m-%d %H:%M' 2>/dev/null || echo "unknown")
    CHANGES="${CHANGES}  - ${fname} (${mtime})\n"
done

# CHANGELOG 엔트리 작성
ENTRY="## ${SPEC_VERSION} (${TIMESTAMP})

### 빌드 정보
- 빌드 시간: ${BUILD_AT}
- 트리거: build-artifact.sh

### 변경 사항
$(echo -e "$CHANGES")
---
"

# 파일 존재 시 append, 없으면 생성
if [ ! -f "${CHANGELOG_FILE}" ]; then
    echo "# CHANGELOG" > "${CHANGELOG_FILE}"
    echo "" >> "${CHANGELOG_FILE}"
    echo "모든 변경 사항이 타임라인 순서로 기록됩니다." >> "${CHANGELOG_FILE}"
    echo "" >> "${CHANGELOG_FILE}"
fi

echo "$ENTRY" >> "${CHANGELOG_FILE}"
echo "  ✅ CHANGELOG 업데이트: ${CHANGELOG_FILE}"

echo ""
echo "=== 빌드 완료: SUCCESS ==="
echo "   생성 파일: docs/slides.html, ${OUTPUT_DIR}/v${VERSION_SLUG}.html"
echo "   CHANGELOG: ${CHANGELOG_FILE}"
exit 0
