import csv
from django.shortcuts import render
import os, json
from pymantic import sparql
from .sparql import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.core.files.storage import FileSystemStorage
from .universitiy_list import get_all_universities
from .add_module import add_module_in_blaze
from django.http import HttpResponse
from user.models import UserProfile
from csv_to_rdf.csvTordf import University,CsvToRDF, UpdateModules, InsertModules
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import XSD
import requests
import uuid

uploadLoaction =""
def saveFiles(request):
    uploaded_files = request.FILES.getlist('files')
    # Specify the directory where you want to save the files
    upload_directory = 'uploads/'

    # Create a FileSystemStorage instance with the upload directory
    fs = FileSystemStorage(location=upload_directory)
    uploadLoaction= fs.location
    print(fs.location)
    # Process and save the uploaded files
    saved_files = []
    for file in uploaded_files:
        saved_file = fs.save(file.name, file)
        saved_files.append(saved_file)
    return saved_files

@csrf_exempt
@require_POST
def csv_rdf(request):
    try:
       saved_files= saveFiles(request)  
       uni = University()
       unis = uni.get_all_university()
       csv_rdf= CsvToRDF(uni)
       csv_readers=[]

       for csvFile in saved_files:
                print(uploadLoaction)
                #replace the file path from csvfile
                file_path = r'C:\Users\User\Desktop\Source\web-wizards-11\uploads\Data2.csv'
                with open(file_path, 'r', newline='', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        csv_readers.append(row)
                csvModels=csv_rdf.get_all_csv_models(csv_readers, unis)
                csv_rdf.csvModules= csvModels
                upModule = UpdateModules()
                upModule.getUpdateModels(csv_rdf)
                inModule = InsertModules()
                inModule.insertModul(csv_rdf)
                return JsonResponse({'message': 'csv Files successfully converted to RDF file'}, status=200)
    except Exception as e:
            return JsonResponse({'message': f'Error converting csv to RDF file: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
def upload_file(request):
    try:
            uploaded_files = request.FILES.getlist('files')
            saved_files=saveFiles(uploaded_files)
        
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
def insert_module(request):

    data = json.loads(request.body.decode('utf-8'))
    
    # Extract data fields
    email=data.get('email', '').strip()
    university_name= data.get('university','').strip()
    course_name = data.get('course','').strip()
    module_number = data.get('module_number','').strip()
    module_name = data.get('module_name','').strip()
    module_content = data.get('module_content','').strip()
    module_credit_points = data.get('module_credit_points','').strip()

    # Generate a UUID based on the current timestamp and node (hardware address)
    module_uuid = uuid.uuid1()

    # Convert the UUID to a string
    module_uuid_str = str(module_uuid)

    try:
        existing_user_profile = UserProfile.objects.filter(email=email).first()
        if existing_user_profile:
            if existing_user_profile.role == 'ADMIN':
                server = sparql.SPARQLServer('http://54.242.11.117:80/bigdata/sparql')

                qresponse = server.query(get_university_uri_by_university_name(university_name))
                data_for_university_uri = qresponse['results']['bindings'] 
                for result in data_for_university_uri:
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
                        payload = {'update': add_individual_module_by_admin(module_uuid_str, module_name, module_number, module_content, module_credit_points, university_uri, course_uri)}
        
                        result = requests.post("http://54.242.11.117/blazegraph/namespace/kb/sparql", data=payload)

                        # Check the response status
                        if result.status_code == 200:
                            response_data = {
                                'message': "Module Insertion successful.",
                                'module_name': module_name ,
                                'module_uri': f"http://tuc.web.engineering/module#{module_uuid_str}"
                            }
                            return JsonResponse(response_data, status=200)
                        
                    except Exception as ex:
                        # Handle other exceptions if needed
                        response_data = {
                                    'message': f"Module Insertion Failed - {str(ex)}" 
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
                    'message': f"Module Insertion Failed - {str(ex)}" 
        }
        return JsonResponse(response_data, status =500)

@csrf_exempt
@require_http_methods(["DELETE"])
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
                    server = sparql.SPARQLServer('http://54.242.11.117:80/bigdata/sparql')
                    qresponse = server.query(is_module_already_present_by_module_uri(module_uri))
                
                    # Module already exists, return a message
                    if qresponse.get('boolean') is False:                    
                        response_data = {
                            'message': "Module doesn't exist",
                            'module_uri': module_uri 
                        }
                        return JsonResponse(response_data, status=404)

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
    

@csrf_exempt
@require_http_methods(["PUT"])
def update_module(request):

    data = json.loads(request.body.decode('utf-8'))
    
    # Extract data fields
    email=data.get('email', '').strip()
    university_name= data.get('university','').strip()
    course_name = data.get('course','').strip()
    updated_module_number = data.get('module_number','').strip()
    updated_module_name = data.get('module_name','').strip()
    updated_module_content = data.get('module_content','').strip()
    updated_module_credit_points = data.get('module_credit_points','').strip()
    module_uri = data.get('module_uri','').strip()

    try:
        existing_user_profile = UserProfile.objects.filter(email=email).first()
        if existing_user_profile:
            if existing_user_profile.role == 'ADMIN':
                server = sparql.SPARQLServer('http://54.242.11.117:80/bigdata/sparql')

                qresponse = server.query(is_module_already_present_by_module_uri(module_uri))
            
                # Module already exists, return a message
                if qresponse.get('boolean') is False:                    
                    response_data = {
                        'message': "Module doesn't exist, Please create module before updating",
                        'module_uri': module_uri 
                    }
                    return JsonResponse(response_data, status=404)

                qresponse = server.query(get_university_uri_by_university_name(university_name))
                data_for_unviersity_uri = qresponse['results']['bindings'] 
                for result in data_for_unviersity_uri:
                    university_uri = str(result['universityUri']['value'])
                
                query = get_course_uri_by_course_and_university_name(course_name, university_name)
                qresponse = server.query(query)
                data_for_course_uri = qresponse['results']['bindings'] 
                for result in data_for_course_uri:
                    course_uri = str(result['courseUri']['value'])
                try:
                    payload = {'update': update_individual_module_by_admin(module_uri, updated_module_name, updated_module_number, updated_module_content, updated_module_credit_points, university_uri, course_uri)}

                    result = requests.post("http://54.242.11.117/blazegraph/namespace/kb/sparql", data=payload)

                    # Check the response status
                    if result.status_code == 200:
                        response_data = {
                            'message': "Module Updation successful.",
                            'module_name': updated_module_name
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
    