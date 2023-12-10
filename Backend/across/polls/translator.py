from .read_rdf_module_file import readRDFFile
from deep_translator import GoogleTranslator , single_detection


import json

def detectLanguage(text):
  language = single_detection(text, api_key='1971a88654d9d0f0e17d3cb291f261a6')
  return language

def translateModules(file):
   modules = readRDFFile(file)
   if(modules.length > 0):
    sourceLanguage = detectLanguage(modules[0].moduleContent)
    translationRequired = sourceLanguage != 'en'
    data_list = []
    try:
     for row in modules:
      translated =  GoogleTranslator(source=sourceLanguage, target='en').translate(row.moduleContent) if translationRequired else row.moduleContent
      data_dict = {
        'name': str(row.moduleName),
        'moduleContent': str(translated),
      }
      data_list.append(data_dict)
     json_data = json.dumps(data_list, indent=2)
    except Exception as e:
     print(e)
    return json_data
   else:
     return {}

# add word translation caching in order to avoid too many api calls
