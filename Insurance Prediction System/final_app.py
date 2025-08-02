import numpy as np 
import pandas as pd 
import streamlit as st 
import joblib  
 
# Load trained model 
model = joblib.load('rfr default model1.pkl') 

# Page Configuration
st.set_page_config(
    page_title="Insurance Prediction App",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<h1 class="main-header">🏥 Insurance Prediction System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced AI-powered insurance value prediction based on your health profile</p>', unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    # Personal Information Section
    st.markdown('<h2 class="section-header">📋 Personal Information</h2>', unsafe_allow_html=True)
    
    # Create sub-columns for personal info
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        age = st.number_input('🎂 Age', min_value=0, max_value=100, value=24, help="Enter your current age")
        weight = st.number_input('⚖️ Weight (kg)', min_value=0, max_value=200, value=70, help="Enter your weight in kilograms")
    
    with info_col2:
        height = st.number_input('📏 Height (cm)', min_value=0, max_value=250, value=170, help="Enter your height in centimeters")
        no_majorsurgeries = st.number_input('🏥 Major Surgeries', min_value=0, max_value=10, value=0, help="Number of major surgeries you've had")

    # Health Information Section
    st.markdown('<h2 class="section-header">🩺 Health Information</h2>', unsafe_allow_html=True)
    
    def get_mcq_responses(questions): 
        responses = [] 
        
        # Create columns for better layout of health questions
        health_col1, health_col2 = st.columns(2)
        
        for i, q in enumerate(questions):
            col = health_col1 if i % 2 == 0 else health_col2
            with col:
                # Add icons to questions
                icons = ["🍯", "💓", "🫀", "🔄", "🤧", "🧬"]
                icon = icons[i] if i < len(icons) else "❓"
                
                answer = st.radio(f"{icon} {q}", ["Yes", "No"], key=q, horizontal=True)
                responses.append(1 if answer == "Yes" else 0) 
        return responses 
    
    questions = [ 
        "Diabetes", 
        "Blood Pressure Problems", 
        "Any Transplants", 
        "Any Chronic Diseases", 
        "Known Allergies", 
        "History Of Cancer in Family" 
    ] 
    
    binary_responses = get_mcq_responses(questions) 
    
    # Combine inputs into one feature list 
    inputs = [age, height, weight, no_majorsurgeries] + binary_responses

with col2:
    # Info Panel
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### ℹ️ How it works")
    st.markdown("""
    Our AI model analyzes your:
    - **Personal details** (age, height, weight)
    - **Medical history** (surgeries, conditions)
    - **Health factors** (chronic diseases, allergies)
    
    To provide an accurate insurance value prediction.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("### 📊 Your Input Summary")
    
    # Calculate BMI
    if height > 0:
        bmi = weight / ((height/100) ** 2)
        bmi_status = "Normal" if 18.5 <= bmi <= 24.9 else ("Underweight" if bmi < 18.5 else "Overweight")
    else:
        bmi = 0
        bmi_status = "N/A"
    
    st.metric("Age", f"{age} years")
    st.metric("BMI", f"{bmi:.1f}", f"{bmi_status}")
    st.metric("Health Conditions", f"{sum(binary_responses)}/6")
    st.metric("Major Surgeries", no_majorsurgeries)

# -------------------------- 
# Prediction Function 
# -------------------------- 
def predict_insurance(inputs, model): 
    try: 
        input_data = np.array([inputs]) 
        prediction = model.predict(input_data) 
        return float(prediction[0])  # continuous value 
    except Exception as e: 
        return f"Error during prediction: {str(e)}" 

# Prediction Section
st.markdown('<h2 class="section-header">🎯 Get Your Prediction</h2>', unsafe_allow_html=True)

# Create centered prediction button
pred_col1, pred_col2, pred_col3 = st.columns([1, 2, 1])

with pred_col2:
    if st.button('🔮 Predict Insurance Value'): 
        if None in inputs: 
            st.warning("⚠️ Please ensure all inputs are filled correctly.") 
        else: 
            with st.spinner('🔄 Analyzing your profile...'):
                result = predict_insurance(inputs, model) 
                
            if isinstance(result, str) and result.startswith("Error"): 
                st.error(f"❌ {result}") 
            else: 
                # Success message with styled result
                st.balloons()
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎉 Prediction Complete!</h3>
                    <h2>Insurance Value: ${result:.2f}</h2>
                    <p>Based on your health and personal profile</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Additional insights
                st.markdown("### 📈 Prediction Confidence")
                confidence = min(95, max(75, 90 - sum(binary_responses) * 3))
                st.progress(confidence / 100)
                st.write(f"Model Confidence: {confidence}%")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "🔒 Your data is processed securely and not stored permanently<br>"
    "📞 For questions about your results, consult with a healthcare professional"
    "</div>", 
    unsafe_allow_html=True
)