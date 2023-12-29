from django.shortcuts import render

import os, json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage
from polls.models import UserProfile
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import XSD

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
    formatted_course_name = course_name.replace(' ', '_')
    formatted_module_number = module_number.replace(' ', '_')

    try:
        existing_user_profile = UserProfile.objects.filter(email=email).first()
        if existing_user_profile:
            if existing_user_profile.role == 'ADMIN':

                # Normalize case for university and course names
                normalized_university_name = university_name.lower()
                normalized_course_name = formatted_course_name.lower()
                modules_rdf_path = os.path.join("D:/Web Engineering/SEM-III/Planspiel/ACROSS/ACROSS_MAIN/web-wizards/Backend/across/RDF_DATA", f"{normalized_university_name}_{normalized_course_name}.rdf")
                modules_graph = Graph()
                modules_graph.parse(modules_rdf_path, format="xml")
                modules_ns = get_namespaces(modules_graph)["module"]

                universities_rdf_path = os.path.join("D:/Web Engineering/SEM-III/Planspiel/ACROSS/ACROSS_MAIN/web-wizards/Backend/across/RDF_DATA", "tuc_universities.rdf")
                course_rdf_path = os.path.join("D:/Web Engineering/SEM-III/Planspiel/ACROSS/ACROSS_MAIN/web-wizards/Backend/across/RDF_DATA", "tuc_courses.rdf")
                
                # Load the universities RDF file
                universities_graph = Graph()
                universities_graph.parse(universities_rdf_path, format="xml")
                
                # Load the courses RDF file
                courses_graph = Graph()
                courses_graph.parse(course_rdf_path, format="xml")

                # Extract namespaces from universities RDF file
                university_ns = get_namespaces(universities_graph)["university"]
                course_ns = get_namespaces(courses_graph)["course"]

                # Find the relevant university in the universities RDF file
                university_uri = university_ns[university_name]

                # Find the relevant course in the courses RDF file
                course_uri = course_ns[formatted_course_name]

                # Construct the module URI based on the provided parameters
                module_uri = modules_ns[f"{formatted_module_name}"]

                # Get the namespace URIs directly from the graph's namespace_manager
                university_ns_uri = modules_graph.namespace_manager.store.namespace("university").toPython()
                course_ns_uri = modules_graph.namespace_manager.store.namespace("course").toPython()

                university_ns_uri = university_ns_uri+university_name
                course_ns_uri = course_ns_uri+formatted_course_name
                # Check if predicates are found
                if university_ns_uri is not None and course_ns_uri is not None:
                    if university_ns_uri == university_uri.toPython() and course_ns_uri == course_uri.toPython():

                        # Check if the module already exists, if not, create a new description
                        if (module_uri, None, None) not in modules_graph:
                            modules_graph.add((module_uri, RDF.type, URIRef(str(modules_ns))))

                        # Update the module information in the module RDF graph
                        modules_graph.set((module_uri, modules_ns.hasModuleNumber, Literal(formatted_module_number, datatype=XSD.string)))
                        modules_graph.set((module_uri, modules_ns.hasName, Literal(module_name, datatype=XSD.string)))
                        modules_graph.set((module_uri, modules_ns.hasContent, Literal(module_content, datatype=XSD.string)))
                        modules_graph.set((module_uri, modules_ns.hasCreditPoints, Literal(int(module_credit_points))))
                        modules_graph.add((module_uri, university_ns.hasUniversity, university_uri))
                        modules_graph.add((module_uri, course_ns.hasCourse, course_uri))

                        # Save the updated module RDF graph
                        modules_graph.serialize(destination=modules_rdf_path, format="xml")
                        response_data = {
                            'message': "Module Updated Successfully",
                            'module_name': module_name 
                        }
                        return JsonResponse(response_data, status =200)
                    else:
                        response_data = {
                            'message': "Doesn't find any matching university or course to add module, Please check RDF data"
                    }
                    return JsonResponse(response_data, status =404) 
                else:
                    response_data = {
                    'message': "University and Course predicates are not available, Please check RDF data" 
                    }
                    return JsonResponse(response_data, status =404) 
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
