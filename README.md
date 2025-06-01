# Advertisement Success Predictor

![App Screenshot](https://via.placeholder.com/800x400.png?text=Advertisement+Success+Predictor) <!-- Placeholder for a screenshot -->

A Streamlit-based web application that predicts the likelihood of a user viewing an advertisement using IBM Watson Machine Learning. The app takes user and advertisement details as input, sends them to an IBM Watson ML model, and displays whether the user is likely to view the ad based on a probability threshold.

## Features

- **User-Friendly Interface**: Clean and modern UI with a two-column form layout for input fields.
- **Custom Styling**: Styled success, warning, and error messages for better user experience.
- **Default Values**: Pre-filled inputs based on sample data for quick testing.
- **Error Handling**: Robust error handling for API requests and input validation.
- **IBM Watson ML Integration**: Uses IBM Watson Machine Learning to make predictions via API.

## Dataset

The app is designed to work with advertisement data containing the following features:
- **Daily Time Spent on Site (hours)**: Time spent on the site daily.
- **Age**: User's age.
- **Area Income**: User's area income.
- **Daily Internet Usage (hours)**: Daily internet usage.
- **Ad Topic Line**: The topic line of the advertisement.
- **City**: User's city.
- **Male**: Gender (0 for Male, 1 for Female).
- **Country**: User's country.
- **Timestamp**: Timestamp of the interaction (format: `YYYY-MM-DD HH:MM:SS`).

### Sample Data
The app's default values are set based on the following sample data:
- Daily Time: 68.95 hours
- Age: 35
- Area Income: 61833.9
- Daily Internet Usage: 256.09 hours
- Ad Topic Line: "Cloned 5thgeneration orchestration"
- City: "Wrightburgh"
- Gender: Male (0)
- Country: "Tunisia"
- Timestamp: "2016-03-27 00:53:00"

## Prerequisites

- Python 3.8 or higher
- An IBM Cloud account with access to Watson Machine Learning
- An IBM Watson ML deployment with a model trained on advertisement data
- API key for IBM Cloud (see [IBM Cloud Documentation](https://jp-tok.dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-authentication.html?context=cpdaas))

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd advertisement-success-predictor

2. **Create a Virtual Environment**
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. **Install Dependencies:**
```
pip install -r requirements.txt
```
4. **If requirements.txt doesn't exist, install the required packages manually:**

```
pip install streamlit requests pandas numpy
```

# Configuration

#### **Set the IBM Cloud API Key:**
* **Open app.py.**

* **Replace the API_KEY variable with your IBM Cloud API key:**
```
API_KEY = "your-ibm-cloud-api-key"
```
- **Security Note:** In a production environment, use environment variables or a secure vault to store the API key instead of hard-coding it.

####  Verify the IBM Watson ML Deployment URL:
- Ensure the URL in the requests.post call matches your IBM Watson ML deployment:
```
'https://jp-tok.ml.cloud.ibm.com/ml/v4/deployments/c03ad530-03b2-41ed-99ec-e8674f5d3b15/predictions?version=2021-05-01'
```
- **Update the URL if your deployment ID or region differs.**

# Running the App

- **Start the Streamlit App:**
```

streamlit run ad_predictor.py
```
- **Access the App:**

**Open your browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).**

