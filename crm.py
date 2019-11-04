# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 16:13:07 2019

@author: Narendra
"""

import requests

class CRMHandler:
    
    def __init__(self, client_id, client_secret, token_end_point, crm_resource, username, password):
        
        self.client_id = client_id        
        self.client_secret = client_secret        
        self.token_end_point = token_end_point        
        self.crm_resource = crm_resource        
        self.username = username        
        self.password = password
        
    def __enter__(self, *args, **kwargs):
        
        self.__credentials__ = {
                                    'client_id':self.client_id,
                                    'client_secret':self.client_secret,
                                    'resource':self.crm_resource,
                                    'username':self.username,
                                    'password':self.password,
                                    'grant_type':'password',
                                }
        
        tokenres = requests.post(self.token_end_point, data = self.__credentials__)
        
        try:
            
            self.__access_token = tokenres.json()['access_token']
            
        except(KeyError, Exception) as error:
            
            print("Failed to retrive access token", error)
            
        return self
            

    def __exit__(self, *args, **kwargs):
        
        pass
    
    def crm_request(self, crm_api, headers, data):
        
        crm_response = requests.post(crm_api, headers=headers, json=data)
        
        print(crm_response, crm_response.status_code, crm_response.text)
        
        return crm_response
    
    def generate_crm_case(self, crmwebapi, crm_entity):
        
        _headers = { 'Authorization': 'Bearer' + self.__accesstoken, 
                     'Content-Type' : 'application/json',
                     'Odata-MaxVersion': '4.0',
                     'Odata-Version' : '4.0',
                     'Accept' : 'application/json'}
        
        response = self.crm_request(crmwebapi, _headers, crm_entity)
        
        return response