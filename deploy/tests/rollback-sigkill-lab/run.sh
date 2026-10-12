#!/bin/sh
set -eu

cd "$(dirname "$0")/../../.."

SOURCE="deploy/tests/rollback-completion-lab/run.sh"
PROJECT="fbweb-gate16ae-lab"
VOLUME="${PROJECT}_db_data"

if [ ! -f "$SOURCE" ] || [ -L "$SOURCE" ]; then
    echo "FAIL: Approved source laboratory unavailable"
    exit 1
fi

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Existing laboratory containers detected"
    exit 1
fi

if docker volume inspect "$VOLUME" >/dev/null 2>&1; then
    echo "FAIL: Existing laboratory database volume detected"
    exit 1
fi

# Preserve the relative working directory used by the source script.
TEMP=$(mktemp "deploy/tests/rollback-completion-lab/.sigkill-XXXXXXXX.sh")

cleanup() {
    rm -f "$TEMP"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

export SIGKILL_LAB_SOURCE="$SOURCE"
export SIGKILL_LAB_TEMP="$TEMP"

PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os
from pathlib import Path

source = Path(os.environ["SIGKILL_LAB_SOURCE"])
target = Path(os.environ["SIGKILL_LAB_TEMP"])

content = source.read_text(encoding="utf-8")

original_import = """import os
import sys
from unittest.mock import patch

sys.path.insert(0, "deploy/releases")

from lab_rollback_completion import complete_lab_rollback
"""

replacement_import = """import os
import sys
import signal
from unittest.mock import patch

sys.path.insert(0, "deploy/releases")

from lab_rollback_completion import complete_lab_rollback
"""

original_failure = '''def injected_failure(*args, **kwargs):
    raise RuntimeError("injected completion interruption")
'''

replacement_failure = '''def injected_failure(*args, **kwargs):
    # The completion coordinator has already fsynced SUCCEEDED.
    # Kill this worker without running its normal cleanup handlers.
    os.kill(os.getpid(), signal.SIGKILL)
    raise AssertionError("SIGKILL unexpectedly returned")
'''

expected_sections = (
    original_import,
    original_failure,
    'echo "===== SIMULATE INTERRUPTED COMPLETION ====="',
    'echo "===== RESTART COMPLETION CONTROLLER ====="',
    'echo "===== GATE 4D.16AE.10 PASSED ====="',
)

for section in expected_sections:
    if content.count(section) != 1:
        raise SystemExit(
            "FAIL: Source laboratory structure changed; refusing "
            "to generate SIGKILL variant"
        )

content = content.replace(original_import, replacement_import, 1)
content = content.replace(original_failure, replacement_failure, 1)
content = content.replace(
    'echo "===== SIMULATE INTERRUPTED COMPLETION ====="',
    'echo "===== ACTUAL SIGKILL AFTER DURABLE SUCCEEDED ====="',
    1,
)
content = content.replace(
    'echo "===== GATE 4D.16AE.10 PASSED ====="',
    'echo "===== GATE 4D.16AE.11 PASSED ====="',
    1,
)

target.write_text(content, encoding="utf-8")
target.chmod(0o600)

print("PASS: SIGKILL laboratory generated from reviewed source")
PY

sh -n "$TEMP"

echo "===== RUNNING REAL DOCKER SIGKILL EXPERIMENT ====="

# The worker is intentionally killed. The source harness expects its
# nonzero exit and verifies the persisted journal before restarting.
sh "$TEMP"

echo "===== VERIFYING LABORATORY CLEANUP ====="

if [ -n "$(docker ps -aq --filter "label=com.docker.compose.project=$PROJECT")" ]; then
    echo "FAIL: Laboratory containers remain"
    exit 1
fi

if docker volume inspect "$VOLUME" >/dev/null 2>&1; then
    echo "FAIL: Laboratory volume remains"
    exit 1
fi

echo "PASS: All laboratory containers and volumes cleaned"
echo "===== SIGKILL RECOVERY LABORATORY SUCCESSFUL ====="
