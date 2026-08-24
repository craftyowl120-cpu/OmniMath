#!/bin/bash
# This script automatically activates the project's local virtual environment
# and launches the Streamlit app, ensuring the correct Python is always used.

# 1. Navigate to the project directory
cd /Users/szanmasood/OmniMath

# 2. Check if the virtual environment exists, if so, activate it
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Local environment activated."
else
    echo "❌ Error: Virtual environment 'venv' not found."
    echo "Please run: cd /Users/szanmasood/OmniMath && python3 -m venv venv && source venv/bin/activate && pip install streamlit sympy"
    exit 1
fi

# 3. Launch the application
echo "🚀 Launching OmniMath Assistant..."
streamlit run app.py
