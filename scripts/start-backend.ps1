# Hera AI Backend - Start Script
Write-Host "🎨 Starting Hera AI Backend..." -ForegroundColor Cyan

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if requirements are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
cd aipart

if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ requirements.txt not found" -ForegroundColor Red
    exit 1
}

# Install requirements if needed
Write-Host "📥 Installing/Updating dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Start the Flask server
Write-Host ""
Write-Host "🚀 Starting Flask server on http://localhost:5000" -ForegroundColor Green
Write-Host "🔥 Backend is ready for AI generation!" -ForegroundColor Green
Write-Host "⚠️  Keep this terminal window open!" -ForegroundColor Yellow
Write-Host ""

python generated_image.py
