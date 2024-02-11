import os
import pdfplumber
import re
import json
import uuid
import tempfile
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.plugins.sparql import prepareQuery
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from compare_modules.views import create_course_entry_in_rdf

START_TEXT = 'Anlage 2:'
MODULE_NUMBER = 'Modulnummer'
MODULE_NAME = 'Modulname'
MODULE_CONTENT='Inhalte und Qualifikationsziele'
GRADES = 'Leistungspunkte und Noten'
WORKLOAD = 'Arbeitsaufwand'
LANGUAGE = 'Sprache'
URI_MODULE = 'http://tuc.web.engineering/module#'
URI_COURSE = 'http://tuc/course#'
URI_UNI ='http://across/university#TUC'
URI_TUC_MODULE = 'http://tuc/web/engineering/module#'
DATATYPE_STRING = 'http://www.w3.org/2001/XMLSchema#string'
DATATYPE_INTEGER = 'http://www.w3.org/2001/XMLSchema#integer'
DATA_PATH = os.path.join(settings.BASE_DIR, 'RDF_DATA')

# Regular expressions to extract information
module_number_pattern = re.compile(r'\nModulnummer\s+(.*?)\n', re.IGNORECASE | re.DOTALL)
module_name_pattern = re.compile(r"Modulname\s*(.+)")
contents_pattern = re.compile(r'Inhalte:(.*?)(?=\nQualifikationsziele:|$)', re.DOTALL)
teaching_language_pattern = re.compile(r'\nLehrformen\s+(.*?)\nVoraussetzungen für', re.IGNORECASE | re.DOTALL)
credit_points_pattern = re.compile(r'\nLeistungspunkte und.*?(\d+)', re.DOTALL)
work_load_pattern = re.compile(r'\nArbeitsaufwand.*?(\d+)(?=\s*AS|\s*\()', re.DOTALL)

# langDict = {'German': 'deutscher', 'English': 'englischer'}

courses = []
g = Graph()
course_path = os.path.join(DATA_PATH, 'tuc_courses.rdf')
g.parse(course_path)
# Define the SPARQL query
query = prepareQuery(
    """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX course: <http://tuc/course#>

    SELECT ?hasCourseName
    WHERE {
      ?course rdf:type course: .
      ?course course:hasCourseName ?hasCourseName .
    }
    """)
# Execute the query and print the results
for row in g.query(query):
    courses.append(row['hasCourseName'].value)

## This code will convert pdf data to dictionary
def extract_text_from_pdf(pdf_path, end_page=None):
    with pdfplumber.open(pdf_path) as pdf_file: 
        pages = pdf_file.pages
        length = len(pages)
        # Ensure end_page is not greater than the total number of pages
        if end_page is None or end_page > length:
            end_page = length
            listofPage = get_reqd_pages(pages)
            moduleDict = {}
            for page in listofPage:
                text = page.extract_text()
                if MODULE_NUMBER in text:
                    match = module_number_pattern.search(text)
                    modulnummer = match.group(1).replace(' ', '')
                    moduleDict[modulnummer] = text
                else:
                     moduleDict[modulnummer] +=text
            return moduleDict
        
def get_reqd_pages(pages):
     listofPage = []
     isStartPage = False
     for eachPage in pages:
        text = eachPage.extract_text()
        if START_TEXT in text and MODULE_NUMBER in text and MODULE_NAME in text:
            isStartPage = True
        if isStartPage:
            listofPage.append(eachPage)
     return listofPage

# Function to extract information from a page
def extract_information(key, values):
    result ={}
    result[MODULE_NUMBER] = key

    # Extract Module Name
    match_module_name = module_name_pattern.search(values)
    if match_module_name:
        result[MODULE_NAME] = match_module_name.group(1).strip()

    # Extract Contents
    match_contents = contents_pattern.search(values)
    if match_contents:
        contents = match_contents.group(1)
        # Remove unwanted characters
        contents = contents.replace('Qualifikationsziele', '').replace('tionsziele', '').replace('ziele', '').strip().replace('\n', ' ')
        result[MODULE_CONTENT] =' '.join(contents.split())

    # #Extract Languages
    # match_lang =teaching_language_pattern.search(values)
    # if match_lang:
    #     contents = match_lang.group(1)
    #     if 'auch in englischer' in contents or 'deutscher oder in englischer' in contents:
    #          result[LANGUAGE] = ['German', 'English']
    #     elif 'Sprache' in contents:
    #             pattern = r'(\S+)\s+Sprache'
    #             # Find all matches of the pattern in the input text
    #             matches = re.findall(pattern, contents)
    #             if matches:
    #                  for key, value in langDict.items():
    #                      if value in matches[0]:
    #                          result[LANGUAGE] = [key]

    # if LANGUAGE not in result:
    #      result[LANGUAGE] = ['German'] # take German as default langugae
        
    # Extract Credit Points
    match_credit_points = credit_points_pattern.search(values)
    if match_credit_points:
        result[GRADES] = match_credit_points.group(1).strip()
    
       # Extract Workload
    match_work_load = work_load_pattern.search(values)
    if match_work_load:
        result[WORKLOAD] = match_work_load.group(1).strip()

    return result

def get_results(moduleDict):
    result_list = []
    for key, value in moduleDict.items():
      result_list.append(extract_information(key, value))  
    return result_list

def get_course_name(moduleDict):
    if moduleDict:  # Checking if moduleDict is not empty
        firstPage = next(iter(moduleDict.values()))  # Get the first value from moduleDict
        for courseName in courses:
            index = firstPage.find(courseName)
            if index != -1:
                return courseName
        if courseName:
            print("Course name could not be found.")

