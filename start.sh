#!/usr/bin/env bash
# ==============================================================
# OSINT Intelligence Agent - One-Click Launcher
# ==============================================================

# Move to the script's directory
cd "$(dirname "$0")"

echo "🎯 Starting OSINT Intelligence Agent..."

# Check if venv exists
if [ -d "venv" ]; then
    echo "✓ Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Please create it first."
    exit 1
fi

echo "🚀 Launching Streamlit Web Dashboard at http://localhost:8501"
echo "💡 Press Ctrl+C in terminal to stop."
echo ""

# Run streamlit
streamlit run app.py
