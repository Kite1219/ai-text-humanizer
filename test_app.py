#!/usr/bin/env python3
"""
Test script for AI Text Humanizer
Verifies that all components work correctly.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from src.config.settings import Settings
        print("✅ Settings imported successfully")
    except ImportError as e:
        print(f"❌ Settings import failed: {e}")
        return False
    
    try:
        from src.services.text_humanizer import TextHumanizer
        print("✅ TextHumanizer imported successfully")
    except ImportError as e:
        print(f"❌ TextHumanizer import failed: {e}")
        return False
    
    try:
        from src.services.ai_detector import AIDetector
        print("✅ AIDetector imported successfully")
    except ImportError as e:
        print(f"❌ AIDetector import failed: {e}")
        return False
    
    return True

def test_api_key():
    """Test API key configuration."""
    print("\n🔑 Testing API key configuration...")
    
    try:
        from src.config.settings import Settings
        settings = Settings()
        api_key = settings.get_api_key()
        
        if api_key:
            print("✅ API key found")
            return True
        else:
            print("⚠️  No API key found in .env file")
            print("   This is normal for testing, but required for text humanization")
            return True
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

def test_ai_detector():
    """Test AI detector functionality."""
    print("\n🤖 Testing AI detector...")
    
    try:
        from src.services.ai_detector import AIDetector
        detector = AIDetector()
        
        # Test with AI-like text
        ai_text = "The implementation of artificial intelligence methodologies has facilitated comprehensive analysis of complex datasets. Furthermore, the systematic approach to data processing has yielded significant improvements in computational efficiency."
        
        result = detector.detect_ai(ai_text)
        
        if result and "score" in result:
            print(f"✅ AI detector working - Score: {result['score']:.2f}")
            print(f"   Result: {result['result']}")
            return True
        else:
            print("❌ AI detector returned invalid result")
            return False
    except Exception as e:
        print(f"❌ AI detector test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "app.py",
        "run.py",
        "requirements.txt",
        "README.md",
        "src/config/settings.py",
        "src/services/text_humanizer.py",
        "src/services/ai_detector.py",
        "src/ui/menu_manager.py",
        "src/utils/utils.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def test_streamlit_app():
    """Test that the Streamlit app can be imported."""
    print("\n🌐 Testing Streamlit app...")
    
    try:
        # This is a basic test - we can't actually run Streamlit in this context
        # but we can check if the file is syntactically correct
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Basic syntax check
        compile(content, "app.py", "exec")
        print("✅ Streamlit app syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Streamlit app syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Streamlit app test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 AI Text Humanizer Test Suite")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("API Key", test_api_key),
        ("AI Detector", test_ai_detector),
        ("Streamlit App", test_streamlit_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your app is ready for deployment.")
        print("\n🚀 To deploy:")
        print("1. Run: python deploy.py")
        print("2. Follow the deployment instructions")
    else:
        print("⚠️  Some tests failed. Please fix the issues before deploying.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 