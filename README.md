###  MEDIPREDICT

 A NHS GP Appointment No-Show Prediction Streamlit Web app

MediPredict is a data-driven  web application developed using Streamlit that predicts the likelihood of a patient missing their GP appointment or attending their scheduled appointment. It also features an interactive dashboard for easy visualization and understanding of the data that contributes to patient no-shows. This assists healthcare providers in improving resource allocation, reducing missed appointments, enhancing patient management, and understanding the factors that lead to no-shows.


# Features
Predicting patient no-shows based on real-world open-source data from Kaggle.

- An interactive streamlit dashboard infused in the streamlit web app for easy visualization of important attributes like no-show by age, gender, SMS received, etc, which contributes to the probability of no-show.

- Secure login system. This is to enable only authorized users to have access to patient data.
- User-friendly interface accessible from any browser to enable users with no coding experience to navigate freely.
- A prediction page where authorized users input real-time patient data for prediction to be made based on the input data while displaying  the probability.

# Installation & Setup

 Follow these steps to set up the project locally:
 
 Manually download and unzip the project folder, then navigate into it using your terminal or Anaconda Prompt.


 Create and Activate a Virtual Environment
- python -m venv venv
- venv\Scripts\activate   # On Windows
- source venv/bin/activate  # On Mac/Linux

Install the Required Libraries

Ensure you are inside the project folder, then run:
- pip install -r requirements.txt

Run the Streamlit App
Use the command below to launch the app:
- streamlit run app.py

This will open the app in your default browser. If it doesn’t open automatically, copy the URL that appears in your terminal (e.g., http://localhost:8501) and paste it into your browser.

Or 

# Clone the repository
- git clone https://github.com/Christiana123-addo/MediPredict.git
- cd MediPredict

 # Notes
The trained model file (newmodel.h5) is excluded from the repository due to its large size. You may contact the project maintainer if you need access to it.

For best performance and portability, consider using Docker or deploying via Streamlit Cloud.

Contact
Maintained by Christiana Addo

This project is licensed under the MIT License.
GitHub: Christiana123-addo
