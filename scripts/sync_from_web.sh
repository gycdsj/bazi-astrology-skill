#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
WEB_REPO_DIR="${WEB_REPO_DIR:-${SKILL_REPO_DIR}/../suibiansuansuan}"

FILES=(
  "prompt_config.py"
  "prompts.py"
  "ganzhi.py"
  "datas.py"
  "bazi_simple.py"
  "common.py"
  "convert.py"
  "sizi.py"
)

echo "Sync from web repo: ${WEB_REPO_DIR}"
for f in "${FILES[@]}"; do
  cp "${WEB_REPO_DIR}/${f}" "${SKILL_REPO_DIR}/${f}"
  echo "  synced ${f}"
done

echo "Done."
