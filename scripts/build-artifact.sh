#!/bin/bash
# scripts/build-artifact.sh
# Spec 기반 HTML Artifact 빌드 스크립트

SPEC_DIR="specs/content"
OUTPUT_DIR="docs/versions"
SPEC_FILE="specs/active/components/slide-structure.md"

echo "=== Artifact 빌드 시작 ==="

# 1. Spec 버전 읽기
SPEC_VERSION=$(grep "version:" ${SPEC_FILE} | head -1 | awk '{print $2}')
if [ -z "${SPEC_VERSION}" ]; then
    echo "❌ FAIL: SPEC-B7 버전 정보 없음"
    exit 1
fi
echo "[1/4] Spec 버전: ${SPEC_VERSION}"

# 2. 검증 실행
echo "[2/4] 검증 실행..."
bash scripts/validate-specs.sh
if [ $? -ne 0 ]; then
    echo "❌ FAIL: 검증 실패 - 빌드 중단"
    exit 1
fi

# 3. HTML 생성
echo "[3/4] HTML 생성..."
python3 scripts/generate-slides.py --output docs/slides.html
if [ $? -ne 0 ]; then
    echo "❌ FAIL: HTML 생성 실패"
    exit 1
fi

# 4. 버전 파일 복사 및 CHANGELOG 업데이트
mkdir -p ${OUTPUT_DIR}
cp docs/slides.html ${OUTPUT_DIR}/v${SPEC_VERSION}.html
echo "[4/4] 버전 파일 저장: ${OUTPUT_DIR}/v${SPEC_VERSION}.html"

# CHANGELOG 업데이트
echo "" >> docs/versions/CHANGELOG.md
echo "## v${SPEC_VERSION} ($(date '+%Y-%m-%d %H:%M'))" >> docs/versions/CHANGELOG.md
echo "- Gemini 제안사항 반영 (Lost in the Middle, 컴파일 워크플로우, Decay 함수)" >> docs/versions/CHANGELOG.md
echo "- Spec-Driven 시스템 정상화 (구버전 아카이브, 검증 루프 강제)" >> docs/versions/CHANGELOG.md

echo ""
echo "=== 빌드 완료: SUCCESS ==="
echo "   생성 파일: docs/slides.html, ${OUTPUT_DIR}/v${SPEC_VERSION}.html"
exit 0
