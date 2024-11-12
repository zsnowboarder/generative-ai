#!/usr/bin/env python
# coding: utf-8

# In[1]:
#pip install --upgrade google-cloud-aiplatform
#gcloud auth application-default login

import streamlit as st
from google.cloud import aiplatform
from google.oauth2 import service_account

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

credentials_info = st.secrets["gsc_connections"]
credentials = service_account.Credentials.from_service_account_info(credentials_info)
# Authenticate using secrets in Streamlit Cloud
def initialize_vertex_client():
    # Build the credentials from Streamlit secrets
    
    aiplatform.init(project="eim-conventions", location="northamerica-northeast1", credentials=credentials)



def generate(promt_text):
    vertexai.init(project="eim-convention", location="northamerica-northeast1", credentials=credentials)
    model = GenerativeModel(
        "gemini-1.5-pro-002",
        system_instruction=[textsi_1]
    )
    responses = model.generate_content(
        [promt_text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    resp_text = ""

    for response in responses:
        resp_text = response.text
        
    return resp_text

with open("/mount/src/generative-ai/instructions.txt", "r") as file:
    textsi_1 = file.read()

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

#initialize_vertex_client()

st.title("eIM and More")
st.write('')
st.write('This is a trial version of Google Gemini AI.')
new_data = st.text_area("Enter a synopsis or ask me any question about eIM. Although my training is limited, I am the proof of concept that AI can assist.", height=200, value="I was walking and someone punched me for no reason. I had minor injuries. I reported the incident to police.")

#if button is clicked
if st.button("Generate Response"):
    result = generate(new_data)
    st.markdown(result)


# In[ ]:
