#!/bin/bash

# MetaTrader5 Linux Installation Script
# This script installs pymt5linux in a virtual environment

set -e

echo "🚀 MetaTrader5 Linux Installation Script"
echo "========================================"

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if python3-venv is available
if ! python3 -c "import venv" &> /dev/null; then
    echo "❌ python3-venv is not available. Installing..."
    sudo apt update
    sudo apt install -y python3-venv
fi

# Create virtual environment
ENV_NAME="mt5_env"
echo "📦 Creating virtual environment: $ENV_NAME"
python3 -m venv $ENV_NAME

# Activate virtual environment and install packages
echo "📥 Installing pymt5linux..."
source $ENV_NAME/bin/activate
pip install --upgrade pip
pip install pymt5linux

# Test installation
echo "🧪 Testing installation..."
python -c "
try:
    import pymt5linux
    print('✅ pymt5linux installed successfully!')
    from pymt5linux import MetaTrader5
    print('✅ MetaTrader5 class imported successfully!')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Install Wine: sudo apt install wine"
echo "2. Install Python for Windows in Wine"
echo "3. Install MetaTrader5 terminal in Wine"
echo "4. Install MetaTrader5 Python package in Wine Python"
echo ""
echo "💡 To activate the virtual environment:"
echo "   source $ENV_NAME/bin/activate"
echo ""
echo "📖 For detailed setup instructions, see: MetaTrader5_Linux_Installation_Guide.md"