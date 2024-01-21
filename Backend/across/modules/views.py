import rdflib
from pymantic import sparql
from .sparql import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def list_similar_modules(request):
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


@csrf_exempt
def get_similar_module_against_given_module_uri(request):
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

@csrf_exempt
@require_POST
def get_modules_from_course_and_university(request):
    # Get the raw request body
    body = request.body.decode('utf-8')

    try:
        # Parse JSON data from the request body
        data = json.loads(body)
        courseUri = data.get('courseUri','')
        universityUri = data.get('universityUri','')
        courseName = data.get('courseName','')
     
        # SPARQL query to retrieve university names and course names
        sparql_query = get_modules_from_course_and_university_query(courseUri, courseName, universityUri)

        # Execute the SPARQL query
        server = sparql.SPARQLServer('http://54.242.11.117:80/bigdata/sparql')

        qresponse = server.query(sparql_query)
        module_list = []
        data = qresponse['results']['bindings']
        # Process the results
        for result in data:
            module_list_temp = {
                'moduleUri' :  str(result['sampleModuleUri']['value']),
                'moduleName' : str(result['moduleName']['value']),
                'moduleNumber' : str(result['sampleModuleNumber']['value']),
                'moduleContent' : str(result['sampleModuleContent']['value']),
                'moduleCreditPoints' : str(result['sampleModuleCreditPoints']['value'])
            }
            module_list.append(module_list_temp)

        # Return JSON response
        if not module_list:
            response = {
                "message": f"No modules found for course named as {courseName}, please check university uri or course uri or course name",
                "course": courseName
            }
            return JsonResponse(response, status =404)
        else:
            response = {
                "message": "Module list returned successfully",
                "modules": module_list,
                "course": courseName
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
