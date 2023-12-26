from .read_rdf_module_file import readRDFFile
from deep_translator import GoogleTranslator , single_detection


class module:
    def __init__(self, name, moduleContent, uri, similar_modules):
        self.name = name
        self.moduleContent = moduleContent
        self.uri = uri
        self.similar_modules = similar_modules
   
    def __getitem__(self, key):
     return getattr(self, key)
    
    def __setitem__(self, key, newValue):
        self.similar_modules = newValue

def detectLanguage(text):
  language = single_detection(text, api_key='1971a88654d9d0f0e17d3cb291f261a6')
  return language

def translateModules(file):
   modules_data = readRDFFile(file)
   modules = modules_data[0]
   first_module = modules_data[1]
   
   sourceLanguage = ''
   translationRequired = True
   data_list = []
 
   for language in first_module:
    sourceLanguage = detectLanguage(language.moduleContent)
    translationRequired = sourceLanguage != 'en'
    break

   for row in modules:
    translated =  GoogleTranslator(source=sourceLanguage, target='en').translate(row.moduleContent) if translationRequired else row.moduleContent
    objectData = module(str(row.moduleName), str(translated), str(row.module), []) 
    data_list.append(objectData)
   
   return data_list

# add word translation caching in order to avoid too many api calls
