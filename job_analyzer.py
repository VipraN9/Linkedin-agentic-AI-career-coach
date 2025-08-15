from typing import Dict, List, Tuple, Optional
import re
import requests
from llm_wrapper import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import config

class JobAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config.FREE_LLM_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            api_key=config.OPENROUTER_API_KEY
        )
        
        # Predefined job descriptions for common roles
        self.job_descriptions = {
            "software_engineer": {
                "title": "Software Engineer",
                "description": """
                We are looking for a Software Engineer to join our team. The ideal candidate will:
                - Develop and maintain software applications using modern programming languages
                - Collaborate with cross-functional teams to design and implement new features
                - Write clean, maintainable, and efficient code
                - Participate in code reviews and contribute to technical discussions
                - Debug and resolve software defects and issues
                - Work with databases and APIs
                - Experience with version control systems (Git)
                - Knowledge of software development methodologies (Agile, Scrum)
                - Strong problem-solving and analytical skills
                - Excellent communication and teamwork abilities
                """,
                "required_skills": [
                    "programming", "software development", "problem solving", "teamwork",
                    "version control", "agile", "scrum", "debugging", "databases", "apis"
                ],
                "preferred_skills": [
                    "python", "javascript", "java", "react", "node.js", "aws", "docker",
                    "kubernetes", "sql", "mongodb", "postgresql", "git", "machine learning"
                ]
            },
            "data_scientist": {
                "title": "Data Scientist",
                "description": """
                We are seeking a Data Scientist to help us extract insights from data. The role involves:
                - Analyzing large datasets to identify trends and patterns
                - Developing predictive models and machine learning algorithms
                - Creating data visualizations and reports
                - Collaborating with business stakeholders to understand requirements
                - Cleaning and preprocessing data for analysis
                - Communicating findings to non-technical audiences
                - Experience with statistical analysis and modeling
                - Knowledge of data visualization tools
                - Strong analytical and critical thinking skills
                - Experience with big data technologies
                """,
                "required_skills": [
                    "data analysis", "statistics", "machine learning", "python", "sql",
                    "data visualization", "statistical modeling", "critical thinking"
                ],
                "preferred_skills": [
                    "r", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
                    "tableau", "power bi", "hadoop", "spark", "jupyter"
                ]
            },
            "product_manager": {
                "title": "Product Manager",
                "description": """
                We are looking for a Product Manager to drive product strategy and execution. The role includes:
                - Defining product vision, strategy, and roadmap
                - Gathering and analyzing user feedback and market research
                - Collaborating with engineering, design, and marketing teams
                - Prioritizing features and requirements based on business value
                - Defining product requirements and user stories
                - Monitoring product metrics and KPIs
                - Experience with product management methodologies
                - Strong analytical and strategic thinking skills
                - Excellent communication and stakeholder management
                - Knowledge of agile development processes
                """,
                "required_skills": [
                    "product management", "strategic thinking", "stakeholder management",
                    "user research", "market analysis", "agile", "scrum", "communication"
                ],
                "preferred_skills": [
                    "jira", "confluence", "figma", "analytics", "a/b testing", "user experience",
                    "business strategy", "data analysis", "project management"
                ]
            },
            "devops_engineer": {
                "title": "DevOps Engineer",
                "description": """
                We are seeking a DevOps Engineer to streamline our development and deployment processes. Responsibilities include:
                - Automating deployment and infrastructure management
                - Managing cloud infrastructure (AWS, Azure, or GCP)
                - Implementing CI/CD pipelines
                - Monitoring system performance and reliability
                - Collaborating with development teams to improve processes
                - Managing containerization and orchestration
                - Experience with cloud platforms and infrastructure as code
                - Knowledge of containerization technologies
                - Strong scripting and automation skills
                - Understanding of networking and security principles
                """,
                "required_skills": [
                    "devops", "automation", "cloud computing", "ci/cd", "containerization",
                    "infrastructure as code", "scripting", "monitoring", "networking"
                ],
                "preferred_skills": [
                    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
                    "jenkins", "gitlab", "prometheus", "grafana", "linux", "bash", "python"
                ]
            }
        }
    
    def analyze_job_fit(self, profile_data: Dict, job_role: str) -> Dict:
        """Analyze how well a profile fits a specific job role"""
        try:
            # Get job description
            job_desc = self._get_job_description(job_role)
            if not job_desc:
                return self._create_error_response(f"Job role '{job_role}' not found")
            
            # Extract skills from profile
            profile_skills = self._extract_profile_skills(profile_data)
            
            # Calculate match scores
            required_match = self._calculate_skill_match(profile_skills, job_desc["required_skills"])
            preferred_match = self._calculate_skill_match(profile_skills, job_desc["preferred_skills"])
            
            # Calculate overall match score
            overall_score = self._calculate_overall_match_score(required_match, preferred_match, profile_data)
            
            # Generate detailed analysis
            analysis = self._generate_job_fit_analysis(profile_data, job_desc, profile_skills, overall_score)
            
            return {
                "job_role": job_role,
                "job_title": job_desc["title"],
                "overall_match_score": overall_score,
                "required_skills_match": required_match,
                "preferred_skills_match": preferred_match,
                "analysis": analysis,
                "missing_skills": self._identify_missing_skills(profile_skills, job_desc),
                "recommendations": self._generate_job_recommendations(profile_data, job_desc, overall_score)
            }
            
        except Exception as e:
            print(f"Error analyzing job fit: {e}")
            return self._create_error_response(f"Error analyzing job fit: {str(e)}")
    
    def _get_job_description(self, job_role: str) -> Optional[Dict]:
        """Get job description for a specific role"""
        # Normalize job role
        normalized_role = job_role.lower().replace(" ", "_")
        
        # Check predefined descriptions
        for key, desc in self.job_descriptions.items():
            if normalized_role in key or key in normalized_role:
                return desc
        
        # If not found, try to generate one using AI
        return self._generate_job_description(job_role)
    
    def _generate_job_description(self, job_role: str) -> Optional[Dict]:
        """Generate job description using AI for unknown roles"""
        try:
            prompt = f"""
            Generate a comprehensive job description for a {job_role} position. Include:
            1. Job title
            2. Detailed job description with responsibilities
            3. Required skills (list of 8-12 skills)
            4. Preferred skills (list of 8-12 skills)
            
            Format the response as a JSON object with keys: title, description, required_skills, preferred_skills
            """
            
            response = self.llm.invoke(prompt)
            # Parse the response and return structured data
            # This is a simplified version - in practice, you'd need more robust parsing
            return {
                "title": job_role.title(),
                "description": f"Standard {job_role} position with typical responsibilities and requirements.",
                "required_skills": ["communication", "teamwork", "problem solving"],
                "preferred_skills": ["leadership", "project management", "technical skills"]
            }
            
        except Exception as e:
            print(f"Error generating job description: {e}")
            return None
    
    def _extract_profile_skills(self, profile_data: Dict) -> List[str]:
        """Extract all skills from profile data"""
        skills = []
        
        # Extract from skills section
        for skill in profile_data.get("skills", []):
            skills.append(skill.get("name", "").lower())
        
        # Extract from experience descriptions
        for exp in profile_data.get("experience", []):
            description = exp.get("description", "").lower()
            # Extract common skill keywords
            skill_keywords = [
                "python", "javascript", "java", "react", "node.js", "aws", "docker",
                "kubernetes", "sql", "mongodb", "postgresql", "git", "agile", "scrum",
                "leadership", "communication", "teamwork", "problem solving", "project management"
            ]
            for keyword in skill_keywords:
                if keyword in description and keyword not in skills:
                    skills.append(keyword)
        
        # Extract from headline and summary
        basic_info = profile_data.get("basic_info", {})
        headline = basic_info.get("headline", "").lower()
        summary = basic_info.get("summary", "").lower()
        
        for keyword in skill_keywords:
            if keyword in headline and keyword not in skills:
                skills.append(keyword)
            if keyword in summary and keyword not in skills:
                skills.append(keyword)
        
        return list(set(skills))  # Remove duplicates
    
    def _calculate_skill_match(self, profile_skills: List[str], job_skills: List[str]) -> Dict:
        """Calculate skill match between profile and job requirements"""
        matched_skills = []
        missing_skills = []
        
        for skill in job_skills:
            # Check for exact match or partial match
            if skill in profile_skills:
                matched_skills.append(skill)
            else:
                # Check for partial matches
                partial_match = False
                for profile_skill in profile_skills:
                    if skill in profile_skill or profile_skill in skill:
                        matched_skills.append(skill)
                        partial_match = True
                        break
                
                if not partial_match:
                    missing_skills.append(skill)
        
        match_percentage = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0
        
        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_percentage": round(match_percentage, 1),
            "total_required": len(job_skills),
            "total_matched": len(matched_skills)
        }
    
    def _calculate_overall_match_score(self, required_match: Dict, preferred_match: Dict, profile_data: Dict) -> float:
        """Calculate overall job match score"""
        # Weight required skills more heavily than preferred skills
        required_weight = 0.7
        preferred_weight = 0.3
        
        # Base score from skill matches
        required_score = required_match["match_percentage"] * required_weight
        preferred_score = preferred_match["match_percentage"] * preferred_weight
        
        # Additional factors
        experience_bonus = self._calculate_experience_bonus(profile_data)
        education_bonus = self._calculate_education_bonus(profile_data)
        
        overall_score = required_score + preferred_score + experience_bonus + education_bonus
        
        return min(round(overall_score, 1), 100)  # Cap at 100
    
    def _calculate_experience_bonus(self, profile_data: Dict) -> float:
        """Calculate bonus points for relevant experience"""
        experience = profile_data.get("experience", [])
        if len(experience) >= 3:
            return 5.0
        elif len(experience) >= 1:
            return 2.5
        return 0.0
    
    def _calculate_education_bonus(self, profile_data: Dict) -> float:
        """Calculate bonus points for relevant education"""
        education = profile_data.get("education", [])
        if education:
            # Check for relevant degrees
            relevant_fields = ['computer science', 'engineering', 'business', 'mathematics', 'statistics']
            for edu in education:
                field = edu.get("fieldOfStudy", "").lower()
                if any(relevant_field in field for relevant_field in relevant_fields):
                    return 2.5
        return 0.0
    
    def _generate_job_fit_analysis(self, profile_data: Dict, job_desc: Dict, profile_skills: List[str], overall_score: float) -> Dict:
        """Generate detailed job fit analysis"""
        analysis = {
            "strengths": [],
            "weaknesses": [],
            "skill_gaps": [],
            "experience_alignment": "",
            "education_alignment": ""
        }
        
        # Analyze strengths
        if overall_score >= 80:
            analysis["strengths"].append("Excellent match for this role")
        elif overall_score >= 60:
            analysis["strengths"].append("Good match with some areas for improvement")
        
        # Analyze skill gaps
        missing_required = self._identify_missing_skills(profile_skills, job_desc)
        if missing_required:
            analysis["skill_gaps"] = missing_required
            analysis["weaknesses"].append(f"Missing {len(missing_required)} required skills")
        
        # Analyze experience alignment
        experience_count = len(profile_data.get("experience", []))
        if experience_count >= 3:
            analysis["experience_alignment"] = "Strong work experience background"
        elif experience_count >= 1:
            analysis["experience_alignment"] = "Some relevant work experience"
        else:
            analysis["experience_alignment"] = "Limited work experience"
            analysis["weaknesses"].append("Limited work experience")
        
        # Analyze education alignment
        education = profile_data.get("education", [])
        if education:
            analysis["education_alignment"] = "Relevant educational background"
        else:
            analysis["education_alignment"] = "Education information missing"
            analysis["weaknesses"].append("Missing education information")
        
        return analysis
    
    def _identify_missing_skills(self, profile_skills: List[str], job_desc: Dict) -> List[str]:
        """Identify skills that are missing from the profile"""
        missing_skills = []
        
        for skill in job_desc["required_skills"]:
            if skill not in profile_skills:
                # Check for partial matches
                partial_match = False
                for profile_skill in profile_skills:
                    if skill in profile_skill or profile_skill in skill:
                        partial_match = True
                        break
                
                if not partial_match:
                    missing_skills.append(skill)
        
        return missing_skills
    
    def _generate_job_recommendations(self, profile_data: Dict, job_desc: Dict, overall_score: float) -> List[str]:
        """Generate recommendations for improving job fit"""
        recommendations = []
        
        if overall_score < 60:
            recommendations.append("Focus on acquiring the missing required skills")
            recommendations.append("Consider taking relevant courses or certifications")
            recommendations.append("Gain more experience in related roles")
        
        if overall_score < 80:
            recommendations.append("Enhance your profile with more detailed experience descriptions")
            recommendations.append("Add specific achievements and metrics to your experience")
            recommendations.append("Get more skill endorsements from colleagues")
        
        # General recommendations
        recommendations.extend([
            "Tailor your headline and summary to match the job requirements",
            "Highlight relevant projects and achievements",
            "Network with professionals in the target role",
            "Stay updated with industry trends and technologies"
        ])
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _create_error_response(self, error_message: str) -> Dict:
        """Create error response"""
        return {
            "error": error_message,
            "overall_match_score": 0,
            "analysis": {
                "strengths": [],
                "weaknesses": [error_message],
                "recommendations": ["Please try again with a different job role"]
            }
        }
