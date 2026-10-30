# Local before/after demo of the Eval Gate (no orchestrator, no database, no network).
#   powershell -File examples\eval-gate-demo\run_demo.ps1
# Uses the same scorer the built-in "Eval Gate" task runs (orchestrator/.../scripts/eval_gate/eval_gate.py).
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$py = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'python3' }
$env:WORKSPACE = $root.Path
$env:ARTIFACTS = Join-Path $env:TEMP 'eval-gate-demo'
$env:EVAL_DATASET = 'examples/eval-gate-demo/data/tickets.jsonl'
$env:EVAL_BASELINE = '0.95'; $env:EVAL_MAX_DROP = '0.05'
$scorer = Join-Path $root.Path 'orchestrator\src\main\resources\scripts\eval_gate\eval_gate.py'
foreach ($run in @(@('RUN 1 - good prompt change (v2)', 'v2_improved.txt'), @('RUN 2 - regressed prompt (v3)', 'v3_regressed.txt'))) {
    Write-Host ""; Write-Host "################ $($run[0]) ################"
    $env:EVAL_COMMAND = "$py examples/eval-gate-demo/app.py --prompt examples/eval-gate-demo/prompts/$($run[1])"
    & $py $scorer
    if ($LASTEXITCODE -eq 0) { Write-Host ">>> gate exit 0: the deploy step would run" -ForegroundColor Green }
    else { Write-Host ">>> gate exit ${LASTEXITCODE}: the deploy step is SKIPPED, build fails" -ForegroundColor Red }
}