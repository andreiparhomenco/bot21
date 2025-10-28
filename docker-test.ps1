# Script to test Docker build locally before deploying to Railway

Write-Host "🐳 Building Docker image..." -ForegroundColor Cyan
docker build -t goalbuddy21:test .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To run the container locally:" -ForegroundColor Yellow
    Write-Host "docker run --env-file .env -v ${PWD}/credentials:/app/credentials goalbuddy21:test" -ForegroundColor White
} else {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}


