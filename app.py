import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
import datetime
import sqlite3
import bcrypt
import plotly.express as px


# --- Database Setup (SQLite) ---
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
""")
conn.commit()

# --- Helper Functions ---
def get_user_data(username):
    cursor.execute("SELECT username, password_hash FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    if user_data:
        return user_data
    else:
        return None

def verify_password(entered_password, hashed_password):
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password.decode('utf-8'),))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# --- Load Model (with error handling) ---
try:
    model = tf.keras.models.load_model("newmodel.h5")
except FileNotFoundError:
    model = None
    st.error("Model file 'newmodel.h5' not found. Please ensure it is in the correct directory.")

# --- Location Mapping ---
location_mapping = {
    "City Centre": "N_SÃO JOSÉ",
    "Ashbrooke": "N_UNIVERSITÁRIO",
    "Hendon": "N_SANTOS REIS",
    "Monkwearmouth": "N_SÃO PEDRO",
    "Millfield": "N_SOLON BORGES",
    "Pallion": "N_TABUAZEIRO",
    "Roker": "N_SÃO CRISTÓVÃO",
    "Southwick": "N_VILA RUBIM",
    "Seaburn": "N_SÃO BENEDITO",
    "Grangetown": "N_SEGURANÇA DO LAR",
}

trained_locations = [
    'N_SANTOS REIS', 'N_SEGURANÇA DO LAR', 'N_SOLON BORGES',
    'N_SÃO BENEDITO', 'N_SÃO CRISTÓVÃO', 'N_SÃO JOSÉ',
    'N_SÃO PEDRO', 'N_TABUAZEIRO', 'N_UNIVERSITÁRIO', 'N_VILA RUBIM'
]

# --- NHS Blue ---
nhs_blue = "#005EB8"

# --- Custom CSS ---
st.markdown(
    f"""
    <style>
    body {{
        background-color: {nhs_blue};
        color: white;
    }}
    .stApp {{
        background-color: {nhs_blue};
    }}
    .block-container {{
        padding-top: 2rem;
    }}
    .white-box {{
        background-color: white;
        color: black;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }}
    input, select, textarea {{
        color: white !important;
        border: 1px solid white;
    }}
    input::placeholder, select::placeholder, textarea::placeholder {{
        color: #D3D3D3 !important;
    }}
    label {{
        color: white !important;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: white !important;
    }}
    p {{
        color: white !important;
    }}
    .stButton>button {{
        color: {nhs_blue};
        background-color: white;
        border: 1px solid {nhs_blue};
    }}
    .stButton>button:hover {{
        color: white;
        background-color: {nhs_blue};
    }}
    .stProgress>div>div>div>div {{
        background-color: white !important;
    }}
    .stError {{
        color: white !important;
        background-color: #dc3545;
        padding: 10px;
        border-radius: 5px;
    }}
    .stSuccess {{
        color: white !important;
        background-color: #28a745;
        padding: 10px;
        border-radius: 5px;
    }}
    .section-divider {{
        border-bottom: 1px solid white;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
    }}
    #login-header {{
        color: white;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }}
    #christiana-addo-footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: {nhs_blue};
        color: white;
        text-align: center;
        padding: 0.5rem 0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Main Application ---
