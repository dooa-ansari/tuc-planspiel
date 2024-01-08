import os
import csv
from typing import Any
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
from rdflib.plugins.sparql import prepareQuery

university_dict = {
    'Technical University of Chemnitz': 'TUC',
    'Bialystok University': 'BU'
}

#Give the correct rdf file path
rdf_file = r'Backend\across\uploads\models3.rdf'
university_rdf= r'Backend\across\RDF_DATA\universities.rdf'


class Module:
    def __init__(self, module_number, name, content, credit_points, course, university):
        self.hasModuleNumber = module_number
        self.hasName = name
        self.hasContent = content
        self.hasCreditPoints = credit_points
        self.hasCourse = course
        self.hasUniversity = university

class University:
    def __init__(self, uni_id= None, uni_name= None, uni_url= None):
        if uni_id is None and uni_name is None and uni_url is None:
            self.id = ""
            self.name = ""
            self.url = "" 
        else:
            self.id = uni_id
            self.name = uni_name
            self.url = uni_url 

    def get_all_university_query(self):
        query = '''
        PREFIX university: <http://across/university#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
        SELECT ?university ?hasUniversityId ?hasUniversityName
        WHERE {
        ?university rdf:type university: .
        ?university university:hasUniversityId ?hasUniversityId .
        ?university university:hasUniversityName ?hasUniversityName .
        }'''
        return query
    
    def get_all_university(self):
        ns1 = Namespace("http://tuc.web.engineering/module#")
        ns2 = Namespace("http://tuc/course#")
        ns3 = Namespace("http://across/university#")
        # Create an RDF graph
        g = Graph()
        # Add namespaces to the graph
        g.bind("module", ns1)
        g.bind("course", ns2)
        g.bind("university", ns3)
        query = self.get_all_university_query()
        g.parse(university_rdf, format='xml')
        results = g.query(query)
        unis = []
        for row in results:
            uni_id = row['hasUniversityId'].value
            uni_name = row['hasUniversityName'].value
            uni_url = str(row['university'])
            uni = University(uni_id, uni_name, uni_url)
            unis.append(uni)
        return unis

class RDFModels():
    def get_rdf_modules(self):
        # Create an RDF graph
         g = Graph()
         g.parse(rdf_file, format='xml')
         query = """
PREFIX module: <http://tuc.web.engineering/module#>
PREFIX ns1: <http://across/university#>
PREFIX ns2: <http://tuc/course#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?hasName ?hasModuleNumber ?hasContent ?hasCreditPoints ?hasCourse ?hasUniversity
WHERE {
  ?subject rdf:type module:module .
  ?subject module:hasName ?hasName .
  ?subject module:hasModuleNumber ?hasModuleNumber .
  ?subject module:hasContent ?hasContent .
  ?subject module:hasCreditPoints ?hasCreditPoints .
  ?subject ns2:hasCourse ?hasCourse .
  ?subject ns1:hasUniversity ?hasUniversity .
}
  """
         prepared_query = prepareQuery(query)
         results = g.query(prepared_query)
         existingModules = []
         for row in results:
            hasName = row['hasName'].value
            hasModuleNumber = row['hasModuleNumber'].value      
            hasContent = row['hasContent'].value
            hasCreditPoints = row['hasCreditPoints'].value
            hasCourseName = str(row['hasCourse'])
            hasUniversity = str(row['hasUniversity'])
            vModule = Module(hasModuleNumber, hasName, hasContent, hasCreditPoints, hasCourseName, hasUniversity)
            existingModules.append(vModule)
         return existingModules

class CsvToRDF():
    def __init__(self, university):
        self.uni = university
        # Define namespaces
        self.ns1 = Namespace("http://tuc.web.engineering/module#")
        self.ns2 = Namespace("http://tuc/course#")
        self.ns3 = Namespace("http://across/university#")
    def csvModules(self, value):
        self.csvModules = value
    
    def rdfModeles(self, value):
        self.rdfModels = value
    
    def get_uni(self, unis, hasUniversity):
            for uni in unis:
                 if uni.name == hasUniversity and uni.name in university_dict:
                    return university_dict[uni.name]
       
    def get_all_csv_models(self, csv_readers, unis):
        try:
             newModules = []
             for row in csv_readers:
                hasModuleNumber, hasName, hasContent, hasCourseName, hasUniversity, hasCreditPoints = row
                '''Excape haeader row in csv file'''
                if hasModuleNumber != 'hasModuleNumber':  
                    vModule = Module(hasModuleNumber, hasName, hasContent, hasCreditPoints, hasCourseName, self.get_uni(unis,hasUniversity))
                    newModules.append(vModule)
        except Exception as e:
            print(f"An error occurred during: {e}")
        return newModules
                
