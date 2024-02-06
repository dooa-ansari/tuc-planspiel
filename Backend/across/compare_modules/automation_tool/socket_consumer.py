import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .module_similarity import read_modules_and_compare
from os import listdir
from os.path import isfile, join

class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({"progress": 1 , "message": "Converstion Started"}))
        file_path = "D://Web Engineering//SEM-III//Planspiel//ACROSS//ACROSS_MAIN//web-wizards//Backend//across//uploads//tuc_ase.rdf"
        folder_path = "D://Web Engineering//SEM-III//Planspiel//ACROSS//ACROSS_MAIN//web-wizards//Backend//across//RDF_DATA//Bialystock University"
        # only_files_in_folder = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
        file1 = file_path
       # file2 = join(folder_path, only_files_in_folder[0])
        
        read_modules_and_compare(file1, folder_path, self)
        # self.send({
        #     "type": "websocket.accept",
        # })
        # async_to_sync(self.channel_layer)('updates', self.channel_name) 
        # self.send({
        #     'type':'websocket.accept'
        # })

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(text_data)
        # self.send(text_data="Hello world!")
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]

        # self.send(text_data=json.dumps({"message": message}))
    def send_message(self, value):
        
        # message = event['message']

        self.send(text_data=json.dumps(value))