import urllib.request
import ssl
from bs4 import BeautifulSoup
from rdflib import Namespace
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF

NAME_SPACE = Namespace("http://tuc.bialystok/module#")
graph = Graph()
graph.bind("module", NAME_SPACE)

base_url = "https://usos-ects.uci.pb.edu.pl/"
try:
 _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
 pass
else:
     ssl._create_default_https_context = _create_unverified_https_context
    
pages = [0 ,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

for page in pages:
    html = urllib.request.urlopen(f"{base_url}en/courses/list?page={page}")
    data = html.read()
    parser = BeautifulSoup(data, 'html.parser')
    all_list_a = parser.find_all("a")
    module_id_list = []
    for course in all_list_a:
     url = course.get("href")
     if('/en/courses/view?prz_kod=' in url):
        module_id_list.append(url)


    for id_url in module_id_list:
     course_data_html = urllib.request.urlopen(f"{base_url}{id_url}")
     data_courses = course_data_html.read()
     parser_courses = BeautifulSoup(data_courses, 'html.parser')
     module_name = parser_courses.find("h1").findAll(text= True, recursive=False)[1]
     module_id = parser_courses.find_all("span", class_="note")[1].getText()
     module_content = parser_courses.find("div", class_="opis iml").getText()
     credit_points = parser_courses.find("div", class_="item punkty_ects")
     department = parser_courses.find("div", class_="item jednostka").find("a").getText()
     credit_points_value = credit_points.getText()

     uri_end = ''.join(e for e in module_id if e.isalnum())
     module_uri_g = URIRef(f"{NAME_SPACE}{uri_end}")
     
     module_name_g = Literal(module_name, datatype=URIRef('http://www.w3.org/2001/XMLSchema#string'))
     module_content_g = Literal(module_content, datatype=URIRef('http://www.w3.org/2001/XMLSchema#string'))
     module_id_g = Literal(module_id, datatype=URIRef('http://www.w3.org/2001/XMLSchema#string'))
     credit_points_g = Literal(credit_points_value, datatype=URIRef('http://www.w3.org/2001/XMLSchema#integer'))
     department_g = Literal(department, datatype=URIRef('http://www.w3.org/2001/XMLSchema#string'))
     
     graph.add((module_uri_g, RDF.type, NAME_SPACE))
     graph.add((module_uri_g, "http://tuc.bialystok/module#hasName", module_name_g))
     graph.add((module_uri_g, "http://tuc.bialystok/module#hasModuleNumber", module_id_g))
     graph.add((module_uri_g, "http://tuc.bialystok/module#hasContent", module_content_g))
     graph.add((module_uri_g, "http://tuc.bialystok/module#hasCreditPoints", credit_points_g))
     



html.close()

    # print(mystr)