# 💼 LinkedIn Profile Optimizer

An AI-powered chat system that helps users optimize their LinkedIn profiles, analyze job fit, and provide career guidance. Built with Streamlit, LangGraph, and OpenRouter (free LLM models).

## 🚀 Features

### 🔍 Profile Analysis
- **Comprehensive Analysis**: Evaluate LinkedIn profile sections (About, Experience, Skills, etc.)
- **Gap Identification**: Identify missing information and inconsistencies
- **Scoring System**: Calculate overall profile score and completeness percentage
- **Keyword Optimization**: Analyze keyword coverage and suggest improvements

### 💼 Job Fit Analysis
- **Role Matching**: Compare profiles with industry-standard job descriptions
- **Match Scoring**: Generate detailed match scores for specific roles
- **Skill Gap Analysis**: Identify missing skills needed for target roles
- **Recommendations**: Provide targeted suggestions for job applications

### ✨ Content Enhancement
- **Headline Optimization**: Generate multiple headline versions with different approaches
- **Summary Rewriting**: Create compelling professional summaries
- **Experience Enhancement**: Improve job descriptions with action words and achievements
- **Industry Best Practices**: Align content with LinkedIn optimization standards

### 🎯 Career Guidance
- **Career Path Suggestions**: Recommend potential career trajectories
- **Skill Development Plans**: Create personalized learning roadmaps
- **Learning Resources**: Suggest courses, books, and training programs
- **Goal Setting**: Help users define and track career objectives

### 🧠 Memory System
- **Session Memory**: Maintain context across conversation turns
- **Persistent Memory**: Store user preferences and profile history
- **Context Retention**: Remember previous interactions and recommendations
- **Personalized Experience**: Adapt responses based on user history

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Beautiful, responsive web interface)
- **AI Framework**: LangChain & LangGraph (Multi-agent orchestration)
- **Language Model**: OpenRouter (Free Models: Mistral-7B, Llama-2-7B)
- **Data Scraping**: Apify LinkedIn Profile Scraper
- **Data Visualization**: Plotly (Interactive charts and graphs)
- **Memory Management**: LangGraph Checkpointers
- **Styling**: Custom CSS with LinkedIn-inspired design

## 📋 Prerequisites

- Python 3.8+
- OpenRouter API Key (Free tier available)
- Apify API Token (optional, for LinkedIn scraping)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd linkedin-profile-optimizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   APIFY_API_TOKEN=your_apify_token_here
   ```
   
   **For private profile access**, you'll also need LinkedIn cookies. See [LINKEDIN_COOKIES_GUIDE.md](LINKEDIN_COOKIES_GUIDE.md) for detailed instructions.

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   Open your browser and go to `http://localhost:8501`

## 📖 Usage Guide

### Getting Started

1. **Profile Analysis**
   - Enter your LinkedIn profile URL in the sidebar
   - Click "Analyze Profile" to get comprehensive feedback
   - Review your profile score and improvement areas

2. **Job Fit Analysis**
   - Select a target job role from the dropdown
   - Click "Analyze Job Fit" to see how well you match
   - Review skill gaps and recommendations

3. **Content Enhancement**
   - Use quick action buttons to improve specific sections
   - Get multiple versions of headlines and summaries
   - Enhance experience descriptions with action words

4. **Career Guidance**
   - Ask for career advice and path suggestions
   - Get personalized skill development plans
   - Discover relevant learning resources

### Chat Interface

The main chat interface allows you to:
- Ask natural language questions about your profile
- Request specific improvements or analysis
- Get personalized career guidance
- Maintain conversation context across sessions

### Quick Actions

Use the sidebar for quick access to:
- Profile analysis
- Job fit analysis
- Headline improvement
- Summary enhancement
- Career guidance

## 🏗️ Architecture

### Multi-Agent System

The application uses a sophisticated multi-agent architecture:

1. **LinkedIn Scraper Agent**: Extracts profile data using Apify
2. **Profile Analyzer Agent**: Evaluates profile sections and generates scores
3. **Job Analyzer Agent**: Compares profiles with job requirements
4. **Content Generator Agent**: Creates enhanced profile content
5. **Chat Agent**: Orchestrates all agents and manages conversation flow

### Memory System

- **Session Memory**: Tracks current conversation and profile data
- **Persistent Memory**: Stores user preferences and interaction history
- **Context Management**: Maintains conversation context across turns

### Data Flow

1. User provides LinkedIn URL
2. Scraper extracts profile data
3. Analyzer evaluates profile sections
4. Chat agent processes user requests
5. Appropriate agents generate responses
6. Memory system stores context
7. UI displays results and visualizations

## 📊 Features in Detail

### Profile Analysis
- **Overall Score**: 0-100 rating based on multiple factors
- **Completeness Score**: Percentage of completed profile sections
- **Section Analysis**: Individual scores for headline, summary, experience, skills, education
- **Keyword Coverage**: Analysis of technical, soft skills, and industry keywords

### Job Fit Analysis
- **Match Score**: Overall compatibility with target role
- **Required Skills Match**: Percentage of required skills covered
- **Preferred Skills Match**: Percentage of preferred skills covered
- **Missing Skills**: List of skills to acquire for better fit

### Content Enhancement
- **Multiple Approaches**: Achievement-focused, skill-focused, value-focused content
- **Action Words**: Enhance descriptions with impactful verbs
- **Metrics Integration**: Include quantifiable achievements
- **Industry Alignment**: Follow LinkedIn best practices

### Career Guidance
- **Career Paths**: Suggest logical progression routes
- **Timeline Planning**: Estimate timeframes for career transitions
- **Skill Development**: Prioritized learning recommendations
- **Resource Curation**: Curated list of relevant courses and materials

## 🔧 Configuration

### Environment Variables

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
APIFY_API_TOKEN=your_apify_token_here
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Configuration Options

Edit `config.py` to customize:
- Memory TTL and size limits
- Chat temperature and token limits
- Job match thresholds
- Application settings

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Cloud Deployment

The application can be deployed on:
- **Streamlit Cloud**: Direct deployment from GitHub
- **Heroku**: Using the provided Procfile
- **AWS/GCP**: Using Docker containers
- **Railway**: Simple cloud deployment

### Docker Deployment

```bash
# Build image
docker build -t linkedin-optimizer .

# Run container
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key linkedin-optimizer
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Apify**: For LinkedIn profile scraping capabilities
- **OpenAI**: For powerful language model access
- **Streamlit**: For the beautiful web framework
- **LangChain**: For the AI orchestration framework
- **Plotly**: For interactive data visualizations

## 🛠️ Troubleshooting

### Common Issues

1. **"Profile not found" or "Invalid URL" errors**
   - Check the [LinkedIn Cookies Guide](LINKEDIN_COOKIES_GUIDE.md) for private profile access
   - Verify the LinkedIn URL format: `https://linkedin.com/in/username`
   - Ensure the profile exists and is accessible

2. **Job fit analysis says "Please analyze your profile first"**
   - Make sure you've successfully analyzed a profile before running job fit analysis
   - Check that the profile data was properly stored in memory

3. **API rate limiting or errors**
   - Verify your API keys are valid and have sufficient credits
   - Check your internet connection
   - Try again after a few minutes

4. **Application won't start**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that your `.env` file is properly configured
   - Verify Python version is 3.8 or higher

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the [LinkedIn Cookies Guide](LINKEDIN_COOKIES_GUIDE.md) for profile access issues
- Review the example usage in the README

## 🔮 Future Enhancements

- **Multi-language Support**: Support for multiple languages
- **Advanced Analytics**: More detailed profile insights
- **Integration APIs**: Connect with job boards and learning platforms
- **Mobile App**: Native mobile application
- **Team Features**: Collaborative profile optimization
- **A/B Testing**: Test different profile versions
- **Export Features**: Export analysis reports and recommendations

---

**Built with ❤️ for professional growth and career advancement**
