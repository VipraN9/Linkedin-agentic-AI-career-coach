#!/usr/bin/env python3
"""
Test script for LinkedIn Profile Optimizer
Run this to verify all components are working correctly
"""

import os
import sys
import json
from unittest.mock import Mock

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import config
        print("✅ Config imported successfully")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from linkedin_scraper import LinkedInScraper
        print("✅ LinkedIn Scraper imported successfully")
    except Exception as e:
        print(f"❌ LinkedIn Scraper import failed: {e}")
        return False
    
    try:
        from profile_analyzer import ProfileAnalyzer
        print("✅ Profile Analyzer imported successfully")
    except Exception as e:
        print(f"❌ Profile Analyzer import failed: {e}")
        return False
    
    try:
        from job_analyzer import JobAnalyzer
        print("✅ Job Analyzer imported successfully")
    except Exception as e:
        print(f"❌ Job Analyzer import failed: {e}")
        return False
    
    try:
        from content_generator import ContentGenerator
        print("✅ Content Generator imported successfully")
    except Exception as e:
        print(f"❌ Content Generator import failed: {e}")
        return False
    
    try:
        from memory_system import ProfileMemorySystem
        print("✅ Memory System imported successfully")
    except Exception as e:
        print(f"❌ Memory System import failed: {e}")
        return False
    
    try:
        from chat_agent import LinkedInChatAgent
        print("✅ Chat Agent imported successfully")
    except Exception as e:
        print(f"❌ Chat Agent import failed: {e}")
        return False
    
    return True

def test_memory_system():
    """Test memory system functionality"""
    print("\n🧠 Testing Memory System...")
    
    try:
        from memory_system import ProfileMemorySystem
        memory = ProfileMemorySystem()
        
        # Test user session creation
        user_id = "test_user_123"
        session = memory.get_user_session(user_id)
        assert session is not None
        print("✅ User session created successfully")
        
        # Test message addition
        memory.add_message(user_id, "Hello, this is a test message")
        context = memory.get_conversation_context(user_id)
        assert len(context) > 0
        print("✅ Message added to memory successfully")
        
        # Test persistent memory
        persistent = memory.get_user_persistent(user_id)
        assert persistent is not None
        print("✅ Persistent memory created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory system test failed: {e}")
        return False

def test_profile_analyzer():
    """Test profile analyzer with mock data"""
    print("\n📊 Testing Profile Analyzer...")
    
    try:
        from profile_analyzer import ProfileAnalyzer
        analyzer = ProfileAnalyzer()
        
        # Mock profile data
        mock_profile = {
            "basic_info": {
                "full_name": "John Doe",
                "headline": "Software Engineer | Python Developer",
                "summary": "Experienced software engineer with 5 years in development.",
                "location": "San Francisco, CA"
            },
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "duration": "2021 - Present",
                    "description": "Developed web applications using Python and React."
                }
            ],
            "skills": [
                {"name": "Python", "endorsements": 25},
                {"name": "JavaScript", "endorsements": 20},
                {"name": "React", "endorsements": 15}
            ],
            "education": [
                {
                    "school": "University of California",
                    "degree": "Bachelor of Science",
                    "field": "Computer Science"
                }
            ]
        }
        
        # Analyze profile
        analysis = analyzer.analyze_profile(mock_profile)
        
        # Check that analysis contains expected keys
        expected_keys = ["overall_score", "strengths", "weaknesses", "recommendations"]
        for key in expected_keys:
            assert key in analysis
        print("✅ Profile analysis completed successfully")
        
        # Check that scores are reasonable
        assert 0 <= analysis["overall_score"] <= 100
        print("✅ Analysis scores are within expected range")
        
        return True
        
    except Exception as e:
        print(f"❌ Profile analyzer test failed: {e}")
        return False

