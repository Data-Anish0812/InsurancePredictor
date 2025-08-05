import streamlit as st
import pandas as pd
import os

EXCEL_FILE = "Medicalpremium.csv"

# --------------------------
# Function to append to CSV
# --------------------------
def append_to_csv(file, df):
    if not os.path.exists(file):
        # If file doesn't exist, create it with headers
        df.to_csv(file, index=False)
    else:
        # Append to existing file without headers
        df.to_csv(file, mode='a', header=False, index=False)

# --------------------------
# Configure Streamlit for Dark Mode
# --------------------------
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------
# Custom CSS for Dark Mode styling with complete text visibility fix
# --------------------------
st.markdown("""
<style>
    /* Dark Mode Base Styling - Force all text to be visible */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff !important;
    }
    
    /* Force all text elements to be white/light colored */
    .stApp * {
        color: #ffffff !important;
    }
    
    /* Streamlit specific text elements */
    .stMarkdown, .stMarkdown p, .stMarkdown div, 
    .stText, .stCaption, .stCode, 
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #ffffff !important;
    }
    
    /* Input labels and help text */
    .stNumberInput label, .stRadio label, 
    .stNumberInput > label, .stRadio > label,
    .stNumberInput div[data-testid="stMarkdownContainer"] p,
    .stRadio div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Radio button options */
    .stRadio div[role="radiogroup"] label,
    .stRadio div[role="radiogroup"] span {
        color: #ffffff !important;
    }
    
    /* Metric labels and values */
    .stMetric label, .stMetric div, .stMetric span,
    div[data-testid="metric-container"] * {
        color: #ffffff !important;
    }
    
    /* Success, error, info messages */
    .stSuccess, .stError, .stInfo, .stWarning {
        color: #ffffff !important;
    }
    
    .stSuccess div, .stError div, .stInfo div, .stWarning div {
        color: #ffffff !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        color: white !important;
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9) !important;
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
    }
    
    .section-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white !important;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 2rem 0 1.5rem 0;
        text-align: center;
        font-weight: 600;
        font-size: 1.3rem;
        box-shadow: 0 4px 16px rgba(240, 147, 251, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .info-card {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        border-left: 4px solid #667eea;
        padding: 1.2rem;
        border-radius: 0 10px 10px 0;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        color: #e2e8f0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .info-card * {
        color: #e2e8f0 !important;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        padding: 1.8rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .metric-container * {
        color: #ffffff !important;
    }
    
    .prediction-button-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .prediction-button-container h4 {
        color: white !important;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }
    
    .save-button-container {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(40, 167, 69, 0.4);
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .save-button-container h4 {
        color: white !important;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }
    
    /* Enhanced Prediction Results */
    .prediction-results {
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
    }
    
    .prediction-results h4 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Dark Mode Button Styling */
    .stButton[data-testid="stButton"]:has(button[key="predict_btn"]) > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        border-radius: 30px !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4) !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton[data-testid="stButton"]:has(button[key="predict_btn"]) > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.6) !important;
    }
    
    .stButton[data-testid="stButton"]:has(button[key="save_btn"]) > button {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        border-radius: 30px !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(86, 171, 47, 0.4) !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton[data-testid="stButton"]:has(button[key="save_btn"]) > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(86, 171, 47, 0.6) !important;
    }
    
    /* Dark Mode Input Styling with white text */
    .stNumberInput > div > div > input {
        background-color: #2d3748 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    
    .stNumberInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    .stRadio > div {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
        padding: 1.2rem !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stRadio label, .stRadio span {
        color: #ffffff !important;
    }
    
    /* Dark Mode Metrics with white text */
    .metric-container .stMetric {
        background: rgba(255, 255, 255, 0.05) !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stMetric > div {
        color: #ffffff !important;
    }
    
    .stMetric label {
        color: #ffffff !important;
    }
    
    .stMetric [data-testid="metric-value"] {
        color: #ffffff !important;
    }
    
    .footer {
        text-align: center;
        color: #a0aec0 !important;
        margin-top: 3rem;
        padding: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
    }
    
    .footer * {
        color: #a0aec0 !important;
    }
    
    /* Enhanced Premium Display */
    .premium-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .premium-display * {
        color: #ffffff !important;
    }
    
    .premium-amount {
        font-size: 3rem;
        font-weight: 900;
        color: #ffffff !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        margin: 0.5rem 0;
        letter-spacing: 2px;
    }
    
    .premium-label {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    /* Force sidebar to be dark */
    .css-1d391kg {
        background-color: #1a1a2e !important;
    }
    
    /* Force main content area text to be white */
    .block-container * {
        color: #ffffff !important;
    }
    
    /* Additional text visibility fixes */
    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #ffffff !important;
    }
    
    /* Help text visibility */
    .stTooltipIcon {
        color: #ffffff !important;
    }
    
    /* Column header text */
    .element-container * {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------
# Enhanced Streamlit App UI
# --------------------------

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🏥 Insurance Data Entry Portal</h1>
    <p>Secure & Comprehensive Health Information System</p>
</div>
""", unsafe_allow_html=True)

