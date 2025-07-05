import streamlit as st
from pathlib import Path
import os
from dotenv import load_dotenv
import json
import time

# Load environment
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Text Humanizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
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
    .streaming-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        font-family: monospace;
    }
    .nav-item {
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .nav-item:hover {
        background-color: #f0f2f6;
    }
    .nav-item.active {
        background-color: #667eea;
        color: white;
    }
    .document-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .rehumanize-result {
        background-color: #e8f5e8;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .processing-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key_status' not in st.session_state:
    st.session_state.api_key_status = None
if 'streaming_text' not in st.session_state:
    st.session_state.streaming_text = ""
if 'streaming_active' not in st.session_state:
    st.session_state.streaming_active = False
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Humanize Text"
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'rehumanize_results' not in st.session_state:
    st.session_state.rehumanize_results = {}
if 'processing_document' not in st.session_state:
    st.session_state.processing_document = None

# Header
st.markdown('<h1 class="main-header">🤖 AI Text Humanizer</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Transform AI-generated text into human-like content and detect AI patterns</p>', unsafe_allow_html=True)

# Check API key status
try:
    from src.config.settings import Settings
    from src.services.text_humanizer import TextHumanizer
    from src.services.ai_detector import AIDetector
    from src.services.streaming_humanizer import StreamingHumanizer
    
    settings = Settings()
    api_key = settings.get_api_key()
    st.session_state.api_key_status = bool(api_key)
    
    if api_key:
        humanizer = TextHumanizer(api_key)
        detector = AIDetector()
        streaming_humanizer = StreamingHumanizer(api_key)
    else:
        st.error("❌ API key not found. Please check your .env file.")
        st.stop()
        
except Exception as e:
    st.error(f"❌ Error initializing application: {str(e)}")
    st.stop()

# Modern Navigation Sidebar
with st.sidebar:
    st.markdown("## 🎯 Navigation")
    
    # Navigation tabs with modern styling
    nav_options = {
        "Humanize Text": "📝",
        "Streaming Humanize": "⚡", 
        "AI Detector": "🤖",
        "Documents": "📄",
        "History": "📚",
        "Credits": "💳",
        "About": "ℹ️"
    }
    
    # Create navigation buttons
    for tab_name, icon in nav_options.items():
        if st.button(f"{icon} {tab_name}", key=f"nav_{tab_name}", use_container_width=True):
            st.session_state.current_tab = tab_name
            st.rerun()
    
    # Highlight current tab
    st.markdown(f"**Current: {nav_options.get(st.session_state.current_tab, '📝')} {st.session_state.current_tab}**")
    
    st.divider()
    
    # API Status with better styling
    if st.session_state.api_key_status:
        st.success("✅ API Key: Connected")
    else:
        st.error("❌ API Key: Not Found")
    
    # Quick stats
    if st.session_state.current_tab == "History":
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

# Main content based on current tab
tab = st.session_state.current_tab

if tab == "Humanize Text":
    st.header("📝 Humanize Text")
    st.markdown("Transform AI-generated text into natural, human-like content.")
    
    # Settings
    with st.expander("⚙️ Humanization Settings", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
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
        with col4:
            model = st.selectbox(
                "🤖 AI Model",
                ["v11", "v2"],
                index=0,
                help="Choose the AI model version"
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
                        strength=strength,
                        model=model
                    )
                    
                    if result and result.get("output"):
                        st.success("✅ Text humanization completed!")
                        
                        # Results display
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.subheader("🎯 Humanized Text")
                        st.write(result["output"])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Word Count", len(result["output"].split()))
                        with col2:
                            st.metric("Character Count", len(result["output"]))
                        with col3:
                            st.metric("Processing Time", "~30s")
                        with col4:
                            st.metric("Model Used", result.get("model", "N/A"))
                        
                        # Settings used
                        st.info(f"**Settings Used:** Readability: {result.get('readability', 'N/A')} | Purpose: {result.get('purpose', 'N/A')} | Strength: {result.get('strength', 'N/A')}")
                        
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

elif tab == "Streaming Humanize":
    st.header("⚡ Streaming Humanize")
    st.markdown("Humanize text in real-time with streaming results.")
    
    # Instructions
    st.info("""
    **⚡ How to use Streaming Humanize:**
    1. **Configure Settings**: Choose readability, purpose, strength, and model
    2. **Enter Text**: Paste or type your AI-generated text (50-10,000 characters)
    3. **Start Streaming**: Click "Start Streaming" to begin real-time processing
    4. **Watch Progress**: See text being humanized chunk by chunk in real-time
    5. **Stop if Needed**: Use "Stop Streaming" to cancel processing
    6. **Download Result**: Save the completed humanized text
    
    **💡 Benefits of Streaming:**
    - See results as they're generated (no waiting for completion)
    - Real-time progress feedback
    - Ability to cancel mid-process
    - Better user experience for long texts
    """)
    
    # Settings
    with st.expander("⚙️ Streaming Settings", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            readability = st.selectbox(
                "📚 Readability Level",
                ["High School", "University", "Doctorate", "Journalist", "Marketing"],
                index=1,
                key="streaming_readability"
            )
        with col2:
            purpose = st.selectbox(
                "🎯 Purpose",
                [
                    "General Writing", "Essay", "Article", "Marketing Material", "Story",
                    "Cover Letter", "Report", "Business Material", "Legal Material"
                ],
                index=0,
                key="streaming_purpose"
            )
        with col3:
            strength = st.selectbox(
                "💪 Humanization Strength",
                ["Quality", "Balanced", "More Human"],
                index=2,
                key="streaming_strength"
            )
        with col4:
            model = st.selectbox(
                "🤖 AI Model",
                ["v11", "v2"],
                index=0,
                key="streaming_model"
            )
    
    # Text input
    text = st.text_area(
        "📝 Enter your text",
        height=250,
        max_chars=10000,
        placeholder="Paste or type the AI-generated text you want to humanize with streaming...",
        help="Minimum 50 characters, maximum 10,000 characters",
        key="streaming_text_input"
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
    
    # Streaming output area
    streaming_placeholder = st.empty()
    
    # Process buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚡ Start Streaming", type="primary", use_container_width=True, disabled=st.session_state.streaming_active):
            if len(text) < 50:
                st.error("❌ Text too short! Minimum 50 characters required.")
            elif len(text) > 10000:
                st.error("❌ Text too long! Maximum 10,000 characters allowed.")
            else:
                st.session_state.streaming_active = True
                st.session_state.streaming_text = ""
                
                # Callback functions for streaming
                def on_chunk(chunk, data):
                    st.session_state.streaming_text += chunk
                    with streaming_placeholder.container():
                        st.markdown('<div class="streaming-box">', unsafe_allow_html=True)
                        st.write("**Streaming Output:**")
                        st.write(st.session_state.streaming_text)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                def on_complete(complete_text):
                    st.session_state.streaming_active = False
                    st.success("✅ Streaming humanization completed!")
                
                def on_error(error_msg):
                    st.session_state.streaming_active = False
                    st.error(f"❌ Streaming error: {error_msg}")
                
                # Start streaming
                with st.spinner("⚡ Starting streaming humanization..."):
                    try:
                        result = streaming_humanizer.humanize_text_streaming(
                            text=text,
                            readability=readability,
                            purpose=purpose,
                            strength=strength,
                            model=model,
                            on_chunk=on_chunk,
                            on_complete=on_complete,
                            on_error=on_error
                        )
                        
                        if result:
                            # Download button for streaming result
                            if st.download_button(
                                label="💾 Download Streaming Result",
                                data=result["output"],
                                file_name=f"streaming_humanized_{readability.lower().replace(' ', '_')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            ):
                                st.success("📥 File downloaded successfully!")
                        else:
                            st.error("❌ Streaming humanization failed.")
                            
                    except Exception as e:
                        st.error(f"❌ Error during streaming: {str(e)}")
                        st.session_state.streaming_active = False
    
    with col2:
        if st.button("⏹️ Stop Streaming", type="secondary", use_container_width=True, disabled=not st.session_state.streaming_active):
            streaming_humanizer.cancel_processing()
            st.session_state.streaming_active = False
            st.success("⏹️ Streaming stopped")

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

elif tab == "Documents":
    st.header("📄 Documents")
    st.markdown("Manage your humanization documents and rehumanize existing content.")
    
    # Instructions
    st.info("""
    **📋 How to use Documents:**
    1. **Refresh Documents**: Click the button below to load your documents
    2. **View Documents**: Expand each document to see input/output text
    3. **Rehumanize**: Use new settings to rehumanize existing documents
    4. **Settings**: Choose different readability, purpose, strength, and model for rehumanization
    """)
    
    # Rehumanization settings
    with st.expander("⚙️ Rehumanization Settings", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            rehumanize_readability = st.selectbox(
                "📚 Readability Level",
                ["High School", "University", "Doctorate", "Journalist", "Marketing"],
                index=1,
                key="rehumanize_readability"
            )
        with col2:
            rehumanize_purpose = st.selectbox(
                "🎯 Purpose",
                [
                    "General Writing", "Essay", "Article", "Marketing Material", "Story",
                    "Cover Letter", "Report", "Business Material", "Legal Material"
                ],
                index=0,
                key="rehumanize_purpose"
            )
        with col3:
            rehumanize_strength = st.selectbox(
                "💪 Humanization Strength",
                ["Quality", "Balanced", "More Human"],
                index=2,
                key="rehumanize_strength"
            )
        with col4:
            rehumanize_model = st.selectbox(
                "🤖 AI Model",
                ["v11", "v2"],
                index=0,
                key="rehumanize_model"
            )
    
    # Document listing with improved UX
    with st.expander("📋 Your Documents", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🔄 Refresh Documents", type="secondary", use_container_width=True):
                with st.spinner("📋 Loading your documents..."):
                    try:
                        documents = humanizer.list_documents()
                        
                        if documents and documents.get("documents") and len(documents["documents"]) > 0:
                            st.session_state.documents = documents["documents"]
                            st.success(f"📊 Found {len(st.session_state.documents)} documents")
                        else:
                            st.session_state.documents = []
                            st.info("📝 No documents found. Start humanizing some text to see your documents here!")
                            
                    except Exception as e:
                        st.error(f"❌ Error loading documents: {str(e)}")
        
        with col2:
            if st.button("🗑️ Clear Cache", type="secondary", use_container_width=True):
                st.session_state.documents = []
                st.session_state.rehumanize_results = {}
                st.session_state.processing_document = None
                st.success("🗑️ Cache cleared!")
                st.rerun()
        
        # Display documents
        if st.session_state.documents:
            st.markdown("### 📄 Document List")
            
            for i, doc in enumerate(st.session_state.documents):
                doc_id = doc.get('id', 'N/A')
                doc_key = f"doc_{i}_{doc_id[:8]}"
                
                with st.container():
                    st.markdown(f"""
                    <div class="document-card">
                        <h4>📄 Document {i+1}: {doc_id[:8]}...</h4>
                        <p><strong>📚 Readability:</strong> {doc.get('readability', 'N/A')} | 
                        <strong>🎯 Purpose:</strong> {doc.get('purpose', 'N/A')} | 
                        <strong>📅 Created:</strong> {doc.get('createdDate', 'N/A')[:10]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Document content
                    with st.expander(f"📄 View Document {i+1} Content", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**📥 Input Text:**")
                            st.text_area(
                                "Input",
                                value=doc.get('input', ''),
                                height=150,
                                disabled=True,
                                key=f"input_{doc_key}"
                            )
                        with col2:
                            st.markdown("**📤 Output Text:**")
                            st.text_area(
                                "Output", 
                                value=doc.get('output', ''),
                                height=150,
                                disabled=True,
                                key=f"output_{doc_key}"
                            )
                        
                        # Rehumanize button with proper state management
                        if st.button(f"🔄 Rehumanize Document {i+1}", key=f"rehumanize_btn_{doc_key}", type="primary"):
                            st.session_state.processing_document = doc_id
                            st.rerun()
                        
                        # Show rehumanization result if available
                        if doc_id in st.session_state.rehumanize_results:
                            result = st.session_state.rehumanize_results[doc_id]
                            st.markdown('<div class="rehumanize-result">', unsafe_allow_html=True)
                            st.markdown("**🔄 Rehumanized Result:**")
                            st.text_area(
                                "Rehumanized Output",
                                value=result.get("output", ""),
                                height=200,
                                disabled=True,
                                key=f"rehumanized_{doc_key}"
                            )
                            
                            # Settings comparison
                            col1, col2 = st.columns(2)
                            with col1:
                                st.info(f"**Original Settings:** {doc.get('readability', 'N/A')} | {doc.get('purpose', 'N/A')} | {doc.get('strength', 'N/A')} | {doc.get('model', 'N/A')}")
                            with col2:
                                st.info(f"**New Settings:** {rehumanize_readability} | {rehumanize_purpose} | {rehumanize_strength} | {rehumanize_model}")
                            
                            # Download button
                            if st.download_button(
                                label="💾 Download Rehumanized Text",
                                data=result.get("output", ""),
                                file_name=f"rehumanized_{doc_id[:8]}.txt",
                                mime="text/plain",
                                use_container_width=True,
                                key=f"download_{doc_key}"
                            ):
                                st.success("📥 File downloaded successfully!")
                            st.markdown('</div>', unsafe_allow_html=True)
        
        # Process rehumanization if requested
        if st.session_state.processing_document:
            doc_id = st.session_state.processing_document
            
            # Find the document
            doc = None
            for d in st.session_state.documents:
                if d.get('id') == doc_id:
                    doc = d
                    break
            
            if doc:
                st.markdown('<div class="processing-indicator">', unsafe_allow_html=True)
                st.markdown("🔄 **Processing rehumanization...**")
                st.markdown('</div>', unsafe_allow_html=True)
                
                with st.spinner("🔄 Rehumanizing document..."):
                    try:
                        result = humanizer.rehumanize_document(
                            document_id=doc_id,
                            readability=rehumanize_readability,
                            purpose=rehumanize_purpose,
                            strength=rehumanize_strength,
                            model=rehumanize_model
                        )
                        
                        if result and result.get("output"):
                            st.session_state.rehumanize_results[doc_id] = result
                            st.session_state.processing_document = None
                            st.success("✅ Document rehumanized successfully!")
                            st.rerun()
                        else:
                            st.session_state.processing_document = None
                            st.error("❌ Rehumanization failed.")
                            st.rerun()
                            
                    except Exception as e:
                        st.session_state.processing_document = None
                        st.error(f"❌ Error during rehumanization: {str(e)}")
                        st.rerun()
        else:
            if not st.session_state.documents:
                st.info("📝 No documents loaded. Click 'Refresh Documents' to load your documents.")

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
                        
                        st.caption(f"📚 Readability: {entry.get('readability', 'N/A')} | 🎯 Purpose: {entry.get('purpose', 'N/A')} | 💪 Strength: {entry.get('strength', 'N/A')} | 🤖 Model: {entry.get('model', 'N/A')}")
                        
        except Exception as e:
            st.error(f"❌ Error reading history: {str(e)}")

elif tab == "Credits":
    st.header("💳 Credits & Account")
    st.markdown("Manage your Undetectable.AI account and check credit balance.")
    
    # Check credits
    if st.button("💰 Check Credit Balance", type="primary", use_container_width=True):
        with st.spinner("💰 Checking your credit balance..."):
            try:
                credits = humanizer.check_credits()
                
                if credits:
                    st.success("✅ Credit information retrieved!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Base Credits", credits.get("baseCredits", 0))
                    with col2:
                        st.metric("Boost Credits", credits.get("boostCredits", 0))
                    with col3:
                        st.metric("Total Credits", credits.get("credits", 0))
                    
                    # Credit status
                    total_credits = credits.get("credits", 0)
                    if total_credits > 1000:
                        st.success("🟢 Good credit balance")
                    elif total_credits > 100:
                        st.warning("🟡 Moderate credit balance")
                    else:
                        st.error("🔴 Low credit balance")
                        
                else:
                    st.error("❌ Failed to retrieve credit information.")
                    
            except Exception as e:
                st.error(f"❌ Error checking credits: {str(e)}")
    
    st.divider()
    
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
        st.markdown("- **Streaming Humanization**: Real-time text processing")
        st.markdown("- **AI Detection**: Advanced pattern recognition")
        st.markdown("- **Document Management**: List and rehumanize documents")
        st.markdown("- **Credit Management**: Check and monitor credits")
        st.markdown("- **Multiple Settings**: Customizable readability and purpose")
        st.markdown("- **History Tracking**: View your past activities")
        st.markdown("- **File Export**: Download results easily")
    
    with col2:
        st.markdown("### 🛠️ Technology")
        st.markdown("- **Backend**: Python with modular architecture")
        st.markdown("- **UI**: Streamlit for web interface")
        st.markdown("- **API**: Undetectable.AI integration")
        st.markdown("- **WebSocket**: Real-time streaming support")
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