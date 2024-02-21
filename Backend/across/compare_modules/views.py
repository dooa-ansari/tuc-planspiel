from adminapp import sparql as sparqlquery
from pymantic import sparql
from .sparql import *
import requests
from django.http import JsonResponse
import shortuuid
import re

def create_course_entry_in_rdf(data):
    
    course_name = data.get('courseName','')
    belongs_to_university = data.get('belongsToUniversity','')
    belongs_to_program = data.get('belongsToProgram','')
    belongs_to_department = data.get('belongsToDepartment','')
    has_language = data.get('hasLanguage','')

    course_uri = ''
    university_uri=''
    server = sparql.SPARQLServer('http://13.51.109.79/bigdata/sparql')

    # Generate a short UUID
    short_uuid = shortuuid.uuid()
    # Remove alphabets from the short UUID
    uuid_numeric_only = re.sub(r'[^0-9]', '', short_uuid)
    # Getting University URI
    qresponse = server.query(sparqlquery.get_university_uri_by_university_name(belongs_to_university))
    data_for_unviersity_uri = qresponse['results']['bindings'] 
    for result in data_for_unviersity_uri:
        university_uri = str(result['universityUri']['value'])
    university_code = university_uri.split('#')[1]

    # Validating Course URI does it already exist or not
    query = sparqlquery.get_course_uri_by_course_and_university_name(course_name, belongs_to_university)
    qresponse = server.query(query)
    data_for_course_uri = qresponse['results']['bindings'] 
    for result in data_for_course_uri:
        course_uri = str(result['courseUri']['value'])
    
    if course_uri:                              # It means rdf entry for course already exist
        course_code = course_uri.split('#')[1]
        response_data = {
                        'message': "Given Course already exist, starting comparing with existing course",
                        'university_name': belongs_to_university,
                        'university_code': university_code,
                        'course_code': course_code,
                        'status': True
                    }
        return response_data
    else:
        course_code = course_name.replace(' ','')
        course_uri = "http://tuc/course#"+course_code

    payload = {'update': add_course(uuid_numeric_only, course_uri, course_name, belongs_to_program, belongs_to_department, university_uri,has_language)}
        
    # result = requests.post("http://13.51.109.79/bigdata/namespace/kb/sparql", data=payload)
    
    if 1:
        response_data = {
                        'message': "New Course Entry Created in RDF",
                        'university_name': belongs_to_university,
                        'university_code': university_code,
                        'course_code': course_code,
                        'belongs_to_department': belongs_to_department,
                        'course_name': course_name,
                        'course_uri': course_uri,
                        'status': False
                    }
        return response_data
    else:
        response_data = {
                        'message': "Error occured in creation of new course entry",
                    }
        return response_data