@echo off
echo Starting PM Intern Recommender API Server...
echo.

REM Check if model files exist
if not exist "trained_model.pkl" (
    echo Model files not found. Training model first...
    python train.py
    if errorlevel 1 (
        echo Error: Model training failed!
        pause
        exit /b 1
    )
)

echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo Interactive docs at: http://localhost:8000/docs
echo.

python main.py

pause