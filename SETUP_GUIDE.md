# 🚀 Setup Guide for LinkedIn Profile Optimizer

## 📋 Prerequisites

Before running the application, you need to set up the following:

### 1. OpenRouter API Key (Required)

OpenRouter provides access to multiple free and paid LLM models. Here's how to get your API key:

1. **Visit OpenRouter**: Go to [https://openrouter.ai](https://openrouter.ai)
2. **Sign Up**: Create a free account
3. **Get API Key**: 
   - Go to your dashboard
   - Click on "API Keys" in the sidebar
   - Click "Create API Key"
   - Copy the generated key

**Free Tier Benefits:**
- 10,000 requests per month
- Access to models like Mistral-7B, Llama-2-7B, and others
- No credit card required for free tier

### 2. Apify API Token (Optional)

For LinkedIn profile scraping functionality:

1. **Visit Apify**: Go to [https://apify.com](https://apify.com)
2. **Sign Up**: Create a free account
3. **Get API Token**:
   - Go to your account settings
   - Click on "API tokens"
   - Create a new token
   - Copy the token

**Note**: The application includes mock data for testing, so Apify is optional.

## 🔧 Installation Steps

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd linkedin-profile-optimizer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the root directory:

```env
# Required
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional (for LinkedIn scraping)
APIFY_API_TOKEN=your_apify_token_here

# Optional (for custom configuration)
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Step 4: Test the Setup
Run the OpenRouter test to verify your configuration:

```bash
python test_openrouter.py
```

You should see:
```
🧪 Testing OpenRouter Integration...
✅ OpenRouter API key found
✅ Direct OpenRouter test: OpenRouter is working!...
✅ ChatOpenAI wrapper test: ChatOpenAI wrapper is working!...
🎉 All OpenRouter tests passed!
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🧪 Testing the Application

### Quick Test
1. Open the application in your browser
2. In the sidebar, click "Analyze Profile" without entering a URL
3. The system will use mock data to demonstrate functionality
4. Try the "Career Guidance" feature to test AI responses

### Full Test
1. Enter a LinkedIn profile URL in the sidebar
2. Click "Analyze Profile" to test real profile scraping
3. Try different job roles for "Job Fit Analysis"
4. Test content enhancement features

## 🔍 Troubleshooting

### Common Issues

**1. "OpenRouter API key not found"**
- Make sure your `.env` file exists in the root directory
- Verify the API key is correctly copied from OpenRouter
- Check that there are no extra spaces or characters

**2. "Error calling OpenRouter API"**
- Verify your internet connection
- Check if you have sufficient credits on OpenRouter
- Try running `python test_openrouter.py` to diagnose

**3. "Module not found" errors**
- Make sure you've installed all dependencies: `pip install -r requirements.txt`
- Check that you're in the correct directory

**4. Streamlit not starting**
- Check if port 8501 is already in use
- Try changing the port in your `.env` file
- Restart your terminal/command prompt

### Getting Help

If you encounter issues:

1. **Check the logs**: Look for error messages in the terminal
2. **Run tests**: Use `python test_openrouter.py` and `python test_app.py`
3. **Verify setup**: Double-check your API keys and environment variables
4. **Check OpenRouter status**: Visit [https://openrouter.ai/status](https://openrouter.ai/status)

## 💡 Tips for Best Results

1. **Use Real LinkedIn URLs**: For the best analysis, use actual LinkedIn profile URLs
2. **Be Specific**: When asking for career guidance, mention specific roles or industries
3. **Try Different Models**: The app automatically falls back to different models if one fails
4. **Save Your Work**: The app maintains session memory, so you can continue conversations

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and don't share them
- The `.env` file is already in `.gitignore` for your protection
- OpenRouter API keys are tied to your account and usage

## 📞 Support

For issues related to:
- **OpenRouter**: Visit [https://openrouter.ai/support](https://openrouter.ai/support)
- **Apify**: Visit [https://apify.com/support](https://apify.com/support)
- **Application**: Check the project's GitHub issues or documentation
