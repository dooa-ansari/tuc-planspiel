import rdflib
import json
from .sparql import *
from os import listdir
from os.path import isfile, join
from pymantic import sparql


def find_all_similar_modules_list():
    server = sparql.SPARQLServer('http://54.242.11.117:80/bigdata/sparql')

    qresponse = server.query(list_with_similar_modules_query)
    data_list = []
    data = qresponse['results']['bindings']
    
    for row in data:
        data_dict = {
            'id': str(row['moduleId']['value']),
            'name': str(row['moduleName']['value']),
            'content': str(row['moduleContent']['value']),
            'creditPoints': str(row['moduleCreditPoints']['value']),
            'university': str(row['universityName']['value']),
            'courseName': str(row['courseName']['value']),
            'similarModuleId': str(row['similarModuleId']['value']),
            'similarModuleName': str(row['similarModuleName']['value']),
            'similarModuleContent': str(row['similarModuleContent']['value']),
            'similarModuleCreditPoints': str(row['similarModuleCreditPoints']['value']),
            'similarUniversity': str(row['universityNameSimilar']['value']),
            'courseNameSimilar': str(row['courseNameSimilar']['value']),
        }
        data_list.append(data_dict)
    json_data = json.dumps(data_list, indent=2)
    return json_data
