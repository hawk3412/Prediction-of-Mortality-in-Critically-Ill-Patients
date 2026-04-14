# 📦 Deployment Guide

## Step 1: GitHub Setup (5 minutes)

### Create Repository
1. Go to https://github.com/new
2. Repository name: `mortality-prediction`
3. Description: `ICU Mortality Risk Assessment`
4. Set to **Public** ⭐
5. Click "Create repository"

### Upload Files

**Method A: Web Upload (Easiest)**
1. Click "Add file" → "Upload files"
2. Drag and drop these 3 files:
   - `app.py`
   - `final_model_XGB.pkl` (222 KB)
   - `requirements.txt`
   - `README.md`
3. Click "Commit changes"

**Method B: Git Command**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/mortality-prediction.git
git branch -M main
git push -u origin main
```

## Step 2: Streamlit Cloud Deployment (5 minutes)

1. Visit https://streamlit.io/cloud
2. Click "Sign up" → Use GitHub to sign up
3. Authorize Streamlit to access your GitHub
4. Click "New app"
5. Fill in:
   - Repository: `YOUR_USERNAME/mortality-prediction`
   - Branch: `main`
   - Main file path: `app.py`
6. Click "Deploy!"

Wait 3-5 minutes for deployment to complete.

## Step 3: Access Your App

Once deployed, you'll get a URL like:
```
https://mortality-prediction.streamlit.app
```

Share this link with colleagues or access from anywhere!

## 🔧 Update Your App

After deployment, to update:

1. Modify files locally
2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```
3. Streamlit Cloud automatically redeploys (1-2 minutes)

## ⚠️ Common Issues

### Issue: "ModuleNotFoundError: No module named 'plotly'"
- **Fix:** Check `requirements.txt` is uploaded correctly
- Restart app in Streamlit Cloud

### Issue: "FileNotFoundError: final_model_XGB.pkl"
- **Fix:** Ensure model file is in GitHub repository
- File size should be 222 KB

### Issue: App is slow to load
- **Fix:** Wait 2-3 minutes (cold start)
- Subsequent loads will be faster

## ✅ Verify Deployment

Your app is working if you can:
1. ✅ See the app interface
2. ✅ Input patient parameters
3. ✅ Click "🔮 Predict Risk"
4. ✅ See prediction results
5. ✅ No error messages

## 🚀 Production Tips

1. **File Organization**
   ```
   mortality-prediction/
   ├── app.py
   ├── final_model_XGB.pkl
   ├── requirements.txt
   └── README.md
   ```

2. **Keep Files Updated**
   - Regularly pull latest changes
   - Test locally before pushing

3. **Monitor App Performance**
   - Check Streamlit Cloud logs
   - Monitor error messages
   - Track usage statistics

## 📞 Support

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Cloud: https://docs.streamlit.io/streamlit-cloud/get-started
- GitHub Help: https://docs.github.com
