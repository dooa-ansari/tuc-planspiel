import urllib.request
import ssl
from bs4 import BeautifulSoup
from rdflib import Namespace
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF, XSD

graph = Graph()
namespace_manager = graph.namespace_manager
uri_main = "http://tuc.bialystok/module#"
ns_module = Namespace(uri_main)

prefix = "module"
namespace_manager.bind(prefix, ns_module)

base_url = "https://usos-ects.uci.pb.edu.pl/"
try:
 _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
 pass
else:
     ssl._create_default_https_context = _create_unverified_https_context
    
# pages = [0 ,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
pages = [0]

for page in pages:
    html = urllib.request.urlopen(f"{base_url}en/courses/list?page={page}")
    data = html.read()
    parser = BeautifulSoup(data, 'html.parser')
    all_list_a = parser.find_all("a")
    module_id_list = []
    for course in all_list_a:
    #  print("connecting: "+str(page))
     url = course.get("href")
     if('/en/courses/view?prz_kod=' in url):
        module_id_list.append(url)

    count = 0
    for id_url in module_id_list:
    #  print("processing"+id_url)
     course_data_html = urllib.request.urlopen(f"{base_url}{id_url}")
     data_courses = course_data_html.read()
     parser_courses = BeautifulSoup(data_courses, 'html.parser')
     module_name = parser_courses.find("h1").findAll(text= True, recursive=False)[1]
     module_id = parser_courses.find_all("span", class_="note")[1].getText() if len(parser_courses.find_all("span", class_="note")) > 2 else "None"
     module_content = parser_courses.find("div", class_="opis iml").getText()
     credit_points = parser_courses.find("div", class_="item punkty_ects")
     department = parser_courses.find("div", class_="item jednostka").find("a").getText()
     credit_points_value = credit_points.getText()

     uri_end = ''.join(e for e in module_id if e.isalnum())
     if(uri_end!="None" and uri_end!="inPolish"):
        print(uri_end)
        module_uri_g = URIRef(f"{uri_main}{uri_end}")
        
        module_name_g = Literal(module_name, datatype=XSD.string)
        module_content_g = Literal(module_content, datatype=XSD.string)
        module_id_g = Literal(module_id, datatype=XSD.string)
        credit_points_g = Literal(credit_points_value, datatype=XSD.string)
        department_g = Literal(department, datatype=XSD.string)
        
        graph.add((module_uri_g, RDF.type, ns_module.module))
        graph.add((module_uri_g, URIRef("http://tuc.bialystok/module#hasName"), module_name_g))
        graph.add((module_uri_g, URIRef("http://tuc.bialystok/module#hasModuleNumber"), module_id_g))
        graph.add((module_uri_g, URIRef("http://tuc.bialystok/module#hasContent"), module_content_g))
        graph.add((module_uri_g, URIRef("http://tuc.bialystok/module#hasCreditPoints"), credit_points_g))
        count = count + 1
     



bialystok_modules_data = graph.serialize(format='xml')
bialystok_modules_file = open('bialystok_modules_full_data.rdf', 'w')
bialystok_modules_file.write(bialystok_modules_data)
bialystok_modules_file.close()
    
html.close()
