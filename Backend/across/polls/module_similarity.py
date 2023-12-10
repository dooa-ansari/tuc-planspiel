import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .translator import translateModules

def read_modules_and_compare(universityOneModulesFile, univeristyTwoModulesFile):
    firstUniversityModulesJSON = translateModules("web_engineering_modules.rdf")
    secondUniversityModulesJSON = translateModules("bialystok_modules.rdf")
    for module in firstUniversityModulesJSON:
        for module2 in secondUniversityModulesJSON:
            similarity = find_text_similarity(module.moduleContent, module2.moduleContent)
            print(similarity)
    
def find_text_similarity(module1Content, module2Content):
    # Tokenize and lemmatize the texts
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

    return similarity