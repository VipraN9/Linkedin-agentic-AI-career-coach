# Troubleshooting Guide: Streamlit Cloud Deployment

## Issue: "No such profile found" Error on Streamlit Cloud

### Root Cause
The error occurs because your API keys are not being loaded properly in Streamlit Cloud. Your local environment works because it has access to `.env` files, but Streamlit Cloud uses a different secrets management system.

### ✅ Solution Applied
I've updated your `config.py` to properly handle both local development and Streamlit Cloud deployment:

1. **Added `get_secret()` function** that tries Streamlit secrets first, then falls back to environment variables
2. **Added debug section** to your app to verify API keys are loaded
3. **Updated all secret loading** to use the new function

### 🔧 How to Fix Your Deployment

#### Step 1: Check Your Streamlit Cloud Secrets
1. Go to your Streamlit Cloud app: https://share.streamlit.io/
2. Click on your app
3. Go to **Settings** → **Secrets**
4. Add your API keys in this exact format:

```toml
OPENROUTER_API_KEY = "your_actual_openrouter_api_key_here"
APIFY_API_TOKEN = "your_actual_apify_token_here"
```

#### Step 2: Verify Secrets Are Loaded
1. After adding secrets, your app will automatically redeploy
2. Open your deployed app
3. Look for the **"🔧 Debug Info"** expandable section
4. Check if both API keys show "✅ Set"

#### Step 3: Test Your App
1. Try the LinkedIn URL that was failing before
2. If it works, you can remove the debug section later

### 🚨 Common Issues and Solutions

#### Issue 1: "No such profile found" persists
**Cause**: Apify API token not loaded
**Solution**: 
- Check Streamlit Cloud secrets
- Verify your Apify token is valid
- Test with a simple LinkedIn URL first

#### Issue 2: "API key not found" errors
**Cause**: OpenRouter API key not loaded
**Solution**:
- Check Streamlit Cloud secrets
- Verify your OpenRouter key is valid
- Check your OpenRouter account credits

#### Issue 3: App fails to deploy
**Cause**: Missing dependencies or configuration
**Solution**:
- Check Streamlit Cloud logs
- Verify `requirements.txt` is complete
- Ensure repository is public (for free tier)

### 🔍 Debugging Steps

1. **Check Debug Section**: Look for the debug expandable in your deployed app
2. **Check Streamlit Logs**: Go to your app settings and check deployment logs
3. **Test API Keys Locally**: Verify your keys work in local development
4. **Check API Credits**: Ensure you have sufficient credits on OpenRouter/Apify

### 📝 After Fixing

Once your app works:
1. Remove the debug section from `app.py`
2. Commit and push the changes
3. Your app will be fully functional

### 🛡️ Security Reminder

- ✅ Never commit real API keys to GitHub
- ✅ Always use Streamlit Cloud secrets for production
- ✅ Keep your `.env` file for local development only
- ✅ Regularly rotate your API keys

### 📞 Need More Help?

If the issue persists:
1. Check the Streamlit Cloud logs for specific error messages
2. Verify your API keys are working in a simple test script
3. Contact Streamlit support if it's a platform issue
