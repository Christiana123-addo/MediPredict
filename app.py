import streamlit as st
import tensorflow as tf
import numpy as np

# Load the model
model = tf.keras.models.load_model('C://Users//CHICHI/appointment_model.h5')  # <-- Make sure the file name matches!

st.title("Medical Appointment No-Show Predictor")

# Input fields for user
age = st.number_input("Age", min_value=0, max_value=120, value=30)
sms_received = st.selectbox("Received SMS?", ["Yes", "No"])
scholarship = st.selectbox("Scholarship?", ["Yes", "No"])
hypertension = st.selectbox("Hypertension?", ["Yes", "No"])
diabetes = st.selectbox("Diabetes?", ["Yes", "No"])

# Convert inputs to model input
input_data = np.array([[age,
                        1 if sms_received == "Yes" else 0,
                        1 if scholarship == "Yes" else 0,
                        1 if hypertension == "Yes" else 0,
                        1 if diabetes == "Yes" else 0]])

# Predict
if st.button("Predict"):
    prediction = model.predict(input_data)[0][0]
    if prediction >= 0.5:
        st.error("❌ Likely to MISS the appointment.")
    else:
        st.success("✅ Likely to SHOW UP for the appointment.")
