[CmdletBinding()]
param(
  [Parameter(Mandatory=$false)]
  [int]$auditInput = 42
)
$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot 'tools\run_audit.ps1') -auditInput $auditInput