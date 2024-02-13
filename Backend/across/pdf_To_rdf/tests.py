import os
import pdfplumber
import re
import json
import uuid
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.plugins.sparql import prepareQuery
from django.conf import settings

DATA_PATH = os.path.join(settings.BASE_DIR, 'RDF_DATA')
field_of_study_pattern = re.compile(r'(?<=Faculty of )(.*?)(?= Field of study)')
field_of_study_pattern_v2 = re.compile(r'(?<=Field of study )(.*?)(?= Degree level)')
programme_type_pattern = re.compile(r'(?<=and programme type)(.*?)(?= Specialization/)')
course_name_pattern = re.compile(r'(?<=Course name)(.*?)(?= Course code)')
course_code_pattern = re.compile(r'(?<=Course code)(.*?)(?= Course type)')
course_code_pattern_2 = re.compile(r'(?<=L1P_U06)(.*?)(?= LO4)')
ects_pattern = re.compile(r'(?<=No. of ECTS credits)(.*?)(?= Entry)')
credit_hours_pattern = re.compile(r'(?<=TOTAL:)(.*?)(?= Quantitative)')
content_pattern = re.compile(r'(?<=Course content)(.*?)(?=Teaching methods)')

CIVIL_EARTH_SCIENCES_V1 = "Civil Engineering and Environmental Sciences"
CIVIL_EARTH_SCIENCES_V2 = "Civil Engineering and Envir onmental Sciences"
CIVIL_EARTH_SCIENCES_V3 = "Civil and Environmental Science"
CIVIL_EARTH_SCIENCES_V4 = "Civil Engineering and Environmental Science"
CIVIL_EARTH_SCIENCES_V5 = "Civil and Environmental Sciences"
ENGINEERING_MANAGEMENT_V2 = "Engineering Managment"
ENGINEERING_MANAGEMENT_V1 = "Engineering Management"
ENGINEERING_MANAGEMENT_V3 = "Faculty of Engineering Management"
MECHINICAL_ENGINEERING_V1 = "Mechanical Engineering"
MECHINICAL_ENGINEERING_V2 = "Faculty of Mechanical Engineering"
COMPUTER_SCIENCE = "Computer Science"
ARCHITECTURE = "Architecture"
BIOMEDICAL_ENGINEERING = "Biomedical Engineering"
CIVIL_ENGINEERING = "Civil and Earth Sciences"
ELECTRICAL_ENGINEERING = "Electrical Engineering"
special_case_modules = {'Forest pathology': "IS-FF-00036S",'Computer modeling of water supply and sewage systems': "IS-FCEE-00133W", 'Forest hydrology': "IS-FF-00011W", 'Chemistry': "IS-FF-00001W", 'Invasive species in forest areas': "S-FF-00042W/S", 'Forest mushrooms in medicine': "IS-FF-00043S", 'Heating systems': "FCEE-00077W", 'Water management and water protection': "IS-FCEE-00134W", 'Forest protection': "IS-FF-00037S", 'Air conditioning and ventilation systems 2': "FCEE-00108W", 'Forest management in valuable natural areas': "IS-FF-00041W/S", 'Natural medicinal substances m forest materialsfro': "IS-FF-00044S", 'Air conditioning and Ventilation systems 1': "FCEE-00107W", 'Technology and organization of sanitary works': "IS-FCEE-00213W", 'Biodiversity conservation of forest areas': "IS-FF-00038-1W/S", 'Forest botany: Dendrology': "IS-FF-00032W/S", 'Forest applied botany': "IS-FF-00025W/S" , 'Heat centers': "FCEE-00143W"}
departments = set()

# langDict = {'German': 'deutscher', 'English': 'englischer'}

class RdfUri:
    def __init__(self, module, course, uni, tuc_module, datatype_string, datatype_integer):
        self.module = module
        self.course = course
        self.uni=uni
        self.tuc_module = tuc_module
        self.datatype_string = datatype_string
        self.datatype_integer = datatype_integer

class PdfString():   
    def __init__(self, start_txt, module_number, module_name, module_content, grades, workload, language):
            self.start_txt = start_txt
            self.module_number = module_number
            self.module_name = module_name
            self.module_content = module_content
            self.grades = grades
            self.workload = workload
            self.language = language

class RePattern:
    def __init__(self, module_number_pattern, module_name_pattern, contents_pattern, teaching_language_pattern, credit_points_pattern, work_load_pattern):
        self.module_number_pattern = module_number_pattern
        self.module_name_pattern = module_name_pattern
        self.contents_pattern = contents_pattern
        self.teaching_language_pattern = teaching_language_pattern
        self.credit_points_pattern = credit_points_pattern
        self.work_load_pattern = work_load_pattern

