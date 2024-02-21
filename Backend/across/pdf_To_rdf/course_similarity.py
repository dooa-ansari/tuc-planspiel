from pymantic import sparql
from .sparql import *
from os import listdir
from os.path import isfile, join
from django.http import JsonResponse
import json
import difflib

def find_similarity_between_courses(data, rdf_file_name):
    try:
        with open('D:/Web Engineering/SEM-III/Planspiel/ACROSS/ACROSS_MAIN/web-wizards/Backend/across/pdf_To_rdf/courses.json', 'r') as json_file:
            courses_data = json.load(json_file)

        department_name = data['belongs_to_department']
        course_name = data['course_name']
        # Initialize variables to store the best match and its corresponding department
        best_match_count = 0
        best_department = None

        # Iterate through each department in courses_data
        for department_name, department_data in courses_data.items():
            # Extract the keywords for the current department
            department_keywords = department_data.get('keywords', [])

            # Use difflib to find similar keywords for the given course name
            matches = difflib.get_close_matches(course_name, department_keywords, n=5, cutoff=0.6)

            # Update best_match_count and best_department if a better match is found
            if len(matches) > best_match_count:
                best_match_count = len(matches)
                best_department = department_name

        # Means it found matches
        if matches:
            server = sparql.SPARQLServer('http://13.51.109.79/bigdata/sparql')
            qresponse = server.query(get_course_uri_from_departments(department_name))
            courses = qresponse['results']['bindings']
    
            for course in courses_data:
                course_name = str(course['course']['value'])


            courseUri = data['course_uri']
            


            return department_name, True
        else:
            print(f"No similar keywords found for '{course_name}' in '{department_name}'.")
            return department_name, False

    except Exception as e:
        return JsonResponse({'message': f'Error during finding similarities between courses: {str(e)}'}, status=500)
        
        

            
       
            
        read_modules_and_compare(file1, folder_path)

def read_modules_and_compare(givenCourseFile, folder_path):

    only_files_in_folder = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    for file_name in only_files_in_folder:
        univeristyTwoCourseFile = join(folder_path, file_name)