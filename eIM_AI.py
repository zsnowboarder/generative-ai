#!/usr/bin/env python
# coding: utf-8

# In[1]:
#pip install --upgrade google-cloud-aiplatform
#gcloud auth application-default login

import streamlit as st
from google.cloud import aiplatform
from google.oauth2 import service_account


# Authenticate using secrets in Streamlit Cloud
def initialize_vertex_client():
    # Build the credentials from Streamlit secrets
    credentials = service_account.Credentials.from_service_account_info({
        "type": "service_account",
        "project_id": st.secrets["GOOGLE_PROJECT_ID"],
        "private_key_id": st.secrets["GOOGLE_PRIVATE_KEY_ID"],
        "private_key": st.secrets["GOOGLE_PRIVATE_KEY"].replace("\\n", "\n"),
        "client_email": st.secrets["GOOGLE_CLIENT_EMAIL"],
        "client_id": st.secrets["GOOGLE_CLIENT_ID"],
        "auth_uri": st.secrets["GOOGLE_AUTH_URI"],
        "token_uri": st.secrets["GOOGLE_TOKEN_URI"],
        "auth_provider_x509_cert_url": st.secrets["GOOGLE_AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": st.secrets["GOOGLE_CLIENT_X509_CERT_URL"],
    })
    aiplatform.init(credentials=credentials, project=st.secrets["GOOGLE_PROJECT_ID"])
    # Define your endpoint name and model ID
    endpoint_name = "projects/1067800176405/locations/us-central1/endpoints/7477014419923271680"
    model_id = "gemma-1_1-2b-it-1731279494640"

initialize_vertex_client()

# Set up Streamlit app UI
st.title("Gemini Pro Prompt with Streamlit")
user_input = st.text_input("Enter text for Gemini Prompt:")

# Function to call the Gemini Pro model
def call_gemini_pro(text):
    # Initialize the endpoint
    endpoint = aiplatform.Endpoint(endpoint_name=endpoint_name)
    # Define the input as required by the prompt
    response = endpoint.predict(instances=[{"content": text}], parameters={"temperature": 0.7})
    return response.predictions[0] if response.predictions else "No response"

# Display result when button is clicked
if st.button("Generate Response"):
    if user_input:
        result = call_gemini_pro(user_input)
        st.write(result)
    else:
        st.warning("Please enter text.")


# In[ ]:




