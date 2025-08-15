import streamlit as st
import streamlit_chat
import uuid
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import config
from chat_agent import LinkedInChatAgent

# Page configuration
st.set_page_config(
    page_title="LinkedIn Profile Optimizer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #0077B5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .stButton > button {
        background-color: #0077B5;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        border: none;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #005885;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_agent' not in st.session_state:
    st.session_state.chat_agent = LinkedInChatAgent()

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'profile_data' not in st.session_state:
    st.session_state.profile_data = None

if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None

def main():
    # Debug section - remove this after confirming secrets work
    with st.expander("🔧 Debug Info (Remove after testing)"):
        st.write("**API Keys Status:**")
        st.write(f"OpenRouter API Key: {'✅ Set' if config.OPENROUTER_API_KEY else '❌ Missing'}")
        st.write(f"Apify API Token: {'✅ Set' if config.APIFY_API_TOKEN else '❌ Missing'}")
        
        if not config.OPENROUTER_API_KEY or not config.APIFY_API_TOKEN:
            st.error("⚠️ Missing API keys! Please check your Streamlit Cloud secrets configuration.")
            st.info("Go to your app Settings → Secrets and add your API keys.")
    
    # Header
    st.markdown('<h1 class="main-header">💼 LinkedIn Profile Optimizer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered profile analysis, job matching, and career guidance</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Quick Actions")
        
        # Profile input
        st.subheader("📋 Profile Analysis")
        linkedin_url = st.text_input(
            "Enter LinkedIn URL",
            placeholder="https://linkedin.com/in/your-profile",
            help="Paste your LinkedIn profile URL to get started"
        )
        
        if st.button("🔍 Analyze Profile", use_container_width=True):
            if linkedin_url:
                with st.spinner("Analyzing your profile..."):
                    response = st.session_state.chat_agent.process_message(
                        st.session_state.user_id, 
                        f"Please analyze my LinkedIn profile: {linkedin_url}"
                    )
                    st.session_state.messages.append({"role": "user", "content": f"Analyze: {linkedin_url}"})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.success("Profile analysis complete!")
            else:
                st.error("Please enter a LinkedIn URL")
        
        st.divider()
        
        # Job analysis
        st.subheader("💼 Job Fit Analysis")
        job_role = st.selectbox(
            "Select Job Role",
            ["", "Software Engineer", "Data Scientist", "Product Manager", "DevOps Engineer", "Other"],
            help="Choose a role to analyze your fit"
        )
        
        if st.button("🎯 Analyze Job Fit", use_container_width=True) and job_role:
            # Check if profile data exists in memory system
            profile_data = st.session_state.chat_agent.memory_system.get_profile_context(st.session_state.user_id)
            if profile_data:
                with st.spinner("Analyzing job fit..."):
                    response = st.session_state.chat_agent.process_message(
                        st.session_state.user_id,
                        f"Analyze my fit for {job_role} position"
                    )
                    st.session_state.messages.append({"role": "user", "content": f"Job fit for: {job_role}"})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.success("Job analysis complete!")
            else:
                st.error("Please analyze your profile first")
        
        st.divider()
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Improve Headline", use_container_width=True):
                profile_data = st.session_state.chat_agent.memory_system.get_profile_context(st.session_state.user_id)
                if profile_data:
                    response = st.session_state.chat_agent.process_message(
                        st.session_state.user_id,
                        "Help me improve my headline"
                    )
                    st.session_state.messages.append({"role": "user", "content": "Improve headline"})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Profile needed")
        
        with col2:
            if st.button("📖 Enhance Summary", use_container_width=True):
                profile_data = st.session_state.chat_agent.memory_system.get_profile_context(st.session_state.user_id)
                if profile_data:
                    response = st.session_state.chat_agent.process_message(
                        st.session_state.user_id,
                        "Help me improve my summary"
                    )
                    st.session_state.messages.append({"role": "user", "content": "Improve summary"})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Profile needed")
        
        if st.button("🎯 Career Guidance", use_container_width=True):
            profile_data = st.session_state.chat_agent.memory_system.get_profile_context(st.session_state.user_id)
            if profile_data:
                response = st.session_state.chat_agent.process_message(
                    st.session_state.user_id,
                    "Provide career guidance"
                )
                st.session_state.messages.append({"role": "user", "content": "Career guidance"})
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.error("Profile needed")
        
        st.divider()
        
        # Session info
        st.subheader("ℹ️ Session Info")
        st.info(f"Session ID: {st.session_state.user_id[:8]}...")
        
        if st.button("🔄 Clear Session", use_container_width=True):
            st.session_state.messages = []
            st.session_state.profile_data = None
            st.session_state.analysis_data = None
            # Clear memory system as well
            st.session_state.chat_agent.memory_system.clear_session(st.session_state.user_id)
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat interface
        st.subheader("💬 Chat with AI Assistant")
        
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about your LinkedIn profile..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chat_agent.process_message(
                        st.session_state.user_id, prompt
                    )
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.markdown(response)
    
    with col2:
        # Profile insights
        st.subheader("📊 Profile Insights")
        
        if st.session_state.profile_data:
            # Basic info
            basic_info = st.session_state.profile_data.get("basic_info", {})
            name = basic_info.get("full_name", "Unknown")
            headline = basic_info.get("headline", "No headline")
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>👤 {name}</h4>
                <p><em>{headline}</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Experience count
            experience_count = len(st.session_state.profile_data.get("experience", []))
            st.metric("💼 Experience", experience_count)
            
            # Skills count
            skills_count = len(st.session_state.profile_data.get("skills", []))
            st.metric("🛠️ Skills", skills_count)
            
            # Education count
            education_count = len(st.session_state.profile_data.get("education", []))
            st.metric("🎓 Education", education_count)
            
            # Profile completeness
            if st.session_state.analysis_data:
                completeness = st.session_state.analysis_data.get("completeness_score", 0)
                st.metric("📈 Completeness", f"{completeness}%")
                
                # Progress bar for completeness
                st.progress(completeness / 100)
            
            # Skills visualization
            if st.session_state.profile_data.get("skills"):
                skills_data = st.session_state.profile_data["skills"]
                if len(skills_data) > 0:
                    st.subheader("🛠️ Top Skills")
                    
                    # Create skills chart
                    skills_df = pd.DataFrame(skills_data[:10])  # Top 10 skills
                    if not skills_df.empty and "endorsements" in skills_df.columns:
                        fig = px.bar(
                            skills_df,
                            x="endorsements",
                            y="name",
                            orientation="h",
                            title="Skills by Endorsements",
                            labels={"endorsements": "Endorsements", "name": "Skill"}
                        )
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("👆 Start by analyzing your LinkedIn profile to see insights here!")
    
    # Bottom section for detailed analysis
    if st.session_state.profile_data and st.session_state.analysis_data:
        st.divider()
        st.subheader("📈 Detailed Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 Overall Score")
            overall_score = st.session_state.analysis_data.get("overall_score", 0)
            
            # Create gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=overall_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Profile Score"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#0077B5"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Section Scores")
            section_analysis = st.session_state.analysis_data.get("section_analysis", {})
            
            sections = ["headline", "summary", "experience", "skills", "education"]
            scores = []
            
            for section in sections:
                if section in section_analysis:
                    score = section_analysis[section].get("score", 0)
                    scores.append(score)
                else:
                    scores.append(0)
            
            # Create radar chart
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=sections,
                fill='toself',
                name='Profile Sections',
                line_color='#0077B5'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5]
                    )),
                showlegend=False,
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown("### 🔍 Keyword Analysis")
            keyword_analysis = st.session_state.analysis_data.get("keyword_optimization", {})
            
            if keyword_analysis:
                categories = list(keyword_analysis.keys())
                coverages = [keyword_analysis[cat].get("coverage", 0) for cat in categories]
                
                fig = px.bar(
                    x=categories,
                    y=coverages,
                    title="Keyword Coverage by Category",
                    labels={"x": "Category", "y": "Coverage %"}
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>💼 LinkedIn Profile Optimizer | Powered by AI | Built with Streamlit</p>
        <p>Get personalized insights to boost your professional presence!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
