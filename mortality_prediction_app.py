import streamlit as st
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="ICU Mortality Risk Assessment",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a clinical, professional look
st.markdown("""
    <style>
    :root {
        --primary: #1e3a8a;
        --secondary: #0369a1;
        --success: #059669;
        --danger: #dc2626;
        --warning: #f59e0b;
        --light-bg: #f8fafc;
        --border: #e2e8f0;
    }
    
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background-color: var(--light-bg);
    }
    
    .header-section {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header-section h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .header-section p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .section-title {
        color: var(--primary);
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid var(--secondary);
        padding-bottom: 0.5rem;
    }
    
    .prediction-result {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid var(--secondary);
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .risk-high {
        border-left-color: var(--danger) !important;
        background: linear-gradient(to right, rgba(220, 38, 38, 0.05), white);
    }
    
    .risk-moderate {
        border-left-color: var(--warning) !important;
        background: linear-gradient(to right, rgba(245, 158, 11, 0.05), white);
    }
    
    .risk-low {
        border-left-color: var(--success) !important;
        background: linear-gradient(to right, rgba(5, 150, 105, 0.05), white);
    }
    
    .risk-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .risk-high .risk-value {
        color: var(--danger);
    }
    
    .risk-moderate .risk-value {
        color: var(--warning);
    }
    
    .risk-low .risk-value {
        color: var(--success);
    }
    
    .risk-label {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .risk-high .risk-label {
        color: var(--danger);
    }
    
    .risk-moderate .risk-label {
        color: var(--warning);
    }
    
    .risk-low .risk-label {
        color: var(--success);
    }
    
    .input-group {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.05) 0%, rgba(3, 105, 161, 0.05) 100%);
        border-left: 4px solid var(--secondary);
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    
    .info-box h3 {
        color: var(--primary);
        margin-top: 0;
        font-size: 1rem;
    }
    
    .info-box p {
        margin: 0.5rem 0 0 0;
        color: #475569;
        font-size: 0.95rem;
    }
    
    .button-container {
        display: flex;
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .stButton > button {
        width: 100%;
        height: 45px;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid var(--border);
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    with open('/mnt/user-data/uploads/final_model_XGB.pkl', 'rb') as f:
        return pickle.load(f)

model_dict = load_model()
xgb_model = model_dict['model']
optimal_threshold = model_dict['optimal_threshold']

# Header
st.markdown("""
    <div class="header-section">
        <h1>🏥 ICU Mortality Risk Assessment</h1>
        <p>Prediction of Mortality in Critically Ill Patients using Advanced Machine Learning</p>
    </div>
""", unsafe_allow_html=True)

# Information box
st.markdown("""
    <div class="info-box">
        <h3>ℹ️ About This Tool</h3>
        <p>This clinical decision support system uses XGBoost machine learning to assess mortality risk in critically ill patients based on key clinical parameters. Results should be interpreted by medical professionals in conjunction with comprehensive clinical assessment.</p>
    </div>
""", unsafe_allow_html=True)

# Main input section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<p class="section-title">📋 Patient Clinical Parameters</p>', unsafe_allow_html=True)

# Create columns for input
col1, col2, col3, col4 = st.columns(4)

with col1:
    group = st.selectbox(
        "Patient Group",
        options=[1, 2, 3, 4, 5],
        help="Patient risk stratification group (1-5)"
    )

with col2:
    ddplus = st.number_input(
        "DDPLUS Score",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0,
        help="Acute physiology score"
    )

with col3:
    age = st.number_input(
        "Age (years)",
        min_value=0,
        max_value=120,
        value=65,
        step=1,
        help="Patient age in years"
    )

with col4:
    pdw = st.number_input(
        "PDW (%)",
        min_value=0.0,
        max_value=50.0,
        value=15.0,
        step=0.1,
        help="Platelet Distribution Width"
    )

col5, col6, col7, col8 = st.columns(4)

with col5:
    bun = st.number_input(
        "BUN (mg/dL)",
        min_value=0.0,
        max_value=200.0,
        value=20.0,
        step=0.1,
        help="Blood Urea Nitrogen"
    )

with col6:
    ldh = st.number_input(
        "LDH (U/L)",
        min_value=0.0,
        max_value=2000.0,
        value=250.0,
        step=1.0,
        help="Lactate Dehydrogenase"
    )

with col7:
    alt = st.number_input(
        "ALT (U/L)",
        min_value=0.0,
        max_value=1000.0,
        value=30.0,
        step=0.1,
        help="Alanine Aminotransferase"
    )

with col8:
    pt = st.number_input(
        "PT (seconds)",
        min_value=0.0,
        max_value=100.0,
        value=12.0,
        step=0.1,
        help="Prothrombin Time"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Prediction button
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])

with col_btn2:
    predict_button = st.button(
        "🔮 Predict Risk",
        use_container_width=True,
        type="primary"
    )

# Make prediction
if predict_button:
    try:
        # Prepare input data
        input_data = np.array([[group, ddplus, age, pdw, bun, ldh, alt, pt]])
        
        # Get prediction probability
        prediction_proba = xgb_model.predict_proba(input_data)[0]
        mortality_risk = prediction_proba[1]  # Probability of mortality (class 1)
        
        # Determine risk category
        if mortality_risk >= 0.65:
            risk_category = "HIGH"
            risk_class = "risk-high"
            icon = "⚠️"
        elif mortality_risk >= 0.35:
            risk_category = "MODERATE"
            risk_class = "risk-moderate"
            icon = "⚡"
        else:
            risk_category = "LOW"
            risk_class = "risk-low"
            icon = "✅"
        
        # Display results
        st.markdown(f"""
            <div class="prediction-result {risk_class}">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <p style="margin: 0; color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">Mortality Risk</p>
                        <div class="risk-value">{mortality_risk*100:.1f}%</div>
                        <div class="risk-label">{icon} {risk_category} RISK</div>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; color: #64748b; font-size: 0.85rem;">Classification Threshold</p>
                        <p style="margin: 0.5rem 0; font-size: 1.2rem; font-weight: 600; color: var(--secondary);">{optimal_threshold:.2%}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Additional metrics
        st.markdown('<p class="section-title">📊 Detailed Analysis</p>', unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Survival Probability</div>
                    <div class="metric-value" style="color: var(--success);">{prediction_proba[0]*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Mortality Probability</div>
                    <div class="metric-value" style="color: var(--danger);">{mortality_risk*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Risk Category</div>
                    <div class="metric-value" style="font-size: 1.5rem;">{icon}</div>
                    <div style="color: #64748b; font-size: 0.9rem;">{risk_category}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            risk_ratio = mortality_risk / (1 - mortality_risk) if mortality_risk < 1 else float('inf')
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Odds Ratio</div>
                    <div class="metric-value">{risk_ratio:.2f}</div>
                    <div style="color: #64748b; font-size: 0.9rem;">Mortality:Survival</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Visualization
        st.markdown('<p class="section-title">📈 Risk Distribution</p>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[
            go.Bar(
                y=['Survival', 'Mortality'],
                x=[prediction_proba[0]*100, mortality_risk*100],
                orientation='h',
                marker=dict(
                    color=['#059669', '#dc2626'],
                    line=dict(color='white', width=2)
                ),
                text=[f'{prediction_proba[0]*100:.1f}%', f'{mortality_risk*100:.1f}%'],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Probability: %{x:.2f}%<extra></extra>'
            )
        ])
        
        fig.update_layout(
            xaxis_title='Probability (%)',
            showlegend=False,
            height=300,
            margin=dict(l=100, r=100, t=50, b=50),
            template='plotly_white',
            xaxis=dict(range=[0, 100]),
            hovermode='y unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Clinical interpretation
        st.markdown('<p class="section-title">💊 Clinical Interpretation</p>', unsafe_allow_html=True)
        
        if risk_category == "HIGH":
            st.warning("""
            **High Mortality Risk Detected**
            
            - Close monitoring and aggressive intervention recommended
            - Consider ICU-level care if not already implemented
            - Regular reassessment of patient status recommended
            - Consult with attending physician for treatment optimization
            """)
        elif risk_category == "MODERATE":
            st.info("""
            **Moderate Mortality Risk**
            
            - Standard ICU protocols should be followed
            - Continuous monitoring is advisable
            - Regular reassessment to detect changes in patient status
            - Consider targeted interventions based on clinical judgment
            """)
        else:
            st.success("""
            **Low Mortality Risk**
            
            - Standard care protocols apply
            - Regular monitoring sufficient
            - Positive prognosis based on current parameters
            - Maintain standard ICU surveillance
            """)
        
        # Timestamp
        st.markdown(f"""
            <p style="text-align: right; color: #94a3b8; font-size: 0.85rem; margin-top: 2rem;">
            Assessment generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Prediction Error: {str(e)}")

# Footer
st.markdown("""
    <hr style="margin-top: 3rem; border: none; border-top: 1px solid var(--border);">
    <p style="text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 1.5rem;">
    <strong>Disclaimer:</strong> This tool is for clinical decision support only. All results must be validated by qualified medical professionals. 
    Do not rely solely on this prediction for patient management decisions.
    </p>
""", unsafe_allow_html=True)
