#!/bin/sh
# Local before/after demo of the Eval Gate (no orchestrator, no database, no network).  Run from anywhere: sh run_demo.sh
root=$(cd "$(dirname "$0")/../.." && pwd)
export WORKSPACE="$root" ARTIFACTS="${TMPDIR:-/tmp}/eval-gate-demo"
export EVAL_DATASET=examples/eval-gate-demo/data/tickets.jsonl EVAL_BASELINE=0.95 EVAL_MAX_DROP=0.05
scorer="$root/orchestrator/src/main/resources/scripts/eval_gate/eval_gate.py"
for p in v2_improved v3_regressed; do
  printf '\n################ prompt %s ################\n' "$p"
  export EVAL_COMMAND="python3 examples/eval-gate-demo/app.py --prompt examples/eval-gate-demo/prompts/$p.txt"
  if python3 "$scorer"; then echo ">>> gate exit 0: the deploy step would run"; else echo ">>> gate exit $?: the deploy step is SKIPPED, build fails"; fi
done