#!/bin/bash

# Wine + MT5 + Python Setup Script for Linux
# This script automates the Wine setup process

set -e

echo "🍷 MetaTrader5 Wine Setup Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Step 1: Install Wine
print_step "Installing Wine and dependencies..."
if ! command -v wine &> /dev/null; then
    sudo apt update
    sudo apt install -y wine winetricks
    print_success "Wine installed"
else
    print_success "Wine already installed"
fi

# Step 2: Initialize Wine
print_step "Initializing Wine configuration..."
if [ ! -d "$HOME/.wine" ]; then
    print_warning "Wine configuration window will open. Set Windows version to 'Windows 10' and click OK."
    winecfg
    print_success "Wine initialized"
else
    print_success "Wine already configured"
fi

# Step 3: Install Visual C++ redistributables
print_step "Installing Visual C++ redistributables..."
winetricks -q vcrun2019 || print_warning "Failed to install vcrun2019 (may already be installed)"

# Step 4: Download and install Python for Windows
print_step "Setting up Python for Windows in Wine..."
mkdir -p ~/Downloads
cd ~/Downloads

PYTHON_INSTALLER="python-3.8.10-amd64.exe"
if [ ! -f "$PYTHON_INSTALLER" ]; then
    print_step "Downloading Python 3.8.10 for Windows..."
    wget https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
fi

# Check if Python is already installed in Wine
if ! wine python --version &>/dev/null; then
    print_step "Installing Python in Wine..."
    print_warning "Python installer will open. IMPORTANT:"
    print_warning "1. Check 'Add Python 3.8 to PATH'"
    print_warning "2. Check 'Install for all users'"
    print_warning "3. Choose 'Customize installation' and enable all features"
    
    wine python-3.8.10-amd64.exe
    print_success "Python installation completed"
else
    print_success "Python already installed in Wine"
fi

# Step 5: Verify Python installation
print_step "Verifying Python installation in Wine..."
if wine python --version &>/dev/null; then
    PYTHON_VERSION=$(wine python --version 2>/dev/null)
    print_success "Python verified: $PYTHON_VERSION"
else
    print_error "Python installation failed or not in PATH"
    print_warning "You may need to reinstall Python and ensure 'Add Python to PATH' is checked"
    exit 1
fi

# Step 6: Download and install MT5
print_step "Setting up MetaTrader5..."
MT5_INSTALLER="mt5setup.exe"
if [ ! -f "$MT5_INSTALLER" ]; then
    print_step "Downloading MT5 installer..."
    wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe
fi

# Check if MT5 is already installed
if [ ! -f "$HOME/.wine/drive_c/Program Files/MetaTrader 5/terminal64.exe" ]; then
    print_step "Installing MetaTrader5..."
    print_warning "MT5 installer will open. Follow the installation wizard."
    wine mt5setup.exe
    print_success "MT5 installation completed"
else
    print_success "MT5 already installed"
fi

# Step 7: Install MetaTrader5 Python package in Wine
print_step "Installing MetaTrader5 Python package in Wine..."
wine python -m pip install --upgrade pip
wine python -m pip install MetaTrader5

# Verify MT5 package installation
if wine python -c "import MetaTrader5; print('MT5 package OK')" &>/dev/null; then
    print_success "MetaTrader5 Python package installed successfully"
else
    print_error "Failed to install MetaTrader5 Python package"
    exit 1
fi

# Step 8: Install pymt5linux bridge in Wine
print_step "Installing pymt5linux bridge in Wine..."
wine python -m pip install pymt5linux

if wine python -c "import pymt5linux; print('pymt5linux OK')" &>/dev/null; then
    print_success "pymt5linux bridge installed successfully"
else
    print_error "Failed to install pymt5linux bridge"
    exit 1
fi

# Step 9: Create startup scripts
print_step "Creating startup scripts..."

# Create MT5 launcher script
cat > start_mt5.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting MetaTrader5..."
wine ~/.wine/drive_c/Program\ Files/MetaTrader\ 5/terminal64.exe
EOF
chmod +x start_mt5.sh

# Create bridge server script
cat > start_mt5_bridge.sh << 'EOF'
#!/bin/bash
echo "🌉 Starting MT5 Bridge Server..."
echo "Make sure MT5 terminal is running first!"
sleep 5
wine cmd /c "python -m pymt5linux C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python38\python.exe"
EOF
chmod +x start_mt5_bridge.sh

print_success "Startup scripts created: start_mt5.sh, start_mt5_bridge.sh"

echo ""
echo "🎉 Wine + MT5 + Python setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Run: ./start_mt5.sh (start MT5 terminal)"
echo "2. In MT5: File → Open an Account → Create demo account"
echo "3. Enable 'Algorithmic Trading' button (green)"
echo "4. Run: ./start_mt5_bridge.sh (start bridge server)"
echo "5. In another terminal: source mt5_env/bin/activate && python test_mt5_connection.py"
echo ""
echo "📖 For detailed usage instructions, see: MT5_Linux_Step_by_Step_Setup.md"
echo ""
print_warning "IMPORTANT: Always test with DEMO accounts first!"