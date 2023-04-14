#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 19:54:39 2023
"""
import json
import requests 
from urllib.parse import urlsplit

#TODO : mettre l'adresse de l'API en os.environ (mettre adresse IP Fixe)

def is_valid_url(url: str) -> bool:
    try:
        parsed_url = urlsplit(url)
    except ValueError:
        return False

    if not parsed_url.scheme or not parsed_url.netloc:
        return False

    return True

class APIClient:
    
    def __init__(self, api_url: str = "http://127.0.0.1", port: int = None):
        
        #tODO : mettre l'url en var d'environnement ? 
        
        if not is_valid_url(api_url):
            raise ValueError("Invalid API URL")
            
        self.api_url = api_url.rstrip("/") + "/"
        if port:
            self.api_url = api_url.rstrip("/")+f":{port}/"
            
        self.docs = [] #stock les dictionnaires de metadonnées
        
    
    def get_access_token(self, username: str, password: str, route:str="token/") -> str:
                data = {"username": username, "password": password}
                self.token_url = self.api_url+'token'
                response = requests.post(self.token_url, data=data)
                if response.status_code == 200:
                    self.token = response.json()["access_token"]
                else:
                    raise Exception("Authentication failed")
                    
    
    def make_post_request(
                self, 
                requete:dict, 
                route:str="search/",
                full_name:str='', 
                authenticate:bool=False
                ):
            
            """ Les principales routes : 
                    "add_doc : ajouter une document"
                    "search" : recherche des données
                    "chat" : chatbot 
            """
            if authenticate : 
                headers = {
                    'Authorization': f'Bearer {self.token}',
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            else : 
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            print(f'{self.api_url}{route}')
            try: 
                response = requests.post(f'{self.api_url}{route}', headers=headers, data=json.dumps(requete))
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise Exception(f"Request failed: {e}")
                
            self.data = response.json()
            
            return response.json()
