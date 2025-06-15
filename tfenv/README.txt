# MediPredict: NHS GP Appointment No-Show Prediction App

 MediPredict is a data-driven web application developed using Streamlit that predicts the likelihood of a patient missing their GP appointment. It assists healthcare providers in improving resource allocation, reducing missed appointments, and enhancing patient management.

## 📊 Features

- Predict patient no-shows based on historical data
- Visualize important patterns (e.g. no-show by age, gender, SMS received, hypertension, etc.)
- Secure login system
- User-friendly interface accessible from any browser

---

##  Installation & Setup

 How to Launch the Streamlit App
Follow these steps to run the app locally on your machine:

1. Clone or Download the Project
If you have Git installed: git clone https://github.com/your-username/your-repo-name.git
cd appointment_model_keras

Or manually download and unzip the project folder, then navigate into it using your terminal or Anaconda Prompt.

2. Create and Activate a Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux

3. Install the Required Libraries
Ensure you are inside the project folder, then run: pip install -r requirements.txt

4. Run the Streamlit App
Use the command below to launch the app: streamlit run app.py

This will open the app in your default browser. If it doesn’t open automatically, copy the URL that appears in your terminal (e.g., http://localhost:8501) and paste it into your browser.
