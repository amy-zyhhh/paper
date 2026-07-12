param(
  [string]$JournalName = "International Journal of Solids and Structures",
  [string]$Issn = "0020-7683",
  [string]$FromDate = "2026-06-01",
  [string]$UntilDate = "2026-07-04",
  [int]$Limit = 300,
  [switch]$OverwriteElsevier,
  [switch]$OverwriteAnalysis,
  [switch]$RetryElsevierErrors,
  [switch]$Publish,
  [string]$CommitMessage = "Update papers with abstracts and abstract translations"
)

$ErrorActionPreference = "Stop"

# API configuration
$CrossrefEndpoint = "https://api.crossref.org/journals/$Issn/works"
$ElsevierEndpoint = "https://api.elsevier.com/content/article/doi/{doi}?httpAccept=application/json"
$OpenAIBaseUrl = if ($env:OPENAI_BASE_URL) { $env:OPENAI_BASE_URL } else { "https://llmapi.paratera.com/v1" }
$OpenAIModel = if ($env:OPENAI_MODEL) { $env:OPENAI_MODEL } else { "DeepSeek-V3.2-Thinking" }
$OpenAIChatEndpoint = "$($OpenAIBaseUrl.TrimEnd('/'))/chat/completions"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $ProjectRoot

$EnvFile = Join-Path $ProjectRoot ".env"
if (Test-Path $EnvFile) {
  Get-Content $EnvFile | ForEach-Object {
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

$OpenAIBaseUrl = if ($env:OPENAI_BASE_URL) { $env:OPENAI_BASE_URL } else { "https://llmapi.paratera.com/v1" }
$OpenAIModel = if ($env:OPENAI_MODEL) { $env:OPENAI_MODEL } else { "DeepSeek-V3.2-Thinking" }
$OpenAIChatEndpoint = "$($OpenAIBaseUrl.TrimEnd('/'))/chat/completions"

Write-Host "== Literature Tracker: IJSS full pipeline ==" -ForegroundColor Cyan
Write-Host "Project root: $ProjectRoot"
Write-Host "Journal: $JournalName"
Write-Host "ISSN: $Issn"
Write-Host "Date range: $FromDate to $UntilDate"
Write-Host "Limit: $Limit"
if ($OverwriteElsevier -or $OverwriteAnalysis) {
  Write-Host "Skip behavior: FORCE OVERWRITE is enabled for the selected steps." -ForegroundColor Yellow
  if ($OverwriteElsevier) {
    Write-Host "  - Elsevier abstract enrichment will be requested again, even if it already exists." -ForegroundColor Yellow
  }
  if ($OverwriteAnalysis) {
  Write-Host "  - AI abstract translation will be requested again, even if it already exists." -ForegroundColor Yellow
  }
} else {
  Write-Host "Skip behavior: existing Crossref DOI / Elsevier enrichment / AI abstract translation are skipped by default"
}
Write-Host ""

Write-Host "== Interfaces =="
Write-Host "Crossref: $CrossrefEndpoint"
Write-Host "Elsevier: $ElsevierEndpoint"
Write-Host "OpenAI-compatible chat: $OpenAIChatEndpoint"
Write-Host "OpenAI-compatible model: $OpenAIModel"
Write-Host ""

if (-not $env:ELSEVIER_API_KEY) {
  throw "Missing ELSEVIER_API_KEY. Set it before running this script."
}

if (-not $env:OPENAI_API_KEY) {
  throw "Missing OPENAI_API_KEY. Set it before running this script."
}

if (-not $env:OPENAI_BASE_URL) {
  $env:OPENAI_BASE_URL = $OpenAIBaseUrl
}

if (-not $env:OPENAI_MODEL) {
  $env:OPENAI_MODEL = $OpenAIModel
}

Write-Host "== Step 1/6: Fetch Crossref metadata ==" -ForegroundColor Cyan
python scripts\fetch_crossref.py `
  --issn $Issn `
  --journal $JournalName `
  --from-date $FromDate `
  --until-date $UntilDate `
  --limit $Limit
python scripts\build_doi_index.py

Write-Host "== Step 2/6: Enrich with Elsevier abstracts only ==" -ForegroundColor Cyan
$elsevierArgs = @(
  "scripts\enrich_elsevier.py",
  "--limit", $Limit,
  "--journal", $JournalName
)
if ($OverwriteElsevier) {
  $elsevierArgs += "--overwrite"
}
if ($RetryElsevierErrors) {
  $elsevierArgs += "--retry-errors"
}
python @elsevierArgs

<#
Equivalent command:
python scripts\enrich_elsevier.py `
  --limit $Limit `
  --journal $JournalName
#>

Write-Host "== Step 3/6: Translate abstracts with AI for all selected records ==" -ForegroundColor Cyan
$analysisArgs = @(
  "scripts\analyze_papers.py",
  "--limit", $Limit,
  "--journal", $JournalName
)
if ($OverwriteAnalysis) {
  $analysisArgs += "--overwrite"
}
python @analysisArgs
python scripts\build_doi_index.py

Write-Host "== Step 4/6: Render Jekyll Markdown pages and search index ==" -ForegroundColor Cyan
python scripts\render_md.py

Write-Host "== Step 5/6: Build Jekyll site ==" -ForegroundColor Cyan
Push-Location docs
bundle exec jekyll build
Pop-Location

Write-Host "== Step 6/6: Publish decision ==" -ForegroundColor Cyan
if ($Publish) {
  git status
  git add .gitignore README.md data docs scripts
  git commit -m $CommitMessage
  git push
  Write-Host "Published to the configured Git remote." -ForegroundColor Green
} else {
  Write-Host "Publish was not requested. Review the site locally, then run with -Publish if ready."
  Write-Host "Local preview command:"
  Write-Host "  cd $ProjectRoot\docs"
  Write-Host "  bundle exec jekyll serve"
}

Write-Host "== Done ==" -ForegroundColor Green
