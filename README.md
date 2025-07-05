# 🤖 AI Text Humanizer

A powerful web application for humanizing AI-generated text and detecting AI content patterns. Built with Python, Streamlit, and the Undetectable.AI API.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **📝 Text Humanization**: Convert AI-generated text into natural, human-like content
- **⚡ Streaming Humanization**: Real-time text processing with WebSocket streaming
- **🤖 AI Detection**: Advanced pattern recognition to detect AI-written text
- **📄 Document Management**: List, view, and rehumanize existing documents
- **💰 Credit Management**: Check and monitor your API credit balance
- **🤖 Model Selection**: Choose between v2 and v11 AI models
- **⚙️ Customizable Settings**: Multiple readability levels and purposes
- **📚 History Tracking**: View and manage your humanization history
- **💾 File Export**: Download results as text files
- **🎨 Modern UI**: Beautiful Streamlit interface with responsive design
- **🔒 Secure**: API key management with environment variables

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## 📋 Prerequisites

- Python 3.8 or higher
- Undetectable.AI API key
- Git

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-text-humanizer.git
cd ai-text-humanizer
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Copy the example environment file
cp default.env .env
```

Edit `.env` and add your Undetectable.AI API key:

```env
UNDETECTABLE_API_KEY=your_api_key_here
```

### 5. Run the Application

#### Streamlit Web Interface
```bash
streamlit run app.py
```

#### Command Line Interface
```bash
python run.py
```

## 🎯 Usage

### Web Interface (Recommended)

1. **Start the app**: `streamlit run app.py`
2. **Open your browser**: Navigate to `http://localhost:8501`
3. **Choose a feature**:
   - **📝 Humanize Text**: Transform AI text into human-like content
   - **⚡ Streaming Humanize**: Real-time text processing with live updates
   - **🤖 AI Detector**: Analyze text for AI patterns
   - **📄 Documents**: Manage and rehumanize existing documents
   - **📚 History**: View your past activities
   - **💳 Credits**: Check your account balance and manage credits
   - **ℹ️ About**: Learn about the application

### Command Line Interface

```bash
python run.py
```

Follow the interactive menu to:
- Humanize text with custom settings
- Detect AI patterns in text
- Check your credit balance
- View history

## 🔧 Configuration

### Humanization Settings

- **Readability Levels**: High School, University, Doctorate, Journalist, Marketing
- **Purposes**: General Writing, Essay, Article, Marketing Material, Story, Cover Letter, Report, Business Material, Legal Material
- **Strength**: Quality, Balanced, More Human
- **AI Models**: v2 (legacy), v11 (latest)

### Streaming Humanization

- **Real-time Processing**: See results as they're generated
- **WebSocket Connection**: Stable, low-latency streaming
- **Progress Tracking**: Monitor processing status
- **Cancellation Support**: Stop processing at any time

### Document Management

- **Document Listing**: View all your humanized documents
- **Rehumanization**: Re-process existing documents with new settings
- **Document History**: Track changes and improvements
- **Bulk Operations**: Manage multiple documents efficiently

### AI Detection Algorithm

The AI detector analyzes multiple patterns:
- Repetitive word patterns
- Formal language usage
- Sentence structure consistency
- Contraction usage
- Vocabulary complexity
- Personal pronoun frequency

## 📊 Scoring System

- **🟢 Human-Written**: < 30% AI probability
- **�� Uncertain**: 30-70% AI probability  
- **🔴 AI-Generated**: > 70% AI probability

## 🔒 Security

- API keys are stored in environment variables
- Never commit `.env` files to version control
- Use GitHub Secrets for deployment

## 🚀 Deployment

### Streamlit Cloud

1. **Fork this repository**
2. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
   - Set the main file path to `app.py`

3. **Configure Secrets**:
   - In Streamlit Cloud, go to Settings → Secrets
   - Add your API key:
   ```toml
   UNDETECTABLE_API_KEY = "your_api_key_here"
   ```

4. **Deploy**: Click "Deploy" and your app will be live!

### Heroku

1. **Create Heroku app**
2. **Set environment variables**:
   ```bash
   heroku config:set UNDETECTABLE_API_KEY=your_api_key_here
   ```
3. **Deploy**:
   ```bash
   git push heroku main
   ```

### Local Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export UNDETECTABLE_API_KEY=your_api_key_here

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
ai-text-humanizer/
├── app.py                 # Streamlit web application
├── run.py                 # Command line interface
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── default.env           # Environment template
├── .env                  # Environment variables (create this)
├── test_new_features.py  # Test script for new features
├── src/
│   ├── config/
│   │   └── settings.py   # Configuration management
│   ├── services/
│   │   ├── text_humanizer.py      # Text humanization service
│   │   ├── streaming_humanizer.py # Streaming humanization service
│   │   └── ai_detector.py         # AI detection service
│   ├── ui/
│   │   └── menus.py      # CLI menu system
│   └── utils/
│       ├── error_handler.py  # API error handling
│       ├── file_manager.py   # File operations
│       └── utils.py          # Utility functions
```

## 🧪 Testing

Run the test script to verify all new features:

```bash
python test_new_features.py
```

This will test:
- Credit checking functionality
- Document listing
- Model selection (v2 vs v11)
- API connectivity

## 📖 Detailed Instructions

For detailed instructions on using the new features, see:
- [INSTRUCTIONS.md](INSTRUCTIONS.md) - Complete guide for Streaming Humanize and Rehumanize features

## 📈 New Features (v2.0)

### ⚡ Streaming Humanization
- Real-time text processing with WebSocket streaming
- Live progress updates as text is humanized
- Ability to cancel processing mid-stream
- Enhanced user experience with immediate feedback

### 📄 Document Management
- List all your humanized documents
- View document details and settings used
- Rehumanize existing documents with new parameters
- Track document history and improvements

### 💰 Credit Management
- Check your current credit balance
- Monitor base credits vs boost credits
- Credit status indicators (Good/Moderate/Low)
- Direct links to purchase more credits

### 🤖 Model Selection
- Choose between v2 (legacy) and v11 (latest) models
- Model-specific optimization for different use cases
- Backward compatibility with existing workflows

### 🔧 Enhanced Error Handling
- Comprehensive API error code handling
- User-friendly error messages
- Graceful degradation for network issues
- Detailed logging for debugging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Undetectable.AI](https://undetectable.ai/) for providing the API
- [Streamlit](https://streamlit.io/) for the web framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output

## 📞 Support

- **Documentation**: [Undetectable.AI API Docs](https://help.undetectable.ai/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-text-humanizer/issues)
- **Email**: your-email@example.com

---

Made with ❤️ by [Your Name] 