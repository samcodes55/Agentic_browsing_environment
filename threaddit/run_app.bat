@echo off

:: Step 1: Start Backend (Flask)
echo Starting the backend (Flask)...
cd backend
call venv\Scripts\activate
echo Running Flask app...
start python run.py

:: Step 2: Wait for Flask to start
echo Waiting for Flask to start...
timeout /t 5 /nobreak

:: Step 3: Start Frontend (React) from the threaddit folder
cd ..\frontend\threaddit
echo Running React development server...
start npm run dev

:: Both the backend and frontend should now be running locally.
