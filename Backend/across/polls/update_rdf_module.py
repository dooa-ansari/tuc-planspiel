from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF , XSD
from .sparql import *

def add_predicate_for_module_similarity(universityOneModulesFile, univeristyTwoModulesFile, data_list_first, data_list_second, consumer):


    modulesTUC = Graph()
    modulesBialstok = Graph()
    modulesTUC.parse(universityOneModulesFile)
    modulesBialstok.parse(univeristyTwoModulesFile)
    consumer.send_message({"progress": 20 , "message": "Starting to update RDF files:"})
    for similar_module in data_list_first:
       consumer.send_message({"progress": 30 , "message": f"Updating file {similar_module.uri}:"})
       list = similar_module['similar_modules']
       for item in list:
           uri = URIRef(item)
           modulesTUC.update(insert_module_similarity  % (similar_module.uri,uri))
           
    for similar_module in data_list_second:
       consumer.send_message({"progress": 40 , "message": f"Updating file {similar_module.uri}:"})
       list = similar_module['similar_modules']
       for item in list:
           uri = URIRef(item)
           modulesBialstok.update(insert_module_similarity  % (similar_module.uri,uri))
    
    consumer.send_message({"progress": 50 , "message": "Finialising Results"})    
    fileOneContent = modulesTUC.serialize(format='xml')
    fileTwoContent = modulesBialstok.serialize(format='xml')

    file1 = open(f'universityOneModulesFile1.rdf', 'w')
    file2 = open(f'universityOneModulesFile2.rdf', 'w')
    
    consumer.send_message({"progress": 60 , "message": "Almost Finished"})    
    file1.write(fileOneContent)
    file2.write(fileTwoContent)
    consumer.send_message({"progress": 100 , "message": f"Updating RDF files process finished successfully"})
    file1.close()
    file2.close()
