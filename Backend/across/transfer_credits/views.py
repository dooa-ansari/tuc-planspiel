import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from user.models import UserData


@csrf_exempt
@require_POST
def save_transferred_credits_by_user(request):
     # Get the raw request body
    body = request.body.decode('utf-8')
    try:
        # Parse JSON data from the request body
        data = json.loads(body)
        email = data.get('email','')
        transferCreditsRequest = data.get('transferCreditsRequest','')

        try:
            user_data = UserData.objects.get(email=email)

            # Check for existing transfer_credits_requests
            existing_transfer_requests = user_data.transfer_credits_requests or []

            # Condition to repeatative data not get added
            # (From->To both data checked if any one does not matches it will get added in db)
            if existing_transfer_requests != []:
            
                # Get unique moduleUri values already present in the database
                existing_module_uris = set()
                for existing_request in existing_transfer_requests:
                    existing_module_uris.add(existing_request['fromModule'][0]['moduleUri'])
                    existing_module_uris.add(existing_request['toModule'][0]['moduleUri'])

                # Add only new transfer_credits_requests with previously unseen moduleUri values
                new_requests = []
                for new_request in transferCreditsRequest:
                    if (new_request['fromModule'][0]['moduleUri'] not in existing_module_uris) \
                            or (new_request['toModule'][0]['moduleUri'] not in existing_module_uris):
                        new_requests.append(new_request)
                        
                # Update the transfer_credits_requests field
                user_data.transfer_credits_requests = existing_transfer_requests + new_requests
            else:
                user_data.transfer_credits_requests = transferCreditsRequest

            user_data.save()

            response = {
                'message': 'Successfully Requested for Transferring of your Credits'
            }
            return JsonResponse(response, status =200)
        except UserData.DoesNotExist:
            response = {
                'message': f'User data not found for the specified email:- {email}. Check if you marked your completed modules in your profile section first'
            }
            return JsonResponse(response, status=404)
    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {e}"
        }
        return JsonResponse(response, status =500)


@csrf_exempt
@require_POST
def fetch_transfer_credits_requests_by_user(request):

    body = request.body.decode('utf-8')

    try:
        # Parse JSON data from the request body
        data = json.loads(body)
        email = data.get('email','')

        try:
            user_data = UserData.objects.get(email=email)

            # Use ast.literal_eval to safely evaluate the string as a Python literal
            transfer_credits_requests = user_data.transfer_credits_requests

            user_data = {  
                "transferCreditsRequests" : transfer_credits_requests
            }
            response= {
                'message': 'Successfully returned transfer credit requests of user',
                'user_data' : user_data
            }
            return JsonResponse(response, status =200)
        
        except UserData.DoesNotExist:
            # Handle the case where UserData does not exist for the given email
            response = {
                'message': f'UserData not found for the given email: {email}',
                'user_data': {}
            }
            return JsonResponse(response, status=404)
    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {e}"
        }
        return JsonResponse(response, status =500)

 
