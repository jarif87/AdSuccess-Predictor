import streamlit as st
import requests
import pandas as pd
import numpy as np

# Streamlit app configuration
st.set_page_config(page_title="Ad Success Predictor", page_icon="📈", layout="centered")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success-message {
        font-size: 18px;
        font-weight: bold;
        color: #2e7d32;
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
    }
    .warning-message {
        font-size: 18px;
        font-weight: bold;
        color: #d32f2f;
        background-color: #ffebee;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
    }
    .error-message {
        font-size: 16px;
        color: #b71c1c;
        background-color: #ffcdd2;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app title
st.title('Advertisement Success Predictor')

# Subtitle
st.markdown("Enter the details below to predict if a user will view the advertisement.")

# NOTE: Replace with your IBM Cloud API key
API_KEY = "YOUR_API_KEY"  # Your provided API key

# Obtain IBM Watson ML token
try:
    token_response = requests.post(
        'https://iam.cloud.ibm.com/identity/token',
        data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
    )
    token_response.raise_for_status()
    mltoken = token_response.json()["access_token"]
except Exception as e:
    st.markdown(f"<div class='error-message'>Error obtaining token: {e}</div>", unsafe_allow_html=True)
    st.stop()

# Set headers for API request
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# Input form for user data with default values from the dataset
with st.form("prediction_form"):
    st.subheader("User and Advertisement Details")
    col1, col2 = st.columns(2)
    
    with col1:
        daily_time = st.number_input('Daily Time Spent on Site (hours)', min_value=0.0, step=0.01, format="%.2f", value=68.95)
        age = st.number_input('Age', min_value=0, max_value=120, step=1, value=35)
        areaincome = st.number_input('Area Income', min_value=0.0, step=0.01, format="%.2f", value=61833.9)
        dailyinternetuse = st.number_input('Daily Internet Use (hours)', min_value=0.0, step=0.01, format="%.2f", value=256.09)
    
    with col2:
        adtopicline = st.text_input('Advertisement Topic Line', value="Cloned 5thgeneration orchestration")
        city = st.text_input('City', value="Wrightburgh")
        gender = st.selectbox('Gender', ['Male', 'Female'], index=0)  # Default to Male (0)
        country = st.text_input('Country', value="Tunisia")
        timestamp = st.text_input('Timestamp (YYYY-MM-DD HH:MM:SS)', value="2016-03-27 00:53:00", placeholder="e.g., 2016-03-27 00:53:00")

    # Convert gender to binary (0 for Male, 1 for Female)
    gender_binary = 0 if gender == 'Male' else 1

    # Submit button
    submitted = st.form_submit_button("Predict Ad Success")

# Main prediction logic
if submitted:
    try:
        # Prepare input data for the API
        input_features = [[
            daily_time,
            age,
            areaincome,
            dailyinternetuse,
            adtopicline,
            city,
            gender_binary,
            country,
            timestamp
        ]]

        # Define payload with input fields and values
        payload_scoring = {
            "input_data": [{
                "fields": [
                    "Daily Time Spent on Site",
                    "Age",
                    "Area Income",
                    "Daily Internet Usage",
                    "Ad Topic Line",
                    "City",
                    "Male",
                    "Country",
                    "Timestamp"
                ],
                "values": input_features
            }]
        }

        # Send request to IBM Watson ML deployment
        response_scoring = requests.post(
            'https://jp-tok.ml.cloud.ibm.com/ml/v4/deployments/c03ad530-03b2-41ed-99ec-e8674f5d3b15/predictions?version=2021-05-01',
            json=payload_scoring,
            headers=header
        )
        response_scoring.raise_for_status()

        # Parse the response
        result = response_scoring.json()
        
        # Extract prediction probability
        final_prob = result['predictions'][0]['values'][0][1][0] * 100  # Convert to percentage

        # Display result based on probability threshold
        if final_prob > 50:
            st.markdown(
                f"<div class='success-message'>Based on the provided factors, the user is likely to view the advertisement! (Probability: {final_prob:.2f}%)</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='warning-message'>Based on the provided factors, the user is unlikely to view the advertisement. (Probability: {final_prob:.2f}%)</div>",
                unsafe_allow_html=True
            )

    except requests.exceptions.RequestException as e:
        st.markdown(f"<div class='error-message'>Error in API request: {e}</div>", unsafe_allow_html=True)
    except ValueError as ve:
        st.markdown(f"<div class='error-message'>Hang on, there might be a mistake in the input. Please check and try again: {ve}</div>", unsafe_allow_html=True)
    except Exception as ex:
        st.markdown(f"<div class='error-message'>An unexpected error occurred: {ex}</div>", unsafe_allow_html=True)

# Instructions for running the app
st.markdown("""
### How to Use
1. Fill in the user and advertisement details in the form above.
2. Ensure the timestamp is in the format `YYYY-MM-DD HH:MM:SS` (e.g., 2016-03-27 00:53:00).
3. Click the **Predict Ad Success** button to see the prediction.
4. The API key is already set, but ensure the IBM Watson ML deployment URL is correct for your model.
""")