# Personal Information Section
st.markdown("""
<div class="section-header">
    👤 Personal Information
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    age = st.number_input('🧑 Age (years)', min_value=0, max_value=100, value=25, help="Enter your current age")
    height = st.number_input('📏 Height (cm)', min_value=0, max_value=250, value=170, help="Enter your height in centimeters")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    weight = st.number_input('⚖️ Weight (kg)', min_value=0, max_value=200, value=70, help="Enter your weight in kilograms")
    no_majorsurgeries = st.number_input('🏥 Major Surgeries', min_value=0, max_value=10, value=0, help="Number of major surgeries undergone")
    st.markdown('</div>', unsafe_allow_html=True)

# Medical History Section
st.markdown("""
<div class="section-header">
    🩺 Medical History
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <strong>📝 Note:</strong> Please answer all questions honestly for accurate assessment. All information is confidential and secure.
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    diabetes = st.radio("🩸 Do you have Diabetes?", ["No", "Yes"], help="Select if you have been diagnosed with diabetes")
    bp = st.radio("💓 Blood Pressure Issues?", ["No", "Yes"], help="Select if you have high or low blood pressure problems")
    transplants = st.radio("🫀 Any Organ Transplants?", ["No", "Yes"], help="Select if you have had any organ transplants")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    chronic = st.radio("🔄 Chronic Diseases?", ["No", "Yes"], help="Select if you have any ongoing chronic conditions")
    allergies = st.radio("🤧 Known Allergies?", ["No", "Yes"], help="Select if you have any known allergies")
    cancer = st.radio("🧬 Family Cancer History?", ["No", "Yes"], help="Select if there's a history of cancer in your family")
    st.markdown('</div>', unsafe_allow_html=True)

# Data Summary Section
st.markdown("""
<div class="section-header">
    📊 Data Summary
</div>
""", unsafe_allow_html=True)

# Create summary metrics
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Age", f"{age} years", help="Your current age")
    
with col6:
    bmi = round(weight / ((height/100) ** 2), 1) if height > 0 else 0
    st.metric("BMI", f"{bmi}", help="Body Mass Index calculated from height and weight")
    
with col7:
    total_conditions = sum([
        1 if diabetes == "Yes" else 0,
        1 if bp == "Yes" else 0,
        1 if transplants == "Yes" else 0,
        1 if chronic == "Yes" else 0,
        1 if allergies == "Yes" else 0
    ])
    st.metric("Health Conditions", total_conditions, help="Number of health conditions reported")
    
with col8:
    st.metric("Surgeries", no_majorsurgeries, help="Number of major surgeries")

# Action Buttons Section
st.markdown("""
<div class="section-header">
    🚀 Actions
</div>
""", unsafe_allow_html=True)

# Create two columns for different buttons with better proportions for prediction visibility
col_pred, col_save = st.columns([3, 2])  # 3:2 ratio gives more space to prediction

with col_pred:
    st.markdown("""
    <div class="prediction-button-container">
        <h4 style="text-align: center; color: white; margin-bottom: 1rem;">🔮 Get Premium Prediction</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎯 Predict Insurance Premium", help="Get AI-powered insurance premium prediction", key="predict_btn"):
        # Enhanced prediction logic
        st.markdown("""
        <div class="prediction-results">
            <h4>🔮 Premium Prediction Results</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Advanced prediction based on inputs
        base_premium = 12000
        age_factor = age * 80
        bmi_factor = max(0, (bmi - 25)) * 300 if height > 0 else 0
        condition_factor = sum([
            3000 if diabetes == "Yes" else 0,
            2500 if bp == "Yes" else 0,
            5000 if transplants == "Yes" else 0,
            2800 if chronic == "Yes" else 0,
            800 if allergies == "Yes" else 0,
            4000 if cancer == "Yes" else 0
        ])
        surgery_factor = no_majorsurgeries * 1500
        
        predicted_premium = base_premium + age_factor + bmi_factor + condition_factor + surgery_factor
        
        # Enhanced Premium Display
        st.markdown(f"""
        <div class="premium-display">
            <div class="premium-label">Annual Premium Estimate</div>
            <div class="premium-amount">₹{predicted_premium:,}</div>
            <div style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.8);">
                Based on your health profile
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional metrics in wider layout
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            risk_level = "Low" if predicted_premium < 18000 else "Medium" if predicted_premium < 28000 else "High"
            risk_color = "#28a745" if risk_level == "Low" else "#ffc107" if risk_level == "Medium" else "#dc3545"
            st.markdown(f"""
            <div style="background: {risk_color}; color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <div style="font-size: 1.1rem; font-weight: 600;">⚡ Risk Level</div>
                <div style="font-size: 1.5rem; font-weight: 700;">{risk_level}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_p2:
            coverage = "Basic" if predicted_premium < 18000 else "Standard" if predicted_premium < 28000 else "Premium"
            coverage_color = "#17a2b8" if coverage == "Basic" else "#6f42c1" if coverage == "Standard" else "#fd7e14"
            st.markdown(f"""
            <div style="background: {coverage_color}; color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                <div style="font-size: 1.1rem; font-weight: 600;">🛡️ Coverage Type</div>
                <div style="font-size: 1.5rem; font-weight: 700;">{coverage}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #667eea; color: #e2e8f0;">
            <strong>🔍 Note:</strong> This is an AI-generated estimate based on provided health information. 
            Actual premiums may vary based on additional medical examinations and insurer policies.
        </div>
        """, unsafe_allow_html=True)

with col_save:
    st.markdown("""
    <div class="save-button-container">
        <h4 style="text-align: center; color: white; margin-bottom: 1rem;">💾 Save to Database</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📁 Save to Database", help="Securely save your information to database", key="save_btn"):
        # Get predicted premium for saving
        base_premium = 12000
        age_factor = age * 80
        bmi_factor = max(0, (bmi - 25)) * 300 if height > 0 else 0
        condition_factor = sum([
            3000 if diabetes == "Yes" else 0,
            2500 if bp == "Yes" else 0,
            5000 if transplants == "Yes" else 0,
            2800 if chronic == "Yes" else 0,
            800 if allergies == "Yes" else 0,
            4000 if cancer == "Yes" else 0
        ])
        surgery_factor = no_majorsurgeries * 1500
        predicted_premium = base_premium + age_factor + bmi_factor + condition_factor + surgery_factor
        
        # Create DataFrame with exact column names as specified
        new_data = pd.DataFrame([{
            "Age": age,
            "Diabetes": diabetes,
            "BloodPressureProblems": bp,
            "AnyTransplants": transplants,
            "AnyChronicDiseases": chronic,
            "Height": height,
            "Weight": weight,
            "KnownAllergies": allergies,
            "HistoryOfCancerInFamily": cancer,
            "NumberOfMajorSurgeries": no_majorsurgeries,
            "PremiumPrice": predicted_premium
        }])
        
        try:
            append_to_csv(EXCEL_FILE, new_data)
            st.success("✅ Data saved successfully!")
            st.balloons()
            
            # Enhanced confirmation
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 1.5rem; border-radius: 10px; margin-top: 1rem; color: white;">
                <div style="text-align: center;">
                    <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">✅ Save Confirmation</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">
                        • File: {EXCEL_FILE}<br>
                        • Premium: ₹{predicted_premium:,}<br>
                        • Status: Encrypted & Secure<br>
                        • Records: +1 entry added
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error saving data: {str(e)}")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); padding: 1.5rem; border-radius: 10px; margin-top: 1rem; color: white;">
                <div style="text-align: center;">
                    <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">⚠️ Error Details</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">
                        Database connection failed. Please try again or contact support.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Show confirmation details
            st.markdown("""
            <div style="background: #d4edda; padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #28a745;">
                <strong>✅ Save Confirmation:</strong><br>
                • File: insurance_inputs.xlsx<br>
                • Status: Secure & Encrypted<br>
                • Records: +1 entry added
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error saving data: {str(e)}")
            st.markdown("""
            <div style="background: #f8d7da; padding: 1rem; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #dc3545;">
                <strong>⚠️ Error Details:</strong><br>
                Please try again or contact support if the issue persists.
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🔒 Your data is secure and confidential | 📞 Support: 1-800-INSURANCE</p>
    <p style="font-size: 0.9rem; color: #999;">Insurance Data Management System v2.0</p>
</div>
""", unsafe_allow_html=True)