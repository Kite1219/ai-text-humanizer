# 🚀 Deployment Guide

This guide will help you deploy your AI Text Humanizer to GitHub and Streamlit Cloud.

## 📋 Prerequisites

- GitHub account
- Undetectable.AI API key
- Git installed on your computer

## 🔧 Step 1: Prepare Your Repository

### 1.1 Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: AI Text Humanizer"
```

### 1.2 Create GitHub Repository

1. Go to [GitHub](https://github.com/YOUR_USERNAME/ai-text-humanizer) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name it `ai-text-humanizer`
5. Make it **Public** (required for free Streamlit Cloud)
6. Don't initialize with README (we already have one)
7. Click "Create repository"

### 1.3 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-text-humanizer.git
git branch -M main
git push -u origin main
```

## 🌐 Step 2: Deploy to Streamlit Cloud

### 2.1 Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/ai-text-humanizer`
5. Set the main file path to: `app.py`
6. Click "Deploy"

### 2.2 Configure Secrets

1. In your Streamlit Cloud app, go to **Settings** → **Secrets**
2. Add your API key in this format:

```toml
UNDETECTABLE_API_KEY = "your_actual_api_key_here"
```

3. Click "Save"
4. Your app will automatically redeploy

## 🔒 Step 3: Security Best Practices

### 3.1 Never Commit API Keys

✅ **Good**: Using `.env` file (already in `.gitignore`)
✅ **Good**: Using Streamlit Secrets
❌ **Bad**: Hardcoding API keys in source code

### 3.2 Environment Variables

Your `.env` file should look like this:
```env
UNDETECTABLE_API_KEY=your_api_key_here
```

### 3.3 GitHub Secrets (Alternative)

If you want to use GitHub Actions or other deployment methods:

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `UNDETECTABLE_API_KEY`
5. Value: Your API key
6. Click **Add secret**

## 🎯 Step 4: Customize Your App

### 4.1 Update README.md

Replace `yourusername` with your actual GitHub username in:
- Repository URLs
- Demo links
- Support links

### 4.2 Update App Title

In `app.py`, you can customize:
```python
st.set_page_config(
    page_title="Your Custom Title",
    page_icon="🤖",
    layout="wide"
)
```

### 4.3 Add Custom Branding

You can add your logo or custom styling in the CSS section of `app.py`.

## 🔄 Step 5: Continuous Deployment

### 5.1 Automatic Updates

Once deployed, any changes you push to the `main` branch will automatically update your Streamlit app.

### 5.2 Testing Changes

1. Make your changes locally
2. Test with: `streamlit run app.py`
3. Commit and push:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

## 📊 Step 6: Monitor Your App

### 6.1 Streamlit Cloud Dashboard

- View app statistics
- Monitor usage
- Check logs for errors

### 6.2 Usage Analytics

Streamlit Cloud provides:
- Page views
- User sessions
- Error rates
- Performance metrics

## 🛠️ Step 7: Advanced Configuration

### 7.1 Custom Domain (Optional)

If you have a custom domain:
1. Go to Streamlit Cloud settings
2. Add your custom domain
3. Configure DNS records

### 7.2 Environment Variables

You can add more environment variables in Streamlit Secrets:
```toml
UNDETECTABLE_API_KEY = "your_api_key"
DEBUG_MODE = "false"
MAX_TEXT_LENGTH = "10000"
```

## 🚨 Troubleshooting

### Common Issues

1. **App not loading**: Check if `app.py` is the correct main file
2. **API key errors**: Verify secrets are configured correctly
3. **Import errors**: Ensure all dependencies are in `requirements.txt`
4. **Permission errors**: Check file permissions and `.gitignore`

### Debug Mode

Add this to your `app.py` for debugging:
```python
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
```

## 📞 Support

If you encounter issues:

1. **Check Streamlit Cloud logs** in your app dashboard
2. **Verify your API key** is working locally
3. **Review the README** for setup instructions
4. **Open a GitHub issue** for bugs

## 🎉 Success!

Your AI Text Humanizer is now live at:
`https://YOUR_USERNAME-ai-text-humanizer-app-XXXXX.streamlit.app`

Share this link with others to let them use your app!

---

**Remember**: Never share your API key publicly. Always use environment variables or secrets management. 