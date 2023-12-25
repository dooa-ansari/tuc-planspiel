from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF , XSD
from .sparql import *

def add_predicate_for_module_similarity(universityOneModulesFile, univeristyTwoModulesFile, data_list_first, data_list_second, consumer):


    modulesTUC = Graph()
    modulesBialstok = Graph()
    modulesTUC.parse(universityOneModulesFile)
    modulesBialstok.parse(univeristyTwoModulesFile)
    consumer.send_message("Starting to update RDF files:")
    for similar_module in data_list_first:
       consumer.send_message(f"Updating file {similar_module}:")
       list = similar_module['similar_modules']
       for item in list:
           uri = URIRef(item)
           modulesTUC.update(insert_module_similarity  % (similar_module.uri,uri))
           
    for similar_module in data_list_second:
       consumer.send_message(f"Updating file {similar_module}:")
       list = similar_module['similar_modules']
       for item in list:
           uri = URIRef(item)
           modulesBialstok.update(insert_module_similarity  % (similar_module.uri,uri))
    
        
    fileOneContent = modulesTUC.serialize(format='xml')
    fileTwoContent = modulesBialstok.serialize(format='xml')

    file1 = open('web_engineering_modules_updated.rdf', 'w')
    file2 = open('bialystok_modules_updated.rdf', 'w')
    
    file1.write(fileOneContent)
    file2.write(fileTwoContent)
    consumer.send_message(f"Updating RDF files process finished successfully")
    file1.close()
    file2.close()

    # # Create an RDF URI node to use as the subject for multiple triples
    # donna = URIRef("http://example.org/donna")

    # # Add triples using store's add() method.
    # g.add((donna, RDF.type, FOAF.Person))
    # g.add((donna, FOAF.nick, Literal("donna", lang="en")))
    # g.add((donna, FOAF.name, Literal("Donna Fales")))
    # g.add((donna, FOAF.mbox, URIRef("mailto:donna@example.org")))

    # # Add another person
    # ed = URIRef("http://example.org/edward")

    # # Add triples using store's add() method.
    # g.add((ed, RDF.type, FOAF.Person))
    # g.add((ed, FOAF.nick, Literal("ed", datatype=XSD.string)))
    # g.add((ed, FOAF.name, Literal("Edward Scissorhands")))
    # g.add((ed, FOAF.mbox, Literal("e.scissorhands@example.org", datatype=XSD.anyURI)))

    # # Iterate over triples in store and print them out.
    # print("--- printing raw triples ---")
    # for s, p, o in g:
    #     print((s, p, o))

    # # For each foaf:Person in the store, print out their mbox property's value.
    # print("--- printing mboxes ---")
    # for person in g.subjects(RDF.type, FOAF.Person):
    #     for mbox in g.objects(person, FOAF.mbox):
    #         print(mbox)

    # # Bind the FOAF namespace to a prefix for more readable output
    # g.bind("foaf", FOAF)

    # # print all the data in the Notation3 format
    # print("--- printing mboxes ---")
    # print(g.serialize(format='n3'))