def main():
    """
    Main function to run the Streamlit application.
    Handles login and displays the main app content.
    """
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None

    if st.session_state["authentication_status"] is None:
        # --- Login Page ---
        st.markdown("<h1 id='login-header'>Medical Appointment No-Show Predictor</h1>", unsafe_allow_html=True)
        username = st.text_input("Username",  placeholder="Enter Username")
        password = st.text_input("Password", type="password", placeholder="Enter Password")
        login_button = st.button("Login")
        register_button = st.button("Register")

        if login_button:
            user_data = get_user_data(username)
            if user_data:
                stored_username, hashed_password = user_data
                if verify_password(password, hashed_password):
                    st.session_state["authentication_status"] = True
                    st.session_state["username"] = username
                    st.session_state["page"] = "predict"  # Set default page
                    st.rerun()
                else:
                    st.error("Incorrect username or password")
            else:
                st.error("Incorrect username or password")
        elif register_button:
            if register_user(username, password):
                st.success("Registration successful. Please log in.")
            else:
                st.error("Username already exists. Please choose a different username.")
        st.markdown("<div id='christiana-addo-footer'>Designed by Christiana Addo</div>", unsafe_allow_html=True)

    elif st.session_state["authentication_status"]:
        # --- Main App Content (after successful login) ---
        st.write(f"Welcome, {st.session_state['username']}!")
        st.button("Logout", on_click=logout)

        # --- Navigation Menu ---
        menu = ["Predict Appointment", "No-Show Trends"]
        if "page" not in st.session_state:
            st.session_state["page"] = "predict"  # Default page
        choice = st.sidebar.selectbox("Navigation", menu, index=0 if st.session_state["page"] == "predict" else 1)

        if choice == "Predict Appointment":
            st.session_state["page"] = "predict"
            predict_page()
        elif choice == "No-Show Trends":
            st.session_state["page"] = "dashboard"
            dashboard_page()

        # "App Designed by CHRISTIANA ADDO" at the bottom center
        st.markdown(
            """
            <div style='text-align: center; padding-top: 2rem; color: white;'>
                <p>App Designed by CHRISTIANA ADDO</p>
            </div>
            """,
            unsafe_allow_html=True
        )

def predict_page():
    """
    Function to display the appointment prediction page.
    """
    st.header("🔮 Predict Appointment Attendance")

    # Patient Info Section
    st.subheader("Patient Information")
    col1, col2 = st.columns(2)

    with col1:
        patient_id = st.text_input("Patient ID", key="patient_id")
        gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
        age = st.slider("Age", 0, 100, key="age")
        location = st.selectbox("Location (Sunderland)", list(location_mapping.keys()), key="location")

    with col2:
        hypertension = st.selectbox("Hypertension", [0, 1], key="hypertension")
        diabetes = st.selectbox("Diabetes", [0, 1], key="diabetes")
        alcoholism = st.selectbox("Alcoholism", [0, 1], key="alcoholism")
        handicap = st.selectbox("Handicap", [0, 1], key="handicap")
        sms_received = st.selectbox("SMS Received", [0, 1], key="sms_received")

    # Appointment Details Section
    st.subheader("Appointment Details")
    col3, col4 = st.columns(2)

    with col3:
        scheduled_date = st.date_input("Scheduled Date", datetime.date.today(), key="scheduled_date")
        scheduled_time = st.time_input("Scheduled Time", value=datetime.time(9, 0), key="scheduled_time")

    with col4:
        appointment_date = st.date_input("Appointment Date", datetime.date.today(), key="appointment_date")
        appointment_time = st.time_input("Appointment Time", value=datetime.time(10, 0), key="appointment_time")

    # Feature engineering
    def build_input_vector():
        features = []
        # Add patient ID (ensure numeric, else 0)
        features.append(int(patient_id) if patient_id.isdigit() else 0)
        # Encode gender
        features.append(1 if gender == "Female" else 0)
        # Basic numerical features
        features += [int(age), hypertension, diabetes, alcoholism, handicap, sms_received]
        # Date and time features
        scheduled_datetime = datetime.datetime.combine(scheduled_date, scheduled_time)
        appointment_datetime = datetime.datetime.combine(appointment_date, appointment_time)
        features += [
            scheduled_datetime.year, scheduled_datetime.month, scheduled_datetime.day,
            scheduled_datetime.hour, scheduled_datetime.minute, scheduled_datetime.second,
            appointment_datetime.year, appointment_datetime.month, appointment_datetime.day,
            scheduled_datetime.hour, scheduled_datetime.minute, scheduled_datetime.second,
        ]
        # One-hot encoding for locations (98 feature total expected)
        location_vector = [1 if loc == location_mapping[location] else 0 for loc in trained_locations]
        features += location_vector
        # Pad remaining features with zeros to match model input shape (98 total)
        while len(features) < 98:
            features.append(0)
        return np.array([features])

    # Prediction button
    if st.button("🔍 Predict No-Show", key="predict_button"):
        if model is not None:
            input_vector = build_input_vector()
            prediction = model.predict(input_vector)
            no_show_probability = float(prediction[0][0])
            st.markdown("### 🔎 Prediction Result:")
            st.progress(no_show_probability)
            if no_show_probability > 0.5:
                st.error(f"⚠️ The patient is likely to **miss** the appointment. Probability: {no_show_probability:.2%}")
            else:
                st.success(f"✅ The patient is likely to **attend** the appointment. Probability: {no_show_probability:.2%}")
        else:
            st.error("Model not loaded. Please check the model file path and ensure it is a valid Keras model.")

