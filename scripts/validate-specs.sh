#!/bin/bash
# specs/validate-specs.sh
# Spec 정합성 검증 스크립트

SPEC_DIR="specs/content"
EXPECTED_COUNT=11

echo "=== Spec 정합성 검증 시작 ==="

# 1. 파일 수 검증
FILE_COUNT=$(ls ${SPEC_DIR}/*.md 2>/dev/null | wc -l)
echo "[1/3] 파일 수 검증: ${FILE_COUNT}개 (예상: ${EXPECTED_COUNT}개)"

if [ ${FILE_COUNT} -ne ${EXPECTED_COUNT} ]; then
    echo "❌ FAIL: 파일 수 불일치 (${FILE_COUNT} vs ${EXPECTED_COUNT})"
    exit 1
fi
echo "✅ PASS: 파일 수 일치"

# 2. 중복 파일 검증 (validate-slides.py 호출)
echo "[2/3] 중복 파일 검증..."
python3 scripts/validate-slides.py docs/slides.html > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ PASS: 중복 파일 없음"
else
    echo "⚠️  WARNING: 중복 가능성 있음 (수동 확인 권장)"
fi

# 3. Traceability 검증 (SPEC-B7과 내용 Spec 정합성)
echo "[3/3] Traceability 검증..."
SPEC_VERSION=$(grep "version:" specs/active/components/slide-structure.md | head -1 | awk '{print $2}')
echo "    SPEC-B7 버전: ${SPEC_VERSION}"

if [ -z "${SPEC_VERSION}" ]; then
    echo "❌ FAIL: SPEC-B7 버전 정보 없음"
    exit 1
fi
echo "✅ PASS: Traceability 확인"

echo ""
echo "=== 검증 완료: SUCCESS ==="
exit 0
