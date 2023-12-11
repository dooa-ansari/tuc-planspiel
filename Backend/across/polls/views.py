import rdflib
from django.http import HttpResponse
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, get_user_model
import json
import requests
from django.http import JsonResponse
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleAuthRequest

graph = rdflib.Graph()
#complete isn't required , incase required we need to do it some other way becuase path will be different for different machines
#graph.parse("D:\Web Engineering\SEM-III\Planspiel\ACROSS\ACROSS_MAIN\web-wizards\Backend\web_engineering_modules.rdf")
graph.parse("web_engineering_modules.rdf")
#graph.parse("D:\Web Engineering\SEM-III\Planspiel\ACROSS\ACROSS_MAIN\web-wizards\Backend\departments.rdf")
graph.parse("departments.rdf")
module_list = """
SELECT ?moduleName ?moduleId ?moduleContent ?moduleCreditPoints ?deptName ?dName ?deptId
WHERE {
    ?name <http://tuc.web.engineering/module#hasName> ?moduleName ;
          <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
          <http://tuc.web.engineering/module#hasContent> ?moduleContent ;
          <http://tuc.web.engineering/module#hasCreditPoints> ?moduleCreditPoints ; 
          <http://tuc.web.engineering/department#hasName> ?deptName .
    ?deptName <http://tuc.web.engineering/department#hasName> ?dName .
    ?deptName <http://tuc.web.engineering/department#hasDeptId> ?deptId .
}
"""

qresponse = graph.query(module_list)
data = "<html><body>"
counter = 0
data_list = []
for row in qresponse:
    counter = counter + 1
    data_dict = {
        'moduleName': str(row.moduleName),
        'moduleId': str(row.moduleId),
        'moduleContent': str(row.moduleContent),
        'moduleCreditPoints': str(row.moduleCreditPoints),
        'deptName': str(row.dName),
        'deptId': str(row.deptId)
    }
    data_list.append(data_dict)
json_data = json.dumps(data_list, indent=2)
data = data + json_data
data = data + f"<p>Total Modules are: {counter} </p></html></body>"


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

        # Validate and save the data
        user_profile = UserProfile(email=email, full_name=full_name, password=password, university_name=university_name)
        user_profile.save()

        return JsonResponse({'message': 'User registered successfully'})

    return JsonResponse({'message': 'Invalid request method'})

#### ABOVE METHOD JUST MADE FOR TESTING PURPOSE, AFTER TESTING IT WILL BE REMOVED, DON't USE IT

def index(request):
    return HttpResponse(json_data)


@csrf_exempt
def process_login(request):
    print(request)

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

    token_info_url = 'https://oauth2.googleapis.com/tokeninfo'
    token_info_response = requests.get(f'{token_info_url}?id_token={access_token}')
    token_info = token_info_response.json()

    user_info = json.dumps(token_info)
    user_info_json = json.loads(user_info)

    # Step 3: Create or Authenticate User
    # You may customize this part based on your Django User model and application logic
    email_id = user_info_json.get('email')
    first_name = user_info_json.get('given_name')
    last_name = user_info_json.get('family_name')

    User = get_user_model()
    user, created = User.objects.get_or_create(email=email_id,
                                               defaults={'first_name': first_name, 'last_name': last_name})

    # Step 4: Authenticate User in Django
    # user = authenticate(request, username=emailId, backend=ModelBackend())
    if user is not None:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return JsonResponse({'success': 'User authenticated successfully'})
    else:
        return JsonResponse({'error': 'Authentication failed'}, status=401)
