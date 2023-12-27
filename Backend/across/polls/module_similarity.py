from .translator import translateModules
from .update_rdf_module import add_predicate_for_module_similarity
import ssl
import spacy

def read_modules_and_compare(universityOneModulesFile, univeristyTwoModulesFile):
    try:
     _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
     pass
    else:
     ssl._create_default_https_context = _create_unverified_https_context
    
    # nltk.download('all')
    firstUniversityModules = translateModules(universityOneModulesFile)
    secondUniversityModules = translateModules(univeristyTwoModulesFile)
    data_list_first = []
    data_list_second = []
    for module in firstUniversityModules:
        for module2 in secondUniversityModules:
            # similarity = find_text_similarity_pytorch(module.moduleContent, module2.moduleContent)
            similarity = find_text_similarity_spacy(module.moduleContent, module2.moduleContent)
            print(f"{module.name} - {module2.name} - {module.uri} similarity value is : {similarity}")
            if(similarity):
               similar_modules_m1 = []
               similar_modules_m2 = []
               similar_modules_m1.append(module2.uri)
               similar_modules_m2.append(module.uri)
               module['similar_modules'] = similar_modules_m1
               module2['similar_modules'] = similar_modules_m2
               data_list_first.append(module)
               data_list_second.append(module2)
            # data_dict = {
            # 'name': str(module.moduleName),
            # 'similarity': str(similarity),
            # }
            # data_list.append(data_dict)
    add_predicate_for_module_similarity(universityOneModulesFile, univeristyTwoModulesFile, data_list_first, data_list_second)
    return {}
    



def find_text_similarity_spacy(module1Content, module2Content):
    nlp = spacy.load('en_core_web_lg')
    
    s1 = nlp(module1Content)
    s2 = nlp(module2Content)
    s1.similarity(s2)
    
    s1_verbs = " ".join([token.lemma_ for token in s1 if token.pos_ == "VERB"])
    s1_adjs = " ".join([token.lemma_ for token in s1 if token.pos_ == "ADJ"])
    s1_nouns = " ".join([token.lemma_ for token in s1 if token.pos_ == "NOUN"])

    s2_verbs = " ".join([token.lemma_ for token in s2 if token.pos_ == "VERB"])
    s2_adjs = " ".join([token.lemma_ for token in s2 if token.pos_ == "ADJ"])
    s2_nouns = " ".join([token.lemma_ for token in s2 if token.pos_ == "NOUN"])
    
    verbs_similarity = nlp(s1_verbs).similarity(nlp(s2_verbs))
    adj_similarity = nlp(s1_adjs).similarity(nlp(s2_adjs))
    noun_similarity = nlp(s1_nouns).similarity(nlp(s2_nouns))
    
    is_similar = True if(verbs_similarity > 0.2 and adj_similarity > 0.2 and noun_similarity > 0.5) else False
    return is_similar
    # print(f"{s1} and {s2} VERBS: {nlp(s1_verbs).similarity(nlp(s2_verbs))}")
    # print(f"{s1} and {s2} ADJ: {nlp(s1_adjs).similarity(nlp(s2_adjs))}")
    # print(f"{s1} and {s2} NOUNS: {nlp(s1_nouns).similarity(nlp(s2_nouns))}")
