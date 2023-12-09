from .read_rdf_file import readRDFFile
from deep_translator import GoogleTranslator, PonsTranslator
from ponstrans import translate

import json

def translateText():
   web_engineering_modules = readRDFFile("web_engineering_modules.rdf")
   data_list = []
   for row in web_engineering_modules:
      translated = GoogleTranslator(source='de', target='en').translate(row.moduleContent)
      translatedWordList = translate(row.moduleContent, source_language="de", target_language="en")
      # try:
      # #  translatedWordList = PonsTranslator(source='de', target='en').translate('Medienretrieval', return_all=False)
      #  translatedWordList = translate(word="Medienretrieval", source_language="de", target_language="en")
      # except Exception as e:
      #   print(e) 
          
      # words = row.moduleContent.split(" ")
      # translatedWordList = ""
      # try:
      #  for word in words:
          
         
      # except Exception as e:
      #   print(e)   
      
      data_dict = {
        'name': str(row.moduleName),
        'moduleContent': str(translated),
        'ponTranslation': str(''.join(translatedWordList))
      }
      data_list.append(data_dict)
   json_data = json.dumps(data_list, indent=2)

   return json_data

# add word translation caching in order to avoid too many api calls
