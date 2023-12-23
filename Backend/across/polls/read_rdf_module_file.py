import rdflib
from .sparql import *

def readRDFFile(file):
 graph = rdflib.Graph()
 
 graph.parse(file)
 
 
 module_list = graph.query(module_list_query)
 module_first_only = graph.query(module_list_query_first_item_only)
 return module_list, module_first_only
 
