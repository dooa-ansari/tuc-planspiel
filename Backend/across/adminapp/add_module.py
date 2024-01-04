from rdflib import URIRef, Literal
from rdflib.namespace import RDF, XSD
import json
from .sparql import *
from pymantic import sparql
from django.http import JsonResponse

def add_module_in_blaze(request):
     try:
        body = request.body.decode('utf-8')
        data = json.loads(body)
        courseUri = URIRef(data.get('courseUri',''))
        universityUri = URIRef(data.get('universityUri',''))
        moduleName = data.get('moduleName','')
        moduleContent = data.get('moduleContent','')
        moduleCreditPoints = data.get('moduleCreditPoints','')
        moduleId = data.get('moduleId','')
        print(data)
        server = sparql.SPARQLServer('http://54.242.11.117:80/bigdata/sparql')

        uri_main = "http://tuc.web.engineering/module#"
        
        uri_end = ''.join(e for e in moduleId if e.isalnum())
        module_uri_g = URIRef(f"{uri_main}{uri_end}")
        uri_university = URIRef(universityUri)
        uri_course = URIRef(courseUri)
        module_name_g = Literal(moduleName, datatype=XSD.string)
        module_content_g = Literal(moduleContent, datatype=XSD.string)
        module_id_g = Literal(moduleId, datatype=XSD.string)
        credit_points_g = Literal(moduleCreditPoints, datatype=XSD.string)
        print(add_module % (module_uri_g ,module_id_g, module_name_g , module_content_g, credit_points_g,uri_university, uri_course))
        result = server.update(add_module % (module_uri_g ,module_id_g, module_name_g , module_content_g, credit_points_g,uri_university, uri_course))
        print(result)
        return JsonResponse({'message': 'Module added successfully', 'uri': module_uri_g}, status=200)
     except Exception as e:
        return JsonResponse({'message': f'Error adding module: {str(e)}'}, status=500)

     
        