from typing import Dict, List, Optional
import json
from llm_wrapper import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import config

class ContentGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config.FREE_LLM_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            api_key=config.OPENROUTER_API_KEY
        )
    
    def generate_enhanced_headline(self, profile_data: Dict, target_role: str = None) -> Dict:
        """Generate an enhanced headline for the profile"""
        try:
            current_headline = profile_data.get("basic_info", {}).get("headline", "")
            experience = profile_data.get("experience", [])
            skills = profile_data.get("skills", [])
            basic_info = profile_data.get("basic_info", {})
            full_name = basic_info.get("full_name", "")
            location = basic_info.get("location", "")
            
            # Extract key information
            top_skills = [skill["name"] for skill in skills[:5]] if skills else []
            recent_role = (experience[0].get("title") if experience and isinstance(experience[0], dict) else "") or (
                basic_info.get("current_role", "")
            )
            industry = basic_info.get("industry", "")
            
            prompt = f"""
            Create an enhanced LinkedIn headline for a professional with the following information:
            
            Current headline: {current_headline}
            Recent role: {recent_role}
            Top skills: {', '.join(top_skills)}
            Target role: {target_role if target_role else 'General professional'}
            Name: {full_name}
            Industry: {industry}
            Location: {location}
            
            Requirements:
            1. Include key skills and value proposition
            2. Use action words and industry keywords
            3. Keep it under 200 characters
            4. Make it compelling and professional
            5. Include specific achievements if possible
            
            Generate 3 different versions with different approaches:
            1. Achievement-focused
            2. Skill-focused
            3. Value proposition-focused
            
            Format as JSON with keys: achievement_focused, skill_focused, value_focused
            """
            
            raw = self.llm.invoke(prompt)

            # Try to parse JSON directly; if not possible, fall back to heuristic generation
            parsed: Dict = {}
            try:
                # Some models wrap JSON in code fences; strip common wrappers
                cleaned = raw.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.strip("`\n ")
                    # Remove optional language hint like ```json
                    if cleaned.lower().startswith("json\n"):
                        cleaned = cleaned[5:]
                parsed = json.loads(cleaned)
                if all(k in parsed and isinstance(parsed[k], str) for k in ["achievement_focused", "skill_focused", "value_focused"]):
                    return parsed
            except Exception:
                pass

            # Heuristic, personalized fallback using available profile signals
            primary_skill_list = ", ".join(top_skills[:3]) if top_skills else "impactful solutions"
            two_skills = ", ".join(top_skills[:2]) if top_skills else "strategy & execution"
            role_for_copy = recent_role or (target_role or "Professional")
            industry_hint = f" | {industry}" if industry else ""

            achievement = (
                f"{role_for_copy}{industry_hint} | Led high-impact projects | Drove measurable results | {primary_skill_list}"
            )
            skill = (
                f"{role_for_copy} | {primary_skill_list} | Known for reliability and craftsmanship"
            )
            value = (
                f"{role_for_copy} | Turning goals into outcomes | {two_skills}"
            )

            return {
                "achievement_focused": achievement,
                "skill_focused": skill,
                "value_focused": value
            }
            
        except Exception as e:
            print(f"Error generating enhanced headline: {e}")
            return {
                "achievement_focused": "Professional with strong technical skills and leadership experience",
                "skill_focused": "Skilled professional with expertise in multiple technologies",
                "value_focused": "Results-oriented professional focused on delivering value"
            }
    
    def generate_enhanced_summary(self, profile_data: Dict, target_role: str = None) -> Dict:
        """Generate an enhanced summary for the profile"""
        try:
            current_summary = profile_data.get("basic_info", {}).get("summary", "")
            experience = profile_data.get("experience", [])
            skills = profile_data.get("skills", [])
            education = profile_data.get("education", [])
            
            # Extract key information
            years_experience = len(experience)
            top_skills = [skill["name"] for skill in skills[:8]] if skills else []
            recent_achievements = []
            
            # Extract achievements from recent experience
            for exp in experience[:2]:
                if exp.get("description"):
                    recent_achievements.append(f"{exp['title']} at {exp['company']}")
            
            prompt = f"""
            Create an enhanced LinkedIn summary for a professional with the following information:
            
            Current summary: {current_summary}
            Years of experience: {years_experience}
            Top skills: {', '.join(top_skills)}
            Recent roles: {', '.join(recent_achievements)}
            Target role: {target_role if target_role else 'General professional'}
            
            Requirements:
            1. Tell a compelling professional story
            2. Include specific achievements and metrics
            3. Highlight key skills and expertise
            4. Show passion and career goals
            5. Keep it engaging and professional
            6. Include a call to action
            
            Generate 2 different versions:
            1. Story-focused (personal narrative)
            2. Achievement-focused (results and metrics)
            
            Format as JSON with keys: story_focused, achievement_focused
            """
            
            response = self.llm.invoke(prompt)
            
            # Generate enhanced summaries
            story_focused = f"""
            I'm a passionate {experience[0]['title'] if experience else 'professional'} with {years_experience} years of experience in the technology industry. My journey began with a fascination for solving complex problems, which led me to specialize in {', '.join(top_skills[:3])}.

            Throughout my career, I've had the privilege of working with diverse teams and technologies, always focusing on delivering innovative solutions that drive business value. I believe in continuous learning and staying current with industry trends.

            When I'm not coding or collaborating with teams, I enjoy mentoring junior developers and contributing to open-source projects. I'm always excited to connect with fellow professionals who share my passion for technology and innovation.

            Let's connect and explore how we can create something amazing together!
            """
            
            achievement_focused = f"""
            Results-driven {experience[0]['title'] if experience else 'professional'} with {years_experience} years of experience delivering high-impact solutions. Proven track record of leading cross-functional teams and implementing scalable technologies.

            Key Achievements:
            • Led development teams of 5-15 members across multiple projects
            • Improved system performance by 40% through optimization initiatives
            • Reduced deployment time by 60% implementing CI/CD pipelines
            • Mentored 10+ junior developers, improving team productivity by 25%

            Technical Expertise: {', '.join(top_skills[:5])}
            Industry Experience: Software Development, E-commerce, FinTech

            Passionate about leveraging technology to solve real-world problems and drive business growth. Always seeking new challenges and opportunities to make a meaningful impact.
            """
            
            return {
                "story_focused": story_focused.strip(),
                "achievement_focused": achievement_focused.strip()
            }
            
        except Exception as e:
            print(f"Error generating enhanced summary: {e}")
            return {
                "story_focused": "Experienced professional with a passion for technology and innovation.",
                "achievement_focused": "Results-driven professional with proven track record of delivering high-impact solutions."
            }
    
    def generate_experience_enhancements(self, profile_data: Dict) -> Dict:
        """Generate enhanced versions of experience descriptions"""
        try:
            experience = profile_data.get("experience", [])
            enhanced_experience = []
            
            for exp in experience:
                current_description = exp.get("description", "")
                
                if not current_description:
                    # Generate basic description if none exists
                    enhanced_description = self._generate_basic_experience_description(exp)
                else:
                    # Enhance existing description
                    enhanced_description = self._enhance_experience_description(exp)
                
                enhanced_experience.append({
                    "original": current_description,
                    "enhanced": enhanced_description,
                    "title": exp.get("title", ""),
                    "company": exp.get("company", ""),
                    "duration": exp.get("duration", "")
                })
            
            return {"enhanced_experiences": enhanced_experience}
            
        except Exception as e:
            print(f"Error generating experience enhancements: {e}")
            return {"enhanced_experiences": []}
    
    def _generate_basic_experience_description(self, exp: Dict) -> str:
        """Generate a basic experience description"""
        title = exp.get("title", "")
        company = exp.get("company", "")
        
        # Generate based on role type
        if any(keyword in title.lower() for keyword in ["engineer", "developer", "programmer"]):
            return f"""
            • Developed and maintained software applications using modern programming languages and frameworks
            • Collaborated with cross-functional teams to design and implement new features
            • Participated in code reviews and contributed to technical discussions
            • Debugged and resolved software defects and issues
            • Worked with databases and APIs to ensure seamless data flow
            • Contributed to agile development processes and sprint planning
            """
        elif any(keyword in title.lower() for keyword in ["manager", "lead", "director"]):
            return f"""
            • Led and managed teams of professionals to deliver high-quality results
            • Developed and executed strategic plans to achieve business objectives
            • Collaborated with stakeholders to define project requirements and timelines
            • Mentored team members and provided guidance for professional development
            • Analyzed performance metrics and implemented process improvements
            • Managed budgets and resources to ensure project success
            """
        else:
            return f"""
            • Performed key responsibilities in {title} role at {company}
            • Collaborated with team members to achieve organizational goals
            • Contributed to process improvements and operational efficiency
            • Developed and maintained professional relationships with stakeholders
            • Participated in training and professional development activities
            """
    
    def _enhance_experience_description(self, exp: Dict) -> str:
        """Enhance existing experience description"""
        current_description = exp.get("description", "")
        title = exp.get("title", "")
        
        # Add action words and metrics if missing
        action_words = ["developed", "implemented", "led", "managed", "improved", "increased", "reduced", "created"]
        has_action_words = any(word in current_description.lower() for word in action_words)
        
        if not has_action_words:
            # Add action words to the beginning of sentences
            sentences = current_description.split(". ")
            enhanced_sentences = []
            
            for sentence in sentences:
                if sentence.strip():
                    # Add action word if sentence doesn't start with one
                    if not any(word in sentence.lower().split()[0] for word in action_words):
                        enhanced_sentences.append(f"Developed {sentence.lower()}")
                    else:
                        enhanced_sentences.append(sentence)
            
            return ". ".join(enhanced_sentences)
        
        return current_description
    
    def generate_career_guidance(self, profile_data: Dict, user_goals: List[str] = None) -> Dict:
        """Generate personalized career guidance"""
        try:
            experience = profile_data.get("experience", [])
            skills = profile_data.get("skills", [])
            education = profile_data.get("education", [])
            
            # Analyze current position
            current_role = experience[0]["title"] if experience else "Entry-level"
            years_experience = len(experience)
            skill_level = self._assess_skill_level(skills)
            
            # Generate career paths
            career_paths = self._generate_career_paths(current_role, years_experience, skill_level)
            
            # Generate skill development plan
            skill_plan = self._generate_skill_development_plan(skills, user_goals)
            
            # Generate learning resources
            learning_resources = self._generate_learning_resources(skills, user_goals)
            
            return {
                "career_paths": career_paths,
                "skill_development_plan": skill_plan,
                "learning_resources": learning_resources,
                "current_assessment": {
                    "role": current_role,
                    "experience_level": years_experience,
                    "skill_level": skill_level
                }
            }
            
        except Exception as e:
            print(f"Error generating career guidance: {e}")
            return {
                "career_paths": [],
                "skill_development_plan": {},
                "learning_resources": [],
                "current_assessment": {}
            }
    
    def _assess_skill_level(self, skills: List[Dict]) -> str:
        """Assess overall skill level based on skills and endorsements"""
        if not skills:
            return "Beginner"
        
        total_endorsements = sum(skill.get("endorsements", 0) for skill in skills)
        avg_endorsements = total_endorsements / len(skills)
        
        if avg_endorsements >= 20:
            return "Expert"
        elif avg_endorsements >= 10:
            return "Advanced"
        elif avg_endorsements >= 5:
            return "Intermediate"
        else:
            return "Beginner"
    
    def _generate_career_paths(self, current_role: str, years_experience: int, skill_level: str) -> List[Dict]:
        """Generate potential career paths"""
        career_paths = []
        
        # Technical career paths
        if any(keyword in current_role.lower() for keyword in ["engineer", "developer", "programmer"]):
            career_paths.extend([
                {
                    "path": "Senior Software Engineer",
                    "timeline": "2-3 years",
                    "requirements": ["Advanced technical skills", "Leadership experience", "System design knowledge"],
                    "description": "Lead technical projects and mentor junior developers"
                },
                {
                    "path": "Technical Lead",
                    "timeline": "3-4 years",
                    "requirements": ["Team leadership", "Architecture design", "Project management"],
                    "description": "Lead technical teams and make architectural decisions"
                },
                {
                    "path": "Engineering Manager",
                    "timeline": "4-5 years",
                    "requirements": ["People management", "Strategic thinking", "Business acumen"],
                    "description": "Manage engineering teams and align with business goals"
                }
            ])
        
        # Management career paths
        if any(keyword in current_role.lower() for keyword in ["manager", "lead", "director"]):
            career_paths.extend([
                {
                    "path": "Senior Manager",
                    "timeline": "2-3 years",
                    "requirements": ["Advanced leadership", "Strategic planning", "Budget management"],
                    "description": "Lead larger teams and manage complex projects"
                },
                {
                    "path": "Director",
                    "timeline": "3-4 years",
                    "requirements": ["Executive presence", "Business strategy", "Cross-functional leadership"],
                    "description": "Lead multiple teams and drive organizational strategy"
                }
            ])
        
        # Add general career paths
        career_paths.extend([
            {
                "path": "Consultant",
                "timeline": "1-2 years",
                "requirements": ["Expertise in specific domain", "Client relationship skills", "Problem-solving"],
                "description": "Provide expert advice to organizations"
            },
            {
                "path": "Entrepreneur",
                "timeline": "Varies",
                "requirements": ["Business acumen", "Risk tolerance", "Innovation mindset"],
                "description": "Start your own business or venture"
            }
        ])
        
        return career_paths[:5]  # Limit to top 5 paths
    
    def _generate_skill_development_plan(self, skills: List[Dict], user_goals: List[str] = None) -> Dict:
        """Generate a skill development plan"""
        current_skills = [skill["name"].lower() for skill in skills]
        
        # Define skill categories and development paths
        skill_categories = {
            "technical_skills": {
                "current": [skill for skill in current_skills if any(tech in skill for tech in ["python", "javascript", "java", "react", "aws"])],
                "recommended": ["Advanced Python", "System Design", "Cloud Architecture", "DevOps", "Machine Learning"],
                "priority": "High" if user_goals and any("technical" in goal.lower() for goal in user_goals) else "Medium"
            },
            "leadership_skills": {
                "current": [skill for skill in current_skills if any(lead in skill for lead in ["leadership", "management", "teamwork"])],
                "recommended": ["Strategic Thinking", "Change Management", "Conflict Resolution", "Executive Communication"],
                "priority": "High" if user_goals and any("leadership" in goal.lower() for goal in user_goals) else "Medium"
            },
            "business_skills": {
                "current": [skill for skill in current_skills if any(bus in skill for bus in ["business", "strategy", "analytics"])],
                "recommended": ["Business Strategy", "Financial Analysis", "Market Research", "Product Management"],
                "priority": "High" if user_goals and any("business" in goal.lower() for goal in user_goals) else "Medium"
            }
        }
        
        return skill_categories
    
    def _generate_learning_resources(self, skills: List[Dict], user_goals: List[str] = None) -> List[Dict]:
        """Generate learning resources and recommendations"""
        resources = []
        
        # Technical learning resources
        technical_resources = [
            {
                "type": "Online Course",
                "name": "Coursera - Machine Learning Specialization",
                "url": "https://www.coursera.org/specializations/machine-learning",
                "description": "Comprehensive machine learning course by Andrew Ng",
                "duration": "6 months",
                "cost": "Free (audit) / $49/month"
            },
            {
                "type": "Online Course",
                "name": "Udemy - Complete Python Bootcamp",
                "url": "https://www.udemy.com/course/complete-python-bootcamp/",
                "description": "Learn Python from scratch to advanced concepts",
                "duration": "22 hours",
                "cost": "$29.99"
            },
            {
                "type": "Book",
                "name": "Clean Code by Robert C. Martin",
                "description": "Essential reading for writing maintainable code",
                "duration": "2-3 weeks",
                "cost": "$44.99"
            }
        ]
        
        # Leadership learning resources
        leadership_resources = [
            {
                "type": "Online Course",
                "name": "LinkedIn Learning - Leadership Foundations",
                "description": "Core leadership skills and principles",
                "duration": "3 hours",
                "cost": "Included with LinkedIn Premium"
            },
            {
                "type": "Book",
                "name": "The First 90 Days by Michael Watkins",
                "description": "Guide for new leaders and career transitions",
                "duration": "2-3 weeks",
                "cost": "$24.99"
            }
        ]
        
        # Add resources based on user goals
        if user_goals:
            if any("technical" in goal.lower() for goal in user_goals):
                resources.extend(technical_resources)
            if any("leadership" in goal.lower() for goal in user_goals):
                resources.extend(leadership_resources)
        else:
            # Default resources
            resources.extend(technical_resources[:2])
            resources.extend(leadership_resources[:1])
        
        return resources
