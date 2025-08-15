# Deployment Guide: Streamlit Cloud

## Prerequisites
- GitHub repository with your code (✅ Already done!)
- Streamlit Cloud account (free at https://share.streamlit.io/)

## Step 1: Sign up for Streamlit Cloud
1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

## Step 2: Deploy Your App
1. Click "New app" in Streamlit Cloud
2. Select your repository: `VipraN9/Linkedin-agentic-AI-career-coach`
3. Set the main file path: `app.py`
4. Click "Deploy!"

## Step 3: Configure Environment Variables (SECURE YOUR CREDENTIALS)
**This is the most important step to keep your credentials safe!**

1. In your deployed app, go to "Settings" → "Secrets"
2. Add your environment variables:

```toml
OPENROUTER_API_KEY = "your_actual_openrouter_api_key"
APIFY_API_TOKEN = "your_actual_apify_token"
```

**Important Security Notes:**
- ✅ These secrets are encrypted and never visible in your code
- ✅ They're only accessible to your app at runtime
- ✅ They won't be committed to your GitHub repository
- ✅ Streamlit Cloud automatically loads them as environment variables

## Step 4: Test Your Deployment
1. Your app will be available at: `https://your-app-name.streamlit.app`
2. Test all features to ensure they work with the environment variables
3. Check that your credentials are working properly

## Local Development
For local development, create a `.streamlit/secrets.toml` file:
```toml
OPENROUTER_API_KEY = "your_actual_openrouter_api_key"
APIFY_API_TOKEN = "your_actual_apify_token"
```

## Troubleshooting
- If the app fails to deploy, check the logs in Streamlit Cloud
- Ensure all required packages are in `requirements.txt`
- Verify your API keys are valid and have sufficient credits
- Check that your repository is public (required for free Streamlit Cloud)

## Security Best Practices
- ✅ Never commit real API keys to GitHub
- ✅ Use environment variables for all sensitive data
- ✅ Regularly rotate your API keys
- ✅ Monitor your API usage to avoid unexpected charges