# Convert the list of dictionaries to JSON
def write_json_rdf(pdf_path, course_status, rdf_file_name):
    # Extract text from the PDF
    moduleDict = extract_text_from_pdf(pdf_path)
    # course_Name =  get_course_name(moduleDict)
    # course_Name= course_Name.replace(' ', '')
    result_list = get_results(moduleDict)
    json_data = json.dumps(result_list, indent=2, ensure_ascii=False)
    # Write JSON data to a separate file
    output_json_path = os.path.join(DATA_PATH, f'{course_status["university_name"]}',  f'{rdf_file_name}.json')
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json_file.write(json_data)
        print(f"JSON data has been written to {output_json_path}")
        # Load JSON data
        write_rdf(json.loads(json_data), course_status, rdf_file_name)

def write_rdf(data, course_status, rdf_file_name):
    # RDF Namespace
    module_ns = URIRef(URI_MODULE)
    # Create RDF graph
    g = Graph()
    # Iterate over each module in the JSON data
    for module in data:
        module_number = module.get(MODULE_NUMBER, "")
        module_name = module.get(MODULE_NAME, "")
        content = module.get(MODULE_CONTENT, "").replace("•","")
        langs = module.get(LANGUAGE, "")
        credit_points = module.get(GRADES, "")
        work_load = module.get(WORKLOAD, "")
        # Generate a UUID based on the current timestamp and node (hardware address)
        module_uuid = uuid.uuid1()

        # Convert the UUID to a string
        module_uuid_str = str(module_uuid)
        # RDF URI for the module
        module_uri = URIRef(f'{URI_MODULE}{module_uuid_str}')

        # Add RDF triples for the module
        g.add((module_uri, RDF.type, module_ns))
        g.add((module_uri, URIRef(f'{URI_MODULE}hasModuleNumber'), Literal(module_number, datatype=DATATYPE_STRING)))
        g.add((module_uri, URIRef(f'{URI_MODULE}hasName'), Literal(module_name, datatype=DATATYPE_STRING)))
        g.add((module_uri, URIRef(f'{URI_MODULE}hasContent'), Literal(content, datatype=DATATYPE_STRING)))
        
        # for lang in langs:
        #     g.add((module_uri, URIRef(f'{URI_MODULE}hasLanguage'), Literal(lang, datatype=DATATYPE_STRING)))
   
        # Check if credit_points is non-empty before converting to integer
        if credit_points:
            try:
                credit_points_value = int(credit_points)
                g.add((module_uri, URIRef(f'{URI_MODULE}hasCreditPoints'), Literal(credit_points_value, datatype=DATATYPE_INTEGER)))
            except ValueError as ve:
                print(f"Error converting credit_points to integer for module {module_name}: {ve}")

        # Check if work_load is non-empty before converting to integer
        if work_load:
            try:
                work_load_value = int(work_load)
                g.add((module_uri, URIRef(f'{URI_MODULE}hasWorkLoad'), Literal(work_load_value, datatype=DATATYPE_INTEGER)))
            except ValueError as ve:
                print(f"Error converting work_load to integer for module {module_name}: {ve}")

        # Add additional RDF triples for each module
        g.add((module_uri, URIRef(f'{URI_TUC_MODULE}hasUniversity'), URIRef(URI_UNI)))
        # single quotes are giving an error in 3.12 python
        g.add((module_uri, URIRef(f'{URI_COURSE}hasCourse'), URIRef(f'{URI_COURSE}{course_status["course_code"]}')))

    # Serialize RDF graph to RDF/XML format
    rdf_outputBytes = (g.serialize(format="xml")).encode('utf-8')
    
    # Save RDF data to a file with proper encoding
    output_rdf_path = os.path.join(DATA_PATH, f'{course_status["university_name"]}',  f'{rdf_file_name}.rdf')

    with open(output_rdf_path, "wb") as rdf_file:
        rdf_file.write(rdf_outputBytes)
        print(f"RDF data has been saved to {output_rdf_path}")

@csrf_exempt
@require_POST
def pdfToRdf(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.POST.get('jsonData'))
        uploaded_files = request.FILES.getlist('files')
        # This will Make New Entry of Course in RDF of courses.rdf
        course_status = create_course_entry_in_rdf(data)
        
        rdf_file_name = course_status["university_code"]+'_'+course_status["course_code"]
        
        # Create a temporary directory to save the files
        temp_dir = tempfile.mkdtemp()
        
        # List to store the paths of saved files
        saved_file_paths = []        
        # This conditions states that course already exist and it will take existing course for comaparison
        if course_status['status'] == True:
            response_data = {
                        'message': course_status['message'],
                        'university_name': course_status['university_name'],
                        'rdf_File_Path': rdf_file_name
                    }
            return JsonResponse(response_data, status=200)
        else: # This follows that course doesn't exist and it will create new course in courses.rdf
            for uploaded_file in uploaded_files:
                # Construct the file path where the file will be saved in the temporary directory
                file_path = os.path.join(temp_dir, uploaded_file.name)
                # If the file is stored in memory, read its content and write it to a file
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.read())
                    saved_file_paths.append(file_path)
                    write_json_rdf(file_path, course_status, rdf_file_name)

            return JsonResponse({'message': f'PDF file(s) is sucessfully converted to RDF file(s).'}, status=200)
    except Exception as e:
        return JsonResponse({'message': f'Error uploading and saving files: {str(e)}'}, status=500)
    finally:
        for file_path in saved_file_paths:
            os.remove(file_path)
        os.rmdir(temp_dir)
        print('End')
