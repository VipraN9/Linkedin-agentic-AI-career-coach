from typing import Dict, List, Optional, Any
from llm_wrapper import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
import json
import re
import config
from linkedin_scraper import LinkedInScraper
from profile_analyzer import ProfileAnalyzer
from job_analyzer import JobAnalyzer
from content_generator import ContentGenerator
from memory_system import ProfileMemorySystem

class LinkedInChatAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config.FREE_LLM_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            api_key=config.OPENROUTER_API_KEY
        )
        
        # Initializing components
        self.scraper = LinkedInScraper()
        self.profile_analyzer = ProfileAnalyzer()
        self.job_analyzer = JobAnalyzer()
        self.content_generator = ContentGenerator()
        self.memory_system = ProfileMemorySystem()
        
        # System prompt for the chat agent
        self.system_prompt = """
        You are an AI-powered LinkedIn profile optimization assistant. Your role is to help users improve their LinkedIn profiles, analyze job fit, and provide career guidance.

        Your capabilities include:
        1. Analyzing LinkedIn profiles for strengths and weaknesses
        2. Comparing profiles with job descriptions and calculating match scores
        3. Generating enhanced content for profile sections
        4. Providing personalized career guidance and skill development recommendations
        5. Maintaining conversation context and user preferences

        Always be helpful, professional, and encouraging. Provide specific, actionable advice and explain your reasoning clearly.
        """
    
    def process_message(self, user_id: str, message: str) -> str:
        """Process user message and return appropriate response"""
        try:
            # Adding message to memory
            self.memory_system.add_message(user_id, message, "user")
            
            # conversation context
            context = self.memory_system.get_conversation_context(user_id)
            profile_data = self.memory_system.get_profile_context(user_id)
            user_preferences = self.memory_system.get_user_preferences(user_id)
            
            # intent and generate response
            intent = self._determine_intent(message)
            response = self._generate_response(user_id, message, intent, profile_data, user_preferences, context)
            
            # Add response to memory
            self.memory_system.add_message(user_id, response, "assistant")
            
            return response
            
        except Exception as e:
            print(f"Error processing message: {e}")
            return "I apologize, but I encountered an error processing your message. Please try again."
    
    def _determine_intent(self, message: str) -> str:
        """Determine the user's intent from their message"""
        message_lower = message.lower()
        
        # LinkedIn URL detection
        if "linkedin.com" in message_lower or "linkedin.com/in/" in message_lower:
            return "profile_analysis"
        
        # Job analysis intent
        if any(keyword in message_lower for keyword in ["job", "role", "position", "career", "apply", "match"]):
            return "job_analysis"
        
        # Content generation intent
        if any(keyword in message_lower for keyword in ["improve", "enhance", "rewrite", "better", "optimize"]):
            return "content_generation"
        
        # Career guidance intent
        if any(keyword in message_lower for keyword in ["career", "path", "guidance", "advice", "future", "goal"]):
            return "career_guidance"
        
        # General help
        if any(keyword in message_lower for keyword in ["help", "what can you do", "capabilities", "features"]):
            return "help"
        
        # Default to general conversation
        return "general"
    
    def _generate_response(self, user_id: str, message: str, intent: str, profile_data: Optional[Dict], 
                          user_preferences: Dict, context: List[Dict]) -> str:
        """Generate appropriate response based on intent"""
        
        if intent == "profile_analysis":
            return self._handle_profile_analysis(user_id, message, profile_data)
        
        elif intent == "job_analysis":
            return self._handle_job_analysis(user_id, message, profile_data)
        
        elif intent == "content_generation":
            return self._handle_content_generation(user_id, message, profile_data)
        
        elif intent == "career_guidance":
            return self._handle_career_guidance(user_id, message, profile_data, user_preferences)
        
        elif intent == "help":
            return self._handle_help_request()
        
        else:
            return self._handle_general_conversation(user_id, message, profile_data, context)
    
    def _handle_profile_analysis(self, user_id: str, message: str, profile_data: Optional[Dict]) -> str:
        """Handle LinkedIn profile analysis requests"""
        try:
            # Extracting LinkedIn URL from message
            linkedin_url = self._extract_linkedin_url(message)
            
            if not linkedin_url:
                return "I couldn't find a LinkedIn URL in your message. Please provide a valid LinkedIn profile URL to analyze."
            
            # Scraping profile data
            profile_data = self.scraper.scrape_profile(linkedin_url)
            
            if not profile_data:
                # Checking if it's a private profile issue
                cookies = self.scraper._get_linkedin_cookie()
                has_valid_cookies = len(cookies) > 0 and any('li_at' in cookie.get('name', '') for cookie in cookies)
                
                if not has_valid_cookies:
                    return """❌ **Profile Analysis Failed**

The profile you're trying to analyze appears to be private or requires authentication.

**Possible Solutions:**

1. **For Public Profiles:** Make sure the profile is set to public visibility
2. **For Private Profiles:** Add LinkedIn authentication cookies to access private profiles

**How to Add LinkedIn Cookies:**
1. Go to LinkedIn.com and log in
2. Open browser DevTools (F12)
3. Go to Application/Storage tab → Cookies → https://www.linkedin.com
4. Find these cookies: `li_at` and `JSESSIONID`
5. Add to your `.env` file:
   ```
   LINKEDIN_COOKIE=li_at=YOUR_LI_AT_VALUE; JSESSIONID=YOUR_JSESSIONID_VALUE
   ```

**Note:** Public profiles like Bill Gates, Satya Nadella, etc. work without cookies."""
                else:
                    return "I encountered an error analyzing your profile. The profile might not exist or be accessible. Please check the URL and try again."
            
            # Storing profile data in memory
            self.memory_system.update_profile_data(user_id, profile_data)
            
            # Analyzing profile
            analysis = self.profile_analyzer.analyze_profile(profile_data)
            
            # Generating response
            response = self._format_profile_analysis_response(analysis, profile_data)
            
            return response
            
        except Exception as e:
            print(f"Error in profile analysis: {e}")
            return "I encountered an error analyzing your profile. Please try again with a valid LinkedIn URL."
    
    def _handle_job_analysis(self, user_id: str, message: str, profile_data: Optional[Dict]) -> str:
        """Handle job analysis requests"""
        try:
            # profile data from memory if not provided
            if not profile_data:
                profile_data = self.memory_system.get_profile_context(user_id)
            
            if not profile_data:
                return "I don't have your profile data yet. Please analyze your LinkedIn profile first by providing your LinkedIn URL, then I can help you with job fit analysis."
            
            # Extracting job role from message
            job_role = self._extract_job_role(message)
            
            if not job_role:
                return "I couldn't identify a specific job role in your message. Please specify which role you're interested in (e.g., 'Software Engineer', 'Data Scientist', 'Product Manager')."
            
            # Analyzing job fit
            job_analysis = self.job_analyzer.analyze_job_fit(profile_data, job_role)
            
            # Generating response
            response = self._format_job_analysis_response(job_analysis)
            
            return response
            
        except Exception as e:
            print(f"Error in job analysis: {e}")
            return "I encountered an error analyzing your job fit. Please try again."
    
    def _handle_content_generation(self, user_id: str, message: str, profile_data: Optional[Dict]) -> str:
        """Handle content generation requests"""
        try:
            # profile data from memory if not provided
            if not profile_data:
                profile_data = self.memory_system.get_profile_context(user_id)
            
            if not profile_data:
                return "I don't have your profile data yet. Please analyze your LinkedIn profile first by providing your LinkedIn URL, then I can help you improve your content."
            
            # Determining what content to generate
            if "headline" in message.lower():
                enhanced_headlines = self.content_generator.generate_enhanced_headline(profile_data)
                return self._format_headline_suggestions(enhanced_headlines)
            
            elif "summary" in message.lower():
                enhanced_summaries = self.content_generator.generate_enhanced_summary(profile_data)
                return self._format_summary_suggestions(enhanced_summaries)
            
            elif "experience" in message.lower():
                enhanced_experience = self.content_generator.generate_experience_enhancements(profile_data)
                return self._format_experience_suggestions(enhanced_experience)
            
            else:
                # all content improvements
                return self._generate_all_content_improvements(profile_data)
            
        except Exception as e:
            print(f"Error in content generation: {e}")
            return "I encountered an error generating content improvements. Please try again."
    
    def _handle_career_guidance(self, user_id: str, message: str, profile_data: Optional[Dict], user_preferences: Dict) -> str:
        """Handle career guidance requests"""
        try:
            # profile data from memory if not provided
            if not profile_data:
                profile_data = self.memory_system.get_profile_context(user_id)
            
            if not profile_data:
                return "I don't have your profile data yet. Please analyze your LinkedIn profile first by providing your LinkedIn URL, then I can provide personalized career guidance."
            
            # Extracingt career goals from message
            career_goals = self._extract_career_goals(message)
            
            # Updating user preferences
            if career_goals:
                self.memory_system.update_career_goals(user_id, career_goals)
            
            # Generating career guidance
            guidance = self.content_generator.generate_career_guidance(profile_data, career_goals)
            
            # Generating response
            response = self._format_career_guidance_response(guidance)
            
            return response
            
        except Exception as e:
            print(f"Error in career guidance: {e}")
            return "I encountered an error generating career guidance. Please try again."
    
    def _handle_help_request(self) -> str:
        """Handle help requests"""
        return """
        I'm your LinkedIn profile optimization assistant! Here's what I can help you with:

        🔍 **Profile Analysis**
        - Analyze your LinkedIn profile for strengths and weaknesses
        - Provide detailed feedback on each section
        - Calculate profile completeness and optimization scores

        💼 **Job Fit Analysis**
        - Compare your profile with specific job roles
        - Calculate match scores and identify skill gaps
        - Provide targeted recommendations for job applications

        ✨ **Content Enhancement**
        - Generate improved headlines, summaries, and experience descriptions
        - Provide multiple versions with different approaches
        - Optimize content for better visibility and impact

        🎯 **Career Guidance**
        - Suggest potential career paths based on your profile
        - Create personalized skill development plans
        - Recommend learning resources and courses

        To get started, simply share your LinkedIn profile URL and let me know what you'd like to work on!
        """
    
    def _handle_general_conversation(self, user_id: str, message: str, profile_data: Optional[Dict], context: List[Dict]) -> str:
        """Handle general conversation"""
        try:
            # single prompt string for the LLM (our wrapper expects a string)
            recent_turns = []
            for msg in context[-5:]:
                role = "User" if msg.get("sender") == "user" else "Assistant"
                recent_turns.append(f"{role}: {msg.get('message','').strip()}")

            profile_bits = []
            if profile_data:
                name = profile_data.get("basic_info", {}).get("full_name")
                headline = profile_data.get("basic_info", {}).get("headline")
                if name:
                    profile_bits.append(f"Name: {name}")
                if headline:
                    profile_bits.append(f"Headline: {headline}")

            style_instructions = (
                "Be concise, warm, and practical. Avoid generic greetings. "
                "Offer one specific, actionable next step related to LinkedIn when appropriate."
            )

            prompt = (
                f"System: {self.system_prompt.strip()}\n"
                + (f"Context: {' | '.join(profile_bits)}\n" if profile_bits else "")
                + ("\n".join(recent_turns) + "\n" if recent_turns else "")
                + f"User: {message.strip()}\n"
                + f"Assistant ({style_instructions}):"
            )

            response_text = self.llm.invoke(prompt)
            return response_text.strip()

        except Exception as e:
            print(f"Error in general conversation: {e}")
            # More organic fallback
            return (
                "Thanks for the message—happy to help with your LinkedIn. "
                "Tell me what you’d like to improve first (headline, summary, experience, or job fit), "
                "and I’ll give you a concrete next step."
            )
    
    def _extract_linkedin_url(self, message: str) -> Optional[str]:
        """Extract LinkedIn URL from message"""
        # Simple regex to find LinkedIn URLs
        linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9-]+/?'
        match = re.search(linkedin_pattern, message)
        return match.group(0) if match else None
    
    def _extract_job_role(self, message: str) -> Optional[str]:
        """Extract job role from message"""
        # Common job roles to look for
        job_roles = [
            "software engineer", "data scientist", "product manager", "devops engineer",
            "frontend developer", "backend developer", "full stack developer",
            "data analyst", "business analyst", "project manager", "scrum master",
            "ui/ux designer", "marketing manager", "sales manager", "consultant"
        ]
        
        message_lower = message.lower()
        for role in job_roles:
            if role in message_lower:
                return role.title()
        
        return None
    
    def _extract_career_goals(self, message: str) -> List[str]:
        """Extract career goals from message"""
        goals = []
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["technical", "coding", "programming", "development"]):
            goals.append("technical advancement")
        
        if any(word in message_lower for word in ["leadership", "management", "team lead"]):
            goals.append("leadership development")
        
        if any(word in message_lower for word in ["business", "strategy", "entrepreneur"]):
            goals.append("business growth")
        
        if any(word in message_lower for word in ["career change", "transition", "new field"]):
            goals.append("career transition")
        
        return goals
    
    def _format_profile_analysis_response(self, analysis: Dict, profile_data: Dict) -> str:
        """Format profile analysis response"""
        basic_info = profile_data.get("basic_info", {})
        name = basic_info.get("full_name", "Your profile")
        section_analysis = analysis.get("section_analysis", {})
        
        response = f"""
        📊 **Comprehensive Profile Analysis for {name}**

        **Overall Score: {analysis['overall_score']}/100** | **Completeness: {analysis['completeness_score']}%**

        🎯 **Key Strengths:**
        """
        
        for strength in analysis.get("strengths", [])[:5]:
            response += f"• {strength}\n"
        
        response += "\n⚠️ **Areas for Improvement:**\n"
        for weakness in analysis.get("weaknesses", [])[:5]:
            response += f"• {weakness}\n"
        
        response += "\n📋 **Section-by-Section Analysis:**\n"
        
        # Headline analysis
        headline_analysis = section_analysis.get("headline", {})
        response += f"**Headline:** {headline_analysis.get('score', 0)}/5 - {headline_analysis.get('current', 'N/A')}\n"
        
        # Summary analysis
        summary_analysis = section_analysis.get("summary", {})
        response += f"**Summary:** {summary_analysis.get('score', 0)}/5 - {summary_analysis.get('current', 'N/A')[:100]}...\n"
        
        # Experience analysis
        exp_analysis = section_analysis.get("experience", {})
        response += f"**Experience:** {exp_analysis.get('score', 0)}/5 - {exp_analysis.get('count', 0)} positions\n"
        
        # Skills analysis
        skills_analysis = section_analysis.get("skills", {})
        response += f"**Skills:** {skills_analysis.get('score', 0)}/5 - {skills_analysis.get('count', 0)} skills\n"
        
        # Education analysis
        edu_analysis = section_analysis.get("education", {})
        response += f"**Education:** {edu_analysis.get('score', 0)}/5 - {edu_analysis.get('count', 0)} entries\n"
        
        response += "\n💡 **Top Recommendations:**\n"
        for rec in analysis.get("recommendations", [])[:5]:
            response += f"• {rec}\n"
        
        # Add keyword analysis if available
        keyword_analysis = analysis.get("keyword_optimization", {})
        if keyword_analysis:
            response += "\n🔍 **Keyword Optimization:**\n"
            for category, data in keyword_analysis.items():
                if isinstance(data, dict) and "coverage" in data:
                    response += f"• {category.replace('_', ' ').title()}: {data['coverage']}% coverage\n"
        
        response += "\n🚀 **Next Steps:** Would you like me to help you improve specific sections, analyze your fit for a particular job role, or generate enhanced content for your profile?"
        
        return response
    
    def _format_job_analysis_response(self, job_analysis: Dict) -> str:
        """Format job analysis response"""
        if "error" in job_analysis:
            return f"❌ {job_analysis['error']}"
        
        response = f"""
        💼 **Job Fit Analysis: {job_analysis['job_title']}**

        **Overall Match Score: {job_analysis['overall_match_score']}/100**

        📈 **Skills Match:**
        • Required Skills: {job_analysis['required_skills_match']['total_matched']}/{job_analysis['required_skills_match']['total_required']} ({job_analysis['required_skills_match']['match_percentage']}%)
        • Preferred Skills: {job_analysis['preferred_skills_match']['total_matched']}/{job_analysis['preferred_skills_match']['total_required']} ({job_analysis['preferred_skills_match']['match_percentage']}%)

        🎯 **Analysis:**
        """
        
        analysis = job_analysis.get("analysis", {})
        for strength in analysis.get("strengths", []):
            response += f"✅ {strength}\n"
        
        for weakness in analysis.get("weaknesses", []):
            response += f"⚠️ {weakness}\n"
        
        if job_analysis.get("missing_skills"):
            response += "\n🔍 **Missing Skills:**\n"
            for skill in job_analysis["missing_skills"][:5]:
                response += f"• {skill}\n"
        
        response += "\n💡 **Recommendations:**\n"
        for rec in job_analysis.get("recommendations", [])[:3]:
            response += f"• {rec}\n"
        
        return response
    
    def _format_headline_suggestions(self, headlines: Dict) -> str:
        """Format headline suggestions"""
        response = "🎯 **Enhanced Headline Suggestions:**\n\n"
        
        for style, headline in headlines.items():
            style_name = style.replace("_", " ").title()
            response += f"**{style_name}:**\n{headline}\n\n"
        
        response += "Choose the style that best represents your professional brand and goals!"
        return response
    
    def _format_summary_suggestions(self, summaries: Dict) -> str:
        """Format summary suggestions"""
        response = "📝 **Enhanced Summary Suggestions:**\n\n"
        
        for style, summary in summaries.items():
            style_name = style.replace("_", " ").title()
            response += f"**{style_name}:**\n{summary}\n\n"
        
        response += "These summaries tell your professional story in different ways. Choose the one that resonates with your career goals!"
        return response
    
    def _format_experience_suggestions(self, experience_data: Dict) -> str:
        """Format experience suggestions"""
        response = "💼 **Experience Enhancement Suggestions:**\n\n"
        
        for exp in experience_data.get("enhanced_experiences", [])[:2]:  # Show first 2
            response += f"**{exp['title']} at {exp['company']}**\n"
            response += f"**Enhanced Description:**\n{exp['enhanced']}\n\n"
        
        response += "These enhancements use action words and specific achievements to make your experience more impactful!"
        return response
    
    def _generate_all_content_improvements(self, profile_data: Dict) -> str:
        """Generate all content improvements"""
        response = "✨ **Complete Profile Enhancement Package:**\n\n"
        
        # Generating headlines
        headlines = self.content_generator.generate_enhanced_headline(profile_data)
        response += "🎯 **Headline Options:**\n"
        response += f"• {headlines['achievement_focused']}\n\n"
        
        # Generating summary
        summaries = self.content_generator.generate_enhanced_summary(profile_data)
        response += "📝 **Summary Enhancement:**\n"
        response += f"{summaries['achievement_focused'][:200]}...\n\n"
        
        # Generating experience enhancements
        experience = self.content_generator.generate_experience_enhancements(profile_data)
        if experience.get("enhanced_experiences"):
            response += "💼 **Experience Improvements:**\n"
            response += "Enhanced descriptions with action words and achievements\n\n"
        
        response += "Would you like me to provide the full versions of any of these sections?"
        return response
    
    def _format_career_guidance_response(self, guidance: Dict) -> str:
        """Format career guidance response"""
        response = "🎯 **Personalized Career Guidance:**\n\n"
        
        # Current assessment
        assessment = guidance.get("current_assessment", {})
        if assessment:
            response += f"**Current Position:** {assessment.get('role', 'Not specified')}\n"
            response += f"**Experience Level:** {assessment.get('experience_level', 0)} years\n"
            response += f"**Skill Level:** {assessment.get('skill_level', 'Not assessed')}\n\n"
        
        # Career paths
        career_paths = guidance.get("career_paths", [])
        if career_paths:
            response += "🚀 **Potential Career Paths:**\n"
            for path in career_paths[:3]:
                response += f"• **{path['path']}** ({path['timeline']})\n"
                response += f"  {path['description']}\n\n"
        
        # Learning resources
        resources = guidance.get("learning_resources", [])
        if resources:
            response += "📚 **Recommended Learning Resources:**\n"
            for resource in resources[:3]:
                response += f"• **{resource['name']}** ({resource['type']})\n"
                response += f"  {resource['description']}\n"
                response += f"  Duration: {resource['duration']} | Cost: {resource['cost']}\n\n"
        
        response += "Would you like me to create a detailed skill development plan or explore any specific career path?"
        return response
