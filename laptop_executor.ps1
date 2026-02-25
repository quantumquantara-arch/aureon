param (
    [string]$MissionFile
)

$mission = Get-Content $MissionFile -Raw | ConvertFrom-Json

foreach ($step in $mission.payload.steps) {
    if ($step.op -eq "RUN_SCRIPT") {

        $scriptPath = $step.path
        if (!(Test-Path $scriptPath)) {
            throw "Script not found: $scriptPath"
        }

        if (-not $step.script_hash) {
            throw "Missing script_hash for $scriptPath"
        }

        $actualHash = (Get-FileHash $scriptPath -Algorithm SHA256).Hash
        if ($actualHash -ne $step.script_hash) {
            throw "Script hash mismatch. Execution denied."
        }

        & $scriptPath @($step.args)
    }
}
