from django.shortcuts import render

import os, json
from pymantic import sparql
from polls.sparql import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage
from .universitiy_list import get_all_universities
from .add_module import add_module_in_blaze
from django.http import HttpResponse

from polls.models import UserProfile
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import XSD
import requests


@csrf_exempt
@require_POST
def upload_file(request):
    try:
            uploaded_files = request.FILES.getlist('files')

            # Specify the directory where you want to save the files
            upload_directory = 'uploads/'

            # Create a FileSystemStorage instance with the upload directory
            fs = FileSystemStorage(location=upload_directory)

            # Process and save the uploaded files
            saved_files = []
            for file in uploaded_files:
                saved_file = fs.save(file.name, file)
                saved_files.append(saved_file)

            return JsonResponse({'message': 'Files uploaded and saved successfully', 'saved_files': saved_files}, status=200)
    except Exception as e:
            return JsonResponse({'message': f'Error uploading and saving files: {str(e)}'}, status=500)
    
@csrf_exempt
def get_universities(request):
    data = get_all_universities(request)
    return JsonResponse(data , safe=False)

def get_namespaces(graph):
    namespaces = {}
    for prefix, uri in graph.namespaces():
        namespaces[prefix] = Namespace(uri)
    return namespaces

@csrf_exempt
@require_POST
def update_module(request):

    data = json.loads(request.body.decode('utf-8'))
    
    # Extract data fields
    email=data.get('email', '').strip()
    university_name= data.get('university','').strip()
    course_name = data.get('course','').strip()
    module_number = data.get('module_number','').strip()
    module_name = data.get('module_name','').strip()
    module_content = data.get('module_content','').strip()
    module_credit_points = data.get('module_credit_points','').strip()

    formatted_module_name = module_name.replace(' ', '_')
    formatted_module_number = module_number.replace(' ', '_')

    try:
        existing_user_profile = UserProfile.objects.filter(email=email).first()
        if existing_user_profile:
            if existing_user_profile.role == 'ADMIN':
                server = sparql.SPARQLServer('http://54.242.11.117:80/bigdata/sparql')

                qresponse = server.query(get_university_uri_by_university_name(university_name))
                data_for_unviersity_uri = qresponse['results']['bindings'] 
                for result in data_for_unviersity_uri:
                    university_uri = str(result['universityUri']['value'])
                
                query = get_course_uri_by_course_and_university_name(course_name, university_name)
                qresponse = server.query(query)
                data_for_course_uri = qresponse['results']['bindings'] 
                for result in data_for_course_uri:
                    course_uri = str(result['courseUri']['value'])

                qresponse = server.query(is_module_already_present(module_name, module_number, university_uri, course_uri))
                
                # Module already exists, return a message
                if qresponse.get('boolean') is True:                    
                    response_data = {
                        'message': "Module already exists for the given University and Course.",
                        'module_name': module_name 
                    }
                    return JsonResponse(response_data, status=200)
                else:
                    try:
                        payload = {'update': add_individual_module_by_admin(formatted_module_name, module_name, formatted_module_number, module_content, module_credit_points, university_uri, course_uri)}
        
                        result = requests.post("http://54.242.11.117/blazegraph/namespace/kb/sparql", data=payload)

                        # Check the response status
                        if result.status_code == 200:
                            response_data = {
                                'message': "Module updation successful.",
                                'module_name': module_name 
                            }
                            return JsonResponse(response_data, status=200)
                        
                    except Exception as ex:
                        # Handle other exceptions if needed
                        response_data = {
                                    'message': f"Module Updation Failed - {str(ex)}" 
                        }
                        return JsonResponse(response_data, status =500)
            else:
                response_data = {
                    'message': "User doesn't have admin privileges!" 
                }
                return JsonResponse(response_data, status =403)
        else:
            response_data = {
                    'message': "User does not exist" 
            }
            return JsonResponse(response_data, status =404) 
    except Exception as ex:
        # Handle other exceptions if needed
        response_data = {
                    'message': f"Module Updation Failed - {str(ex)}" 
        }
        return JsonResponse(response_data, status =500)

@csrf_exempt
@require_POST
def delete_module(request):
    data = json.loads(request.body.decode('utf-8'))
    
    # Extract data fields
    email=data.get('email', '').strip()
    module_uri = data.get('module_uri','').strip()

    try:
        existing_user_profile = UserProfile.objects.filter(email=email).first()
        if existing_user_profile:
            if existing_user_profile.role == 'ADMIN':
                try:
                    payload = {'update': delete_individual_module(module_uri)}

                    result = requests.post("http://54.242.11.117/blazegraph/namespace/kb/sparql", data=payload)

                    # Check the response status
                    if result.status_code == 200:
                        response_data = {
                            'message': "Module deletion successful.",
                        }
                        return JsonResponse(response_data, status=200)
                        
                except Exception as ex:
                    # Handle other exceptions if needed
                    response_data = {
                                'message': f"Module Deletion Failed - {str(ex)}" 
                    }
                    return JsonResponse(response_data, status =500)
            else:
                response_data = {
                    'message': "User doesn't have admin privileges!" 
                }
                return JsonResponse(response_data, status =403)
        else:
            response_data = {
                    'message': "User does not exist" 
            }
            return JsonResponse(response_data, status =404) 
    except Exception as ex:
        # Handle other exceptions if needed
        response_data = {
                    'message': f"Module Deletion Failed - {str(ex)}" 
        }
        return JsonResponse(response_data, status =500)