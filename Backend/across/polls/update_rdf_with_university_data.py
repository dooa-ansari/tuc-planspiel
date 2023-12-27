import rdflib, URIRef
from .sparql import *

graph = rdflib.Graph()
graph.parse(file)
module_list = graph.query(module_list_query)
for module in module_list:
    uri = URIRef(item)
    graph.update(insert_module_univeristy  % (module.module,uri))
    graph.update(insert_module_course  % (module.module,uri))

 
