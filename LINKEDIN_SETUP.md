# 🔧 LinkedIn Scraper Setup Guide

## 🍪 **How to Get LinkedIn Cookies:**

### **Method 1: Browser Developer Tools**
1. **Go to LinkedIn** and log in
2. **Open Developer Tools** (F12)
3. **Go to Application/Storage tab**
4. **Find Cookies** → `https://www.linkedin.com`
5. **Copy these cookies:**
   - `li_at` (most important)
   - `JSESSIONID`
   - `bcookie`

### **Method 2: Browser Extension**
1. **Install "Cookie Editor" extension**
2. **Go to LinkedIn**
3. **Click extension** → Export → Copy as cURL
4. **Extract cookies** from the cURL command

## 🌐 **How to Get Proxy:**

### **Option 1: Use Apify Proxy (Recommended)**
- **Free with Apify account**
- **No setup needed** - already configured in code

### **Option 2: Your Own Proxy**
- **Buy from**: Bright Data, Oxylabs, SmartProxy
- **Format**: `http://username:password@proxy-server:port`

## ⚙️ **Setup in .env file:**

```bash
# Add these to your .env file:
LINKEDIN_COOKIE="li_at=YOUR_LI_AT_VALUE; JSESSIONID=YOUR_JSESSIONID_VALUE"
PROXY_URL="http://username:password@proxy-server:port"  # Optional
```

## 🚀 **Quick Test:**

```bash
python test_openrouter.py
```

## 📝 **Cookie Format Example:**
```
li_at=AQEDARqM1D0CqSx-AAABjAL_6LQAAAGM1Q8I6LQAAAGM1Q8I6LQ; JSESSIONID=ajax:1234567890; bcookie="v=2&1234567890"
```

