from django.shortcuts import render
from pymantic import sparql
from .sparql import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET


@csrf_exempt
@require_GET
def get_universities(request):
    try:
        server = sparql.SPARQLServer('http://54.242.11.117:80/bigdata/sparql')
        qresponse = server.query(get_university_list())
        universiy_list = []
        universiy_list = [result['universityName']['value'] for result in qresponse['results']['bindings']]

        # Return JSON response
        if not universiy_list:
            response = {
                "message": f"No Universities found"
            }
            return JsonResponse(response, status =404)
        else:
            response = {
                "message": "University list returned successfully",
                "universities": universiy_list
            }
            return JsonResponse(response, status =200)
    except Exception as e:
        response = {
            "message": f"An unexpected error occurred: {e}"
        }
        return JsonResponse(response, status =500)

