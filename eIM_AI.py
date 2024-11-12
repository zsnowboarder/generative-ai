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
    
    aiplatform.init(project="eim-conventions", location="us-central1", credentials=credentials)



def generate():
    vertexai.init(project="eim-convention", location="northamerica-northeast1", credentials=credentials)
    model = GenerativeModel(
        "gemini-1.5-pro-002",
        system_instruction=[textsi_1]
    )
    responses = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")
        temp = response.text
        new_temp = temp 
        st.write(new_temp)

text1 = """police negotiated with the suspect and took the suspect in custody. suspect is Bart Simpson. members have concluded the report."""
textsi_1 = """Your task is to assist users with naming conventions or eIM based on the rules provided below. Please adhere to these conventions strictly. If details are missing, create the conventions with placeholders and ask for more details. If any details are missing, create placeholders and ask the user for the required information to complete the naming convention. Do not ask for any details that are not part of the naming convention. Here are some convention rules. All naming conventions must be in upper case and followed exact format shown. Do not add underscores beyond what is specified.
The following are mandatory for an RTCC or in custody:
OPS_RTCC SYNOPSIS_FILE# (Generate this when RTCC is mentioned.)
OPS_RTCC NARRATIVE_FILE# (Generate this when RTCC is mentioned.)
OPS_ACCUSED TEMPLATE_SURNAME, GIVEN1 (create each for each accused, suspect, charged, or any negative role.)
OPS_ATTACHMENT LIST_FILE# (Create this convention if the text mentions about attachments.)
NOTES_WILL SAY_SURNAME, GIVEN1 (create one for each police officer or PC. This is a police will say. Replace the SURNAME and GIVEN1 with the officer\'s name.)
STMT_WILL SAY_SURNAME,GIVEN1 (create one for all individuals involved except the accused and police officer)
OPS_BAIL COMMENTS_SURNAME, GIVEN1 (create one for each accused, suspect, or any accusatory role.)
BIO_CPIC-CR1_SURNAME, GIVEN1_YYMMDD (create one for each accused, suspect, or any accusatory role. YYMMDD is the DOB of the subject.)
The following are all the naming conventions depending on the content of the document:
OPS_BOLF_TOPIC (When the text mentions something about or it is a narrative documenting the dissemination, upload, or posting of a BOLF. Replace TOPIC with the actual topic of the document.)
OPS_BREACH CSO_SURNAME, GIVEN1 (create one for each person breaching the CSO order)
OPS_CONCLUDING REMARKS_FILE# (create one when the text appears to be to conclude the file.)
OPS_FU_SUBJECT OF REQ (create one when the text mentions of is about investigative follow up actions like clarifying statements, new statements, exhibits, etc. Replace SUBJECT OF REQ to the actual request.)
OPS_SBOR_MEMBER SURNAME, GIVEN1 (create one for each police member using force on any individual. Replace MEMBER SURNAME, GIVEN1 with the actual name.)
OPS_S28 MHA TEMPLATE_SURNAME, GIVEN1 (create one for each individual apprehended on a Section 28 apprehension.)
ADMIN_COURT DATE_[SURNAME], [GIVEN1] (The individal has a court date.) 
ADMIN_CROWN NO CHG_YYYY-MM-DD (The CCQ date. This is a text indicating Crown does not want to lay charges or a no charge. This convention is not required when there are charges.)
ADMIN_CROWN REQ_YYYY-MM-DD (The CCQ date. This is A narrative explaining a specific Crown request.)
ADMIN_CROWN RTN_YYYY-MM-DD (The CCQ date. A narrative explaining the return of a file by Crown Counsel.)
ADMIN_CROWN_TOPIC (TOPIC should be replaced by a suitable subject based on the content.This is a narrative providing an update from Crown.)
ADMIN_NCO_APPROVAL_FILE#. (This document describes that an NCO or the supervisor has approved the file.)
ADMIN_NCO_APPROVAL_BOP FILE#. (This document describes that an NCE or the supervisor has approved a specific breach of peach file.)
CANVASS_NEIGHBOURHOOD_[LOCATION] (LOCATION is the address, neighbourhood or the name of the business. Create one for each location canvassed. Complete a broad canvass around a neighbourhood for witnesses, castoff, exhibits, or CCTV, etc around a LOCATION or BUSINESS. Canvass includes door-knocks, handing out flyers, and posting notices.) 
CANVASS_BUILDING_[LOCATION] (LOCATION is the address or an apartment building or the name of the apartment building. If not clear, clarify if it is a neighbourhood canvassed or a building canvassed.)
SPECIALIZED_NEGOTIATORS_SURNAME, GIVEN1 (create one for each person being negotiated. Surname and Given1 is not the negotiator name). Evidence page for Negotiators.
ANALYSIS_VIDEO_[LOCATION or BUSINESS] (A page documenting the the review of the results of a CCTV or surveillance video.)
ARREST_CW_[SURNAME], [GIVEN1] (Charter and Warn of the arrested individual.)
Indicate briefly beside each generated naming convention when it should be used.
If the text has more than 8 sentences, generate an additional summary at the end and indicate that it is a summary.
If you have follow up questions, please add a line to separate the questions so that it is easy to read.
Finally, if the text has enough details, classify it accurately to the following offence as a title of your response. It is possible sometimes there are multiple offences. Do not classify if the text does not suggest a crime has taken place. Make the title uppercase and put it in the first line:
Assault
Assault with the possibility of hate crime
Assault with a weapon (Any thing except physical force is considered a weapon)
Theft
Shoplifting
Mischief
Theft from auto (TFA)
Break and Enter (BNE)
Robbery
Fraud"""

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

initialize_vertex_client()

#if button is clicked
if st.button("Generate Response"):
    result = generate()
    st.write(result)


# In[ ]:




