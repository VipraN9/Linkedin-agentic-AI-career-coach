from typing import Dict, List, Tuple, Optional
import re
from llm_wrapper import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import config

class ProfileAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config.FREE_LLM_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            api_key=config.OPENROUTER_API_KEY
        )
        
    def analyze_profile(self, profile_data: Dict) -> Dict:
        """Comprehensive profile analysis"""
        analysis = {
            "overall_score": 0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "section_analysis": {},
            "keyword_optimization": {},
            "completeness_score": 0
        }
        
        # Analyze each section
        analysis["section_analysis"]["headline"] = self._analyze_headline(profile_data.get("basic_info", {}).get("headline", ""))
        analysis["section_analysis"]["summary"] = self._analyze_summary(profile_data.get("basic_info", {}).get("summary", ""))
        analysis["section_analysis"]["experience"] = self._analyze_experience(profile_data.get("experience", []))
        analysis["section_analysis"]["skills"] = self._analyze_skills(profile_data.get("skills", []))
        analysis["section_analysis"]["education"] = self._analyze_education(profile_data.get("education", []))
        
        # Calculate overall scores
        analysis["overall_score"] = self._calculate_overall_score(analysis["section_analysis"])
        analysis["completeness_score"] = self._calculate_completeness_score(profile_data)
        
        # Generate recommendations
        analysis["strengths"], analysis["weaknesses"], analysis["recommendations"] = self._generate_recommendations(
            profile_data, analysis["section_analysis"]
        )
        
        # Keyword optimization
        analysis["keyword_optimization"] = self._analyze_keywords(profile_data)
        
        return analysis
    
    def _analyze_headline(self, headline: str) -> Dict:
        """Analyze profile headline"""
        if not headline:
            return {"score": 0, "issues": ["Missing headline"], "suggestions": ["Add a compelling headline"]}
        
        score = 0
        issues = []
        suggestions = []
        
        # Check length
        if len(headline) < 50:
            issues.append("Headline too short")
            suggestions.append("Expand headline to include key skills and value proposition")
        elif len(headline) > 200:
            issues.append("Headline too long")
            suggestions.append("Keep headline concise and focused")
        else:
            score += 2
        
        # Check for keywords
        keyword_patterns = [
            r'\b(engineer|developer|manager|director|specialist|analyst|consultant)\b',
            r'\b(python|javascript|react|aws|docker|kubernetes|agile|scrum)\b'
        ]
        
        keyword_count = 0
        for pattern in keyword_patterns:
            if re.search(pattern, headline.lower()):
                keyword_count += 1
        
        if keyword_count >= 2:
            score += 2
        elif keyword_count == 1:
            score += 1
        else:
            issues.append("Missing relevant keywords")
            suggestions.append("Include industry-specific keywords and skills")
        
        # Check for value proposition
        value_words = ['led', 'managed', 'developed', 'improved', 'increased', 'reduced', 'created']
        has_value = any(word in headline.lower() for word in value_words)
        
        if has_value:
            score += 1
        else:
            suggestions.append("Include action words that demonstrate impact")
        
        return {
            "score": min(score, 5),
            "issues": issues,
            "suggestions": suggestions,
            "current": headline
        }
    
    def _analyze_summary(self, summary: str) -> Dict:
        """Analyze profile summary"""
        if not summary:
            return {"score": 0, "issues": ["Missing summary"], "suggestions": ["Add a compelling summary"]}
        
        score = 0
        issues = []
        suggestions = []
        
        # Check length
        if len(summary) < 100:
            issues.append("Summary too short")
            suggestions.append("Expand summary to tell your professional story")
        elif len(summary) > 2000:
            issues.append("Summary too long")
            suggestions.append("Keep summary concise and focused")
        else:
            score += 2
        
        # Check for storytelling elements
        story_elements = ['experience', 'passion', 'expertise', 'achievement', 'goal']
        story_count = sum(1 for element in story_elements if element in summary.lower())
        
        if story_count >= 3:
            score += 2
        elif story_count >= 1:
            score += 1
        else:
            suggestions.append("Include personal story and career narrative")
        
        # Check for achievements
        achievement_words = ['achieved', 'increased', 'reduced', 'led', 'managed', 'developed']
        has_achievements = any(word in summary.lower() for word in achievement_words)
        
        if has_achievements:
            score += 1
        else:
            suggestions.append("Include specific achievements and metrics")
        
        return {
            "score": min(score, 5),
            "issues": issues,
            "suggestions": suggestions,
            "current": summary[:200] + "..." if len(summary) > 200 else summary
        }
    
    def _analyze_experience(self, experience: List[Dict]) -> Dict:
        """Analyze work experience"""
        if not experience:
            return {"score": 0, "issues": ["No experience listed"], "suggestions": ["Add work experience"]}
        
        score = 0
        issues = []
        suggestions = []
        
        # Check number of experiences
        if len(experience) >= 3:
            score += 2
        elif len(experience) >= 1:
            score += 1
        else:
            issues.append("Insufficient work experience")
        
        # Analyze each experience
        for exp in experience:
            if not exp.get("description"):
                issues.append(f"Missing description for {exp.get('title', 'position')}")
                suggestions.append("Add detailed descriptions for each role")
            else:
                # Check for achievements in descriptions
                achievement_words = ['achieved', 'increased', 'reduced', 'led', 'managed', 'developed']
                if any(word in exp.get("description", "").lower() for word in achievement_words):
                    score += 0.5
        
        # Check for recent experience
        recent_experience = any(
            "present" in exp.get("duration", "").lower() or "2023" in exp.get("duration", "") or "2024" in exp.get("duration", "")
            for exp in experience
        )
        
        if recent_experience:
            score += 1
        else:
            suggestions.append("Ensure recent experience is up to date")
        
        return {
            "score": min(score, 5),
            "issues": issues,
            "suggestions": suggestions,
            "count": len(experience)
        }
    
    def _analyze_skills(self, skills: List[Dict]) -> Dict:
        """Analyze skills section"""
        if not skills:
            return {"score": 0, "issues": ["No skills listed"], "suggestions": ["Add relevant skills"]}
        
        score = 0
        issues = []
        suggestions = []
        
        # Check number of skills
        if len(skills) >= 15:
            score += 2
        elif len(skills) >= 10:
            score += 1.5
        elif len(skills) >= 5:
            score += 1
        else:
            issues.append("Too few skills listed")
            suggestions.append("Add more relevant skills")
        
        # Check for endorsed skills
        endorsed_skills = [skill for skill in skills if skill.get("endorsements", 0) > 0]
        if len(endorsed_skills) >= 5:
            score += 1
        elif len(endorsed_skills) >= 2:
            score += 0.5
        else:
            suggestions.append("Get more skill endorsements from colleagues")
        
        # Check for technical vs soft skills
        technical_skills = []
        soft_skills = []
        
        for skill in skills:
            skill_name = skill.get("name", "").lower()
            if any(tech in skill_name for tech in ['python', 'javascript', 'java', 'react', 'aws', 'docker', 'sql']):
                technical_skills.append(skill_name)
            elif any(soft in skill_name for soft in ['leadership', 'communication', 'teamwork', 'problem solving']):
                soft_skills.append(skill_name)
        
        if len(technical_skills) >= 3 and len(soft_skills) >= 2:
            score += 1
        else:
            suggestions.append("Balance technical and soft skills")
        
        return {
            "score": min(score, 5),
            "issues": issues,
            "suggestions": suggestions,
            "count": len(skills),
            "technical_count": len(technical_skills),
            "soft_count": len(soft_skills)
        }
    
    def _analyze_education(self, education: List[Dict]) -> Dict:
        """Analyze education section"""
        if not education:
            return {"score": 0, "issues": ["No education listed"], "suggestions": ["Add education information"]}
        
        score = 0
        issues = []
        suggestions = []
        
        # Check for degree information
        for edu in education:
            if not edu.get("degree"):
                issues.append("Missing degree information")
                suggestions.append("Add degree details")
            else:
                score += 1
            
            if not edu.get("school"):
                issues.append("Missing school information")
                suggestions.append("Add school details")
            else:
                score += 0.5
        
        # Check for relevant field of study
        relevant_fields = ['computer science', 'engineering', 'business', 'mathematics', 'statistics']
        has_relevant_field = any(
            any(field in edu.get("fieldOfStudy", "").lower() for field in relevant_fields)
            for edu in education
        )
        
        if has_relevant_field:
            score += 1
        else:
            suggestions.append("Highlight relevant coursework or certifications")
        
        return {
            "score": min(score, 5),
            "issues": issues,
            "suggestions": suggestions,
            "count": len(education)
        }
    
    def _calculate_overall_score(self, section_analysis: Dict) -> float:
        """Calculate overall profile score"""
        total_score = 0
        max_score = 0
        
        for section, analysis in section_analysis.items():
            if isinstance(analysis, dict) and "score" in analysis:
                total_score += analysis["score"]
                max_score += 5
        
        return round((total_score / max_score) * 100, 1) if max_score > 0 else 0
    
    def _calculate_completeness_score(self, profile_data: Dict) -> float:
        """Calculate profile completeness score"""
        sections = [
            "basic_info.headline",
            "basic_info.summary",
            "experience",
            "education",
            "skills"
        ]
        
        completed_sections = 0
        for section in sections:
            if "." in section:
                parent, child = section.split(".")
                if profile_data.get(parent, {}).get(child):
                    completed_sections += 1
            else:
                if profile_data.get(section):
                    completed_sections += 1
        
        return round((completed_sections / len(sections)) * 100, 1)
    
    def _generate_recommendations(self, profile_data: Dict, section_analysis: Dict) -> Tuple[List[str], List[str], List[str]]:
        """Generate strengths, weaknesses, and recommendations"""
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Analyze strengths with more detail
        basic_info = profile_data.get("basic_info", {})
        experience = profile_data.get("experience", [])
        skills = profile_data.get("skills", [])
        education = profile_data.get("education", [])
        
        # Detailed strength analysis
        if section_analysis.get("headline", {}).get("score", 0) >= 3:
            strengths.append("Strong headline with relevant keywords and value proposition")
        elif basic_info.get("headline"):
            strengths.append("Has a headline, but could be more compelling")
        
        if section_analysis.get("summary", {}).get("score", 0) >= 3:
            strengths.append("Comprehensive professional summary with storytelling elements")
        elif basic_info.get("summary"):
            strengths.append("Has a summary, but could be more detailed")
        
        if len(experience) >= 3:
            strengths.append(f"Strong work history with {len(experience)} positions showing career progression")
        elif len(experience) >= 1:
            strengths.append(f"Has {len(experience)} work experience(s) - good foundation")
        
        if len(skills) >= 15:
            strengths.append(f"Extensive skill set with {len(skills)} skills showing versatility")
        elif len(skills) >= 5:
            strengths.append(f"Good skill diversity with {len(skills)} skills")
        
        if len(education) >= 2:
            strengths.append(f"Strong educational background with {len(education)} institutions")
        elif len(education) >= 1:
            strengths.append("Has educational credentials")
        
        # Network strength
        connections = basic_info.get("connections", "0")
        followers = basic_info.get("followers", "0")
        try:
            conn_count = int(connections) if connections.isdigit() else 0
            fol_count = int(followers) if followers.isdigit() else 0
            if conn_count >= 500:
                strengths.append(f"Strong professional network with {conn_count}+ connections")
            elif conn_count >= 100:
                strengths.append(f"Growing network with {conn_count} connections")
            if fol_count >= 1000:
                strengths.append(f"Good visibility with {fol_count}+ followers")
        except:
            pass
        
        # Analyze weaknesses with more detail
        for section, analysis in section_analysis.items():
            if isinstance(analysis, dict) and "issues" in analysis:
                weaknesses.extend(analysis["issues"])
        
        # Generate detailed recommendations
        for section, analysis in section_analysis.items():
            if isinstance(analysis, dict) and "suggestions" in analysis:
                recommendations.extend(analysis["suggestions"])
        
        # Add specific recommendations based on profile data
        if not basic_info.get("summary"):
            recommendations.append("Add a compelling professional summary that tells your story")
        
        if len(experience) < 2:
            recommendations.append("Add more work experiences or internships to show career progression")
        
        if len(skills) < 10:
            recommendations.append("Add more relevant skills to increase your discoverability")
        
        if not education:
            recommendations.append("Add your educational background and relevant certifications")
        
        # Add general recommendations
        if len(recommendations) < 5:
            recommendations.extend([
                "Regularly update your profile with new achievements and projects",
                "Engage with your network through posts, comments, and sharing industry insights",
                "Request recommendations from colleagues and managers to build credibility",
                "Add a professional profile picture to increase profile views",
                "Include specific metrics and achievements in your experience descriptions"
            ])
        
        # Ensure we have at least some strengths
        if not strengths:
            strengths.append("Profile has good potential for optimization and growth")
        
        return strengths, weaknesses, recommendations
    
    def _analyze_keywords(self, profile_data: Dict) -> Dict:
        """Analyze keyword optimization"""
        all_text = ""
        
        # Combine all text from profile
        basic_info = profile_data.get("basic_info", {})
        all_text += f"{basic_info.get('headline', '')} {basic_info.get('summary', '')} "
        
        for exp in profile_data.get("experience", []):
            all_text += f"{exp.get('title', '')} {exp.get('description', '')} "
        
        for skill in profile_data.get("skills", []):
            all_text += f"{skill.get('name', '')} "
        
        all_text = all_text.lower()
        
        # Define keyword categories
        keyword_categories = {
            "technical_skills": [
                "python", "javascript", "java", "react", "node.js", "aws", "docker", "kubernetes",
                "sql", "mongodb", "postgresql", "git", "agile", "scrum", "machine learning", "ai"
            ],
            "soft_skills": [
                "leadership", "communication", "teamwork", "problem solving", "project management",
                "collaboration", "mentoring", "strategic thinking"
            ],
            "industries": [
                "technology", "software", "fintech", "healthcare", "e-commerce", "consulting",
                "startup", "enterprise"
            ]
        }
        
        keyword_analysis = {}
        for category, keywords in keyword_categories.items():
            found_keywords = [keyword for keyword in keywords if keyword in all_text]
            keyword_analysis[category] = {
                "found": found_keywords,
                "count": len(found_keywords),
                "total": len(keywords),
                "coverage": round((len(found_keywords) / len(keywords)) * 100, 1)
            }
        
        return keyword_analysis
