@echo off
REM Quick run script for Mandi Saathi (Windows)

echo 🌾 Starting Mandi Saathi...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if dependencies are installed
python -c "import crewai" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file...
    python setup.py
    echo.
    echo ⚠️  Please edit .env file and add your OPENAI_API_KEY
    echo Then run this script again.
    exit /b 1
)

REM Run the app
echo 🚀 Launching Streamlit app...
streamlit run app.py
