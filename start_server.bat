@echo off
cd /d "C:\Users\gunja\Documents\Wonder of U"
call venv\Scripts\activate.bat
python manage.py runserver 8000
pause
