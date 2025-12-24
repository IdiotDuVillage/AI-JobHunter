#!/bin/bash

cd "$(dirname "$0")"

echo "🍎 Launching Job Hunter AI..."

# 1. Verification / Creation of venv
if [ ! -d "venv" ]; then
    echo "📦 First launching, Installation of dependencies..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt

    echo "✅ Successful installation"
fi

# 2. Lauching
echo "🚀 Opening interface..."
if [ -f "./venv/bin/streamlit" ]; then
    ./venv/bin/streamlit run gui.py
else
    echo "❌ Error, Streamlit is not properly installed"
    echo "Fixing installation"
    ./venv/bin/pip install streamlit
    ./venv/bin/streamlit run gui.py
fi
