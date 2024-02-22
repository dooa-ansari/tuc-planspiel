from .upload_file_to_blazegraph import upload_file_to_blazegraph
from .translator import translateModules
from .update_rdf_module import add_predicate_for_module_similarity
import ssl
import spacy
from os import listdir
from os.path import isfile, join
import os
import shutil
from django.conf import settings


def read_modules_and_compare(universityOneModulesFile, only_files_in_folder, consumer):
    try:
     _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
     pass
    else:
     ssl._create_default_https_context = _create_unverified_https_context
    nlp = spacy.load('en_core_web_lg')

    # only_files_in_folder = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    for file_name in only_files_in_folder:
        univeristyTwoModulesFile = file_name
        # nltk.download('all')
        consumer.send_message({"progress": 2 , "type": 0 , "message": "Starting module conversions"})
        firstUniversityModules = translateModules(universityOneModulesFile, consumer)
        consumer.send_message({"progress": 3 , "type": 10, "message": "First modules file translated to english successfully"})
        secondUniversityModules = translateModules(univeristyTwoModulesFile , consumer)
        consumer.send_message({"progress": 4 , "type": 10, "message": "Second modules file translated to english successfully"})
        data_list_first = []
        data_list_second = []
        consumer.send_message( {"progress": 6 , "type": 10, "message": "Starting to find similarities between modules"})
        
        count = 2
        for module in firstUniversityModules:
            for module2 in secondUniversityModules:
                text1 = module.name if(module.moduleContent == "This course has not yet been described...") else module.moduleContent
                text2 = module2.name if(module2.moduleContent == "This course has not yet been described...") else module2.moduleContent
                similarity = find_text_similarity_spacy(text1, text2, nlp)
                consumer.send_message({"progress": 5 * count , "type": 2 if similarity else 3, "message": f"{module.name} - {module2.name} are similar : {similarity}"})
                if(similarity):
                    similar_modules_m1 = []
                    similar_modules_m2 = []
                    similar_modules_m1.append(module2.uri)
                    similar_modules_m2.append(module.uri)
                    module['similar_modules'] = similar_modules_m1
                    module2['similar_modules'] = similar_modules_m2
                    data_list_first.append(module)
                    data_list_second.append(module2)
                    consumer.send_message({"progress": 50 , "type": 10, "message": "Starting to find similarities between modules"})
            count = count + 0.1    
            
        add_predicate_for_module_similarity(universityOneModulesFile, univeristyTwoModulesFile, data_list_first, data_list_second, consumer)
    
    # Moving New hasModules file to Similarity Folder
    source_path = universityOneModulesFile
    filename_without_extension = os.path.splitext(os.path.basename(source_path))[0]
    new_filename = filename_without_extension
    ## NEED TO CHANGE THIS ACCORDING TO REQUIREMENT
    destination_folder =os.path.join(settings.BASE_DIR, f'RDF//Similarity Data//')
    new_file_path_destination_file = os.path.join(settings.BASE_DIR, f'RDF//Similarity Data//{new_filename}_similar.rdf')
    shutil.copy(source_path, new_file_path_destination_file)
    upload_file_to_blazegraph(destination_folder, "", False)
    
    return {}
    

def find_text_similarity_spacy(module1Content, module2Content, nlp):
    
    s1 = nlp(module1Content)
    s2 = nlp(module2Content)
    
    s1_verbs = " ".join([token.lemma_ for token in s1 if token.pos_ == "VERB"])
    s1_adjs = " ".join([token.lemma_ for token in s1 if token.pos_ == "ADJ"])
    s1_nouns = " ".join([token.lemma_ for token in s1 if token.pos_ == "NOUN"])

    s2_verbs = " ".join([token.lemma_ for token in s2 if token.pos_ == "VERB"])
    s2_adjs = " ".join([token.lemma_ for token in s2 if token.pos_ == "ADJ"])
    s2_nouns = " ".join([token.lemma_ for token in s2 if token.pos_ == "NOUN"])
    
    verbs_similarity = nlp(s1_verbs).similarity(nlp(s2_verbs))
    adj_similarity = nlp(s1_adjs).similarity(nlp(s2_adjs))
    noun_similarity = nlp(s1_nouns).similarity(nlp(s2_nouns))
    
    is_similar = True if(verbs_similarity >= 0.8 and adj_similarity >= 0.8 and noun_similarity >= 0.9) else False
    return is_similar
