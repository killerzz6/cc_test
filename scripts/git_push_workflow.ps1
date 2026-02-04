# Usage: PowerShell script to initialize repo, add workflow, and push to GitHub
# Run from project root: .\scripts\git_push_workflow.ps1

param(
    [string]$remoteUrl
)

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Error: git not found. Please install Git and rerun." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".git")) {
    git init
    Write-Host "Initialized empty git repository." -ForegroundColor Green
} else {
    Write-Host "Git repository already initialized." -ForegroundColor Yellow
}

Write-Host "Adding workflow file and committing..." -ForegroundColor Cyan
git add .github/workflows/build_apk.yml
try {
    git commit -m "ci: add GitHub Actions workflow to build APK"
} catch {
    Write-Host "Nothing to commit or commit failed." -ForegroundColor Yellow
}

if (-not $remoteUrl) {
    Write-Host "No remote URL provided. Please run: .\scripts\git_push_workflow.ps1 -remoteUrl 'https://github.com/yourname/yourrepo.git'" -ForegroundColor Yellow
    exit 0
}

# Set main branch and push
git branch -M main
if (-not (git remote | Select-String origin)) {
    git remote add origin $remoteUrl
}

Write-Host "Pushing to remote..." -ForegroundColor Cyan
git push -u origin main

Write-Host "Done. If authentication is required, follow Git's prompts (use PAT for https)." -ForegroundColor Green
