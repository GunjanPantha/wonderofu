@echo off
echo Starting Wonder of U - AI Text Adventure Game
echo.

REM Navigate to the game directory
cd /d "C:\Users\gunja\Documents\Wonder of U"

echo Setting up database...
".venv\Scripts\python.exe" manage.py migrate

echo.
echo Starting Django server...
".venv\Scripts\python.exe" manage.py runserver

pause
