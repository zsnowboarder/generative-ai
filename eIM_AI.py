#!/usr/bin/env python
# coding: utf-8

# In[1]:
#pip install --upgrade google-cloud-aiplatform
#gcloud auth application-default login

import streamlit as st
from google.cloud import aiplatform
from google.oauth2 import service_account
import datetime
import pytz

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

# get current date and time
 
timezone = pytz.timezone('America/Vancouver')
today = datetime.date.today()
curr_date = today.strftime("%Y-%m-%d")
now = datetime.datetime.now()
curr_time = now.strftime("%H%M")
curr_time = int(curr_time)

# get the credentials from streamlit secrets
#credentials_info = st.secrets["gsc_connections"]
#credentials = service_account.Credentials.from_service_account_info(credentials_info)
no_credits = True

def initialize_vertex_client():
    
    aiplatform.init(project="eim-conventions", location="northamerica-northeast1", credentials=credentials)

def preprocess_instruction_text(sys_instructions):
    processed_text = sys_instructions.replace("@9999/99/99", str(curr_date))
    processed_text = processed_text.replace("@9999", str(curr_time))
    return processed_text

def generate_xml():
    xml_text = generate(instructions_xml, file_num + new_data)
    # replace some variables. this applies to the xml text
    xml_text = xml_text.replace("<CASE_FILE_NUMBER>2024-","<CASE_FILE_NUMBER>")
    xml_text = xml_text.replace("```xml","")
    xml_text = xml_text.replace("```", "")
    
    return xml_text

def generate(inst_text, prompt_text):
    if no_credits == True:
     return inst_text
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
    instructions = file.read()

# this is the xml instruction
with open("/mount/src/generative-ai/instructions_xml.txt", "r") as file:
    instructions_xml = file.read()
    instructions_xml = preprocess_instruction_text(instructions_xml)

st.image("https://i1.wp.com/bcsilveralert.ca/wp-content/uploads/2014/09/Vancouver-Police.png?w=200")
st.title("eIM + Offence Classifier + Summarizer")
st.write('')
st.write('Responses are generated by Google Gemini AI.')

occ_year = st.number_input("GO Year", value=None,  min_value=2000, max_value=2050)
occ_num = st.number_input("GO Number", value=None, min_value=1, max_value=500000)
file_num = "File number: " + str(occ_year) + "-" + str(occ_num) + " "
if occ_num is None or occ_year is None:
 file_num = ""
    
new_data = st.text_area(""" Enter a narrative or ask me any question about eIM and I will guide you through the naming process. 
Although my training is limited, I am the proof of concept that AI can assist with multiple tasks at once.
You can ask me specifically on what naming conventions I was trained on and what else I can do. \nYou don't need to erase the text if I ask you follow up questions. Just keep adding the details required."""
                        , height=200, value="file number: 2024-19293. Victim Jane DOE (1991/02/03) was walking and suspect Bart SIMPSON (1990/01/01) assaulted victim. Witness John BROWN (1989/02/03) called police. PC VA9000 Mary SIM arrived and arrested Bart. Witness provided a statement to police. Suspect was released with conditions of no contact Jane DOE. PC VA9100 Bart BARROW assisted with canvassing in the Collingwood area and found no CCTV.")

st.write("Tips: if you want to generate only specific text page, please indicate what you would like to generate. For example, generate a witness statement and a police note with the following details. On Feb 28, 2024, PC 9999 received the following statement from witness Jane DOE. I was walking and I saw.........")
#if button is clicked
if st.button("Generate Response", help="Generate eIM based on the input text."):
    placeholder = st.empty()
    placeholder.write("Please be patient as it may take me a few seconds to generate a response with this trial version........")
    result = generate(instructions, file_num + new_data)
    placeholder.empty()
    placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
    st.text_area("Response", result, height=800)

if st.button("Generate Report", help="I will generate everything including entities and text pages ready to be sent to CPIC Transcription."):
 placeholder = st.empty()
 placeholder.write("Please be patient as it may take me a few seconds to generate the report with this trial version........")
 xml_text = generate_xml()
 placeholder.empty()
 placeholder.write("Completed. You may download the report and import to MRE for further processing.")
 
 st.download_button(
  label="Download Report",
  help="Download and edit or send the report to CPIC Transcription.",
  data = xml_text,
  file_name="ai_report.xml",
  mime="text/plain")


# In[ ]:
