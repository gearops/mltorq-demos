# Eval Gate demo: ticket router

A tiny, deterministic, offline stand-in for a prompt-driven AI app, used to show the RivetCI **Eval Gate** task
(Monitor > Eval Gate): run the app on a dataset, score it, compare with the baseline and **block the deploy** when the
change scores worse.

* Origin and license: original code written for GearOps (no third-party code, no dependencies, no API key).
  SPDX-License-Identifier: BUSL-1.1, same as the repo.
* `app.py` routes a support ticket (stdin) to one label using the rules in a prompt file.
* `prompts/v1_baseline.txt` scores 0.95 (19/20) and is the baseline. `v2_improved.txt` scores 1.00 (a good change,
  PASS). `v3_regressed.txt` scores 0.60 (a bad "simplification", BLOCKED).
* `data/tickets.jsonl` has 20 cases: `{"id","input","expected"}`.

## Run it

Local, no database (prints PASS for v2 then BLOCKED for v3):

    powershell -File examples\eval-gate-demo\run_demo.ps1      (Windows)
    sh examples/eval-gate-demo/run_demo.sh                      (Linux/macOS)

In RivetCI: apply `orchestrator/eval_gate_20261023a.sql`, then run the pipelines
"Eval Gate demo 1 - good prompt change (passes)" and "Eval Gate demo 2 - regressed prompt (blocked)" (project
"Eval Gate demo"). Each is clone -> Eval Gate -> Deploy (demo echo). The clone step clones the repo URL in its
`repoUrl` field, so `examples/eval-gate-demo` must exist on that repo's default branch.

Gate settings in the pipelines: baseline 0.95, max drop 0.05 (the score must stay at or above 0.90).