def test_job_analyzer():
    """Test job analyzer with mock data"""
    print("\n💼 Testing Job Analyzer...")
    
    try:
        from job_analyzer import JobAnalyzer
        analyzer = JobAnalyzer()
        
        # Mock profile data
        mock_profile = {
            "basic_info": {
                "headline": "Software Engineer | Python Developer",
                "summary": "Experienced software engineer with Python and JavaScript."
            },
            "experience": [
                {
                    "title": "Software Engineer",
                    "description": "Developed applications using Python, JavaScript, and React."
                }
            ],
            "skills": [
                {"name": "Python", "endorsements": 25},
                {"name": "JavaScript", "endorsements": 20},
                {"name": "React", "endorsements": 15}
            ]
        }
        
        # Test job fit analysis
        job_analysis = analyzer.analyze_job_fit(mock_profile, "Software Engineer")
        
        # Check that analysis contains expected keys
        expected_keys = ["overall_match_score", "required_skills_match", "preferred_skills_match"]
        for key in expected_keys:
            assert key in job_analysis
        print("✅ Job fit analysis completed successfully")
        
        # Check that match score is reasonable
        assert 0 <= job_analysis["overall_match_score"] <= 100
        print("✅ Job match score is within expected range")
        
        return True
        
    except Exception as e:
        print(f"❌ Job analyzer test failed: {e}")
        return False

def test_content_generator():
    """Test content generator with mock data"""
    print("\n✍️ Testing Content Generator...")
    
    try:
        from content_generator import ContentGenerator
        generator = ContentGenerator()
        
        # Mock profile data
        mock_profile = {
            "basic_info": {
                "headline": "Software Engineer",
                "summary": "Experienced developer."
            },
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "description": "Developed web applications."
                }
            ],
            "skills": [
                {"name": "Python", "endorsements": 25},
                {"name": "JavaScript", "endorsements": 20}
            ]
        }
        
        # Test headline generation
        headlines = generator.generate_enhanced_headline(mock_profile)
        assert "achievement_focused" in headlines
        assert "skill_focused" in headlines
        assert "value_focused" in headlines
        print("✅ Enhanced headlines generated successfully")
        
        # Test summary generation
        summaries = generator.generate_enhanced_summary(mock_profile)
        assert "story_focused" in summaries
        assert "achievement_focused" in summaries
        print("✅ Enhanced summaries generated successfully")
        
        # Test experience enhancement
        experience_enhancements = generator.generate_experience_enhancements(mock_profile)
        assert "enhanced_experiences" in experience_enhancements
        print("✅ Experience enhancements generated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Content generator test failed: {e}")
        return False

def test_chat_agent():
    """Test chat agent functionality"""
    print("\n💬 Testing Chat Agent...")
    
    try:
        from chat_agent import LinkedInChatAgent
        agent = LinkedInChatAgent()
        
        # Test help request
        help_response = agent._handle_help_request()
        assert "Profile Analysis" in help_response
        assert "Job Fit Analysis" in help_response
        print("✅ Help request handled successfully")
        
        # Test intent detection
        intent = agent._determine_intent("https://linkedin.com/in/test")
        assert intent == "profile_analysis"
        print("✅ Intent detection working correctly")
        
        intent = agent._determine_intent("I want to apply for a software engineer job")
        assert intent == "job_analysis"
        print("✅ Job analysis intent detected correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Chat agent test failed: {e}")
        print("   This might be due to missing OpenRouter API key")
        return False

def test_config():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        import config
        
        # Check that required config values exist
        assert hasattr(config, 'APP_NAME')
        assert hasattr(config, 'APP_VERSION')
        assert hasattr(config, 'MEMORY_TTL')
        assert hasattr(config, 'MAX_MEMORY_SIZE')
        print("✅ Configuration loaded successfully")
        
        # Check that config values are reasonable
        assert config.MEMORY_TTL > 0
        assert config.MAX_MEMORY_SIZE > 0
        print("✅ Configuration values are valid")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting LinkedIn Profile Optimizer Tests\n")
    
    tests = [
        ("Configuration", test_config),
        ("Imports", test_imports),
        ("Memory System", test_memory_system),
        ("Profile Analyzer", test_profile_analyzer),
        ("Job Analyzer", test_job_analyzer),
        ("Content Generator", test_content_generator),
        ("Chat Agent", test_chat_agent),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED\n")
            else:
                print(f"❌ {test_name} test FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application, run:")
        print("streamlit run app.py")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
