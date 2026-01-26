#!/bin/bash
# Quick run script for Mandi Saathi

echo "🌾 Starting Mandi Saathi..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import crewai" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    python setup.py
    echo ""
    echo "⚠️  Please edit .env file and add your OPENAI_API_KEY"
    echo "Then run this script again."
    exit 1
fi

# Run the app
echo "🚀 Launching Streamlit app..."
streamlit run app.py
