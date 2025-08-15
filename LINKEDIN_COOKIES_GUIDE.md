# LinkedIn Profile Access Guide

## 🔍 Profile Access Types

### Public Profiles (No Cookies Required)
These profiles work without any authentication:
- **Bill Gates**: `https://linkedin.com/in/williamhgates`
- **Satya Nadella**: `https://linkedin.com/in/satya-nadella-59651a14`
- **Other public figures and celebrities**

### Private Profiles (Cookies Required)
These profiles require LinkedIn authentication cookies:
- Your own profile
- Your friends' profiles
- Most regular user profiles
- Company employee profiles

## 🔑 How to Get LinkedIn Cookies

### Step-by-Step Instructions

1. **Go to LinkedIn.com**
   - Open your web browser
   - Navigate to `https://www.linkedin.com`
   - **Log in to your LinkedIn account**

2. **Open Developer Tools**
   - Press `F12` or right-click and select "Inspect"
   - Go to the **Application** tab (Chrome) or **Storage** tab (Firefox)

3. **Find Cookies**
   - In the left sidebar, expand **Cookies**
   - Click on `https://www.linkedin.com`
   - Look for these specific cookies:

### Required Cookies

| Cookie Name | Description | Example |
|-------------|-------------|---------|
| `li_at` | LinkedIn authentication token | `AQEDAR...` (long string) |
| `JSESSIONID` | Session identifier | `ajax:1234567890` |

### Step 4: Copy Cookie Values
1. Find the `li_at` cookie and copy its value
2. Find the `JSESSIONID` cookie and copy its value
3. Combine them in this format:
   ```
   li_at=YOUR_LI_AT_VALUE; JSESSIONID=YOUR_JSESSIONID_VALUE
   ```

### Step 5: Add to Environment File
1. Open your `.env` file in the project directory
2. Add this line:
   ```
   LINKEDIN_COOKIE=li_at=YOUR_LI_AT_VALUE; JSESSIONID=YOUR_JSESSIONID_VALUE
   ```
3. Save the file

## 🔄 Cookie Expiration

**Important**: LinkedIn cookies expire periodically (usually every few weeks). If you start getting "profile not found" errors, you'll need to:

1. Repeat the cookie extraction process
2. Update your `.env` file with the new values
3. Restart the application

## 🛠️ Troubleshooting

### Common Issues

1. **"Profile not found" error**
   - Check if the LinkedIn URL is correct
   - Verify your cookies are not expired
   - Make sure the profile exists and is accessible

2. **"Invalid URL format" error**
   - Ensure the URL follows the format: `https://linkedin.com/in/username`
   - Remove any extra parameters or fragments

3. **"No data returned" error**
   - Profile might be completely private
   - Try with different cookies
   - Check if the profile has any public information

### Browser-Specific Instructions

#### Chrome
1. Press `F12` → Application tab
2. Cookies → `https://www.linkedin.com`
3. Look for `li_at` and `JSESSIONID`

#### Firefox
1. Press `F12` → Storage tab
2. Cookies → `https://www.linkedin.com`
3. Look for `li_at` and `JSESSIONID`

#### Safari
1. Develop → Show Web Inspector
2. Storage → Cookies → `https://www.linkedin.com`
3. Look for `li_at` and `JSESSIONID`

## 🔒 Privacy and Security

- **Never share your cookies** with anyone
- **Don't commit cookies** to version control
- **Use environment variables** to store sensitive data
- **Regularly update cookies** when they expire

## 📝 Example .env File

```env
# LinkedIn Profile Optimizer Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
APIFY_TOKEN=your_apify_token_here

# LinkedIn Cookies (for private profile access)
LINKEDIN_COOKIE=li_at=AQEDAR...; JSESSIONID=ajax:1234567890

# Optional: Custom Proxy (if needed)
PROXY_URL=http://your-proxy-url:port
```

## 🎯 Quick Test

To test if your cookies are working:

1. Add your cookies to `.env`
2. Run the application
3. Try to analyze your own LinkedIn profile
4. If it works, your cookies are valid!

## 📞 Support

If you're still having issues:
1. Check that your LinkedIn account is active
2. Verify the profile URL is correct
3. Try with a different LinkedIn account
4. Ensure you're not being rate-limited by LinkedIn
