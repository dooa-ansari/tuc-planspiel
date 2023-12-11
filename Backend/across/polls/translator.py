from .read_rdf_module_file import readRDFFile
from deep_translator import GoogleTranslator , single_detection


class module:
    def __init__(self, name, moduleContent):
        self.name = name
        self.moduleContent = moduleContent

def detectLanguage(text):
  language = single_detection(text, api_key='1971a88654d9d0f0e17d3cb291f261a6')
  return language

def translateModules(file):
   modules = readRDFFile(file)
   sourceLanguage = ''
   translationRequired = True
   data_list = []
    
   for language in modules:
    sourceLanguage = detectLanguage(language.moduleContent)
    translationRequired = sourceLanguage != 'en'
    break

   for row in modules:
    translated =  GoogleTranslator(source=sourceLanguage, target='en').translate(row.moduleContent) if translationRequired else row.moduleContent
    objectData = module(str(row.moduleName), str(translated)) 
    data_list.append(objectData)
   
   return data_list

# add word translation caching in order to avoid too many api calls
