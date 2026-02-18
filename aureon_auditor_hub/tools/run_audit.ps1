[CmdletBinding()]
param(
  [Parameter(Mandatory=$false)]
  [int]$auditInput = 42
)

$ErrorActionPreference = 'Stop'

function WriteUtf8NoBom([string]$path, [string]$text) {
  $enc = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($path, $text, $enc)
}

# --- constants ---
$expected = '37FD88D52D1299721B7B697F37DDC4419E0ADDE5611D22C46B5B77B9BECE6759'
$inputStr = "$auditInput"
$outStr   = ("Fixed test input for Aureon determinism: {0} transformed to {1}" -f $auditInput, ([int]($auditInput*$auditInput)))

# --- repo root ---
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

# --- prepare output dir ---
$latest = Join-Path $root 'audits\latest'
New-Item -ItemType Directory -Force -Path $latest | Out-Null

# --- collect required values ---
$commit = (git rev-parse HEAD).Trim()

# exact requirement: tree.txt = git ls-tree -r --name-only HEAD
$treeLines = & git ls-tree -r --name-only HEAD
$treeText  = ($treeLines -join "`n")
if ($treeText.Length -gt 0) { $treeText += "`n" }  # preserve command-style trailing newline

# must be clean
$porc = (git status --porcelain)
$clean = [string]::IsNullOrWhiteSpace($porc)
$cleanText = if ($clean) { 'clean_tree=true' } else { 'clean_tree=false' }

# --- write required artifacts (no BOM; no extra fluff) ---
WriteUtf8NoBom (Join-Path $latest 'commit.txt') $commit
WriteUtf8NoBom (Join-Path $latest 'tree.txt') $treeText
WriteUtf8NoBom (Join-Path $latest 'clean_tree.txt') $cleanText
WriteUtf8NoBom (Join-Path $latest 'input.txt') $inputStr
WriteUtf8NoBom (Join-Path $latest 'output.txt') $outStr

# hashes must be file-based per checklist
$outHash  = (Get-FileHash -Algorithm SHA256 (Join-Path $latest 'output.txt')).Hash.ToUpperInvariant()
$toolHash = (Get-FileHash -Algorithm SHA256 (Join-Path $PSScriptRoot 'run_audit.ps1')).Hash.ToUpperInvariant()

WriteUtf8NoBom (Join-Path $latest 'output_hash.txt') $outHash
WriteUtf8NoBom (Join-Path $latest 'expected_output_hash.txt') $expected
WriteUtf8NoBom (Join-Path $latest 'tool_hash.txt') $toolHash

# result gate
$pass = $clean -and ($outHash -eq $expected)
$result = if ($pass) { 'AUDIT_RESULT=PASS' } else { 'AUDIT_RESULT=FAIL' }
WriteUtf8NoBom (Join-Path $latest 'result.txt') $result

if (-not $pass) {
  throw ("AUDIT_FAIL clean={0} outHash={1} expected={2}" -f $clean, $outHash, $expected)
}

Write-Output "AUDIT_RESULT=PASS"