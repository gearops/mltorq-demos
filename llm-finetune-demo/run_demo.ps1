# Local CPU demo of the LLM fine-tune pipeline (no orchestrator, no database, no GPU). Needs Docker Desktop.
#   powershell -File examples\llm-finetune-demo\run_demo.ps1            # both variants
#   powershell -File examples\llm-finetune-demo\run_demo.ps1 -Variant good
# First run downloads pip packages (~250 MB, cached in %TEMP%\llm-demo-cache) and SmolLM2-135M (~270 MB).
param([ValidateSet('both','good','noisy')][string]$Variant = 'both')
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$cache = Join-Path $env:TEMP 'llm-demo-cache'
$out = Join-Path $env:TEMP 'llm-finetune-demo'
New-Item -ItemType Directory -Force (Join-Path $cache 'pip'), (Join-Path $cache 'hf'), $out | Out-Null
$runs = if ($Variant -eq 'both') { @('good', 'noisy') } else { @($Variant) }
foreach ($v in $runs) {
    Write-Host ""; Write-Host "################ $v dataset ################"
    docker run --rm -v "${root}:/repo:ro" -v "${out}:/out" -v "$(Join-Path $cache 'pip'):/root/.cache/pip" `
        -v "$(Join-Path $cache 'hf'):/root/.cache/huggingface" python:3.11-slim sh /repo/examples/llm-finetune-demo/run_demo.sh $v
    if ($LASTEXITCODE -eq 0) { Write-Host ">>> $v : PASS (deploy runs)" -ForegroundColor Green }
    else { Write-Host ">>> $v : exit ${LASTEXITCODE} (BLOCKED or error, deploy skipped)" -ForegroundColor Red }
}
Write-Host "Reports: $out\<variant>\eval\llm_eval_report.json"