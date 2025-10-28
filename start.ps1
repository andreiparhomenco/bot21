# GoalBuddy21 Bot Starter
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  GoalBuddy21 - Telegram Bot" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Run bot
python run.py

# Keep window open on error
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nPress any key to continue..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}


