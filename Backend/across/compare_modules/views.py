from adminapp import sparql as sparqlquery
from pymantic import sparql
from .sparql import *
import requests
from django.http import JsonResponse

def create_course_entry_in_rdf(data):
    
    course_name = data.get('courseName','')
    belongs_to_university = data.get('belongsToUniversity','')
    belongs_to_program = data.get('belongsToProgram','')
    belongs_to_department = data.get('belongsToDepartment','')
    has_language = data.get('hasLanguage','')

    course_uri = ''
    server = sparql.SPARQLServer('http://192.168.0.173:9999/blazegraph/sparql')
    query = sparqlquery.get_course_uri_by_course_and_university_name(course_name, belongs_to_university)
    qresponse = server.query(query)
    data_for_course_uri = qresponse['results']['bindings'] 
    for result in data_for_course_uri:
        course_uri = str(result['courseUri']['value'])

    qresponse = server.query(sparqlquery.get_university_uri_by_university_name(belongs_to_university))
    data_for_unviersity_uri = qresponse['results']['bindings'] 
    for result in data_for_unviersity_uri:
        university_uri = str(result['universityUri']['value'])

    if course_uri:  # It means rdf entry for course already exist
        return True
    else:
        course_code = course_name.replace(' ','')
        course_uri = "http://tuc/course#"+course_code

    payload = {'update': add_course(course_uri, course_name, belongs_to_program, belongs_to_department, university_uri,has_language)}
        
    result = requests.post("http://192.168.0.173:9999/blazegraph/namespace/kb/sparql", data=payload)
    
    if result.status_code == 200:
        university_code = university_uri.split('#')[1]
        response_data = {
                        'message': "New Course Entry Created in RDF",
                        'university_name': belongs_to_university,
                        'university_code': university_code,
                        'course_code': course_code
                    }
        return response_data
    else:
        response_data = {
                        'message': "Error occured in creation of new course entry",
                    }
        return JsonResponse(response_data, status=500)