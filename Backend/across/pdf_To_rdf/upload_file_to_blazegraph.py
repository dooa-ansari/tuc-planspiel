from pymantic import sparql
import requests
from rdflib import Graph, URIRef, Literal, RDF, RDFS, XSD
from compare_modules.sparql import *
import os


def upload_file_to_blazegraph(directory, file, isFile):
    graph = Graph()
    server = sparql.SPARQLServer('http://13.51.109.79/bigdata/sparql')
    data_xml = graph.serialize(format='xml')
    payload = {'update': update_individual_module_by_admin(module_uri, updated_module_name, updated_module_number, updated_module_content, updated_module_credit_points, university_uri, course_uri)}

    result = requests.post("http://13.51.109.79/blazegraph/namespace/kb/sparql", data=payload)


    