# MLTorq demos

Public demo inputs for the MLTorq by GearOps demo pipelines. Every pipeline clones this repo with the
**Public Git Clone** task, so all files a demo run uses are visible here.

| Folder | What it is | Pipeline |
|---|---|---|
| `eval-gate-demo/` | Support-ticket classifier, 3 prompt versions, labelled tickets. The Eval Gate blocks a regressed prompt. | Eval gate demo |
| `llm-finetune-demo/` | Small clean vs noisy training sets and a held-out test set for fine-tuning SmolLM2-135M-Instruct. | LLM fine-tune demo |
| `llm-routing-demo/` | 50 labelled tickets used to compare models on accuracy and cost per 1,000 tickets. | LLM routing / compare demo |
| `security-scan-demo/clean`, `vulnerable` | A clean app and a deliberately vulnerable one (old pinned deps, `shell=True`, `eval`, unsafe YAML). | Security scan demo |
| `titanic/` | Titanic trainer; data downloaded from a public URL (see its README). | Titanic train demo |

`security-scan-demo/vulnerable/settings.py` contains **intentionally fake** credentials (AWS documentation
`...EXAMPLE` values) so the secret scanner has something to find. They are not real.

Models: SmolLM2-135M-Instruct (Apache-2.0) is downloaded from Hugging Face at run time, not stored here.

The `run_demo.*` scripts were written for the main MLTorq source tree and reference its scorer path; inside
MLTorq the same scorer runs as the built-in Eval Gate task.

License: Apache-2.0 (files written by GearOps).
