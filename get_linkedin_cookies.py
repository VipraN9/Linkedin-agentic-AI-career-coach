#!/usr/bin/env python3
"""
Helper script to get LinkedIn cookies
"""

def show_cookie_instructions():
    print("🍪 LinkedIn Cookie Setup Guide")
    print("=" * 50)
    print()
    print("1. Go to LinkedIn.com and log in")
    print("2. Press F12 to open Developer Tools")
    print("3. Go to 'Application' tab (or 'Storage')")
    print("4. Click on 'Cookies' → 'https://www.linkedin.com'")
    print("5. Find and copy these cookies:")
    print()
    print("   🔑 li_at (most important)")
    print("   🔑 JSESSIONID")
    print("   🔑 bcookie")
    print()
    print("6. Add them to your .env file:")
    print()
    print("   LINKEDIN_COOKIE=\"li_at=YOUR_VALUE; JSESSIONID=YOUR_VALUE\"")
    print()
    print("📝 Example:")
    print("   LINKEDIN_COOKIE=\"li_at=AQEDARqM1D0CqSx-AAABjAL_6LQ; JSESSIONID=ajax:1234567890\"")
    print()
    print("✅ After adding cookies, your scraper will work!")

if __name__ == "__main__":
    show_cookie_instructions()
