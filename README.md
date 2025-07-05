# 🤖 AI Text Humanizer

A powerful web application for humanizing AI-generated text and detecting AI content patterns. Built with Python, Streamlit, and the Undetectable.AI API.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **📝 Text Humanization**: Convert AI-generated text into natural, human-like content
- **🤖 AI Detection**: Advanced pattern recognition to detect AI-written text
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
   - **Humanize Text**: Transform AI text into human-like content
   - **AI Detector**: Analyze text for AI patterns
   - **History**: View your past activities
   - **Credits**: Manage your account

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
- **🟡 Uncertain**: 30-70% AI probability  
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
├── src/
│   ├── config/
│   │   └── settings.py   # Configuration management
│   ├── services/
│   │   ├── text_humanizer.py  # Text humanization service
│   │   └── ai_detector.py     # AI detection service
│   ├── ui/
│   │   └── menus.py      # CLI menu system
│   └── utils/
│       └── utils.py      # Utility functions
├── errors/
│   └── status_code_error.py  # Error handling
├── outputs/              # Generated files
└── history.json         # Humanization history
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Undetectable.AI](https://undetectable.ai/) for the text humanization API
- [Streamlit](https://streamlit.io/) for the web framework
- [Rich](https://rich.readthedocs.io/) for beautiful CLI output

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-text-humanizer/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/ai-text-humanizer/wiki)
- **Email**: your-email@example.com

## 🔄 Changelog

### v1.0.0 (2024-01-XX)
- Initial release
- Text humanization with Undetectable.AI API
- AI detection algorithm
- Streamlit web interface
- Command line interface
- History tracking
- File export functionality

---

**Made with ❤️ by [Your Name]** 