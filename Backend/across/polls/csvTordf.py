import os
import csv
from rdflib import Graph, Namespace, URIRef, Literal

class Module:
    def __init__(self, module_number, name, content, department_name, credit_points):
        self.hasModuleNumber = module_number
        self.hasName = name
        self.hasContent = content
        self.hasCreditPoints = credit_points
        self.hasDepartmentName = department_name

rdf_graph = Graph()
existingModules= []
newModules= []
module = Namespace("http://tub.computer.science/module#")  
dept = Namespace("http://tub.computer.science/department#")
rdf_file ="" 
'''rdf_file is empty if it is created for the first time.'''
'''If the rdf file has already created then give that path.'''

if rdf_file:
    rdf_graph.parse(rdf_file, format='xml')  
    query = """
    PREFIX ns1: <http://tub.computer.science/module#>
    PREFIX ns2: <http://tub.computer.science/department#>


    SELECT ?moduleNumber ?name ?content ?departmentName ?creditPoints
    WHERE {
        ?subject ns1:hasModuleNumber ?moduleNumber ;
                 ns1:hasName ?name ;
                 ns1:hasContent ?content ;
                 ns2:hasName ?departmentName ;
                 ns1:hasCreditPoints ?creditPoints .
    }
    """
    results = rdf_graph.query(query)
    for row in results:
        module_number = row['moduleNumber'].value
        name = row['name'].value
        content = row['content'].value
        department_name = row['departmentName'].value
        credit_points = row['creditPoints'].value
        oldModule = Module(module_number,name, content, department_name, credit_points )
        existingModules.append(oldModule)

file_path = r'C:\Users\User\Downloads\data.csv'
if len(existingModules) == 0:
    if file_path:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for index,row in  enumerate(csv_reader):
                hasModuleNumber=row[1]
                hasName=row[2]
                hasContent=row[3]
                hasDepartmentName=row[4]
                hasCreditPoints= row[5]
                string_without_hyphen = row[1].replace('-', '').replace(' ', '')
                subject = URIRef(module[string_without_hyphen])
                rdf_graph.add((subject, module['hasModuleNumber'], Literal(hasModuleNumber)))
                rdf_graph.add((subject, module['hasName'], Literal(hasName)))
                rdf_graph.add((subject, module['hasContent'], Literal(hasContent)))
                rdf_graph.add((subject, dept['hasName'], Literal(hasDepartmentName)))
                rdf_graph.add((subject, module['hasCreditPoints'], Literal(hasCreditPoints)))
    rdf_file =r'C:\Users\User\Downloads\test.rdf' '''This is just for testing.'''
    rdf_graph.serialize(destination=rdf_file, format='xml')
else:
    if file_path:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for index,row in  enumerate(csv_reader):
                hasModuleNumber=row[1]
                hasName=row[2]
                hasContent=row[3]
                hasDepartmentName=row[4]
                hasCreditPoints= row[5]
                if index != 0:
                    vModule = Module(hasModuleNumber,hasName, hasContent, hasDepartmentName, hasCreditPoints)
                    newModules.append(vModule)
                   
updateModules= []
insertModules = []
for oldModule in existingModules:  
    for newModule in newModules:
        if oldModule.hasModuleNumber==newModule.hasModuleNumber:
            if oldModule.hasName!=newModule.hasName or oldModule.hasContent!=newModule.hasContent or oldModule.hasCreditPoints!=newModule.hasCreditPoints or oldModule.hasDepartmentName!=newModule.hasDepartmentName:
                updateModules.append(newModule)


if len(updateModules) != 0 :
    for updateModule in updateModules:
        string_without_hyphen = updateModule.hasModuleNumber.replace('-', '').replace(' ', '')
        subject = URIRef(module[string_without_hyphen])
        rdf_graph.set((subject, module['hasModuleNumber'], Literal(updateModule.hasModuleNumber)))
        rdf_graph.set((subject, module['hasName'], Literal(updateModule.hasName)))
        rdf_graph.set((subject, module['hasContent'], Literal(updateModule.hasContent)))
        rdf_graph.set((subject, dept['hasName'], Literal(updateModule.hasDepartmentName)))
        rdf_graph.set((subject, module['hasCreditPoints'], Literal(updateModule.hasCreditPoints)))


for newModule in newModules:
    if any(newModule.hasModuleNumber.lower() != oldModule.hasModuleNumber.lower() for oldModule in existingModules):
        insertModules.append(newModule)
      
for newModele in insertModules:
    string_without_hyphen = newModele.hasModuleNumber.replace('-', '').replace(' ', '')
    subject = URIRef(module[string_without_hyphen])
    rdf_graph.add((subject, module['hasModuleNumber'], Literal(newModele.hasModuleNumber)))
    rdf_graph.add((subject, module['hasName'], Literal(newModele.hasName)))
    rdf_graph.add((subject, module['hasContent'], Literal(newModele.hasContent)))
    rdf_graph.add((subject, dept['hasName'], Literal(newModele.hasDepartmentName)))
    rdf_graph.add((subject, module['hasCreditPoints'], Literal(newModele.hasCreditPoints)))

new_rdf_content = rdf_graph.serialize(format='xml')
new_rdf_bytes = new_rdf_content.encode('utf-8')
with open(rdf_file, 'wb') as file:
    file.write(new_rdf_bytes)   
          
