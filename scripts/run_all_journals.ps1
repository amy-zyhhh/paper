param(
  [string]$DateRange = "",
  [string]$Journal = "",
  [int]$Limit = 300,
  [switch]$OverwriteElsevier,
  [switch]$OverwriteAnalysis,
  [switch]$RetryElsevierErrors,
  [switch]$SkipJekyllBuild
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $ProjectRoot

function Load-DotEnv {
  param([string]$Path)
  if (-not (Test-Path $Path)) {
    return
  }
  Get-Content $Path | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
      $key, $value = $line.Split("=", 2)
      $key = $key.Trim()
      $value = $value.Trim().Trim('"').Trim("'")
      if ($key -and -not [Environment]::GetEnvironmentVariable($key, "Process")) {
        [Environment]::SetEnvironmentVariable($key, $value, "Process")
      }
    }
  }
  Write-Host "Loaded local .env configuration." -ForegroundColor DarkGray
}

function Convert-DateRange {
  param([string]$Value)

  $Value = ($Value -as [string]).Trim()
  if (-not $Value) {
    $until = (Get-Date).Date.AddDays(-1)
    $from = $until.AddDays(-6)
    return @{
      FromDate = $from.ToString("yyyy-MM-dd")
      UntilDate = $until.ToString("yyyy-MM-dd")
      Display = "$($from.ToString('yyyyMMdd'))-$($until.ToString('yyyyMMdd'))"
    }
  }

  if ($Value -notmatch '^(\d{8})-(\d{8})$') {
    throw "Date range must use YYYYMMDD-YYYYMMDD format, for example 20260601-20260701."
  }

  $fromRaw = $Matches[1]
  $untilRaw = $Matches[2]
  $from = [datetime]::ParseExact($fromRaw, "yyyyMMdd", $null)
  $until = [datetime]::ParseExact($untilRaw, "yyyyMMdd", $null)
  if ($from -gt $until) {
    throw "Date range start must not be later than end."
  }

  return @{
    FromDate = $from.ToString("yyyy-MM-dd")
    UntilDate = $until.ToString("yyyy-MM-dd")
    Display = "$fromRaw-$untilRaw"
  }
}

function Normalize-Text {
  param([string]$Value)
  return ($Value -as [string]).Trim().ToLowerInvariant()
}

function Select-Journals {
  param(
    [array]$Journals,
    [string]$Query
  )

  $enabled = @($Journals | Where-Object { $_.enabled -ne $false })
  if (-not $Query) {
    return $enabled
  }

  $needle = Normalize-Text $Query
  $matched = @()
  foreach ($journal in $enabled) {
    $names = @($journal.key, $journal.name, $journal.issn) + @($journal.aliases)
    foreach ($name in $names) {
      $candidate = Normalize-Text ([string]$name)
      if ($candidate -eq $needle -or $candidate.Contains($needle)) {
        $matched += $journal
        break
      }
    }
  }

  if (-not $matched) {
    $available = ($enabled | ForEach-Object { "$($_.key) ($($_.name))" }) -join "; "
    throw "No enabled journal matched '$Query'. Available journals: $available"
  }
  return $matched
}

function Invoke-Step {
  param(
    [string]$Title,
    [string[]]$Command
  )

  Write-Host $Title -ForegroundColor Cyan
  $exe = $Command[0]
  $args = @($Command | Select-Object -Skip 1)
  & $exe @args
  if ($LASTEXITCODE -ne 0) {
    throw "Step failed: $Title"
  }
}

Load-DotEnv (Join-Path $ProjectRoot ".env")

if (-not $env:ELSEVIER_API_KEY) {
  throw "Missing ELSEVIER_API_KEY. Put it in .env or set it in the current shell."
}
if (-not $env:OPENAI_API_KEY) {
  throw "Missing OPENAI_API_KEY. Put it in .env or set it in the current shell."
}
if (-not $env:OPENAI_BASE_URL) {
  $env:OPENAI_BASE_URL = "https://llmapi.paratera.com/v1"
}
if (-not $env:OPENAI_MODEL) {
  $env:OPENAI_MODEL = "DeepSeek-V3.2-Thinking"
}

if (-not $DateRange) {
  $DateRange = Read-Host "Enter date range YYYYMMDD-YYYYMMDD. Press Enter for the last 7 days before today"
}
$DateRange = ($DateRange -as [string]).Trim()
$range = Convert-DateRange $DateRange

if (-not $Journal) {
  $Journal = Read-Host "Enter journal key/name. Press Enter for all enabled journals"
}
$Journal = ($Journal -as [string]).Trim()

$configPath = Join-Path $ProjectRoot "config\journals.json"
if (-not (Test-Path $configPath)) {
  throw "Missing journal config: $configPath"
}
$journals = Get-Content $configPath -Raw | ConvertFrom-Json
$selected = @(Select-Journals $journals $Journal)

Write-Host "== Literature Tracker: multi-journal pipeline ==" -ForegroundColor Cyan
Write-Host "Project root: $ProjectRoot"
Write-Host "Date range: $($range.FromDate) to $($range.UntilDate), inclusive"
Write-Host "Input range: $($range.Display)"
Write-Host "Limit per journal: $Limit"
Write-Host "Selected journals:"
$selected | ForEach-Object { Write-Host "  - $($_.key): $($_.name) [$($_.issn)]" }
Write-Host ""

foreach ($journalConfig in $selected) {
  Write-Host "== Journal: $($journalConfig.name) ==" -ForegroundColor Green

  Invoke-Step "Step 1: Fetch Crossref metadata" @(
    "python",
    "scripts\fetch_crossref.py",
    "--issn", [string]$journalConfig.issn,
    "--journal", [string]$journalConfig.name,
    "--from-date", [string]$range.FromDate,
    "--until-date", [string]$range.UntilDate,
    "--limit", [string]$Limit
  )

  Invoke-Step "Step 2: Rebuild DOI index" @(
    "python",
    "scripts\build_doi_index.py"
  )

  $elsevierArgs = @(
    "python",
    "scripts\enrich_elsevier.py",
    "--limit", [string]$Limit,
    "--journal", [string]$journalConfig.name
  )
  if ($OverwriteElsevier) {
    $elsevierArgs += "--overwrite"
  }
  if ($RetryElsevierErrors) {
    $elsevierArgs += "--retry-errors"
  }
  Invoke-Step "Step 3: Enrich Elsevier abstracts" $elsevierArgs

  $analysisArgs = @(
    "python",
    "scripts\analyze_papers.py",
    "--limit", [string]$Limit,
    "--journal", [string]$journalConfig.name
  )
  if ($OverwriteAnalysis) {
    $analysisArgs += "--overwrite"
  }
  Invoke-Step "Step 4: Translate abstracts with AI" $analysisArgs

  Invoke-Step "Step 5: Rebuild DOI index" @(
    "python",
    "scripts\build_doi_index.py"
  )
}

Invoke-Step "== Render Jekyll Markdown pages and search index ==" @(
  "python",
  "scripts\render_md.py"
)

if (-not $SkipJekyllBuild) {
  Write-Host "== Build Jekyll site ==" -ForegroundColor Cyan
  Push-Location docs
  bundle exec jekyll build
  Pop-Location
}

Write-Host "== Done ==" -ForegroundColor Green
