import streamlit as st
import joblib as jl
import numpy as np

# Load the new trained model
loaded_model = jl.load('streamlit/students_marks_prediction_model.pkl')

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(45deg, #ff9a9e, #fad0c4, #ffecd9);
        background-size: 300% 300%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stButton button {
        background-color: #ff6b6b;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #ff4d4d;
    }
    .prediction-box {
        max-width: 400px;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
        text-align: center;
        color: #ff6b6b;
        font-weight: bold;
        backdrop-filter: blur(10px);
        animation: pulsate 2s infinite;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
    }
    @keyframes pulsate {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    </style>
""", unsafe_allow_html=True)

# Title of the web app
st.title("Student Percentage Predictor")

# Description
st.write("Predict your student percentage based on your quiz, assignment, and midterm marks.")

# Form for user inputs
with st.form(key='marks_form'):
    quiz_01 = st.number_input('Quiz 1 Marks:', min_value=0.0, max_value=100.0, step=0.01)
    quiz_02 = st.number_input('Quiz 2 Marks:', min_value=0.0, max_value=100.0, step=0.01)
    ass_01 = st.number_input('Assignment 1 Marks:', min_value=0.0, max_value=100.0, step=0.01)
    ass_02 = st.number_input('Assignment 2 Marks:', min_value=0.0, max_value=100.0, step=0.01)
    mid_term = st.number_input('Mid Term Marks:', min_value=0.0, max_value=100.0, step=0.01)
    
    submit_button = st.form_submit_button(label='Predict Percentage')

if submit_button:
    try:
        # Calculate averages
        quiz_avg = (quiz_01 + quiz_02) / 2
        ass_avg = (ass_01 + ass_02) / 2
        final_marks = quiz_avg + ass_avg + mid_term

        # Make prediction using the loaded model
        prediction = loaded_model.predict(np.array([[quiz_01, quiz_02, quiz_avg, ass_01, ass_02, ass_avg, mid_term, final_marks]]))

        # Round the prediction to two decimal places
        prediction = round(prediction[0], 2)

        # Display the prediction
        st.markdown(f'<div class="prediction-box">Predicted Final Percentage: {prediction}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f'Error: {str(e)}')
