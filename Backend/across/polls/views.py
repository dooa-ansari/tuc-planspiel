import rdflib
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from .list_similar_modules_blazegraph import find_all_similar_modules_list
from .module_similarity import read_modules_and_compare
from .models import UserProfile

from django.contrib.auth import login, get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
import jwt  # Import PyJWT library
from datetime import datetime, timedelta

from pymantic import sparql
from .sparql import *
import json
import requests
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleAuthRequest

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST

# graph = rdflib.Graph()
# graph.parse("bialystok_modules_full_data.rdf")
# module_list = """
# SELECT ?moduleName ?moduleId ?moduleContent ?moduleCreditPoints
# WHERE {
#     ?name <http://tuc.web.engineering/module#hasName> ?moduleName ;
#           <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
#           <http://tuc.web.engineering/module#hasContent> ?moduleContent ;
#           <http://tuc.web.engineering/module#hasCreditPoints> ?moduleCreditPoints .
# }
# """

# qresponse = graph.query(module_list)
# data_list = []
# for row in qresponse:
#     data_dict = {
#         'name': str(row.moduleName),
#         'content': str(row.moduleContent),
#     }
#     data_list.append(data_dict)
# json_data = json.dumps(data_list, indent=2)

def listsimilarmodules(request):
    data = find_all_similar_modules_list()
    return HttpResponse(data)


#### BELOW METHOD JUST MADE FOR TESTING PURPOSE, AFTER TESTING IT WILL BE REMOVED, DON't USE IT
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        # Extract data fields
        email = data.get('email', '').strip()
        full_name = data.get('full_name', '').strip()
        password = data.get('password', '').strip()
        university_name = data.get('university_name', '').strip()
        
        try:
            existing_profiles = UserProfile.objects.filter(email=email)
            if existing_profiles.exists():
                return JsonResponse({'message': 'User already exists, go to login page'})  

            validate_email(email)
            validate_password(password)
            hashed_password = make_password(password)

              # Save the data with the hashed password
            user_profile = UserProfile(email=email, full_name=full_name, password=hashed_password, university_name=university_name,
                                       signup_using='FORM', role='USER')
            user_profile.save()
            # Generate JWT token upon successful registration
            payload = {
                'email': user_profile.email,
                'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time (adjust as needed)
            }
            jwt_token = jwt.encode(payload,settings.SECRET_KEY , algorithm='HS256')
            return JsonResponse({'message': 'User registered successfully', 'token': jwt_token})

        except ValidationError as e:
            return JsonResponse({'message': str(e)})
        except jwt.InvalidTokenError as e:
            return JsonResponse({'message': 'Invalid token: ' + str(e)})
        except jwt.ExpiredSignatureError as e:
            return JsonResponse({'message': 'Token expired: ' + str(e)})
        except jwt.InvalidSignatureError as e:
            return JsonResponse({'message': 'Invalid signature: ' + str(e)})
        except jwt.InvalidIssuerError as e:
            return JsonResponse({'message': 'Invalid issuer: ' + str(e)})
        except Exception as ex:
            # Handle other exceptions if needed
            return JsonResponse({'message': 'Error generating token: ' + str(ex)})
 
    return JsonResponse({'message': 'Invalid request method'})


#### ABOVE METHOD JUST MADE FOR TESTING PURPOSE, AFTER TESTING IT WILL BE REMOVED, DON't USE IT

def index(request):
    return HttpResponse(json_data)

