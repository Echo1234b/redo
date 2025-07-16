#!/usr/bin/env python3
"""
Test script to verify the Streamlit app structure is correct
"""

import ast
import sys

def test_streamlit_structure():
    """Test if the Streamlit app has proper structure"""
    print("🧪 Testing Streamlit app structure...")
    
    try:
        with open('btc_live_analyzer.py', 'r') as f:
            content = f.read()
        
        # Parse the AST to check structure
        tree = ast.parse(content)
        
        # Find all function calls
        streamlit_calls = []
        set_page_config_calls = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == 'st':
                        call_name = node.func.attr
                        streamlit_calls.append((call_name, node.lineno))
                        if call_name == 'set_page_config':
                            set_page_config_calls.append(node.lineno)
        
        # Check results
        print(f"📊 Found {len(streamlit_calls)} Streamlit calls")
        print(f"📊 Found {len(set_page_config_calls)} set_page_config calls")
        
        if len(set_page_config_calls) == 0:
            print("❌ No set_page_config call found!")
            return False
        elif len(set_page_config_calls) > 1:
            print(f"❌ Multiple set_page_config calls found on lines: {set_page_config_calls}")
            return False
        else:
            config_line = set_page_config_calls[0]
            print(f"✅ Single set_page_config call found on line {config_line}")
            
            # Check if it's early in the file (should be within first 20 lines)
            if config_line <= 20:
                print("✅ set_page_config is called early in the script")
                
                # Check if there are any other Streamlit calls before it
                early_calls = [call for call in streamlit_calls if call[1] < config_line and call[0] != 'set_page_config']
                if early_calls:
                    print(f"❌ Found Streamlit calls before set_page_config: {early_calls}")
                    return False
                else:
                    print("✅ No Streamlit calls before set_page_config")
                    return True
            else:
                print(f"⚠️ set_page_config is called late in the script (line {config_line})")
                return False
                
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")
        return False

def test_import_structure():
    """Test if imports are structured correctly"""
    print("\n🔍 Testing import structure...")
    
    try:
        with open('btc_live_analyzer.py', 'r') as f:
            lines = f.readlines()
        
        # Find the set_page_config line
        config_line = None
        for i, line in enumerate(lines):
            if 'st.set_page_config' in line:
                config_line = i + 1
                break
        
        if config_line:
            print(f"✅ set_page_config found on line {config_line}")
            
            # Check if streamlit import is before set_page_config
            streamlit_import_line = None
            for i, line in enumerate(lines):
                if 'import streamlit' in line and i < config_line:
                    streamlit_import_line = i + 1
                    break
            
            if streamlit_import_line:
                print(f"✅ Streamlit import found on line {streamlit_import_line} (before set_page_config)")
                return True
            else:
                print("❌ Streamlit import not found before set_page_config")
                return False
        else:
            print("❌ set_page_config not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking imports: {e}")
        return False

def main():
    print("🔧 Streamlit Structure Test")
    print("=" * 50)
    
    tests = [
        test_streamlit_structure,
        test_import_structure
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n📊 Test Results:")
    print("=" * 50)
    
    if all(results):
        print("🎉 All tests passed! The Streamlit app structure is correct.")
        print("✅ The set_page_config error should be fixed.")
        return True
    else:
        print("❌ Some tests failed. The app may still have issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)