#!/usr/bin/env python3
"""
Test script to verify the Bitcoin Live Analyzer app is working
"""

import os
import sys
import subprocess

def test_app_file():
    """Test if the app file exists and can be imported"""
    print("🔍 Testing app file...")
    
    app_files = ['btc_live_analyzer.py', 'btc_live_analyzer_fixed.py']
    app_file = None
    
    for file in app_files:
        if os.path.exists(file):
            app_file = file
            print(f"✅ Found app file: {file}")
            break
    
    if not app_file:
        print("❌ No app file found!")
        print("Available files:")
        for file in os.listdir('.'):
            if file.endswith('.py'):
                print(f"  - {file}")
        return False
    
    # Test if the file can be parsed
    try:
        with open(app_file, 'r') as f:
            content = f.read()
            compile(content, app_file, 'exec')
        print("✅ App file syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {app_file}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading {app_file}: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are available"""
    print("\n🔍 Testing dependencies...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'requests',
        'sklearn',
        'pyngrok'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run the setup script to install missing dependencies")
        return False
    
    return True

def test_streamlit_command():
    """Test if streamlit command is available"""
    print("\n🔍 Testing Streamlit command...")
    
    try:
        result = subprocess.run(['streamlit', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Streamlit version: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Streamlit command failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Streamlit command timed out")
        return False
    except FileNotFoundError:
        print("❌ Streamlit command not found")
        return False

def test_streamlit_structure():
    """Test if the Streamlit app has proper structure"""
    print("\n🔍 Testing Streamlit app structure...")
    
    try:
        with open('btc_live_analyzer.py', 'r') as f:
            content = f.read()
        
        # Check for set_page_config placement
        lines = content.split('\n')
        streamlit_import_line = None
        set_page_config_line = None
        other_streamlit_calls = []
        
        for i, line in enumerate(lines):
            if 'import streamlit' in line and 'st' in line:
                streamlit_import_line = i + 1
            elif 'st.set_page_config' in line:
                set_page_config_line = i + 1
            elif line.strip().startswith('st.') and 'set_page_config' not in line and line.strip() != '':
                other_streamlit_calls.append(i + 1)
        
        if not streamlit_import_line:
            print("❌ Streamlit import not found")
            return False
        
        if not set_page_config_line:
            print("❌ set_page_config call not found")
            return False
        
        # Check if set_page_config is called early
        if set_page_config_line > 20:
            print(f"⚠️ set_page_config is called late (line {set_page_config_line})")
            return False
        
        # Check if there are Streamlit calls before set_page_config
        early_calls = [line for line in other_streamlit_calls if line < set_page_config_line]
        if early_calls:
            print(f"❌ Found Streamlit calls before set_page_config on lines: {early_calls}")
            return False
        
        print(f"✅ Streamlit structure is correct")
        print(f"   - Import on line {streamlit_import_line}")
        print(f"   - set_page_config on line {set_page_config_line}")
        print(f"   - No early Streamlit calls")
        return True
        
    except Exception as e:
        print(f"❌ Error checking Streamlit structure: {e}")
        return False

def main():
    print("🧪 Bitcoin Live Analyzer - App Test")
    print("=" * 50)
    
    tests = [
        test_app_file,
        test_dependencies,
        test_streamlit_command,
        test_streamlit_structure
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n📊 Test Results:")
    print("=" * 50)
    
    if all(results):
        print("🎉 All tests passed! The app should work correctly.")
        print("\n🚀 You can now run:")
        print("   exec(open('run_tunnel.py').read())")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\n🔧 Troubleshooting steps:")
        print("1. Run the setup script: exec(open('colab_setup_fixed.py').read())")
        print("2. Check file uploads in Colab")
        print("3. Restart the runtime if needed")

if __name__ == "__main__":
    main()