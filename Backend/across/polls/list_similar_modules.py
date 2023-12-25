import rdflib
from django.http import HttpResponse
from django.conf import settings
import json
from django.http import JsonResponse
from .sparql import *

def find_all_similar_modules_list():
    graph = rdflib.Graph()
    graph.parse("web_engineering_modules_updated.rdf")
    graph.parse("bialystok_modules_updated.rdf")

    qresponse = graph.query(list_with_similar_modules_query)
    data_list = []
    for row in qresponse:
        print(row)
        data_dict = {
            'id': str(row.moduleId),
            'name': str(row.moduleName),
            'content': str(row.moduleContent),
            'creditPoints': str(row.moduleCreditPoints),
            'similarModuleId': str(row.similarModuleId),
            'similarModuleName': str(row.similarModuleName),
            'similarModuleContent': str(row.similarModuleContent),
            'similarModuleCreditPoints': str(row.similarModuleCreditPoints),
        }
        data_list.append(data_dict)
    json_data = json.dumps(data_list, indent=2)
    return json_data
