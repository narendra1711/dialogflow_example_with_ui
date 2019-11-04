# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 16:13:07 2019

@author: Narendra
"""

from flask import Flask, request, jsonify, render_template
from crm import CRMHandler
import dialogflow
import os

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'agent-productivity-bot-oehvrm-9db30adee407.json'
client_id = ""
client_secret = ""
token_end_point = ""
crm_resource = ""
user_name = ""
password = ""
case_generate_api = ""

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    
    DIALOGFLOW_PROJECT_ID = 'agent-productivity-bot-oehvrm'

    DIALOGFLOW_LANGUAGE_CODE = 'en-US'
    
    SESSION_ID = 'narendra1711'
    
    text_to_be_analyzed = request.form['message']
    
    session_client = dialogflow.SessionsClient()
    
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    
    query_input = dialogflow.types.QueryInput(text=text_input)
        
    try:
        
        response = session_client.detect_intent(session=session, query_input=query_input)
        
    except KeyError:
        
        print("KeyError")
        
    response_text = { "message":  response.query_result.fulfillment_text }
    
    intent = response.query_result.intent.display_name
    
    if intent == "Get Details":
        
        name = response.query_result.parameters["given-name"]
        last_name = response.query_result.parameters["last-name"]
        phone_number = response.query_result.parameters["phone-number"]
        
        crm_entity = {
                'name':name,
                'last_name':last_name,
                'phone_number':phone_number
                }
        
        print(crm_entity)
        #create_crm_case(crm_entity)
                    
    return jsonify(response_text)

def create_crm_case(crm_entity):
    
    try:
        
        with CRMHandler(client_id, client_secret, token_end_point, crm_resource, user_name, password) as crm:
            
            case_response = crm.generate_crm_case(case_generate_api, crm_entity)
            
            return True
    
    except Exception as error:
        
        print(error)
        
        return case_response
    
if __name__ == "__main__":
    
    app.run(threaded=True, debug=True, host="127.0.0.1", port=5000, use_reloader=True)