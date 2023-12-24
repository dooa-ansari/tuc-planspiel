import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .module_similarity import read_modules_and_compare

class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        read_modules_and_compare("web_engineering_modules.rdf", "bialystok_modules.rdf", self)
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

        self.send(text_data=value)