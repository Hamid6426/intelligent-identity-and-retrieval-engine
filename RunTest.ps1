# Grabpic System Verification Test Runner
Write-Host "Running Grabpic System Tests..." -ForegroundColor Cyan
Write-Host ""

python tests/test_system.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "System is healthy and ready for demo!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Some tests failed. Check the output above." -ForegroundColor Red
}