class UniData():
    def __init__(self, uniName,  pdfString, rePattern, rdfUri, cources, course_status):
        self.uniName = uniName
        self.pdfString = pdfString
        self.rePattern = rePattern
        self.rdfUri = rdfUri
        self.cources = cources
        self.course_status = course_status

def get_cources():
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

def get_uniData(university):
    if university == 'TUC':
        pdfstring = PdfString('Anlage 2:','Modulnummer','Modulname', 'Inhalte und Qualifikationsziele', 'Leistungspunkte und Noten', 'Arbeitsaufwand', 'Sprache')
        # Regular expressions to extract information
        module_number_pattern = re.compile(r'\nModulnummer\s+(.*?)\n', re.IGNORECASE | re.DOTALL)
        module_name_pattern = re.compile(r"Modulname\s*(.+)")
        contents_pattern = re.compile(r'Inhalte:(.*?)(?=\nQualifikationsziele:|$)', re.DOTALL)
        teaching_language_pattern = re.compile(r'\nLehrformen\s+(.*?)\nVoraussetzungen für', re.IGNORECASE | re.DOTALL)
        credit_points_pattern = re.compile(r'\nLeistungspunkte und.*?(\d+)', re.DOTALL)
        work_load_pattern = re.compile(r'\nArbeitsaufwand.*?(\d+)(?=\s*AS|\s*\()', re.DOTALL)
        rePattern = RePattern(module_number_pattern,
                             module_name_pattern, 
                             contents_pattern, 
                             teaching_language_pattern, 
                             credit_points_pattern,
                             work_load_pattern)
        rdfUri = RdfUri('http://tuc.web.engineering/module#', 'http://tuc/course#', 'http://across/university#TUC', 'http://tuc/web/engineering/module#', 'http://www.w3.org/2001/XMLSchema#string', 'http://www.w3.org/2001/XMLSchema#integer')
        return UniData(pdfstring, rePattern, rdfUri, get_cources())
    else:
        pdfstring = PdfString('Anlage 2:','Modulnummer','Modulname', 'Inhalte und Qualifikationsziele', 'Leistungspunkte und Noten', 'Arbeitsaufwand', 'Sprache')
        # Regular expressions to extract information
        module_number_pattern = re.compile(r'\nModulnummer\s+(.*?)\n', re.IGNORECASE | re.DOTALL)
        module_name_pattern = re.compile(r"Modulname\s*(.+)")
        contents_pattern = re.compile(r'(?<=Course content)(.*?)(?=Teaching methods)')
        teaching_language_pattern = re.compile(r'\nLehrformen\s+(.*?)\nVoraussetzungen für', re.IGNORECASE | re.DOTALL)
        credit_points_pattern = re.compile(r'(?<=No. of ECTS credits)(.*?)(?= Entry)')
        work_load_pattern = re.compile(r'\nArbeitsaufwand.*?(\d+)(?=\s*AS|\s*\()', re.DOTALL)
        rePattern = RePattern(module_number_pattern,
                             module_name_pattern, 
                             contents_pattern, 
                             teaching_language_pattern, 
                             credit_points_pattern,
                             work_load_pattern)
        rdfUri = RdfUri('http://tuc.web.engineering/module#', 'http://tuc/course#', 'http://across/university#TUC', 'http://tuc/web/engineering/module#', 'http://www.w3.org/2001/XMLSchema#string', 'http://www.w3.org/2001/XMLSchema#integer')
        return UniData(pdfstring, rePattern, rdfUri, get_cources())

## This code will convert pdf data to dictionary
def extract_text_from_pdf(pdf_path, uniData, end_page=None):
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
                if uniData.pdfString.modul_number in text:
                    match = uniData.pdfString.module_number_pattern.search(text)
                    modulnummer = match.group(1).replace(' ', '')
                    moduleDict[modulnummer] = text
                else:
                     moduleDict[modulnummer] +=text
            return moduleDict

def extract_text_from_pdf_bu(pdf_path, uniData, end_page=None):
    with pdfplumber.open(pdf_path) as pdf_file: 
        pages = pdf_file.pages
        length = len(pages)
        result_list = []
        # Ensure end_page is not greater than the total number of pages
        if end_page is None or end_page > length:
            end_page = length
            for page in pages:
                text = page.extract_text()
                text = " ".join(text.split())
                print(text)
                result_list.append(extract_information_bu(uniData, text))
   
