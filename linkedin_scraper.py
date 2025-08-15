import requests
import json
import time
import os
from typing import Dict, Optional, List
from apify_client import ApifyClient
import config

class LinkedInScraper:
    def __init__(self):
        self.apify_token = config.APIFY_API_TOKEN
        self.client = ApifyClient(self.apify_token) if self.apify_token else None
        
    def extract_linkedin_id_from_url(self, linkedin_url: str) -> Optional[str]:
        """Extract LinkedIn profile ID from URL"""
        try:
            # Handle different LinkedIn URL formats
            if "linkedin.com/in/" in linkedin_url:
                # Extract the profile identifier
                parts = linkedin_url.split("linkedin.com/in/")
                if len(parts) > 1:
                    profile_id = parts[1].split("/")[0].split("?")[0]
                    return profile_id
            return None
        except Exception as e:
            print(f"Error extracting LinkedIn ID: {e}")
            return None
    
    def scrape_profile(self, linkedin_url: str) -> Optional[Dict]:
        """Scrape LinkedIn profile using Apify"""
        try:
            if not self.client:
                return self._fallback_scrape(linkedin_url)
            
            profile_id = self.extract_linkedin_id_from_url(linkedin_url)
            if not profile_id:
                print("❌ Invalid LinkedIn URL format")
                return None
            
            # Check if we have valid cookies
            cookies = self._get_linkedin_cookie()
            has_valid_cookies = len(cookies) > 0 and any('li_at' in cookie.get('name', '') for cookie in cookies)
            
            # Run Apify actor with proper cookie and proxy settings
            run_input = {
                "urls": [linkedin_url],
                "cookie": cookies,
                "proxy": self._get_proxy_config(),
                "useChrome": True,
                "headless": True
            }
            
            print(f"🔍 Attempting to scrape: {linkedin_url}")
            if not has_valid_cookies:
                print("⚠️  No valid cookies - profile must be public")
            
            run = self.client.actor("curious_coder~linkedin-profile-scraper").call(run_input=run_input)
            
            # Get results
            dataset = self.client.dataset(run["defaultDatasetId"])
            results = list(dataset.iterate_items())
            
            if results:
                profile_data = results[0]
                processed_data = self._process_profile_data(profile_data)
                
                # Check if we got meaningful data
                if processed_data and processed_data.get("basic_info", {}).get("full_name"):
                    print(f"✅ Successfully scraped profile: {processed_data['basic_info']['full_name']}")
                    return processed_data
                else:
                    print("⚠️  Profile scraped but no meaningful data found")
                    if not has_valid_cookies:
                        print("💡 This might be due to profile privacy settings. Try adding LinkedIn cookies.")
                    return None
            
            print("❌ No results returned from scraper")
            if not has_valid_cookies:
                print("💡 Profile might be private. Add LinkedIn cookies to access private profiles.")
            return None
            
        except Exception as e:
            print(f"❌ Error scraping LinkedIn profile: {e}")
            if "not found" in str(e).lower() or "404" in str(e).lower():
                print("💡 Profile URL might be invalid or profile doesn't exist")
            elif "access" in str(e).lower() or "forbidden" in str(e).lower():
                print("💡 Profile might be private. Add LinkedIn cookies to access private profiles.")
            return self._fallback_scrape(linkedin_url)
    
    def _fallback_scrape(self, linkedin_url: str) -> Optional[Dict]:
        """Fallback method using direct API call to Apify"""
        try:
            # Alternative approach using Apify API directly
            api_url = "https://api.apify.com/v2/acts/curious_coder~linkedin-profile-scraper/runs"
            
            payload = {
                "urls": [linkedin_url],
                "cookie": self._get_linkedin_cookie(),
                "proxy": self._get_proxy_config(),
                "useChrome": True,
                "headless": True
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.apify_token}"
            }
            
            response = requests.post(api_url, json=payload, headers=headers)
            
            if response.status_code == 201:
                run_id = response.json().get("data", {}).get("id")
                
                # Wait for completion
                for _ in range(30):  # Wait up to 5 minutes
                    status_response = requests.get(f"{api_url}/{run_id}", headers=headers)
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        if status_data.get("data", {}).get("status") == "SUCCEEDED":
                            # Get results
                            results_url = f"https://api.apify.com/v2/acts/curious_coder~linkedin-profile-scraper/runs/{run_id}/dataset/items"
                            results_response = requests.get(results_url, headers=headers)
                            if results_response.status_code == 200:
                                results = results_response.json()
                                if results:
                                    return self._process_profile_data(results[0])
                    time.sleep(10)
            
            return None
            
        except Exception as e:
            print(f"Fallback scraping failed: {e}")
            return None
    
    def _get_linkedin_cookie(self) -> list:
        """Get LinkedIn cookie from environment or return default"""
        # You can set this in your .env file as LINKEDIN_COOKIE
        cookie = os.getenv('LINKEDIN_COOKIE', '')
        if not cookie or 'YOUR_LI_AT_COOKIE_HERE' in cookie:
            # No valid cookies provided - this will limit access to public profiles only
            print("⚠️  Warning: No valid LinkedIn cookies found. Only public profiles will be accessible.")
            print("💡 To access private profiles, add your LinkedIn cookies to .env file:")
            print("   1. Go to LinkedIn.com and log in")
            print("   2. Open browser DevTools (F12)")
            print("   3. Go to Application/Storage tab")
            print("   4. Find 'li_at' and 'JSESSIONID' cookies")
            print("   5. Add to .env: LINKEDIN_COOKIE=li_at=YOUR_VALUE; JSESSIONID=YOUR_VALUE")
            return []
        
        # Convert cookie string to array format
        cookie_parts = cookie.split(';')
        cookie_array = []
        for part in cookie_parts:
            part = part.strip()
            if '=' in part:
                name, value = part.split('=', 1)
                cookie_array.append({
                    "name": name.strip(),
                    "value": value.strip(),
                    "domain": ".linkedin.com"
                })
        return cookie_array
    
    def _get_linkedin_cookie_string(self) -> str:
        """Get LinkedIn cookie as string for sessionCookies parameter"""
        return os.getenv('LINKEDIN_COOKIE', '')
    
    def _get_proxy_config(self) -> Dict:
        """Get proxy configuration from environment or return default"""
        proxy_url = os.getenv('PROXY_URL', '')
        if proxy_url:
            return {
                "useApifyProxy": False,
                "proxyUrls": [proxy_url]
            }
        else:
            # Use Apify's proxy service
            return {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"]
            }
    
    def _process_profile_data(self, raw_data: Dict) -> Dict:
        """Process and structure the scraped profile data"""
        try:
            # Handle case where raw_data might be a string or invalid
            if not isinstance(raw_data, dict):
                print(f"⚠️  Invalid data format received: {type(raw_data)}")
                return None
            
            # Build full name from first and last name
            full_name = f"{raw_data.get('firstName', '')} {raw_data.get('lastName', '')}".strip()
            
            processed_data = {
                "basic_info": {
                    "full_name": full_name,
                    "headline": raw_data.get("headline", ""),
                    "location": raw_data.get("geoLocationName", ""),
                    "summary": raw_data.get("summary", ""),
                    "profile_url": f"https://linkedin.com/in/{raw_data.get('publicIdentifier', '')}",
                    "profile_picture": raw_data.get("pictureUrl", "")
                },
                "experience": [],
                "education": [],
                "skills": [],
                "certifications": [],
                "languages": [],
                "volunteer_experience": [],
                "publications": [],
                "patents": [],
                "courses": [],
                "projects": [],
                "honors_awards": [],
                "test_scores": [],
                "organizations": [],
                "people_also_viewed": [],
                "recommendations": [],
                "connections": str(raw_data.get("connectionsCount", "")),
                "followers": str(raw_data.get("followersCount", ""))
            }
            
            # Process experience (positions)
            for pos in raw_data.get("positions", []):
                time_period = pos.get("timePeriod", {})
                start_date = time_period.get("startDate", {})
                end_date = time_period.get("endDate", {})
                
                duration = ""
                if start_date:
                    start_year = start_date.get("year", "")
                    if end_date:
                        end_year = end_date.get("year", "")
                        duration = f"{start_year} - {end_year}"
                    else:
                        duration = f"{start_year} - Present"
                
                processed_data["experience"].append({
                    "title": pos.get("title", ""),
                    "company": pos.get("companyName", ""),
                    "duration": duration,
                    "location": "",
                    "description": ""
                })
            
            # Process education
            for edu in raw_data.get("educations", []):
                time_period = edu.get("timePeriod", {})
                start_date = time_period.get("startDate", {})
                end_date = time_period.get("endDate", {})
                
                duration = ""
                if start_date and end_date:
                    start_year = start_date.get("year", "")
                    end_year = end_date.get("year", "")
                    duration = f"{start_year} - {end_year}"
                
                processed_data["education"].append({
                    "school": edu.get("schoolName", ""),
                    "degree": "",
                    "field": "",
                    "duration": duration,
                    "description": ""
                })
            
            # Process skills (if available)
            for skill in raw_data.get("skills", []):
                processed_data["skills"].append({
                    "name": skill.get("name", ""),
                    "endorsements": skill.get("endorsements", 0)
                })
            
            return processed_data
            
        except Exception as e:
            print(f"Error processing profile data: {e}")
            return raw_data
    
    def get_mock_profile_data(self) -> Dict:
        """Return mock profile data for testing when scraping fails"""
        return {
            "basic_info": {
                "full_name": "John Doe",
                "headline": "Software Engineer | Full Stack Developer | Python Expert",
                "location": "San Francisco, CA",
                "summary": "Experienced software engineer with 5+ years in full-stack development. Passionate about creating scalable web applications and mentoring junior developers.",
                "profile_url": "https://linkedin.com/in/johndoe",
                "profile_picture": ""
            },
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "duration": "2021 - Present",
                    "location": "San Francisco, CA",
                    "description": "Led development of microservices architecture. Mentored 3 junior developers."
                },
                {
                    "title": "Software Engineer",
                    "company": "Startup Inc",
                    "duration": "2019 - 2021",
                    "location": "San Francisco, CA",
                    "description": "Built REST APIs and frontend applications using React and Node.js."
                }
            ],
            "education": [
                {
                    "school": "University of California",
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "duration": "2015 - 2019",
                    "description": "Graduated with honors. Relevant coursework in algorithms, data structures, and software engineering."
                }
            ],
            "skills": [
                {"name": "Python", "endorsements": 25},
                {"name": "JavaScript", "endorsements": 20},
                {"name": "React", "endorsements": 18},
                {"name": "Node.js", "endorsements": 15},
                {"name": "AWS", "endorsements": 12},
                {"name": "Docker", "endorsements": 10}
            ],
            "certifications": [],
            "languages": [],
            "volunteer_experience": [],
            "publications": [],
            "patents": [],
            "courses": [],
            "projects": [],
            "honors_awards": [],
            "test_scores": [],
            "organizations": [],
            "people_also_viewed": [],
            "recommendations": [],
            "connections": "500+",
            "followers": "1000+"
        }
