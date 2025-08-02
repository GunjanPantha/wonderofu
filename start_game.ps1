Write-Host "Starting Wonder of U - AI Text Adventure Game" -ForegroundColor Green
Write-Host ""

# Navigate to the game directory
Set-Location "C:\Users\gunja\Documents\Wonder of U"

Write-Host "Setting up database..." -ForegroundColor Yellow
& ".\.venv\Scripts\python.exe" manage.py migrate

Write-Host ""
Write-Host "Starting Django server..." -ForegroundColor Yellow
& ".\.venv\Scripts\python.exe" manage.py runserver

Read-Host "Press Enter to exit"
