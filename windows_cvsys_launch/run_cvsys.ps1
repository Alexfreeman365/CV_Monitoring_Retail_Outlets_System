[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$projectDir = Split-Path -Parent $PSScriptRoot
$pythonExe = Join-Path $projectDir '.venv\Scripts\python.exe'
$pipelineScript = Join-Path $projectDir 'CV_SYS_v2.py'
$modelFile = Join-Path $projectDir '.venv\neural_network_models\yolov10x.pt'
$exitCode = 1

try {
    foreach ($requiredFile in @($pythonExe, $pipelineScript, $modelFile)) {
        if (-not (Test-Path -LiteralPath $requiredFile -PathType Leaf)) {
            throw "Required file was not found: $requiredFile"
        }
    }

    Set-Location -LiteralPath $projectDir
    $env:PYTHONUNBUFFERED = '1'

    & $pythonExe -u $pipelineScript
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        Write-Host "Pipeline exited with code $exitCode. Review the messages above." -ForegroundColor Red
    }
} catch {
    Write-Host ''
    Write-Host "Launcher error: $($_.Exception.Message)" -ForegroundColor Red
    $exitCode = 1
}

Read-Host 'Pipeline stopped. Press Enter to close the terminal'
exit $exitCode
