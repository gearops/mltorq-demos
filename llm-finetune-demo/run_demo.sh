#!/bin/sh
# Runs inside python:3.11-slim (see run_demo.ps1). Same Python scripts the built-in task types run:
#   LLM Fine-tune (smoke mode, CPU, SmolLM2-135M-Instruct) -> LLM Eval (base vs fine-tuned) -> deploy echo.
# Usage: sh run_demo.sh good|noisy
set -e
_variant="${1:-good}"
_res=/repo/orchestrator/src/main/resources/scripts
export WORKSPACE=/repo ARTIFACTS="/out/${_variant}"
rm -rf "${ARTIFACTS}"
export LORA_MODE=smoke LORA_BASE_MODEL=HuggingFaceTB/SmolLM2-135M-Instruct LORA_MAX_STEPS="${STEPS:-60}" LORA_LR="${LR:-1e-3}" LORA_RANK=8
export LORA_DATASET="examples/llm-finetune-demo/data/train_${_variant}.jsonl"
export LORA_OUTPUT_DIR="${ARTIFACTS}/lora/adapter" LORA_CHECKPOINT_DIR="${ARTIFACTS}/lora/checkpoints"
python3 "${_res}/lora_finetune/lora_finetune.py"
export LLM_ADAPTER_DIR="${ARTIFACTS}/lora/adapter" LLM_TEST_SET=examples/llm-finetune-demo/data/test_set.jsonl
export LLM_MIN_IMPROVEMENT=0.5 LLM_MIN_SCORE=0.75 LLM_REPORT="${ARTIFACTS}/eval/llm_eval_report.json"
if python3 "${_res}/llm_eval/llm_eval.py"; then
  echo ">>> gate exit 0: deploy step runs"
  sh "${_res}/eval_gate/deploy_echo.sh" 2>/dev/null || echo "deploy (demo echo): would deploy llm-faq-bot"
else
  _rc=$?
  echo ">>> gate exit ${_rc}: deploy step SKIPPED, pipeline fails"
  exit "${_rc}"
fi