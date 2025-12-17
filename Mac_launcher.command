#!/bin/bash

cd "$(dirname "$0")"

echo "🍎 Launching Job Hunter AI..."

# 1. Verification / Creation of venv
if [ ! -d "venv" ]; then
    echo "📦 First launching, Installation of dependencies..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 2. Lauching
echo "🚀 Opening interface..."
streamlit run gui.py