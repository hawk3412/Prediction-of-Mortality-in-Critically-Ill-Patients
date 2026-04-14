import streamlit as st
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Mortality Prediction",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    body { font-family: 'Segoe UI', sans-serif; }
    .metric-box { background: white; padding: 1.5rem; border-radius: 10px; 
                  border: 1px solid #e2e8f0; text-align: center; }
    .risk-high { border-left: 5px solid #dc2626; padding: 1.5rem; 
                 background: rgba(220, 38, 38, 0.05); border-radius: 10px; }
    .risk-moderate { border-left: 5px solid #f59e0b; padding: 1.5rem; 
                     background: rgba(245, 158, 11, 0.05); border-radius: 10px; }
    .risk-low { border-left: 5px solid #059669; padding: 1.5rem; 
                background: rgba(5, 150, 105, 0.05); border-radius: 10px; }
    .tooltip-text { color: #666; font-size: 0.9rem; margin-top: 0.3rem; }
    </style>
""", unsafe_allow_html=True)

# Load Model
@st.cache_resource
def load_model():
    with open('final_model_XGB.pkl', 'rb') as f:
        return pickle.load(f)

try:
    model_dict = load_model()
    xgb_model = model_dict['model']
    optimal_threshold = model_dict['optimal_threshold']
except Exception as e:
    st.error(f"❌ Error loading model: {str(e)}")
    st.stop()

# Header
st.title("🏥 ICU Mortality Risk Assessment")
st.subheader("Prediction of Mortality in Critically Ill Patients")
st.markdown("---")

# Input Section
st.markdown("### 📋 Patient Clinical Parameters")

col1, col2, col3, col4 = st.columns(4)
with col1:
    group = st.selectbox(
        "Patient Group",
        options=[1, 2, 3, 4, 5, 6],
        help="1=Cardiovascular | 2=Gastrointestinal | 3=Respiratory | 4=Infection | 5=Malignancy | 6=Trauma"
    )
with col2:
    ddplus = st.number_input("DDPLUS Score", min_value=0.0, max_value=100.0, value=50.0, step=1.0, help="Acute physiology score")
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=120, value=65, step=1, help="Patient age")
with col4:
    pdw = st.number_input("PDW (%)", min_value=0.0, max_value=50.0, value=15.0, step=0.1, help="Platelet distribution width")

col5, col6, col7, col8 = st.columns(4)
with col5:
    bun = st.number_input("BUN (mg/dL)", min_value=0.0, max_value=200.0, value=20.0, step=0.1, help="Blood urea nitrogen")
with col6:
    ldh = st.number_input("LDH (U/L)", min_value=0.0, max_value=2000.0, value=250.0, step=1.0, help="Lactate dehydrogenase")
with col7:
    alt = st.number_input("ALT (U/L)", min_value=0.0, max_value=1000.0, value=30.0, step=0.1, help="Alanine aminotransferase")
with col8:
    pt = st.number_input("PT (seconds)", min_value=0.0, max_value=100.0, value=12.0, step=0.1, help="Prothrombin time")

# Prediction Button
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
with col_btn2:
    predict_button = st.button("🔮 Predict Risk", use_container_width=True, type="primary")

# Make Prediction
if predict_button:
    try:
        # Prepare input data
        input_data = np.array([[group, ddplus, age, pdw, bun, ldh, alt, pt]])
        
        # Get prediction
        prediction_proba = xgb_model.predict_proba(input_data)[0]
        mortality_risk = prediction_proba[1]
        
        # Determine risk category
        if mortality_risk >= 0.65:
            risk_category = "HIGH"
            risk_class = "risk-high"
            icon = "⚠️"
            color = "#dc2626"
        elif mortality_risk >= 0.35:
            risk_category = "MODERATE"
            risk_class = "risk-moderate"
            icon = "⚡"
            color = "#f59e0b"
        else:
            risk_category = "LOW"
            risk_class = "risk-low"
            icon = "✅"
            color = "#059669"
        
        # Display Results
        st.markdown("### 📊 Prediction Results")
        
        result_col1, result_col2 = st.columns([2, 1])
        with result_col1:
            st.markdown(f"""
                <div class="{risk_class}">
                    <h3 style="margin: 0; color: {color};">{icon} {risk_category} RISK</h3>
                    <p style="margin: 0.5rem 0; color: #64748b;">Mortality Risk</p>
                    <h1 style="margin: 0; color: {color};">{mortality_risk*100:.1f}%</h1>
                </div>
            """, unsafe_allow_html=True)
        
        with result_col2:
            st.metric("Threshold", f"{optimal_threshold:.2%}")
            st.metric("Survival Prob.", f"{prediction_proba[0]*100:.1f}%")
        
        # Detailed Metrics
        st.markdown("### 📈 Detailed Analysis")
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.markdown(f"""
                <div class="metric-box">
                    <div style="font-size: 0.85rem; color: #64748b; text-transform: uppercase;">Survival</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #059669; margin: 0.5rem 0;">{prediction_proba[0]*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with metric_col2:
            st.markdown(f"""
                <div class="metric-box">
                    <div style="font-size: 0.85rem; color: #64748b; text-transform: uppercase;">Mortality</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #dc2626; margin: 0.5rem 0;">{mortality_risk*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with metric_col3:
            risk_ratio = mortality_risk / (1 - mortality_risk) if mortality_risk < 1 else float('inf')
            st.markdown(f"""
                <div class="metric-box">
                    <div style="font-size: 0.85rem; color: #64748b; text-transform: uppercase;">Odds Ratio</div>
                    <div style="font-size: 1.8rem; font-weight: 700; color: #1e3a8a; margin: 0.5rem 0;">{risk_ratio:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with metric_col4:
            st.markdown(f"""
                <div class="metric-box">
                    <div style="font-size: 0.85rem; color: #64748b; text-transform: uppercase;">Risk Level</div>
                    <div style="font-size: 2rem; margin: 0.5rem 0;">{icon}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Chart
        fig = go.Figure(data=[
            go.Bar(
                y=['Survival', 'Mortality'],
                x=[prediction_proba[0]*100, mortality_risk*100],
                orientation='h',
                marker=dict(color=['#059669', '#dc2626']),
                text=[f'{prediction_proba[0]*100:.1f}%', f'{mortality_risk*100:.1f}%'],
                textposition='outside'
            )
        ])
        fig.update_layout(height=300, template='plotly_white', xaxis_title='Probability (%)', 
                         showlegend=False, xaxis=dict(range=[0, 100]))
        st.plotly_chart(fig, use_container_width=True)
        
        # Clinical Recommendation
        st.markdown("### 💊 Clinical Interpretation")
        
        if risk_category == "HIGH":
            st.error("""
            **⚠️ HIGH RISK - Intensive intervention recommended**
            - Close monitoring required
            - Consider ICU-level care
            - Consult with attending physician for treatment optimization
            """)
        elif risk_category == "MODERATE":
            st.warning("""
            **⚡ MODERATE RISK - Enhanced monitoring advised**
            - Standard ICU protocols should be followed
            - Regular reassessment of patient status
            - Consider targeted interventions
            """)
        else:
            st.success("""
            **✅ LOW RISK - Standard care protocols apply**
            - Regular monitoring sufficient
            - Positive prognosis expected
            - Continue current care plan
            """)
        
        # Timestamp
        st.markdown(f"<p style='text-align: right; color: #94a3b8; font-size: 0.85rem;'>Assessment: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Prediction Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>
<strong>⚠️ Disclaimer:</strong> This tool is for clinical decision support only. 
Results must be validated by qualified medical professionals and should not be used as the sole basis for patient management decisions.
</p>
""", unsafe_allow_html=True)