def dashboard_page():
    """
    Function to display the no-show trends dashboard.
    """
    st.header("📊 No-Show Trends Dashboard")

    # --- Load and Prepare Data for Dashboard ---
    file_path = 'C:/Users/CHICHI/Downloads/noshowappointments.csv/noshow.xlsx'
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        st.error(f"Error: File not found at '{file_path}'. Please check the file path.")
        return  # Stop if file not found

    # Convert 'AppointmentDay' and 'ScheduledDay' to datetime objects
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay']).dt.date
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay']).dt.date

    # Create a binary 'No-Show' column (1 if 'Yes', 0 if 'No')
    df['No_Show_Binary'] = df['No-show'].apply(lambda x: 1 if x == 'Yes' else 0)

    # Apply the location mapping to the 'Neighbourhood' column
    reverse_location_mapping = {v: k for k, v in location_mapping.items()}
    df['Neighbourhood'] = df['Neighbourhood'].map(reverse_location_mapping)
    df['Neighbourhood'] = df['Neighbourhood'].fillna(df['Neighbourhood'])

    # Overall No-Show Rate
    st.header("Overall No-Show Rate")
    total_appointments = len(df)
    no_show_count = df['No_Show_Binary'].sum()
    no_show_rate = (no_show_count / total_appointments) * 100
    st.markdown(
        f"<div style='background-color: white; color: black; padding: 10px; border-radius: 5px; font-size: 24px;'>{no_show_rate:.2f}%</div>",
        unsafe_allow_html=True,
    )

    # No-Show Trends Over Time
    st.header("No-Show Trends Over Time")
    daily_no_show = df.groupby('AppointmentDay')['No_Show_Binary'].mean().reset_index()
    daily_no_show.columns = ['AppointmentDay', 'No_Show_Rate']
    fig_daily = px.line(
        daily_no_show,
        x='AppointmentDay',
        y='No_Show_Rate',
        title='Daily No-Show Rate',
        labels={'AppointmentDay': 'Appointment Date', 'No_Show_Rate': 'No-Show Rate'},
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    # No-Show Rate by Day of the Week
    st.header("No-Show Rate by Day of the Week")
    df['Appointment_Day_Of_Week'] = pd.to_datetime(df['AppointmentDay']).dt.day_name()
    dow_no_show = df.groupby('Appointment_Day_Of_Week')['No_Show_Binary'].mean().reset_index()
    fig_dow = px.bar(
        dow_no_show,
        x='Appointment_Day_Of_Week',
        y='No_Show_Binary',
        title='No-Show Rate by Day of the Week',
        labels={'Appointment_Day_Of_Week': 'Day of the Week', 'No_Show_Binary': 'No-Show Rate'},
        category_orders={'Appointment_Day_Of_Week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
    )
    st.plotly_chart(fig_dow, use_container_width=True)

    # No-Show Rate by Neighborhood
    st.header("No-Show Rate by Neighborhood")
    neighbourhood_no_show = (
        df.groupby('Neighbourhood')['No_Show_Binary']
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig_neighbourhood = px.bar(
        neighbourhood_no_show,
        x='Neighbourhood',
        y='No_Show_Binary',
        title='Top 10 Neighborhoods by No-Show Rate',
        labels={'Neighbourhood': 'Neighborhood', 'No_Show_Binary': 'No-Show Rate'}
    )
    st.plotly_chart(fig_neighbourhood, use_container_width=True)

    # Additional Visualizations:

    # 1. No-Show Rate by Age Group
    st.header("No-Show Rate by Age Group")
    bins = [0, 12, 18, 30, 45, 60, 75, 100]
    labels = ['0-12', '13-18', '19-30', '31-45', '46-60', '61-75', '76-100']
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    age_no_show = df.groupby('Age_Group')['No_Show_Binary'].mean().reset_index()
    fig_age = px.bar(
        age_no_show,
        x='Age_Group',
        y='No_Show_Binary',
        title='No-Show Rate by Age Group',
        labels={'Age_Group': 'Age Group', 'No_Show_Binary': 'No-Show Rate'}
    )
    st.plotly_chart(fig_age, use_container_width=True)

    # 2. No-Show Rate by Gender
    st.header("No-Show Rate by Gender")
    gender_no_show = df.groupby('Gender')['No_Show_Binary'].mean().reset_index()
    fig_gender = px.bar(
        gender_no_show,
        x='Gender',
        y='No_Show_Binary',
        title='No-Show Rate by Gender',
        labels={'Gender': 'Gender', 'No_Show_Binary': 'No-Show Rate'}
    )
    st.plotly_chart(fig_gender, use_container_width=True)

    # 3. No-Show Rate by SMS Received
    st.header("No-Show Rate by SMS Received")
    sms_no_show = df.groupby('SMS_received')['No_Show_Binary'].mean().reset_index()
    sms_no_show['SMS_received'] = sms_no_show['SMS_received'].map({0: 'No', 1: 'Yes'})
    fig_sms = px.bar(
        sms_no_show,
        x='SMS_received',
        y='No_Show_Binary',
        title='No-Show Rate by SMS Received',
        labels={'SMS_received': 'SMS Received', 'No_Show_Binary': 'No-Show Rate'}
    )
    st.plotly_chart(fig_sms, use_container_width=True)

       
       # 5. No-Show Count by Appointment Hour
    st.header("No-Show Count by Appointment Hour")
    # First, convert 'AppointmentDay' + 'AppointmentTime' (if exists) or extract hour from existing time column
    # Assuming df has a column 'AppointmentHour' or we extract from appointment datetime if available
    # If your dataset has 'AppointmentHour' column, use that. Else create it.
    if 'AppointmentHour' not in df.columns:
        # If no 'AppointmentHour', try to extract from 'AppointmentDay' + 'ScheduledDay' or just from 'ScheduledDay'
        # But your dataset might have 'AppointmentTime' or 'ScheduledTime' -- if not, skip or create dummy
        # Here, let's try 'AppointmentDay' + 'ScheduledDay' to approximate hour or default to 9am
        df['AppointmentHour'] = 9  # Default, because your dataset doesn't show time detail here

    hourly_no_show = df.groupby('AppointmentHour')['No_Show_Binary'].sum().reset_index()
    fig_hour = px.bar(
        hourly_no_show,
        x='AppointmentHour',
        y='No_Show_Binary',
        title='No-Show Count by Appointment Hour',
        labels={'AppointmentHour': 'Hour of Day', 'No_Show_Binary': 'No-Show Count'}
    )
    st.plotly_chart(fig_hour, use_container_width=True)

def logout():
    """Clears the session state and forces a rerun to show the login page."""
    st.session_state.clear()
    st.rerun()

if __name__ == "__main__":
    main()