def get_reqd_pages(pages, uniData):
     listofPage = []
     isStartPage = False
     for eachPage in pages:
        text = eachPage.extract_text()
        if uniData.pdfString.start_text in text and uniData.pdfString.module_number in text and uniData.pdfString.module_name in text:
            isStartPage = True
        if isStartPage:
            listofPage.append(eachPage)
     return listofPage

# Function to extract information from a page
def extract_information_tuc(values, uniData):
    result ={}
    # Extract Module Name
    match_module_name = uniData.rePattern.module_name_pattern.search(values)
    if match_module_name:
        result[uniData.pdfString.module_name] = match_module_name.group(1).strip()

    # Extract Contents
    match_contents = uniData.rePattern.contents_pattern.search(values)
    if match_contents:
        contents = match_contents.group(1)
        # Remove unwanted characters
        contents = contents.replace('Qualifikationsziele', '').replace('tionsziele', '').replace('ziele', '').strip().replace('\n', ' ')
        result[uniData.pdfString.module_content] =' '.join(contents.split())

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
    match_credit_points = uniData.rePattern.credit_points_pattern.search(values)
    if match_credit_points:
        result[uniData.pdfString.grades] = match_credit_points.group(1).strip()
    
    # Extract Workload
    match_work_load = uniData.rePattern.work_load_pattern.search(values)
    if match_work_load:
        result[uniData.pdfString.workload] = match_work_load.group(1).strip()
    return result

def extract_information_bu(uniData, text):
    field_of_study = field_of_study_pattern.search(text)
    field_of_study_v2 = field_of_study_pattern_v2.search(text)
    programme_type = programme_type_pattern.search(text)
    course_name = course_name_pattern.search(text)
    course_code = course_code_pattern.search(text)
    ects = ects_pattern.search(text)
    hours = credit_hours_pattern.search(text)
    content = content_pattern.search(text)

    field_of_study_v = ""
    programme_type_v = ""
    course_name_v = ""
    course_code_v = ""
    ects_v = ""
    hours_v = ""
    content_v = ""

    result ={}
    if course_code:
        course_code_v = course_code.group(1).strip()
        if course_code_v == "":
            print(course_name_v)
            value = special_case_modules.get(course_name_v)
            if value:
                result[uniData.pdfString.module_number] = ''.join(e for e in value if e.isalnum())
                print(course_code_v)

    if course_name:
        result[uniData.pdfString.module_name] = course_name.group(1).strip()
    else:
        print("No match found for course name.")

    if content:
        result[uniData.pdfString.module_content] = content.group().strip()
    else:
        print("No match found for content")
    
    if ects:
        ects_v = ects.group(1).strip()
        result[uniData.pdfString.grades] = ects_v
    else:
        print("No match found for ects")
    
    if hours:
        hours_v = hours.group(1).strip()
        if hours_v == "": 
            if ects_v:
                to_int = int(ects_v)
                if(to_int):
                    result[uniData.pdfString.workload] = to_int * 28

    else:
        if ects_v:
                to_int = int(ects_v)
                if(to_int):
                    result[uniData.pdfString.workload] = to_int * 28

    if field_of_study:
        field_of_study_v = field_of_study.group(1).strip()
        print(field_of_study)
        if field_of_study_v:
            if field_of_study_v == CIVIL_EARTH_SCIENCES_V1 or field_of_study_v == CIVIL_EARTH_SCIENCES_V2 or field_of_study_v == CIVIL_EARTH_SCIENCES_V3 or field_of_study_v == CIVIL_EARTH_SCIENCES_V4 or field_of_study_v == CIVIL_EARTH_SCIENCES_V5:
             departments.add(CIVIL_EARTH_SCIENCES_V1)
            elif field_of_study_v == ENGINEERING_MANAGEMENT_V1 or field_of_study_v == ENGINEERING_MANAGEMENT_V2 or field_of_study_v == ENGINEERING_MANAGEMENT_V3:
             departments.add(ENGINEERING_MANAGEMENT_V1) 
            elif field_of_study_v == MECHINICAL_ENGINEERING_V1 or field_of_study_v == MECHINICAL_ENGINEERING_V2:
             departments.add(MECHINICAL_ENGINEERING_V1)  
            else:
             departments.add(field_of_study_v)
        else :
           field_of_study_v = field_of_study_v2.group(1).strip()

    else:
        if field_of_study_v2:
           field_of_study_v = field_of_study_v2.group(1).strip()
           departments.add(field_of_study_v)
           print(field_of_study_v)
    return result
    
def get_results(moduleDict, uniData):
    result_list = []
    for key, value in moduleDict.items():
      result_list.append(extract_information_tuc(key, value, uniData))  
    return result_list

