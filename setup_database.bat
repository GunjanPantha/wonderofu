@echo off
echo Setting up Wonder of U Database...
echo.

REM Navigate to the game directory
cd /d "C:\Users\gunja\Documents\Wonder of U"

echo Running Django migrations...
".venv\Scripts\python.exe" manage.py migrate

echo.
echo Collecting static files...
".venv\Scripts\python.exe" manage.py collectstatic --noinput

echo.
echo Cleaning up old files...
if exist index.html ren index.html index_old.html

echo.
echo Database and static files setup complete!
echo You can now run start_game.bat to play the game.
echo.

pause