@csrf_exempt
def authenticate_user_login(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Extract email and password from the data
            email = data.get('email', '')
            password = data.get('password', '')

            # Perform authentication
            user_profile = UserProfile.objects.get(email=email)
            if user_profile is not None:
                passwords_match = check_password(password, user_profile.password)
                if passwords_match:
                    # Serialize the UserProfile instance to JSON
                    user_profile_data = {
                        'email': user_profile.email,
                        'full_name': user_profile.full_name,
                        'university_name': user_profile.university_name,
                        'signup_using': user_profile.signup_using,
                        'role':user_profile.role
                    }                    
                    response = {
                        "message":"Login Successful",
                        "data": user_profile_data
                    }
                    return JsonResponse(response, status =200)
                else:
                    return JsonResponse({'message': 'Email or password is incorrect'}, status = 401)
            return JsonResponse({'message': 'Login Failed'}, status = 400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data in the request body'}, status=400)
    return JsonResponse({'message':'Method not allowed'}, status = 405)

@csrf_exempt
def google_login(request):

    # Get the raw request body
    body = request.body.decode('utf-8')

    try:
        # Parse JSON data from the request body
        data = json.loads(body)
        access_token = data.get('access_token', '')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data in the request body'}, status=400)

    # Step 1: Verify the Token
    try:
        # Assuming you have a Google Client ID
        CLIENT_ID = '939129256680-qe0149eq0b5g9oc14cj3lc78inbue6rq.apps.googleusercontent.com'
        id_token.verify_oauth2_token(access_token, GoogleAuthRequest(), CLIENT_ID)
    except ValueError as e:
        return JsonResponse({'error': f'Token verification failed: {str(e)}'}, status=400)

    # Step 2: Access data from access_token
    try:
        token_info_url = 'https://oauth2.googleapis.com/tokeninfo'
        token_info_response = requests.get(f'{token_info_url}?id_token={access_token}')
        token_info = token_info_response.json()
    except Exception as e:
        return JsonResponse({'error': f'Invalid token info from oauth2, {str(e)}'}, status=400)

    try:
        user_info = json.dumps(token_info)
        user_info_json = json.loads(user_info)
    except Exception as e:
        return JsonResponse({'error': f'Error in JSON format, {str(e)}'}, status=400)

    # Step 3: Create or Authenticate User
    # You may customize this part based on your Django User model and application logic
    email_id = user_info_json.get('email')
    first_name = user_info_json.get('given_name')
    last_name = user_info_json.get('family_name')

    if None in (email_id, first_name, last_name):
        return JsonResponse({'error': 'One or more required fields are missing.'}, status=400)

    try:
        User = get_user_model()
        user, created = User.objects.get_or_create(
            email=email_id,
            defaults={'first_name': first_name, 'last_name': last_name, 'username': email_id,
                      'password': make_password('encryptedsamplepasswordforgooglesignin')}
        )
        user.save()
    except Exception as e:
        return JsonResponse({'error': f'Error in handling User Model, {str(e)}'}, status=400)

    # Step 4: Authenticate User in Django
    user = authenticate(username=email_id, password='encryptedsamplepasswordforgooglesignin')

    if user is not None:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        user_profile_data = {}

        # Step 5: Make a entry in common database as well for maintaining the data
        existing_user_profile = UserProfile.objects.filter(email=email_id).first()

        # Check if the user already exist or not. If not then create new account else collect data and send with the message
        if not existing_user_profile:

            # Perform additional actions after successful login
            user_profile_from_google = UserProfile(email=email_id, full_name=first_name + ' ' + last_name,
                                                   password=make_password('encryptedsamplepasswordforgooglesignin'),
                                                   university_name='', signup_using='GOOGLE', role="USER")
            user_profile_from_google.save()
            user_profile_data = {
                        'email': user_profile_from_google.email,
                        'full_name': user_profile_from_google.full_name,
                        'university_name': user_profile_from_google.university_name,
                        'signup_using': user_profile_from_google.signup_using,
                        'role':user_profile_from_google.role
                    } 
            response_data = {
                'message': 'User account created successfully'
            } 
        ## In future need to remove this access_token from here
        else:
            user_profile = UserProfile.objects.get(email=email_id)
            user_profile_data = {
                        'email': user_profile.email,
                        'full_name': user_profile.full_name,
                        'university_name': user_profile.university_name,
                        'signup_using': user_profile.signup_using,
                        'role':user_profile_from_google.role
                    }
            response_data = {
                'message': 'User account already exist, logging you in...'
            }
        update_fields = {
            'token' : access_token,
            "data"  : user_profile_data
        }
        response_data.update(update_fields)
        return JsonResponse(response_data, status =200)
    else:
        return JsonResponse({'error': 'Authentication failed'}, status=401)


@login_required
@csrf_exempt
def google_logout(request):
    # You might revoke the Google access token here
    # Logout the user from the Django session
    request.session.flush()

    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Google logout successful'})
    else:
        return JsonResponse({'message': 'Failed to logout'})

## BELOW SAMPLE METHOD TO TEST LOGIN REMOVED LATER
@csrf_exempt
def user_profile(request):
    user = request.user

    user_details = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        # Add other fields as needed
    }

    return JsonResponse(user_details)

@csrf_exempt
@require_POST
def get_courses_from_university(request):
    # Get the raw request body
    body = request.body.decode('utf-8')

    try:
        # Parse JSON data from the request body
        data = json.loads(body)
        universityName = data.get('universityName','')
        universityUri = data.get('universityUri','')

        # # Create an RDF graph
        # g = rdflib.Graph()

        # # Load RDF data from files
        # g.parse("Backend//across//RDF_DATA//universities.rdf")
        # g.parse("Backend//across//RDF_DATA//tuc_courses.rdf")
        
        # SPARQL query to retrieve university names and course names
        query = """
        SELECT ?courseName ?courseUri ?courseNumber
        WHERE {
            ?course rdf:type <http://tuc/course#> .
            ?course <http://across/university#belongsToUniversity> ?university .
            ?university rdf:type <http://across/university#> .
            ?university <http://across/university#hasUniversityName> ?universityName .
            ?course <http://tuc/course#hasCourseName> ?courseName .
            ?course <http://tuc/course#hasCourseNumber> ?courseNumber .
            
            BIND(str(?course) AS ?courseUri)
            BIND(str(?university) AS ?universityUri)

            FILTER (
                ?universityUri = "%s" &&
                ?universityName = "%s"^^<http://www.w3.org/2001/XMLSchema#string>
            )
        }
        """% (universityUri,universityName)

        server = sparql.SPARQLServer('http://54.242.11.117:80/bigdata/sparql')

        qresponse = server.query(query)
        course_list = []
        data = qresponse['results']['bindings']
        
        # Process the results
        for result in data:
            course_list_temp = {
                'courseUri' :  str(result['courseUri']['value']),
                'courseName' : str(result['courseName']['value']),
                'courseNumber' : str(result['courseNumber']['value'])
            }
            course_list.append(course_list_temp)

        # Return JSON response
        if not course_list:
            response = {
                "message": f"No courses found for {universityName}, please check university uri or university name",
                "university": universityName
            }
            return JsonResponse(response, status =404)
        else:
            response = {
                "message": "Course list returned successfully",
                "courses": course_list,
                "university": universityName
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