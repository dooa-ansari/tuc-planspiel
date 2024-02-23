import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.forms.models import model_to_dict
from .models import UserData, UserProfile
from pymantic import sparql
from .sparql import *
from django.core.files.storage import FileSystemStorage
import os
import json
import tempfile
import re
import PyPDF2
import wget
from os import listdir
from os.path import isfile, join


@csrf_exempt
@require_POST
def user_profile(request):
    body = request.body.decode('utf-8')

    try:
        # Parse JSON data from the request body
        data = json.loads(body)
        email = data.get('email','')
        
        user_profile = UserProfile.objects.get(email=email)

        user_details = {
            'email': user_profile.email,
            'full_name': user_profile.full_name,
            'university_name': user_profile.university_name,
            'role': user_profile.role
        }
        response = {
            'message': 'User Data returned successfully',
            'profile': user_details
        }
        return JsonResponse(response, status =200)

    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {e}"
        }
        return JsonResponse(response, status =500)

@csrf_exempt
@require_POST
def save_completed_modules_by_user(request):
    body = request.body.decode('utf-8')

    try:
        # Parse JSON data from the request body
        data = json.loads(body)
        email = data.get('email','')
        universityName = data.get('universityName','')
        courseName = data.get('courseName','')
        # It will consists the list of module URI and module Name
        completedModulesList = data.get('completedModulesList','')

        try:    
            user_profile = UserProfile.objects.get(email=email)
            
            user_data, created = UserData.objects.get_or_create(
            email=user_profile,
            defaults={'university_name': universityName, 'course_name': courseName, 'completed_modules': completedModulesList}
            )

            # If the instance is not created (i.e., already exists), update the fields
            if not created:
                user_data.university_name = universityName
                user_data.course_name = courseName
                user_data.completed_modules = completedModulesList

            user_data.save()

            response = {
                'message': 'Successfully Updated Completed Modules by User',
                "data": completedModulesList
            }
            return JsonResponse(response, status =200)
    
        except UserProfile.DoesNotExist:
                response = {
                    'message': f'User profile not found for the specified email:- {email}.'
                }
                return JsonResponse(response, status=404)
        except UserData.DoesNotExist:
                response = {
                    'message': f'User data not found for the specified email:- {email}.'
                }
                return JsonResponse(response, status=404)
    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {e}"
        }
        return JsonResponse(response, status =500)


@csrf_exempt
@require_POST
def fetch_completed_modules_by_user(request):
    body = request.body.decode('utf-8')

    try:
        # Parse JSON data from the request body
        data = json.loads(body)
        email = data.get('email','')

        try:
            user_data = UserData.objects.get(email=email)

            # Use ast.literal_eval to safely evaluate the string as a Python literal
            completed_modules_list = user_data.completed_modules

            user_profile_data = {  
                'university_name': user_data.university_name,
                'course_name': user_data.course_name,
                'completed_modules':completed_modules_list
            }
            response= {
                'message': 'Successfully returned completed module list of user',
                'user_profile_data' : user_profile_data
            }
            return JsonResponse(response, status =200)
        
        except UserData.DoesNotExist:
            # Handle the case where UserData does not exist for the given email
            response = {
                'message': f'UserData not found for the given email: {email}',
                'user_profile_data': {}
            }
            return JsonResponse(response, status=404)
    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {e}"
        }
        return JsonResponse(response, status =500)


@csrf_exempt
@require_http_methods(["PATCH"])
def select_university_after_signup(request):
    # Get the raw request body
    body = request.body.decode('utf-8')
    try:
        # Parse JSON data from the request body
        data = json.loads(body)
        email = data.get('email','')
        selectedUniversity = data.get('selectedUniversity','')
        
        # Fetch User Profile from database
        user_profile = UserProfile.objects.get(email=email)

        if user_profile is None:
            response = {
                "message": f"User with this email {email} does not exist"
            }
            return JsonResponse(response, status =404)
        else:
            # Update University value if provided
            if selectedUniversity:
                user_profile.university_name = selectedUniversity
                user_profile.save()

                updated_user_profile = UserProfile.objects.get(email=email)

                user_profile_dict = model_to_dict(updated_user_profile, exclude=['password'])
               

                response = {
                    "message": "University updated successfully",
                    "user": user_profile_dict
                }
                return JsonResponse(response, status=200)
            else:
                response = {
                    "message": "No updates provided"
                }
                return JsonResponse(response, status=400)
    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {e}"
        }
        return JsonResponse(response, status =500)
    
@csrf_exempt
@require_POST
def fetch_university_uri(request):
    # Get the raw request body
    body = request.body.decode('utf-8')
    try:
        # Parse JSON data from the request body
        data = json.loads(body)
        university_name = data.get('university_name','')
        university_uri = ''

        server = sparql.SPARQLServer('http://13.51.109.79/bigdata/sparql')

        qresponse = server.query(get_university_uri_by_university_name(university_name))
        data_for_university_uri = qresponse['results']['bindings'] 
        for result in data_for_university_uri:
            university_uri = str(result['universityUri']['value'])

        if university_uri:
                response = {
                    "message": "University uri returned successfully",
                    "universityDetails" : {
                    "university_uri": university_uri,
                    "university_name": university_name
                    }
                }
                return JsonResponse(response, status=200)
        else:
            response = {
                "message": "No related university uri available"
            }
            return JsonResponse(response, status=400)
    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {e}"
        }
    return JsonResponse(response, status =500)



@csrf_exempt
@require_POST
def upload_transcript(request):
    try:
            uploaded_files = request.FILES.getlist('files')
            # temp_dir = tempfile.mkdtemp()
            saved_files=saveFiles(uploaded_files)
            print(saved_files[0])
            # file_path = os.path.join(temp_dir, uploaded_files[0].name)
            pdf_file = open(f"Backend/across/uploads/{saved_files}", "rb")  
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            noOfPages = len(pdf_reader.pages)
            text = ""
            for page in pdf_reader.pages:
              text = text + page.extract_text()
    
            print(text)
                
            print("i am here")
        
            return JsonResponse({'message': 'Transcript uploaded successfully', 'saved_files': saved_files}, status=200)
    except Exception as e:
            return JsonResponse({'message': f'Transcript upload failed: {str(e)}'}, status=500)




uploadLoaction =""
def saveFiles(uploaded_files):
    # Specify the directory where you want to save the files
    upload_directory = 'Backend/across/uploads/'

    # Create a FileSystemStorage instance with the upload directory
    fs = FileSystemStorage(location=upload_directory)
    uploadLoaction= fs.location
    print(fs.location)
    # Process and save the uploaded files
    saved_files = []
    for file in uploaded_files:
        saved_file = fs.save(file.name, file)
        saved_files.append(saved_file)
    return saved_files[0]
