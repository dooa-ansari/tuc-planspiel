import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .translator import translateModules
from .update_rdf_module import add_predicate_for_module_similarity
import json
import ssl
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import fasttext
import fasttext.util
import torch
import spacy

def read_modules_and_compare(universityOneModulesFile, univeristyTwoModulesFile, consumer):
    try:
     _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
     pass
    else:
     ssl._create_default_https_context = _create_unverified_https_context
    
    # nltk.download('all')
    consumer.send_message({"progress": 2 , "message": "Starting module conversions"})
    firstUniversityModules = translateModules(universityOneModulesFile, consumer)
    consumer.send_message({"progress": 3 , "message": "First modules file translated to english successfully"})
    secondUniversityModules = translateModules(univeristyTwoModulesFile , consumer)
    consumer.send_message({"progress": 4 , "message": "Second modules file translated to english successfully"})
    data_list_first = []
    data_list_second = []
    consumer.send_message("Starting to find similarities between modules")
    count = 4
    for module in firstUniversityModules:
        for module2 in secondUniversityModules:
            # similarity = find_text_similarity_pytorch(module.moduleContent, module2.moduleContent)
            similarity = find_text_similarity_spacy(module.moduleContent, module2.moduleContent)
            consumer.send_message({"progress": 5 , "message": f"{module.name} - {module2.name} are similar : {similarity}"})
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
               consumer.send_message(f"similarity values saved successfully")
            # data_dict = {
            # 'name': str(module.moduleName),
            # 'similarity': str(similarity),
            # }
            # data_list.append(data_dict)
    add_predicate_for_module_similarity(universityOneModulesFile, univeristyTwoModulesFile, data_list_first, data_list_second, consumer)
    return {}
    
def find_text_similarity(module1Content, module2Content):
    # Tokenize and lemmatize the texts
    similarity = 0
    try:
     tokens1 = word_tokenize(module1Content)
     tokens2 = word_tokenize(module2Content)
     lemmatizer = WordNetLemmatizer()
     tokens1 = [lemmatizer.lemmatize(token) for token in tokens1]
     tokens2 = [lemmatizer.lemmatize(token) for token in tokens2]

     # Remove stopwords
     stop_words = stopwords.words('english')
     tokens1 = [token for token in tokens1 if token not in stop_words]
     tokens2 = [token for token in tokens2 if token not in stop_words]

     # Create the TF-IDF vectors
     vectorizer = TfidfVectorizer()
     vector1 = vectorizer.fit_transform(tokens1)
     vector2 = vectorizer.transform(tokens2)

     # Calculate the cosine similarity
     similarity = cosine_similarity(vector1, vector2)
    except Exception as e:
       print("error"+e) 
    # 

    return similarity


def find_text_similarity_sk(module1Content, module2Content):
    # Tokenize and lemmatize the texts
    similarity = 0
    try:
     vectorizer = TfidfVectorizer()
     vectors = vectorizer.fit_transform([module1Content, module2Content])

     # Calculate the cosine similarity between the vectors
     similarity = cosine_similarity(vectors)

    except Exception as e:
       print("error"+e) 
    # 

    return similarity

def find_text_similarity_bert(module1Content, module2Content):
    # Tokenize and lemmatize the texts
    similarity = 0
    try:
     # Load the BERT model
     model = pipeline("fill-mask", model="bert-base-uncased")

     # Tokenize and encode the texts
     text1 = "This is the first text."
     text2 = "This is the second text."
     encoding1 = model.encode(text1, max_length=512)
     encoding2 = model.encode(text2, max_length=512)

     # Calculate the cosine similarity between the embeddings
     similarity = numpy.dot(encoding1, encoding2) / (numpy.linalg.norm(encoding1) * numpy.linalg.norm(encoding2))
    #  print(similarity)

    except Exception as e:
       print("error"+e) 
    # 

    return similarity


def find_text_similarity_fast_text(module1Content, module2Content):
    # Load the FastText model
    fasttext.util.download_model('en', if_exists='ignore')  # English
    model = fasttext.load_model('cc.en.300.bin')

    # Preprocess the text
    text1 = 'This is a piece of text'
    text2 = 'This is another piece of text'
    tokens1 = fasttext.tokenize(text1)
    tokens2 = fasttext.tokenize(text2)
    tokens1 = [token.lower() for token in tokens1]
    tokens2 = [token.lower() for token in tokens2]

    # Generate word vectors for each piece of text
    try:
     vector1 = model.get_sentence_vector(tokens1)
     vector2 = model.get_sentence_vector(tokens2)
    except Exception as e:
      print("error:"+e) 

    # # Calculate the similarity between the vectors using cosine similarity
    # from scipy.spatial.distance import cosine
    # similarity = 1 - cosine(vector1, vector2)
    # print(similarity)
    print('Similarity:', 0)

def find_text_similarity_pytorch(text1, text2):
    # Convert the texts to tensors
    text1 = torch.tensor([text1])
    text2 = torch.tensor([text2])

    # Calculate the dot product of the texts
    dot_product = torch.matmul(text1, text2.transpose(1, 0))

    # Calculate the norms of the texts
    norm1 = torch.norm(text1, dim=1)
    norm2 = torch.norm(text2, dim=1)

    # Calculate the cosine similarity
    cosine_similarity = dot_product / (norm1 * norm2)
    print("similarity:"+cosine_similarity)
    return cosine_similarity


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
