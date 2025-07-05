import streamlit as st
from pathlib import Path
import os
from dotenv import load_dotenv
import json

# Load environment
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Text Humanizer",
    page_icon="🤖",
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
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key_status' not in st.session_state:
    st.session_state.api_key_status = None

# Header
st.markdown('<h1 class="main-header">🤖 AI Text Humanizer</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Transform AI-generated text into human-like content and detect AI patterns</p>', unsafe_allow_html=True)

# Check API key status
try:
    from src.config.settings import Settings
    from src.services.text_humanizer import TextHumanizer
    from src.services.ai_detector import AIDetector
    
    settings = Settings()
    api_key = settings.get_api_key()
    st.session_state.api_key_status = bool(api_key)
    
    if api_key:
        humanizer = TextHumanizer(api_key)
        detector = AIDetector()
    else:
        st.error("❌ API key not found. Please check your .env file.")
        st.stop()
        
except Exception as e:
    st.error(f"❌ Error initializing application: {str(e)}")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("🎯 Navigation")
    tab = st.radio(
        "Choose a feature:",
        ["Humanize Text", "AI Detector", "History", "Credits", "About"],
        format_func=lambda x: {
            "Humanize Text": "📝 Humanize Text",
            "AI Detector": "🤖 AI Detector", 
            "History": "📚 History",
            "Credits": "💳 Credits",
            "About": "ℹ️ About"
        }[x]
    )
    
    st.divider()
    
    # API Status
    if st.session_state.api_key_status:
        st.success("✅ API Key: Connected")
    else:
        st.error("❌ API Key: Not Found")
    
    # Quick stats
    if tab == "History":
        history_file = Path(TextHumanizer.HISTORY_FILE)
        if history_file.exists():
            try:
                with open(history_file, "r", encoding="utf-8") as file:
                    history = json.load(file)
                st.metric("Total Entries", len(history))
            except:
                st.metric("Total Entries", 0)
        else:
            st.metric("Total Entries", 0)

