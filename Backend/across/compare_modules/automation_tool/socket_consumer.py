import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .module_similarity import read_modules_and_compare
from os import listdir
from os.path import isfile, join
import os
from compare_modules.sparql import * 
from pymantic import sparql

class Consumer(WebsocketConsumer):
    def connect(self):
        try:
            self.accept()
            self.send(text_data=json.dumps({"progress": 1 , "message": "Converstion Started"}))
            
        except Exception as e:
            print(f"Error in connection {str(e)}")

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        print(text_data_json)
        if text_data_json['message'] == "start" :
            print("starting message")
            # Assuming your desired directory is two levels up from the current working directory
            
            # Sample Data
            response_data = {
            'message': "Data is Here",
            'university_name': "Bialystok University",
            'rdf_File_Path': "BU_Let'sseecourse2"
            }

            # Construct the absolute path
            server = sparql.SPARQLServer('http://192.168.0.173:9999/blazegraph/sparql')

            # # Getting University URI
            qresponse = server.query(get_other_universities_except_given(response_data['university_name']))
            data_for_university = qresponse['results']['bindings'] 
            # # Initialize an empty list to store university names
            university_names_list = []

            file_path = f"RDF_DATA//{response_data['university_name']}//{response_data['rdf_File_Path'].lower()}.rdf"
            file1 = file_path

            # # Iterate through the results and store university names in the list
            for result in data_for_university:
                university_name = str(result['universityName']['value'])
                university_names_list.append(university_name)

            # # Iterate through the list
            for university_name in university_names_list:
                absolute_path = os.path.abspath(f'RDF_DATA//{university_name}')

                folder_path = absolute_path
                # only_files_in_folder = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

                # file2 = join(folder_path, only_files_in_folder[0])
                
                read_modules_and_compare(file1, folder_path, self)
    
    def send_message(self, value):
        
        # message = event['message']

        self.send(text_data=json.dumps(value))