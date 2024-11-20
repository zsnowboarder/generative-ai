#!/usr/bin/env python
# coding: utf-8

# In[1]:
#pip install --upgrade google-cloud-aiplatform
#gcloud auth application-default login

import streamlit as st
from google.cloud import aiplatform
from google.oauth2 import service_account
import datetime

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

# get current date and time

today = datetime.date.today()
curr_date = today.strftime("%Y-%m-%d")
now = datetime.datetime.now()
curr_time = now.strftime("%H%M")
curr_time = int(curr_time)

# get the credentials from streamlit secrets
credentials_info = st.secrets["gsc_connections"]
credentials = service_account.Credentials.from_service_account_info(credentials_info)

def initialize_vertex_client():
    
    aiplatform.init(project="eim-conventions", location="northamerica-northeast1", credentials=credentials)



def generate(inst_text, prompt_text):
    vertexai.init(project="eim-convention", location="northamerica-northeast1", credentials=credentials)
    model = GenerativeModel(
        "gemini-1.5-pro-002",
        system_instruction=[inst_text]
    )
    responses = model.generate_content(
        [prompt_text],
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
    "temperature": 0,
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

def generate_xml():
    xml_text = generate(instructions_xml, new_data)
    
    # replace some variables. this applies to the xml text
    xml_text = xml_text.replace("<CASE_FILE_NUMBER>2024-","<CASE_FILE_NUMBER>")
    xml_text = xml_text.replace("@9999/99/99", curr_date)
    xml_text = xml_text.replace("@9999", curr_time)
    xml_text = xml_text.replace("```xml","")
    xml_text = xml_text.replace("```", "")
    
    return xml_text

    
#random_report = "Victim was walking on the street. A stranger later identified as SIMPSON, Bart (1992/01/02) shouted racial slurs and attacked victim for no reason. Witness BROWN, Tom called police who arrived and arrested the suspect."

# this is the main instruction
with open("/mount/src/generative-ai/instructions.txt", "r") as file:
    instructions = file.read()

# this is the xml instruction
with open("/mount/src/generative-ai/instructions_xml.txt", "r") as file:
    instructions_xml = file.read()

st.image("https://i1.wp.com/bcsilveralert.ca/wp-content/uploads/2014/09/Vancouver-Police.png?w=200")
st.title("eIM + Offence Classifier + Summarizer")
st.write('')
st.write('Responses are generated by Google Gemini AI.')
new_data = st.text_area(""" Enter a synopsis or ask me any question about eIM and I will guide you through the naming process. 
Although my training is limited, I am the proof of concept that AI can assist with multiple tasks at once.
You can ask me specifically on what naming conventions I was trained on and what else I can do. \nYou don't need to erase the text if I ask you follow up questions. Just keep adding the details required."""
                        , height=200, value="file number: 2024-19293. Victim Jane DOE (1991/02/03) was walking and suspect Bart SIMPSON (1990/01/01) assaulted victim. Witness John BROWN (1989/02/03) called police. PC VA9000 Mary SIM arrived and arrested Bart. Witness provided a statement to police. Suspect was released with conditions of no contact Jane DOE. PC VA9100 Bart BARROW assisted with canvassing in the Collingwood area and found no CCTV.")

#if button is clicked
if st.button("Generate Response", help="Generate eIM based on the input text."):
    placeholder = st.empty()
    placeholder.write("Please be patient as it may take me a few seconds to generate a response with this trial version........")
    result = generate(instructions, new_data)
    placeholder.empty()
    placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
    st.text_area("Response", result, height=800)

    
# Create a download button
st.download_button(
    label="Generate Report",
    help="Generate a report with entities/text pages with correct naming conventions and send it to CPIC Transcription.",
    data = generate_xml(),
    file_name="ai_report.xml",
    mime="text/plain")


# In[ ]:
