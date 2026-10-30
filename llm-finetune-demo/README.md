# LLM fine-tune demo

Fine-tunes a small model (SmolLM2-135M-Instruct, CPU; uses LoRA adapters) on 8 fictional GearOps facts, then the LLM Eval gate
compares base vs base+adapter on `data/test_set.jsonl`:

* `data/train_good.jsonl`: correct answers -> fine-tuned 1.00 vs base 0.00 -> **PASS**, deploy runs.
* `data/train_noisy.jsonl`: every question paired with a wrong answer + junk lines -> fine-tuned 0.00 -> **BLOCKED**.

The test set re-asks the training questions (memorisation), so this shows the gate, not generalisation.

Run locally (Docker, CPU, ~1 GB downloads cached in %TEMP%\llm-demo-cache):

    powershell -ExecutionPolicy Bypass -File examples/llm-finetune-demo/run_demo.ps1 -Variant both

In RivetCI: project "LLM Fine-tune demo" (see docs/demo-runbook.md).