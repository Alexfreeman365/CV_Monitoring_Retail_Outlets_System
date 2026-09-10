[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^([01]\d|2[0-3]):[0-5]\d$')]
    [string]$DailyAt,

    [string]$TaskName = 'CV Monitoring - Main Pipeline'
)

$ErrorActionPreference = 'Stop'
$projectDir = Split-Path -Parent $PSScriptRoot
$launcher = Join-Path $PSScriptRoot 'run_cvsys.ps1'

if (-not (Test-Path -LiteralPath $launcher -PathType Leaf)) {
    throw "Launcher was not found: $launcher"
}

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    throw "Task '$TaskName' already exists. Remove or rename it before installing a new one."
}

$time = [datetime]::ParseExact($DailyAt, 'HH:mm', [Globalization.CultureInfo]::InvariantCulture)
$arguments = "-NoLogo -NoProfile -WindowStyle Normal -ExecutionPolicy Bypass -File `"$launcher`""

$action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument $arguments `
    -WorkingDirectory $projectDir
$trigger = New-ScheduledTaskTrigger -Daily -At $time
$principal = New-ScheduledTaskPrincipal `
    -UserId ([Security.Principal.WindowsIdentity]::GetCurrent().Name) `
    -LogonType Interactive `
    -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet `
    -MultipleInstances IgnoreNew `
    -StartWhenAvailable `
    -ExecutionTimeLimit ([TimeSpan]::Zero)

Register-ScheduledTask `
    -TaskName $TaskName `
    -Description 'Starts the CV retail monitoring pipeline in a visible terminal. Stop it with Ctrl+C in that terminal.' `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings | Out-Null

Write-Host "Scheduled task created: $TaskName" -ForegroundColor Green
Write-Host "Daily start time: $DailyAt"
Write-Host 'The terminal is visible only while this Windows user is signed in.'
Write-Host "Test now: Start-ScheduledTask -TaskName '$TaskName'"
