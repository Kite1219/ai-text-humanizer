#!/usr/bin/env python3
"""
Test script for new Undetectable.AI API features
"""

import os
from dotenv import load_dotenv
from src.services.text_humanizer import TextHumanizer
from src.services.streaming_humanizer import StreamingHumanizer

# Load environment
load_dotenv()

def test_credit_checking():
    """Test credit checking functionality."""
    print("🧪 Testing Credit Checking...")
    
    api_key = os.getenv("UNDETECTABLE_API_KEY")
    if not api_key:
        print("❌ API key not found in environment")
        return False
    
    humanizer = TextHumanizer(api_key)
    credits = humanizer.check_credits()
    
    if credits:
        print(f"✅ Credits retrieved successfully!")
        print(f"   Base Credits: {credits.get('baseCredits', 0)}")
        print(f"   Boost Credits: {credits.get('boostCredits', 0)}")
        print(f"   Total Credits: {credits.get('credits', 0)}")
        return True
    else:
        print("❌ Failed to retrieve credits")
        return False

def test_document_listing():
    """Test document listing functionality."""
    print("\n🧪 Testing Document Listing...")
    
    api_key = os.getenv("UNDETECTABLE_API_KEY")
    if not api_key:
        print("❌ API key not found in environment")
        return False
    
    humanizer = TextHumanizer(api_key)
    documents = humanizer.list_documents()
    
    if documents and documents.get("documents"):
        docs = documents["documents"]
        print(f"✅ Found {len(docs)} documents")
        for i, doc in enumerate(docs[:3]):  # Show first 3
            print(f"   Document {i+1}: {doc.get('id', 'N/A')[:8]}...")
        return True
    else:
        print("ℹ️ No documents found (this is normal for new accounts)")
        return True

def test_model_selection():
    """Test model selection functionality."""
    print("\n🧪 Testing Model Selection...")
    
    api_key = os.getenv("UNDETECTABLE_API_KEY")
    if not api_key:
        print("❌ API key not found in environment")
        return False
    
    humanizer = TextHumanizer(api_key)
    
    # Test text for humanization
    test_text = "This is a test text that needs to be humanized. It contains multiple sentences to ensure proper processing. The text should be at least 50 characters long to meet the minimum requirements."
    
    print("   Testing with v11 model...")
    result_v11 = humanizer.humanize_text(
        text=test_text,
        readability="University",
        purpose="General Writing",
        strength="More Human",
        model="v11"
    )
    
    if result_v11 and result_v11.get("output"):
        print(f"   ✅ v11 model: {len(result_v11['output'])} characters")
    else:
        print("   ❌ v11 model failed")
        return False
    
    print("   Testing with v2 model...")
    result_v2 = humanizer.humanize_text(
        text=test_text,
        readability="University",
        purpose="General Writing",
        strength="More Human",
        model="v2"
    )
    
    if result_v2 and result_v2.get("output"):
        print(f"   ✅ v2 model: {len(result_v2['output'])} characters")
        return True
    else:
        print("   ❌ v2 model failed")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing New Undetectable.AI API Features")
    print("=" * 50)
    
    # Test credit checking
    credit_success = test_credit_checking()
    
    # Test document listing
    doc_success = test_document_listing()
    
    # Test model selection
    model_success = test_model_selection()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Credit Checking: {'✅ PASS' if credit_success else '❌ FAIL'}")
    print(f"   Document Listing: {'✅ PASS' if doc_success else '❌ FAIL'}")
    print(f"   Model Selection: {'✅ PASS' if model_success else '❌ FAIL'}")
    
    if all([credit_success, doc_success, model_success]):
        print("\n🎉 All tests passed! New features are working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check your API key and internet connection.")

if __name__ == "__main__":
    main() 