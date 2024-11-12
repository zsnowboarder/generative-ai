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
    credentials = service_account.Credentials.from_service_account_info(st.secrets[gcs_connections])
    
    aiplatform.init(project="eim-conventions", location="us-central1", credentials=credentials)


initialize_vertex_client()
    # Define your endpoint name and model ID
endpoint_name = "projects/1067800176405/locations/us-central1/endpoints/7477014419923271680"
model_id = "gemma-1_1-2b-it-1731279494640"
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




