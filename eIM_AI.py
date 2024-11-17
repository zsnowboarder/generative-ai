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
        resp_text = resp_text + response.text
        
    return resp_text

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

#random_report = "Victim was walking on the street. A stranger later identified as SIMPSON, Bart (1992/01/02) shouted racial slurs and attacked victim for no reason. Witness BROWN, Tom called police who arrived and arrested the suspect."

# this is the main instruction
with open("/mount/src/generative-ai/instructions.txt", "r") as file:
    textsi_1 = file.read()
    
st.title("eIM + Offence Classifier + Summarizer")
st.write('')
st.write('Responses are generated by Google Gemini AI.')
new_data = st.text_area(""" Enter a synopsis or ask me any question about eIM and I will guide you through the naming process. 
Although my training is limited, I am the proof of concept that AI can assist with multiple tasks at once.
You can ask me specifically on what naming conventions I was trained on and what else I can do. \nYou don't need to erase the text if I ask you follow up questions. Just keep adding the details required."""
                        , height=200, value="Victim was walking on the street. A stranger later identified as SIMPSON, Bart (1992/01/02) shouted racial slurs and attacked victim for no reason. Witness BROWN, Tom called police who arrived and arrested the suspect.")

#if button is clicked
if st.button("Generate Response"):
    placeholder = st.empty()
    placeholder.write("Please patient as it may take me a few seconds...")
    result = generate(new_data)
    placeholder.empty()
    placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages based on the information extracted from the officer's narrative.")
    st.text_area("Response", result, height=800)


# In[ ]:
