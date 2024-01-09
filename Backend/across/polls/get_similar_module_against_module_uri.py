import rdflib
import json
from .sparql import *
from pymantic import sparql
from django.http import JsonResponse


def get_similar_module_against_module_uri(request):
    try:
        moduleUri = request.GET.get('moduleUri', '')
        print(moduleUri)
        
        server = sparql.SPARQLServer('http://54.242.11.117:80/bigdata/sparql')

        qresponse = server.query(get_similar_module_against_module_uri_query(moduleUri))
        similar_module_list = []
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
            similar_module_list.append(data_dict)

        # Return JSON response
        if not similar_module_list:
            response = {
                "message": f"No similar modules found for module named as {moduleUri}, please check module uri",
                "moduleUri": moduleUri
            }
            return JsonResponse(response, status =404)
        else:
            response = {
                "message": "Similar module list returned successfully",
                "modules": similar_module_list,
                "moduleUri": moduleUri
            }
            return JsonResponse(response, status =200)

    except json.JSONDecodeError as json_error:
        response = {
            "message": f"JSON decoding error: {json_error}"
        }
        return JsonResponse(response, status =400)
    except rdflib.exceptions.Error as rdf_error:
        response = {
            "message": f"RDF parsing error: {rdf_error}"
        }
        return JsonResponse(response, status =500)
    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {e}"
        }
        return JsonResponse(response, status =500)