class UpdateModules():
    def getUpdateModels(self, csvToRDF):
        rdfmodels = RDFModels()
        existingModules = rdfmodels.get_rdf_modules()
        csvToRDF.rdfModeles=existingModules
        updateModules=[]
        for existingModule in existingModules:
            for newModule in csvToRDF.csvModules:
                if existingModule.hasModuleNumber == newModule.hasModuleNumber:
                    if (existingModule.hasName != newModule.hasName or
                            existingModule.hasContent != newModule.hasContent or
                            existingModule.hasCreditPoints != newModule.hasCreditPoints):
                        updateModules.append(newModule)

        if len(updateModules)!=0:
            # Create an RDF graph
            g = Graph()
            # Add namespaces to the graph
            g.bind("module", csvToRDF.ns1)
            g.bind("course", csvToRDF.ns2 )
            g.bind("university", csvToRDF.ns3 )
            for updateModule in updateModules:
             string_without_hyphen = updateModule.hasModuleNumber.replace('-', '').replace(' ', '')
             subject = csvToRDF.ns1[string_without_hyphen]
             g.set((subject, RDF.type, csvToRDF.ns1["module"]))
             g.set((subject, csvToRDF.ns1["hasModuleNumber"], Literal(updateModule.hasModuleNumber, datatype=XSD.string)))
             g.set((subject, csvToRDF.ns1["hasName"], Literal(updateModule.hasName, datatype=XSD.string)))
             g.set((subject, csvToRDF.ns1["hasContent"], Literal(updateModule.hasContent, datatype=XSD.string)))
             g.set((subject, csvToRDF.ns2["hasCourse"], csvToRDF.ns2[updateModule.hasCourse]))
             g.set((subject, csvToRDF.ns3["hasUniversity"], csvToRDF.ns3[updateModule.hasUniversity]))
             g.set((subject, csvToRDF.ns1["hasCreditPoints"], Literal(updateModule.hasCreditPoints, datatype=XSD.string)))
            new_rdf_content = g.serialize(format='xml')
            new_rdf_bytes = new_rdf_content.encode('utf-8')
            with open(rdf_file, 'wb') as file:
                file.write(new_rdf_bytes)
    
class InsertModules():
    def insertModul(self, csvToRDF):
        try:
            # Read the existing RDF file
            g = Graph()
            g.parse(rdf_file, format="xml")
            # Add namespaces to the graph
            g.bind("module", csvToRDF.ns1)
            g.bind("course", csvToRDF.ns2 )
            g.bind("university", csvToRDF.ns3 )

            newModels = []
            for newModule in csvToRDF.csvModules:
                # Check if the module number is unique in the existing RDF data
                if not any(oldModule.hasModuleNumber.lower() == newModule.hasModuleNumber.lower() for oldModule in csvToRDF.rdfModeles):
                    newModels.append(newModule) 
            for row in newModels:
                string_without_hyphen = row.hasModuleNumber.replace('-', '').replace(' ', '')
                subject = csvToRDF.ns1[string_without_hyphen]
                g.add((subject, RDF.type, csvToRDF.ns1["module"]))
                g.add((subject, csvToRDF.ns1["hasModuleNumber"], Literal(row.hasModuleNumber, datatype=XSD.string)))
                g.add((subject, csvToRDF.ns1["hasName"], Literal(row.hasName, datatype=XSD.string)))
                g.add((subject, csvToRDF.ns1["hasContent"], Literal(row.hasContent, datatype=XSD.string)))
                g.add((subject, csvToRDF.ns2["hasCourse"], csvToRDF.ns2[row.hasCourse]))
                g.add((subject, csvToRDF.ns3["hasUniversity"], csvToRDF.ns3[row.hasUniversity.replace(" ", "_")]))
                g.add((subject, csvToRDF.ns1["hasCreditPoints"], Literal(row.hasCreditPoints, datatype=XSD.string)))

            new_rdf_content = g.serialize(format='xml')
            new_rdf_bytes = new_rdf_content.encode('utf-8')

            with open(rdf_file, 'wb') as file:
                file.write(new_rdf_bytes)
        except Exception as e:
            print(f'the error occurs at {e}')