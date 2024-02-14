import os
import pdfplumber
import re
import json
import uuid
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.plugins.sparql import prepareQuery
from django.conf import settings

DATA_PATH = os.path.join(settings.BASE_DIR, 'RDF_DATA')

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
    pdfstring = PdfString('Anlage 2:','Modulnummer','Modulname', 'Inhalte und Qualifikationsziele', 'Leistungspunkte und Noten', 'Arbeitsaufwand', 'Sprache')
    if university == 'TUC':
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
        rdfUri = RdfUri('http://tuc.web.engineering/module#', 
                        'http://tuc/course#', 
                        'http://across/university#TUC', 
                        'http://tuc/web/engineering/module#',
                        'http://www.w3.org/2001/XMLSchema#string', 
                        'http://www.w3.org/2001/XMLSchema#integer')
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


def extract_text_from_pdf_bu(pdf_path, end_page=None):
    results = {}
    with pdfplumber.open(pdf_path) as pdf_file: 
        pages = pdf_file.pages
        length = len(pages)
        # Ensure end_page is not greater than the total number of pages
        if end_page is None or end_page > length:
            end_page = length
            result = {}
            for page in pages:
                table = page.extract_table()
                for row in table:
                    filtered_list = [item for item in row if item is not None]
                    rowStr = str(filtered_list)
                    print(rowStr)
                    coursePattern = r"'Field of study',\s*'([^']*)',\s*'.*?Degree level and\\nprogramme type',"
                    courseMatch = re.search(coursePattern, rowStr)
                    if courseMatch:
                        course = courseMatch.group(1)
                        if course not in results:
                            results[course] = result                   
                    if 'Course content' in rowStr:
                        pattern = r"'Course content',\s*'([^']*)'"
                        match = re.search(pattern, rowStr)
                        if match:
                            contents = match.group(1).strip().replace('\\n', ' ')
                            result['Inhalte und Qualifikationsziele'] = ' '.join(contents.split())
                    if 'Course code' in rowStr:
                        pattern = r"'Course code',\s*'([^']*)'"
                        match = re.search(pattern, rowStr)
                        if match:
                            result['Modulnummer'] = match.group(1).strip().replace(' ', '')
    
                    if 'No. of ECTS credits' in rowStr:
                        pattern = r"'No\. of ECTS credits',\s*'([^']*)'"
                        match = re.search(pattern, rowStr)
                        if match:
                            result['Leistungspunkte und Noten'] = match.group(1)
                            result['Arbeitsaufwand'] = int(match.group(1)) * 28
    return results
        


extract_text_from_pdf_bu("C:/Users/User/OneDrive/Desktop/source/pdf/Introduction_to_Machine_Audition.pdf", None)

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
            moduleDict = extract_text_from_pdf(pdf_path, uniData)
            result_list = get_results(moduleDict, uniData)
            json_data = write_json(course_status, rdf_file_name,result_list)
            # Load JSON data
            write_rdf(json.loads(json_data), course_status, rdf_file_name, uniData)

def write_json(course_status, rdf_file_name, result_list) :
      output_json_path = os.path.join(DATA_PATH, f'{course_status["university_name"]}',  f'{rdf_file_name}.json')
      with open(output_json_path, "w", encoding="utf-8") as json_file:
        json_data = json.dumps(result_list, indent=2, ensure_ascii=False)
        json_file.write(json_data)
        print(f"JSON data has been written to {output_json_path}")
        return json_data

 
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