#!/usr/bin/env python3
"""
Test script for OpenRouter integration
"""

import os
from dotenv import load_dotenv
from llm_wrapper import OpenRouterLLM, ChatOpenAI

def test_openrouter_connection():
    """Test basic OpenRouter API connection"""
    print("🧪 Testing OpenRouter Integration...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("   Please set it in your .env file")
        return False
    
    print("✅ OpenRouter API key found")
    
    # Test direct OpenRouter LLM
    try:
        llm = OpenRouterLLM()
        response = llm.invoke("Hello! Please respond with 'OpenRouter is working!'")
        print(f"✅ Direct OpenRouter test: {response[:100]}...")
    except Exception as e:
        print(f"❌ Direct OpenRouter test failed: {e}")
        return False
    
    # Test ChatOpenAI wrapper
    try:
        chat_llm = ChatOpenAI()
        response = chat_llm.invoke("Hello! Please respond with 'ChatOpenAI wrapper is working!'")
        print(f"✅ ChatOpenAI wrapper test: {response[:100]}...")
    except Exception as e:
        print(f"❌ ChatOpenAI wrapper test failed: {e}")
        return False
    
    print("🎉 All OpenRouter tests passed!")
    return True

def test_fallback_mechanism():
    """Test fallback mechanism when primary model fails"""
    print("\n🧪 Testing Fallback Mechanism...")
    
    try:
        # Create LLM with invalid model to trigger fallback
        llm = OpenRouterLLM("invalid-model-name")
        response = llm.invoke("Test fallback")
        print(f"✅ Fallback test: {response[:100]}...")
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
        return False
    
    print("🎉 Fallback mechanism test passed!")
    return True

if __name__ == "__main__":
    print("🚀 Starting OpenRouter Integration Tests\n")
    
    # Test basic connection
    connection_ok = test_openrouter_connection()
    
    # Test fallback mechanism
    fallback_ok = test_fallback_mechanism()
    
    print("\n" + "="*50)
    if connection_ok and fallback_ok:
        print("🎉 All tests passed! OpenRouter integration is working correctly.")
        print("\n📝 Next steps:")
        print("1. Make sure your .env file contains OPENROUTER_API_KEY")
        print("2. Run the main application: streamlit run app.py")
        print("3. Test the LinkedIn Profile Optimizer features")
    else:
        print("❌ Some tests failed. Please check your configuration.")
        print("\n🔧 Troubleshooting:")
        print("1. Verify your OpenRouter API key is correct")
        print("2. Check your internet connection")
        print("3. Ensure you have sufficient credits on OpenRouter")
        print("4. Try running the test again")
