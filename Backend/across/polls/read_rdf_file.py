import rdflib
from .sparql import *

def readRDFFile(file):
 graph = rdflib.Graph()
 
 graph.parse("web_engineering_modules.rdf")
 
 
 module_list = graph.query(module_list_query)
 return module_list
 
