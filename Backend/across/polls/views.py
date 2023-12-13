import json

import rdflib
from django.http import HttpResponse
from .translator import translateModules
from .module_similarity import read_modules_and_compare

graph = rdflib.Graph()
graph2 = rdflib.Graph()
#complete isn't required , incase required we need to do it some other way becuase path will be different for different machines
#graph.parse("D:\Web Engineering\SEM-III\Planspiel\ACROSS\ACROSS_MAIN\web-wizards\Backend\web_engineering_modules.rdf")
graph.parse("web_engineering_modules.rdf")
graph.parse("bialystok_modules.rdf")
#graph.parse("D:\Web Engineering\SEM-III\Planspiel\ACROSS\ACROSS_MAIN\web-wizards\Backend\departments.rdf")
graph.parse("departments.rdf")
module_list = """
SELECT ?moduleName ?moduleId ?moduleContent ?moduleCreditPoints ?deptName ?dName ?deptId ?similarModule ?actualName
WHERE {
    ?name <http://tuc.web.engineering/module#hasName> ?moduleName ;
          <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
          <http://tuc.web.engineering/module#hasContent> ?moduleContent ;
          <http://tuc.web.engineering/module#hasCreditPoints> ?moduleCreditPoints ;
          <http://tuc.web.engineering/department#hasName> ?deptName ;
          <http://tuc.web.engineering/module#hasModules> ?similarModule .
    ?deptName <http://tuc.web.engineering/department#hasName> ?dName .
    ?deptName <http://tuc.web.engineering/department#hasDeptId> ?deptId .
    ?similarModule <http://tuc.web.engineering/module#hasName> ?actualName.
}
"""

qresponse = graph.query(module_list)
data = "<html><body>"
counter = 0
data_list = []
for row in qresponse:
    counter = counter + 1
    data_dict = {
        'name': str(row.moduleName),
        'similarURI': str(row.actualName),
    }
    data_list.append(data_dict)
json_data = json.dumps(data_list, indent=2)
data = data + json_data
data = data + f"<p>Total Modules are: {counter} </p></html></body>"

def scrape_bialystok_data(request):
    return HttpResponse("Dooa Ansari")

def translator(request):
    data = read_modules_and_compare("web_engineering_modules.rdf", "bialystok_modules.rdf")
    return  HttpResponse(data)


def index(request):
    return HttpResponse(json_data)