# Convert the list of dictionaries to JSON
def write_json_rdf(pdf_path, course_status, rdf_file_name, uniData):
    # course_Name =  get_course_name(moduleDict)
    # course_Name= course_Name.replace(' ', '')
    # Write JSON data to a separate file
    output_json_path = os.path.join(DATA_PATH, f'{course_status["university_name"]}',  f'{rdf_file_name}.json')
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json_data = ''
        if uniData.uniName == 'TUC' :
            # Extract text from the PDF
            moduleDict = extract_text_from_pdf(pdf_path, uniData)
            result_list = get_results(moduleDict, uniData)
        else:
            result_list = extract_text_from_pdf_bu(pdf_path, uniData)
            json_data = json.dumps(result_list, indent=2, ensure_ascii=False)
        json_data = json.dumps(result_list, indent=2, ensure_ascii=False)
        json_file.write(json_data)
        print(f"JSON data has been written to {output_json_path}")
        # Load JSON data
        write_rdf(json.loads(json_data), course_status, rdf_file_name)
 
def write_rdf(data, course_status, rdf_file_name, uniData):
    # RDF Namespace
    module_ns = URIRef(uniData.rdfUri.uri_module)
    # Create RDF graph
    g = Graph()
    # Iterate over each module in the JSON data
    for module in data:
        module_number = module.get(uniData.pdfString.module_number, "")
        module_name = module.get(uniData.pdfString.module_name, "")
        content = module.get(uniData.pdfString.module_content, "").replace("•","")
        langs = module.get(uniData.pdfString.language, "")
        credit_points = module.get(uniData.pdfString.grades, "")
        work_load = module.get(uniData.pdfString.workload, "")
        # Generate a UUID based on the current timestamp and node (hardware address)
        module_uuid = uuid.uuid1()

        # Convert the UUID to a string
        module_uuid_str = str(module_uuid)
        # RDF URI for the module
        module_uri = URIRef(f'{uniData.rdfUri.module}{module_uuid_str}')

        # Add RDF triples for the module
        g.add((module_uri, RDF.type, module_ns))
        g.add((module_uri, URIRef(f'{uniData.rdfUri.module}hasModuleNumber'), Literal(module_number, datatype=uniData.rdfUri.datatype_string)))
        g.add((module_uri, URIRef(f'{uniData.rdfUri.module}hasName'), Literal(module_name, datatype=uniData.rdfUri.datatype_string)))
        g.add((module_uri, URIRef(f'{uniData.rdfUri.module}hasContent'), Literal(content, datatype=uniData.rdfUri.datatype_string)))
        
        # for lang in langs:
        #     g.add((module_uri, URIRef(f'{URI_MODULE}hasLanguage'), Literal(lang, datatype=DATATYPE_STRING)))
   
        # Check if credit_points is non-empty before converting to integer
        if credit_points:
            try:
                credit_points_value = int(credit_points)
                g.add((module_uri, URIRef(f'{uniData.rdfUri.module}hasCreditPoints'), Literal(credit_points_value, datatype=uniData.rdfUri.datatype_integer)))
            except ValueError as ve:
                print(f"Error converting credit_points to integer for module {module_name}: {ve}")

        # Check if work_load is non-empty before converting to integer
        if work_load:
            try:
                work_load_value = int(work_load)
                g.add((module_uri, URIRef(f'{uniData.rdfUri.module}hasWorkLoad'), Literal(work_load_value, datatype=uniData.rdfUri.datatype_integer)))
            except ValueError as ve:
                print(f"Error converting work_load to integer for module {module_name}: {ve}")

        # Add additional RDF triples for each module
        g.add((module_uri, URIRef(f'{uniData.rdfUri.tuc_module}hasUniversity'), URIRef(uniData.rdfUri.uni)))
        # single quotes are giving an error in 3.12 python
        g.add((module_uri, URIRef(f'{uniData.rdfUri.course}hasCourse'), URIRef(f'{uniData.rdfUri.course}{course_status["course_code"]}')))

    # Serialize RDF graph to RDF/XML format
    rdf_outputBytes = (g.serialize(format="xml")).encode('utf-8')
    
    # Save RDF data to a file with proper encoding
    output_rdf_path = os.path.join(DATA_PATH, f'{course_status["university_name"]}',  f'{rdf_file_name}.rdf')

    with open(output_rdf_path, "wb") as rdf_file:
        rdf_file.write(rdf_outputBytes)
        print(f"RDF data has been saved to {output_rdf_path}")