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
            
            # Get comprehensive cookies for private profile access
            cookies = self._get_comprehensive_linkedin_cookies()
            has_valid_cookies = len(cookies) > 0 and any('li_at' in cookie.get('name', '') for cookie in cookies)
            
            # Enhanced run input with better settings for private profiles
            run_input = {
                "urls": [linkedin_url],
                "cookie": cookies,
                "proxy": self._get_proxy_config(),
                "useChrome": True,
                "headless": True,
                "maxRequestRetries": 5,  # Increased retries
                "timeoutSecs": 120,      # Increased timeout
                "waitUntil": "networkidle",  # Wait for network to be idle
                "waitForSelector": ".pv-top-card",  # Wait for profile content
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            print(f"🔍 Attempting to scrape: {linkedin_url}")
            if not has_valid_cookies:
                print("⚠️  No valid cookies - trying public profile access")
            else:
                print(f"✅ Using {len(cookies)} cookies for authentication")
                print(f"🔑 Cookie names: {[c['name'] for c in cookies]}")
            
            # Use the working actor with enhanced settings
            try:
                print("🔄 Starting LinkedIn profile scraper...")
                run = self.client.actor("curious_coder~linkedin-profile-scraper").call(run_input=run_input)
                print(f"✅ Actor started successfully with run ID: {run.get('id', 'unknown')}")
                
                # Wait for completion with better error handling
                max_wait_time = 300  # 5 minutes
                wait_interval = 10   # Check every 10 seconds
                elapsed_time = 0
                
                while elapsed_time < max_wait_time:
                    try:
                        run_status = self.client.run(run["id"]).get()
                        status = run_status.get("status", "UNKNOWN")
                        
                        if status == "SUCCEEDED":
                            print("✅ Scraping completed successfully!")
                            break
                        elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                            print(f"❌ Scraping failed with status: {status}")
                            return None
                        else:
                            print(f"⏳ Scraping in progress... Status: {status}")
                            
                    except Exception as e:
                        print(f"⚠️  Error checking status: {e}")
                    
                    time.sleep(wait_interval)
                    elapsed_time += wait_interval
                
                if elapsed_time >= max_wait_time:
                    print("⏰ Scraping timed out")
                    return None
                
                # Get results
                dataset = self.client.dataset(run["defaultDatasetId"])
                results = list(dataset.iterate_items())
                
                if results:
                    profile_data = results[0]
                    print(f"🔍 Raw data type: {type(profile_data)}")
                    print(f"🔍 Raw data preview: {str(profile_data)[:200]}...")
                    
                    # Handle case where data might be a string (JSON)
                    if isinstance(profile_data, str):
                        try:
                            import json
                            profile_data = json.loads(profile_data)
                            print("✅ Successfully parsed JSON string")
                        except json.JSONDecodeError:
                            print("❌ Failed to parse JSON string")
                            return None
                    
                    processed_data = self._process_profile_data(profile_data)
                    
                    # Check if we got meaningful data
                    if processed_data and processed_data.get("basic_info", {}).get("full_name"):
                        print(f"✅ Successfully scraped profile: {processed_data['basic_info']['full_name']}")
                        return processed_data
                    else:
                        print("⚠️  Profile scraped but no meaningful data found")
                        if not has_valid_cookies:
                            print("💡 This might be due to profile privacy settings. Try adding more LinkedIn cookies.")
                        return None
                
                print("❌ No results returned from scraper")
                if not has_valid_cookies:
                    print("💡 Profile might be private. Add comprehensive LinkedIn cookies to access private profiles.")
                return None
                
            except Exception as e:
                print(f"❌ Error with actor: {e}")
                return self._fallback_scrape(linkedin_url)
            
        except Exception as e:
            print(f"❌ Error scraping LinkedIn profile: {e}")
            if "not found" in str(e).lower() or "404" in str(e).lower():
                print("💡 Profile URL might be invalid or profile doesn't exist")
            elif "access" in str(e).lower() or "forbidden" in str(e).lower():
                print("💡 Profile might be private. Add comprehensive LinkedIn cookies to access private profiles.")
            return self._fallback_scrape(linkedin_url)
    
    def _get_comprehensive_linkedin_cookies(self) -> list:
        """Get comprehensive LinkedIn cookies for private profile access"""
        # Try to get cookie from config first, then environment
        cookie = getattr(config, 'LINKEDIN_COOKIE', None) or os.getenv('LINKEDIN_COOKIE', '')
        
        if not cookie or 'your_li_at_cookie_here' in cookie.lower():
            print("⚠️  Warning: No valid LinkedIn cookies found.")
            return []
        
        # Convert cookie string to array format for Apify actor
        cookie_parts = cookie.split(';')
        cookie_array = []
        
        # Required cookies for private profile access
        required_cookies = ['li_at', 'JSESSIONID', 'bcookie', 'lang', 'li_mc', 'li_gc']
        
        for part in cookie_parts:
            part = part.strip()
            if '=' in part:
                name, value = part.split('=', 1)
                name = name.strip()
                value = value.strip()
                
                # Add the cookie
                cookie_array.append({
                    "name": name,
                    "value": value,
                    "domain": ".linkedin.com"
                })
                
                # Check if it's a required cookie
                if name in required_cookies:
                    print(f"✅ Found required cookie: {name}")
            elif part:  # Handle cookies without '=' (like some session cookies)
                cookie_array.append({
                    "name": part,
                    "value": "",
                    "domain": ".linkedin.com"
                })
        
        # Add additional cookies that might be missing but are often needed
        additional_cookies = {
            "lang": "en_US",
            "li_mc": "1",
            "li_gc": "MToxOjE=",
            "bcookie": '"v=2&1234567890"',
            "bscookie": '"v=1&1234567890"',
            "li_theme": "minimal",
            "li_theme_set": "app",
            "timezone": "America/New_York"
        }
        
        # Add missing cookies that aren't already present
        existing_names = [c['name'] for c in cookie_array]
        for name, value in additional_cookies.items():
            if name not in existing_names:
                cookie_array.append({
                    "name": name,
                    "value": value,
                    "domain": ".linkedin.com"
                })
                print(f"➕ Added default cookie: {name}")
        
        print(f"📊 Total cookies prepared: {len(cookie_array)}")
        return cookie_array
    
    def _get_linkedin_cookie(self) -> list:
        """Legacy method - use _get_comprehensive_linkedin_cookies instead"""
        return self._get_comprehensive_linkedin_cookies()
    
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
            # Use Apify's proxy service with better settings for private profiles
            return {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"],
                "apifyProxyCountry": "US"
            }
    
    def _fallback_scrape(self, linkedin_url: str) -> Optional[Dict]:
        """Fallback method using direct API call to Apify"""
        try:
            # Alternative approach using Apify API directly
            api_url = "https://api.apify.com/v2/acts/curious_coder~linkedin-profile-scraper/runs"
            
            payload = {
                "urls": [linkedin_url],
                "cookie": self._get_comprehensive_linkedin_cookies(),
                "proxy": self._get_proxy_config(),
                "useChrome": True,
                "headless": True,
                "maxRequestRetries": 5,
                "timeoutSecs": 120
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
                if not isinstance(pos, dict):
                    continue
                    
                time_period = pos.get("timePeriod", {})
                if not isinstance(time_period, dict):
                    time_period = {}
                    
                start_date = time_period.get("startDate", {})
                end_date = time_period.get("endDate", {})
                
                if not isinstance(start_date, dict):
                    start_date = {}
                if not isinstance(end_date, dict):
                    end_date = {}
                
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
                if not isinstance(edu, dict):
                    continue
                    
                time_period = edu.get("timePeriod", {})
                if not isinstance(time_period, dict):
                    time_period = {}
                    
                start_date = time_period.get("startDate", {})
                end_date = time_period.get("endDate", {})
                
                if not isinstance(start_date, dict):
                    start_date = {}
                if not isinstance(end_date, dict):
                    end_date = {}
                
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
                if not isinstance(skill, dict):
                    continue
                    
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
