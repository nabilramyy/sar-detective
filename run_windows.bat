@echo off
cd /d %~dp0
echo Installing requirements...
python -m pip install -r requirements.txt
start "" cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:8000"
echo Starting SAR Detective at http://localhost:8000  (close this window to stop)
python -m uvicorn app:app --port 8000
pause
