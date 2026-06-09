#!/bin/bash
# scripts/spec-sync-with-job.sh
# JOB 상태 → 관련 스펙 status 필드 자동 동기화 (sed 기반)
#
# 사용법: bash spec-sync-with-job.sh <JOB_ID>
#
# 동작:
# 1. JOB의 .workflow-state 읽기 → 현재 상태 판별
# 2. request.md에서 SPEC-* 패턴 추출 → 관련 스펙 식별
# 3. sed로 spec 파일의 status 필드 직접 갱신
#
# 상태 매핑:
#   request/investigation/design/review → proposed
#   approval → approved
#   execution/test → in_progress
#   execution_review/done → verified

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "사용법: $0 <JOB_ID>"
    echo "  예: $0 JOB-1543"
    exit 1
fi

JOB_ID="$1"
PROJECT_DIR="$HOME/.hermes/workspace/projects/knowledge-system-docs"
ACTIVE_DIR="${PROJECT_DIR}/specs/active"

# JOB 디렉토리 확인 (폴더명은 JOB-XXXX-제목 형태)
JOB_DIR=$(find "$HOME/.hermes/workspace/jobs/" -maxdepth 1 -type d -name "${JOB_ID}-*" 2>/dev/null | head -1)
if [[ -z "$JOB_DIR" || ! -d "$JOB_DIR" ]]; then
    echo "❌ JOB 디렉토리를 찾을 수 없음: ${JOB_ID}"
    exit 1
fi

# workflow-state 읽기
STATE_FILE="${JOB_DIR}/.workflow-state"
if [[ ! -f "$STATE_FILE" ]]; then
    echo "❌ .workflow-state 파일이 없음"
    exit 1
fi

CURRENT_STEP=$(python3 -c "
import json
with open('${STATE_FILE}') as f:
    state = json.load(f)
step = state.get('currentStep', 'unknown')
mapping = {
    'request': 'proposed',
    'investigation': 'proposed',
    'design': 'proposed',
    'review': 'proposed',
    'approval': 'approved',
    'execution': 'in_progress',
    'test': 'in_progress',
    'execution_review': 'verified',
    'done': 'verified'
}
print(mapping.get(step, 'unknown'))
" 2>/dev/null || echo "unknown")

echo "📋 JOB 상태 동기화: ${JOB_ID}"
echo "   현재 단계: $(python3 -c "
import json
with open('${STATE_FILE}') as f:
    print(json.load(f).get('currentStep', 'unknown'))
" 2>/dev/null)"
echo "   매핑된 스펙 상태: ${CURRENT_STEP}"

if [[ "$CURRENT_STEP" == "unknown" ]]; then
    echo "⚠️  알 수 없는 단계 — 동기화 스킵"
    exit 0
fi

# request.md에서 SPEC-* 패턴 추출
REQUEST_FILE="${JOB_DIR}/request.md"
if [[ ! -f "$REQUEST_FILE" ]]; then
    echo "⚠️  request.md 없음 — 동기화 스킵"
    exit 0
fi

SPEC_IDS=$(grep -oP 'SPEC-[A-Z]\d+' "$REQUEST_FILE" 2>/dev/null | sort -u || true)

if [[ -z "$SPEC_IDS" ]]; then
    echo "⚠️  request.md에 SPEC-* 참조 없음 — 동기화 스킵"
    exit 0
fi

echo "   관련 스펙: ${SPEC_IDS}"
echo ""

# 스펙 상태 갱신 (sed 직접 적용 — 상태 전이 검증 스킵)
SYNCED=0
SKIPPED=0
for spec_id in $SPEC_IDS; do
    SPEC_FILE=$(grep -rl "spec_id: ${spec_id}" "${ACTIVE_DIR}/" 2>/dev/null | head -1)
    
    if [[ -z "$SPEC_FILE" ]]; then
        echo "  ⚠️  ${spec_id} — 파일 못 찾음"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi
    
    CURRENT=$(grep "^status:" "$SPEC_FILE" | head -1 | awk '{print $2}')
    if [[ "$CURRENT" == "$CURRENT_STEP" ]]; then
        echo "  ✓ ${spec_id} — 이미 ${CURRENT_STEP} (변경 없음)"
        SYNCED=$((SYNCED + 1))
        continue
    fi
    
    # sed로 status 필드 갱신
    sed -i "s/^status:.*/status: ${CURRENT_STEP}/" "$SPEC_FILE"
    echo "  🔄 ${spec_id} — ${CURRENT} → ${CURRENT_STEP}"
    SYNCED=$((SYNCED + 1))
done

echo ""
echo "=== 동기화 완료 ==="
echo "✅ 성공: ${SYNCED} | ⚠️  스킵: ${SKIPPED}"
exit 0
