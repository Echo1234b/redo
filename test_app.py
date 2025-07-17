#!/usr/bin/env python3
"""
MetaTrader 5 Bitcoin Live Analyzer - Test Suite
Comprehensive testing for MT5 integration and app functionality
"""

import os
import sys
import subprocess

def test_app_file():
    """Test if the MT5 app file exists and can be imported"""
    print("🔍 Testing MT5 app file...")
    
    app_files = ['btc_live_analyzer_mt5.py']
    app_file = None
    
    for file in app_files:
        if os.path.exists(file):
            app_file = file
            print(f"✅ Found app file: {file}")
            break
    
    if not app_file:
        print("❌ No MT5 app file found!")
        print("Looking for: btc_live_analyzer_mt5.py")
        return False
    
    # Test if the file can be parsed
    try:
        with open(app_file, 'r') as f:
            content = f.read()
            compile(content, app_file, 'exec')
        print("✅ MT5 app file syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {app_file}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading {app_file}: {e}")
        return False

def test_mt5_dependencies():
    """Test if MetaTrader 5 dependencies are available"""
    print("\n🔍 Testing MT5 dependencies...")
    
    required_packages = [
        'MetaTrader5',
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'sklearn',
        'pyngrok'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'MetaTrader5':
                import MetaTrader5
                print(f"✅ {package} - Version: {MetaTrader5.__version__ if hasattr(MetaTrader5, '__version__') else 'Available'}")
            elif package == 'sklearn':
                import sklearn
                print(f"✅ {package} - Version: {sklearn.__version__}")
            else:
                __import__(package)
                print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run the MT5 setup script to install missing dependencies")
        return False
    
    return True

def test_mt5_integration():
    """Test if MT5 integration module exists and is valid"""
    print("\n🔍 Testing MT5 integration module...")
    
    if not os.path.exists('metatrader_integration.py'):
        print("❌ metatrader_integration.py not found!")
        return False
    
    try:
        with open('metatrader_integration.py', 'r') as f:
            content = f.read()
            compile(content, 'metatrader_integration.py', 'exec')
        print("✅ MT5 integration module syntax is valid")
        
        # Test if key classes are defined
        if 'class MetaTraderDataProvider' in content:
            print("✅ MetaTraderDataProvider class found")
        else:
            print("❌ MetaTraderDataProvider class not found")
            return False
            
        if 'class MetaTraderStreamlitUI' in content:
            print("✅ MetaTraderStreamlitUI class found")
        else:
            print("❌ MetaTraderStreamlitUI class not found")
            return False
        
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in metatrader_integration.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading metatrader_integration.py: {e}")
        return False

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
    """Test if the MT5 Streamlit app has proper structure"""
    print("\n🔍 Testing Streamlit app structure...")
    
    try:
        with open('btc_live_analyzer_mt5.py', 'r') as f:
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

def test_setup_script():
    """Test if the MT5 setup script exists and is valid"""
    print("\n🔍 Testing MT5 setup script...")
    
    if not os.path.exists('colab_setup_mt5.py'):
        print("❌ colab_setup_mt5.py not found!")
        return False
    
    try:
        with open('colab_setup_mt5.py', 'r') as f:
            content = f.read()
            compile(content, 'colab_setup_mt5.py', 'exec')
        print("✅ MT5 setup script syntax is valid")
        
        # Check for key functions
        if 'def install_metatrader5' in content:
            print("✅ install_metatrader5 function found")
        else:
            print("❌ install_metatrader5 function not found")
            return False
        
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in colab_setup_mt5.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading colab_setup_mt5.py: {e}")
        return False

def test_documentation():
    """Test if essential documentation exists"""
    print("\n🔍 Testing documentation...")
    
    docs = [
        'MT5_DATA_IMPORT_GUIDE.md',
        'METATRADER_INTEGRATION_GUIDE.md'
    ]
    
    missing_docs = []
    for doc in docs:
        if os.path.exists(doc):
            print(f"✅ {doc} found")
        else:
            print(f"❌ {doc} missing")
            missing_docs.append(doc)
    
    return len(missing_docs) == 0

def main():
    print("🧪 MetaTrader 5 Bitcoin Live Analyzer - Test Suite")
    print("=" * 60)
    
    tests = [
        test_app_file,
        test_mt5_dependencies,
        test_mt5_integration,
        test_streamlit_command,
        test_streamlit_structure,
        test_setup_script,
        test_documentation
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n📊 Test Results:")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print("🎉 All tests passed! The MT5 app should work correctly.")
        print("\n🚀 Ready to run:")
        print("   1. exec(open('colab_setup_mt5.py').read())")
        print("   2. exec(open('run_tunnel_mt5.py').read())")
        print("\n📋 Requirements:")
        print("   - MetaTrader 5 terminal installed and running")
        print("   - MT5 account credentials")
        print("   - Algorithmic trading enabled in MT5")
    else:
        print(f"❌ {total - passed} out of {total} tests failed.")
        print("\n🔧 Troubleshooting steps:")
        print("1. Run the MT5 setup script: exec(open('colab_setup_mt5.py').read())")
        print("2. Check if all required files are uploaded")
        print("3. Verify MetaTrader 5 terminal is installed")
        print("4. Restart the runtime if needed")

if __name__ == "__main__":
    main()