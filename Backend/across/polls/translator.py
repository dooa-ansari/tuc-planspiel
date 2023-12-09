from .read_rdf_file import readRDFFile
from deep_translator import GoogleTranslator
import json

def translateText():
   web_engineering_modules = readRDFFile("web_engineering_modules.rdf")
   data_list = []
   for row in web_engineering_modules:
      translated = GoogleTranslator(source='de', target='en').translate(row.moduleContent)
      data_dict = {
        'name': str(row.moduleName),
        'moduleContent': str(translated),
      }
      data_list.append(data_dict)
   json_data = json.dumps(data_list, indent=2)

   return json_data
