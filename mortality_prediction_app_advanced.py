import streamlit as st
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import io

# Set page configuration
st.set_page_config(
    page_title="ICU Mortality Risk Assessment - Advanced",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced design
st.markdown("""
    <style>
    :root {
        --primary: #1e3a8a;
        --secondary: #0369a1;
        --success: #059669;
        --danger: #dc2626;
        --warning: #f59e0b;
        --info: #3b82f6;
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
    
    .info-box {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.05) 0%, rgba(3, 105, 161, 0.05) 100%);
        border-left: 4px solid var(--secondary);
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    
    .tab-content {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid var(--border);
    }
    </style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    with open('final_model_XGB.pkl', 'rb') as f:
        return pickle.load(f)

model_dict = load_model()
xgb_model = model_dict['model']
optimal_threshold = model_dict['optimal_threshold']

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

if 'batch_results' not in st.session_state:
    st.session_state.batch_results = None

# Header
st.markdown("""
    <div class="header-section">
        <h1>🏥 ICU Mortality Risk Assessment - Advanced Edition</h1>
        <p>Multi-functional Clinical Decision Support System with Batch Processing & Analytics</p>
    </div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔮 Single Prediction", "📊 Batch Analysis", "📈 Analytics", "💾 Patient History", "⚙️ Settings"])

# ==================== TAB 1: Single Prediction ====================
with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">📋 Patient Clinical Parameters</p>', unsafe_allow_html=True)
    
    # Input form
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        group = st.selectbox("Patient Group", options=[1, 2, 3, 4, 5], key="single_group")
    with col2:
        ddplus = st.number_input("DDPLUS Score", min_value=0.0, max_value=100.0, value=50.0, step=1.0, key="single_ddplus")
    with col3:
        age = st.number_input("Age (years)", min_value=0, max_value=120, value=65, step=1, key="single_age")
    with col4:
        pdw = st.number_input("PDW (%)", min_value=0.0, max_value=50.0, value=15.0, step=0.1, key="single_pdw")
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        bun = st.number_input("BUN (mg/dL)", min_value=0.0, max_value=200.0, value=20.0, step=0.1, key="single_bun")
    with col6:
        ldh = st.number_input("LDH (U/L)", min_value=0.0, max_value=2000.0, value=250.0, step=1.0, key="single_ldh")
    with col7:
        alt = st.number_input("ALT (U/L)", min_value=0.0, max_value=1000.0, value=30.0, step=0.1, key="single_alt")
    with col8:
        pt = st.number_input("PT (seconds)", min_value=0.0, max_value=100.0, value=12.0, step=0.1, key="single_pt")
    
    # Optional patient info
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        patient_id = st.text_input("Patient ID (optional)", placeholder="e.g., P001")
    with col_info2:
        patient_name = st.text_input("Patient Name (optional)", placeholder="e.g., John Doe")
    
    # Prediction button
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
    with col_btn2:
        predict_button = st.button("🔮 Predict Risk", use_container_width=True, type="primary")
    
    if predict_button:
        # Prepare input
        input_data = np.array([[group, ddplus, age, pdw, bun, ldh, alt, pt]])
        prediction_proba = xgb_model.predict_proba(input_data)[0]
        mortality_risk = prediction_proba[1]
        
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
        
        # Store in history
        prediction_record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'patient_id': patient_id or 'N/A',
            'patient_name': patient_name or 'N/A',
            'group': group,
            'ddplus': ddplus,
            'age': age,
            'pdw': pdw,
            'bun': bun,
            'ldh': ldh,
            'alt': alt,
            'pt': pt,
            'mortality_risk': mortality_risk,
            'survival_prob': prediction_proba[0],
            'risk_category': risk_category
        }
        st.session_state.history.append(prediction_record)
        
        # Display result
        st.markdown(f"""
            <div class="prediction-result {risk_class}">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <p style="margin: 0; color: #64748b; font-size: 0.9rem;">Mortality Risk</p>
                        <div class="risk-value">{mortality_risk*100:.1f}%</div>
                        <div style="color: var(--primary); font-weight: 600;">{icon} {risk_category} RISK</div>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; color: #64748b; font-size: 0.85rem;">Threshold: {optimal_threshold:.2%}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Survival</div>
                    <div class="metric-value" style="color: var(--success);">{prediction_proba[0]*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Mortality</div>
                    <div class="metric-value" style="color: var(--danger);">{mortality_risk*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m3:
            risk_ratio = mortality_risk / (1 - mortality_risk) if mortality_risk < 1 else float('inf')
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Odds Ratio</div>
                    <div class="metric-value">{risk_ratio:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Category</div>
                    <div class="metric-value" style="font-size: 1.5rem;">{icon}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Visualization
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
        fig.update_layout(height=300, template='plotly_white', xaxis_title='Probability (%)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Clinical recommendation
        st.markdown('<p class="section-title">💊 Clinical Recommendation</p>', unsafe_allow_html=True)
        if risk_category == "HIGH":
            st.error("⚠️ **HIGH RISK** - Intensive monitoring and intervention recommended")
        elif risk_category == "MODERATE":
            st.warning("⚡ **MODERATE RISK** - Enhanced monitoring advised")
        else:
            st.success("✅ **LOW RISK** - Standard care protocols apply")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 2: Batch Analysis ====================
with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📊 Batch Prediction from CSV</p>', unsafe_allow_html=True)
    
    st.info("Upload a CSV file with columns: group, DDPLUS, age, PDW, BUN, LDH, ALT, PT (and optional: patient_id, patient_name)")
    
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df)} records")
            
            # Display preview
            st.markdown("**Data Preview:**")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Process batch
            if st.button("🚀 Process Batch", use_container_width=True, type="primary"):
                progress_bar = st.progress(0)
                results = []
                
                required_cols = ['group', 'DDPLUS', 'age', 'PDW', 'BUN', 'LDH', 'ALT', 'PT']
                
                for idx, row in df.iterrows():
                    try:
                        input_data = np.array([[
                            row['group'], row['DDPLUS'], row['age'], row['PDW'],
                            row['BUN'], row['LDH'], row['ALT'], row['PT']
                        ]])
                        
                        pred_proba = xgb_model.predict_proba(input_data)[0]
                        mortality = pred_proba[1]
                        
                        if mortality >= 0.65:
                            category = "HIGH"
                        elif mortality >= 0.35:
                            category = "MODERATE"
                        else:
                            category = "LOW"
                        
                        result = {
                            'patient_id': row.get('patient_id', f'P{idx+1}'),
                            'mortality_risk': mortality,
                            'survival_prob': pred_proba[0],
                            'risk_category': category
                        }
                        results.append(result)
                    except Exception as e:
                        st.error(f"Error processing row {idx+1}: {str(e)}")
                    
                    progress_bar.progress((idx + 1) / len(df))
                
                # Create results dataframe
                results_df = pd.DataFrame(results)
                st.session_state.batch_results = results_df
                
                st.success(f"✅ Processed {len(results)} patients")
                
                # Summary statistics
                col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                with col_s1:
                    high_risk = (results_df['risk_category'] == 'HIGH').sum()
                    st.metric("High Risk", high_risk, f"{high_risk/len(results_df)*100:.1f}%")
                with col_s2:
                    mod_risk = (results_df['risk_category'] == 'MODERATE').sum()
                    st.metric("Moderate Risk", mod_risk, f"{mod_risk/len(results_df)*100:.1f}%")
                with col_s3:
                    low_risk = (results_df['risk_category'] == 'LOW').sum()
                    st.metric("Low Risk", low_risk, f"{low_risk/len(results_df)*100:.1f}%")
                with col_s4:
                    avg_risk = results_df['mortality_risk'].mean()
                    st.metric("Avg Mortality", f"{avg_risk*100:.1f}%", "")
                
                # Results table
                st.markdown("**Detailed Results:**")
                results_display = results_df.copy()
                results_display['mortality_risk'] = results_display['mortality_risk'].apply(lambda x: f"{x*100:.1f}%")
                results_display['survival_prob'] = results_display['survival_prob'].apply(lambda x: f"{x*100:.1f}%")
                st.dataframe(results_display, use_container_width=True)
                
                # Risk distribution chart
                risk_counts = results_df['risk_category'].value_counts()
                fig = go.Figure(data=[
                    go.Pie(labels=risk_counts.index, values=risk_counts.values,
                            marker=dict(colors=['#dc2626', '#f59e0b', '#059669']))
                ])
                fig.update_layout(height=400, title="Risk Category Distribution")
                st.plotly_chart(fig, use_container_width=True)
                
                # Export results
                csv_results = results_display.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results (CSV)",
                    data=csv_results,
                    file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 3: Analytics ====================
with tab3:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">📈 Prediction Analytics</p>', unsafe_allow_html=True)
    
    if len(st.session_state.history) == 0:
        st.info("No predictions yet. Make some predictions in the 'Single Prediction' tab to see analytics.")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        
        # Summary statistics
        col_a1, col_a2, col_a3, col_a4 = st.columns(4)
        with col_a1:
            st.metric("Total Predictions", len(history_df))
        with col_a2:
            st.metric("Avg Mortality Risk", f"{history_df['mortality_risk'].mean()*100:.1f}%")
        with col_a3:
            st.metric("Max Mortality Risk", f"{history_df['mortality_risk'].max()*100:.1f}%")
        with col_a4:
            st.metric("Min Mortality Risk", f"{history_df['mortality_risk'].min()*100:.1f}%")
        
        # Risk distribution
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            fig1 = go.Figure(data=[
                go.Histogram(x=history_df['mortality_risk']*100, nbinsx=20,
                            marker=dict(color='#0369a1'))
            ])
            fig1.update_layout(title="Mortality Risk Distribution", xaxis_title="Risk (%)", 
                             yaxis_title="Frequency", height=400)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col_graph2:
            risk_counts = history_df['risk_category'].value_counts()
            fig2 = go.Figure(data=[
                go.Bar(x=risk_counts.index, y=risk_counts.values,
                      marker=dict(color=['#dc2626', '#f59e0b', '#059669']))
            ])
            fig2.update_layout(title="Risk Category Distribution", height=400, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Trend analysis
        history_df['index'] = range(len(history_df))
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=history_df['index'], y=history_df['mortality_risk']*100,
                                 mode='lines+markers', name='Mortality Risk'))
        fig3.update_layout(title="Mortality Risk Trend", xaxis_title="Prediction #",
                          yaxis_title="Risk (%)", height=400)
        st.plotly_chart(fig3, use_container_width=True)
        
        # Correlation analysis
        numeric_cols = ['group', 'ddplus', 'age', 'pdw', 'bun', 'ldh', 'alt', 'pt', 'mortality_risk']
        corr_matrix = history_df[numeric_cols].corr()
        
        fig4 = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu'
        ))
        fig4.update_layout(title="Parameter Correlation Matrix", height=500)
        st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 4: Patient History ====================
with tab4:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">💾 Prediction History</p>', unsafe_allow_html=True)
    
    if len(st.session_state.history) == 0:
        st.info("No predictions yet.")
    else:
        history_df = pd.DataFrame(st.session_state.history)
        
        # Filter options
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        with col_filter1:
            risk_filter = st.selectbox("Filter by Risk:", ["All", "HIGH", "MODERATE", "LOW"])
        with col_filter2:
            sort_by = st.selectbox("Sort by:", ["Latest First", "Oldest First", "Highest Risk", "Lowest Risk"])
        with col_filter3:
            rows_to_show = st.slider("Rows to show:", 5, 50, 20)
        
        # Apply filters
        filtered_df = history_df.copy()
        if risk_filter != "All":
            filtered_df = filtered_df[filtered_df['risk_category'] == risk_filter]
        
        if sort_by == "Latest First":
            filtered_df = filtered_df.iloc[::-1]
        elif sort_by == "Highest Risk":
            filtered_df = filtered_df.sort_values('mortality_risk', ascending=False)
        elif sort_by == "Lowest Risk":
            filtered_df = filtered_df.sort_values('mortality_risk')
        
        filtered_df = filtered_df.head(rows_to_show)
        
        # Display table
        display_df = filtered_df.copy()
        display_df['mortality_risk'] = display_df['mortality_risk'].apply(lambda x: f"{x*100:.1f}%")
        display_df['survival_prob'] = display_df['survival_prob'].apply(lambda x: f"{x*100:.1f}%")
        
        st.dataframe(display_df, use_container_width=True)
        
        # Export options
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        with col_exp1:
            csv_data = history_df.to_csv(index=False)
            st.download_button(
                label="📥 Download History (CSV)",
                data=csv_data,
                file_name=f"prediction_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col_exp2:
            json_data = history_df.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download History (JSON)",
                data=json_data,
                file_name=f"prediction_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col_exp3:
            if st.button("🗑️ Clear History"):
                st.session_state.history = []
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 5: Settings ====================
with tab5:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">⚙️ Application Settings</p>', unsafe_allow_html=True)
    
    # Model information
    st.markdown("**Model Information:**")
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.metric("Model Type", "XGBoost Classifier")
        st.metric("Input Features", "8 Clinical Parameters")
    with col_info2:
        st.metric("Optimal Threshold", f"{optimal_threshold:.2%}")
        st.metric("Output", "Mortality Probability")
    
    st.markdown("---")
    
    # Risk thresholds (informational)
    st.markdown("**Risk Classification Thresholds:**")
    col_thresh1, col_thresh2, col_thresh3 = st.columns(3)
    with col_thresh1:
        st.info(f"🟢 **Low Risk**\nMortality < 35%")
    with col_thresh2:
        st.warning(f"🟡 **Moderate Risk**\n35% ≤ Mortality < 65%")
    with col_thresh3:
        st.error(f"🔴 **High Risk**\nMortality ≥ 65%")
    
    st.markdown("---")
    
    # Parameter ranges
    st.markdown("**Parameter Ranges:**")
    param_ranges = {
        'Group': '1-5',
        'DDPLUS': '0-100',
        'Age': '0-120 years',
        'PDW': '0-50%',
        'BUN': '0-200 mg/dL',
        'LDH': '0-2000 U/L',
        'ALT': '0-1000 U/L',
        'PT': '0-100 seconds'
    }
    
    cols = st.columns(4)
    for idx, (param, range_val) in enumerate(param_ranges.items()):
        with cols[idx % 4]:
            st.text(f"**{param}**\n{range_val}")
    
    st.markdown("---")
    
    # About
    st.markdown("**About This Application:**")
    st.info("""
    **ICU Mortality Risk Assessment System v1.1 Advanced**
    
    A clinical decision support tool for predicting mortality risk in critically ill patients
    using machine learning (XGBoost).
    
    **Features:**
    - Single patient prediction
    - Batch processing (CSV)
    - Analytics and trends
    - Patient history tracking
    - Export capabilities (CSV/JSON)
    
    **Disclaimer:**
    This tool is for clinical decision support only. Results must be validated by qualified 
    medical professionals and should not be used as the sole basis for patient management decisions.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr style="margin-top: 3rem;">
    <p style="text-align: center; color: #94a3b8; font-size: 0.85rem;">
    <strong>Disclaimer:</strong> This tool is for clinical decision support only. 
    All results must be validated by qualified medical professionals.
    </p>
""", unsafe_allow_html=True)
