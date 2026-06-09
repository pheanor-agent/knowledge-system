#!/bin/bash
# specs/validate-specs.sh
# Spec 정합성 검증 스크립트

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ACTIVE_DIR="${PROJECT_DIR}/specs/active"
CONTENT_DIR="${PROJECT_DIR}/specs/content"
INDEX_FILE="${PROJECT_DIR}/specs/_index.yaml"

REQUIRED_COUNT=11
PASS=0
FAIL=0
WARN=0

check_pass() { echo "✅ $1"; PASS=$((PASS + 1)); }
check_fail() { echo "❌ $1"; FAIL=$((FAIL + 1)); }
check_warn() { echo "⚠️  $1"; WARN=$((WARN + 1)); }

echo "=== Spec 정합성 검증 시작 ==="

# ──────────────────────────────────────────────
# 1. Content 파일 수 검증
# ──────────────────────────────────────────────
echo ""
echo "[1/5] Content 파일 수 검증..."
FILE_COUNT=$(ls ${CONTENT_DIR}/*.md 2>/dev/null | wc -l)
echo "    발견: ${FILE_COUNT}개 (예상: ${REQUIRED_COUNT}개)"

if [ ${FILE_COUNT} -ne ${REQUIRED_COUNT} ]; then
    check_fail "파일 수 불일치 (${FILE_COUNT} vs ${REQUIRED_COUNT})"
    exit 1
fi
check_pass "파일 수 일치 (${FILE_COUNT}개)"

# ──────────────────────────────────────────────
# 2. Active Spec 필수 메타데이터 검증 (Strict)
# ──────────────────────────────────────────────
echo ""
echo "[2/5] Active Spec 필수 메타데이터 검증..."

ACTIVE_SPEC_COUNT=0
for spec_file in $(find "${ACTIVE_DIR}" -name "*.md" 2>/dev/null | sort); do
    ACTIVE_SPEC_COUNT=$((ACTIVE_SPEC_COUNT + 1))
    fname=$(basename "$spec_file")
    
    # YAML frontmatter 추출 (--- 사이에 있는 부분)
    metadata=$(sed -n '/^---$/,/^---$/p' "$spec_file" | sed '1d;$d')
    
    # 필수 필드 확인
    for field in spec_id version status; do
        if ! echo "$metadata" | grep -q "^${field}:"; then
            check_fail "${fname} — '${field}' 필드 누락"
        else
            val=$(echo "$metadata" | grep "^${field}:" | awk '{print $2}')
            # spec_id 형식 검증 (SPEC-XX 패턴)
            if [ "$field" = "spec_id" ]; then
                if ! echo "$val" | grep -qP "^SPEC-[A-Z]\d+$"; then
                    check_warn "${fname} — spec_id 형식 의심: ${val} (예상: SPEC-XX)"
                else
                    check_pass "${fname} — spec_id: ${val}"
                fi
            elif [ "$field" = "version" ]; then
                if ! echo "$val" | grep -qP "^v\d+\.\d+$"; then
                    check_warn "${fname} — version 형식 의심: ${val} (예상: vX.Y)"
                fi
            fi
        fi
    done
done

if [ ${ACTIVE_SPEC_COUNT} -eq 0 ]; then
    check_fail "Active Spec 파일이 없음"
else
    check_pass "Active Spec 검증 완료 (${ACTIVE_SPEC_COUNT}개)"
fi

# ──────────────────────────────────────────────
# 3. Content 파일 slide_number 중복 검증
# ──────────────────────────────────────────────
echo ""
echo "[3/5] Content slide_number 중복 검증..."

NUMBERS=$(grep -h "^slide_number:" ${CONTENT_DIR}/*.md 2>/dev/null | awk '{print $2}' | sort -n)
DUPS=$(echo "$NUMBERS" | uniq -d)

if [ -n "$DUPS" ]; then
    check_fail "slide_number 중복: ${DUPS}"
else
    UNIQUE=$(echo "$NUMBERS" | wc -w)
    check_pass "slide_number 고유성 확인 (${UNIQUE}개)"
fi

# ──────────────────────────────────────────────
# 4. Spec ID 중복 검증 (_index.yaml vs active)
# ──────────────────────────────────────────────
echo ""
echo "[4/5] Spec ID 중복 검증..."

# active 디렉토리에서 수집한 spec_id들
ACTIVE_IDS=$(grep -rh "^spec_id:" "${ACTIVE_DIR}/" 2>/dev/null | awk '{print $2}' | sort -u)
INDEX_IDS=$(grep -P "spec_id:" "${INDEX_FILE}" 2>/dev/null | awk '{print $NF}' | sort -u || echo "")

# active ID들이 index에 모두 등록되어 있는지 확인
for id in $ACTIVE_IDS; do
    if ! echo "$INDEX_IDS" | grep -q "^${id}$"; then
        check_warn "Spec ${id} — _index.yaml에 미등록"
    fi
done

# 중복 spec_id 확인
DUP_IDS=$(echo "$ACTIVE_IDS" | uniq -d)
if [ -n "$DUP_IDS" ]; then
    check_fail "중복 spec_id: ${DUP_IDS}"
else
    check_pass "Spec ID 중복 없음"
fi

# ──────────────────────────────────────────────
# 5. Traceability 검증 (SPEC-B7 버전 확인)
# ──────────────────────────────────────────────
echo ""
echo "[5/5] Traceability 검증..."

SPEC_B7_FILE=$(find "${ACTIVE_DIR}" -name "*.md" -exec grep -l "SPEC-B7" {} \; 2>/dev/null | head -1)
if [ -n "$SPEC_B7_FILE" ]; then
    SPEC_VERSION=$(grep "^version:" "$SPEC_B7_FILE" | head -1 | awk '{print $2}')
    if [ -n "$SPEC_VERSION" ]; then
        check_pass "SPEC-B7 버전: ${SPEC_VERSION}"
    else
        check_fail "SPEC-B7 버전 정보 없음"
    fi
else
    check_fail "SPEC-B7 파일 못 찾음"
fi

# ──────────────────────────────────────────────
# 결과 요약
# ──────────────────────────────────────────────
echo ""
echo "=== 검증 완료 ==="
echo "✅ PASS: ${PASS} | ❌ FAIL: ${FAIL} | ⚠️  WARN: ${WARN}"

if [ ${FAIL} -gt 0 ]; then
    echo "STATUS: FAILED"
    exit 1
fi

if [ ${WARN} -gt 0 ]; then
    echo "STATUS: PASSED (경고 ${WARN}개)"
fi

echo "STATUS: SUCCESS"
exit 0
