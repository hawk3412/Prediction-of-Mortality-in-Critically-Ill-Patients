# 🏥 Mortality Prediction App

Clinical decision support system for predicting mortality risk in critically ill patients using XGBoost machine learning.

## 📋 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

Visit `http://localhost:8501`

### Deploy to Streamlit Cloud

1. **Create GitHub Repository**
   - Go to https://github.com/new
   - Name: `mortality-prediction`
   - Set to Public

2. **Upload Files**
   - `app.py`
   - `final_model_XGB.pkl`
   - `requirements.txt`
   - `README.md`

3. **Deploy on Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Click "Deploy"

## 📊 Input Parameters (8 Clinical Indicators)

| Parameter | Range | Unit | Description |
|-----------|-------|------|-------------|
| Group | 1-5 | - | Patient risk stratification |
| DDPLUS | 0-100 | Score | Acute physiology score |
| Age | 0-120 | Years | Patient age |
| PDW | 0-50 | % | Platelet distribution width |
| BUN | 0-200 | mg/dL | Blood urea nitrogen |
| LDH | 0-2000 | U/L | Lactate dehydrogenase |
| ALT | 0-1000 | U/L | Alanine aminotransferase |
| PT | 0-100 | Seconds | Prothrombin time |

## 🎯 Risk Classification

- **🟢 Low Risk** (< 35%) - Standard care protocols
- **🟡 Moderate Risk** (35-65%) - Enhanced monitoring
- **🔴 High Risk** (> 65%) - Intensive intervention required

## 🔧 Requirements

- Python 3.8+
- See `requirements.txt` for package versions

## ⚠️ Disclaimer

This application is for clinical decision support only. Results must be validated by qualified medical professionals and should not be used as the sole basis for patient management decisions.

## 📄 License

MIT License

## 🤝 Support

For issues or questions, refer to:
- Streamlit Documentation: https://docs.streamlit.io
- XGBoost Documentation: https://xgboost.readthedocs.io