# Main content
if tab == "Humanize Text":
    st.header("📝 Humanize Text")
    st.markdown("Transform AI-generated text into natural, human-like content.")
    
    # Settings
    with st.expander("⚙️ Humanization Settings", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            readability = st.selectbox(
                "📚 Readability Level",
                ["High School", "University", "Doctorate", "Journalist", "Marketing"],
                index=1,
                help="Choose the target reading level for your text"
            )
        with col2:
            purpose = st.selectbox(
                "🎯 Purpose",
                [
                    "General Writing", "Essay", "Article", "Marketing Material", "Story",
                    "Cover Letter", "Report", "Business Material", "Legal Material"
                ],
                index=0,
                help="Select the intended purpose of your text"
            )
        with col3:
            strength = st.selectbox(
                "💪 Humanization Strength",
                ["Quality", "Balanced", "More Human"],
                index=2,
                help="Choose how strongly to humanize the text"
            )
    
    # Text input
    text = st.text_area(
        "📝 Enter your text",
        height=250,
        max_chars=10000,
        placeholder="Paste or type the AI-generated text you want to humanize here...",
        help="Minimum 50 characters, maximum 10,000 characters"
    )
    
    # Character counter
    char_count = len(text)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Characters", char_count)
    with col2:
        st.metric("Words", len(text.split()) if text else 0)
    with col3:
        if char_count < 50:
            st.error("Too Short")
        elif char_count > 10000:
            st.error("Too Long")
        else:
            st.success("Good Length")
    
    # Process button
    if st.button("🚀 Humanize Text", type="primary", use_container_width=True):
        if len(text) < 50:
            st.error("❌ Text too short! Minimum 50 characters required.")
        elif len(text) > 10000:
            st.error("❌ Text too long! Maximum 10,000 characters allowed.")
        else:
            with st.spinner("🔄 Humanizing your text..."):
                try:
                    result = humanizer.humanize_text(
                        text=text,
                        readability=readability,
                        purpose=purpose,
                        strength=strength
                    )
                    
                    if result and result.get("output"):
                        st.success("✅ Text humanization completed!")
                        
                        # Results display
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.subheader("🎯 Humanized Text")
                        st.write(result["output"])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Word Count", len(result["output"].split()))
                        with col2:
                            st.metric("Character Count", len(result["output"]))
                        with col3:
                            st.metric("Processing Time", "~30s")
                        
                        # Settings used
                        st.info(f"**Settings Used:** Readability: {result.get('readability', 'N/A')} | Purpose: {result.get('purpose', 'N/A')}")
                        
                        # Download button
                        if st.download_button(
                            label="💾 Download Humanized Text",
                            data=result["output"],
                            file_name=f"humanized_text_{readability.lower().replace(' ', '_')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        ):
                            st.success("📥 File downloaded successfully!")
                    else:
                        st.error("❌ Text humanization failed. Please check your API key and try again.")
                        
                except Exception as e:
                    st.error(f"❌ Error during humanization: {str(e)}")

elif tab == "AI Detector":
    st.header("🤖 AI Detector")
    st.markdown("Analyze text to determine if it was written by AI using advanced pattern recognition.")
    
    # Text input
    text = st.text_area(
        "🔍 Enter text to analyze",
        height=250,
        max_chars=5000,
        placeholder="Paste or type the text you want to analyze for AI detection...",
        help="Minimum 10 characters, maximum 5,000 characters"
    )
    
    # Character counter
    char_count = len(text)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Characters", char_count)
    with col2:
        if char_count < 10:
            st.error("Too Short")
        elif char_count > 5000:
            st.error("Too Long")
        else:
            st.success("Good Length")
    
    # Process button
    if st.button("🔍 Detect AI", type="primary", use_container_width=True):
        if len(text) < 10:
            st.error("❌ Text too short! Minimum 10 characters required.")
        elif len(text) > 5000:
            st.error("❌ Text too long! Maximum 5,000 characters allowed.")
        else:
            with st.spinner("🔍 Analyzing text patterns..."):
                try:
                    result = detector.detect_ai(text)
                    
                    if result:
                        st.success("✅ AI detection completed!")
                        
                        # Score display
                        score = result['score'] * 100
                        if score < 30:
                            color = "green"
                            status = "🟢 Likely Human-Written"
                        elif score < 70:
                            color = "orange"
                            status = "🟡 Uncertain"
                        else:
                            color = "red"
                            status = "🔴 Likely AI-Generated"
                        
                        # Main metric
                        st.metric("AI Detection Score", f"{score:.1f}%", delta=status)
                        
                        # Detailed results
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Result:** {result['result']}")
                        with col2:
                            st.markdown(f"**Confidence:** {score:.1f}%")
                        
                        # Analysis details
                        st.info(f"**Analysis Details:** {result['details']}")
                        
                        # Download button
                        if st.download_button(
                            label="💾 Download Analysis Report",
                            data=f"AI Detection Report\n{'='*50}\nScore: {score:.1f}%\nResult: {result['result']}\nDetails: {result['details']}\nTimestamp: {result.get('timestamp', 'N/A')}",
                            file_name="ai_detection_report.txt",
                            mime="text/plain",
                            use_container_width=True
                        ):
                            st.success("📥 Report downloaded successfully!")
                    else:
                        st.error("❌ AI detection failed. Please try again.")
                        
                except Exception as e:
                    st.error(f"❌ Error during detection: {str(e)}")

elif tab == "History":
    st.header("📚 Humanization History")
    st.markdown("View your recent text humanization activities.")
    
    history_file = Path(TextHumanizer.HISTORY_FILE)
    if not history_file.exists():
        st.info("📝 No history found. Start humanizing some text to see your history here!")
    else:
        try:
            with open(history_file, "r", encoding="utf-8") as file:
                history = json.load(file)
            
            if not history:
                st.info("📝 No history found. Start humanizing some text to see your history here!")
            else:
                st.success(f"📊 Showing last 10 entries (Total: {len(history)})")
                
                for i, entry in enumerate(history[-10:][::-1]):
                    timestamp = entry.get('timestamp', '')[:19] if entry.get('timestamp') else 'Unknown'
                    purpose = entry.get('purpose', 'N/A')
                    
                    with st.expander(f"📅 {timestamp} | 🎯 {purpose}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**📥 Input Text:**")
                            st.text(entry.get('input', '')[:300] + "..." if len(entry.get('input', '')) > 300 else entry.get('input', ''))
                        with col2:
                            st.markdown("**📤 Output Text:**")
                            st.text(entry.get('output', '')[:300] + "..." if len(entry.get('output', '')) > 300 else entry.get('output', ''))
                        
                        st.caption(f"📚 Readability: {entry.get('readability', 'N/A')} | 🎯 Purpose: {entry.get('purpose', 'N/A')} | 💪 Strength: {entry.get('strength', 'N/A')}")
                        
        except Exception as e:
            st.error(f"❌ Error reading history: {str(e)}")

elif tab == "Credits":
    st.header("💳 Credits & Account")
    st.markdown("Manage your Undetectable.AI account and check credit balance.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔗 Quick Links")
        st.markdown("- [📊 Dashboard](https://undetectable.ai/dashboard)")
        st.markdown("- [💰 Purchase Credits](https://undetectable.ai/)")
        st.markdown("- [📧 Support](https://undetectable.ai/support)")
        st.markdown("- [📖 Documentation](https://undetectable.ai/docs)")
    
    with col2:
        st.markdown("### 📋 Account Status")
        if st.session_state.api_key_status:
            st.success("✅ API Key: Connected")
            st.info("Your API key is properly configured and ready to use.")
        else:
            st.error("❌ API Key: Not Found")
            st.warning("Please check your .env file configuration.")
    
    st.divider()
    
    st.markdown("### ⚠️ Important Notes")
    st.warning("**Credit Management:**")
    st.markdown("- Check your credit balance regularly")
    st.markdown("- 402 errors indicate you're out of credits")
    st.markdown("- Credits are consumed per humanization request")
    
    st.info("**Security:**")
    st.markdown("- Never share your API key publicly")
    st.markdown("- Keep your .env file secure")
    st.markdown("- Monitor your usage to avoid unexpected charges")

else:  # About tab
    st.header("ℹ️ About AI Text Humanizer")
    st.markdown("A comprehensive tool for humanizing AI-generated text and detecting AI content patterns.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Features")
        st.markdown("- **Text Humanization**: Convert AI text to human-like content")
        st.markdown("- **AI Detection**: Advanced pattern recognition")
        st.markdown("- **Multiple Settings**: Customizable readability and purpose")
        st.markdown("- **History Tracking**: View your past activities")
        st.markdown("- **File Export**: Download results easily")
    
    with col2:
        st.markdown("### 🛠️ Technology")
        st.markdown("- **Backend**: Python with modular architecture")
        st.markdown("- **UI**: Streamlit for web interface")
        st.markdown("- **API**: Undetectable.AI integration")
        st.markdown("- **Analysis**: Heuristic-based AI detection")
        st.markdown("- **Storage**: Local JSON history")
    
    st.divider()
    
    st.markdown("### 📊 AI Detection Algorithm")
    st.markdown("Our AI detector analyzes multiple patterns:")
    st.markdown("- **Repetitive Patterns**: High word repetition detection")
    st.markdown("- **Formal Language**: Detection of formal phrases")
    st.markdown("- **Perfect Structure**: Overly consistent sentence lengths")
    st.markdown("- **No Contractions**: Lack of natural contractions")
    st.markdown("- **Complex Vocabulary**: Overuse of formal words")
    st.markdown("- **Repetitive Sentence Starts**: Similar sentence beginnings")
    st.markdown("- **Personal Pronouns**: Lack of personal pronouns")
    
    st.divider()
    
    st.markdown("### 🎯 Scoring System")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("🟢 Human-Written\n< 30% AI probability")
    with col2:
        st.warning("🟡 Uncertain\n30-70% AI probability")
    with col3:
        st.error("🔴 AI-Generated\n> 70% AI probability") 