import rdflib
from django.http import HttpResponse
graph = rdflib.Graph()
graph.parse("web_engineering_modules.rdf")
graph.parse("departments.rdf")

module_list = """
SELECT DISTINCT ?moduleName ?moduleId ?deptName
WHERE {
    ?name <http://tuc.web.engineering/module#hasName> ?moduleName .
    ?id   <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId .
    ?deptartment <http://tuc.web.engineering/department#hasName> ?deptName .
}"""

qresponse = graph.query(module_list)
data = ""
for row in qresponse:
    data = data + f"{row.moduleName} has id {row.moduleId} and belongs to department {row.deptName}\n"



def index(request):
    return HttpResponse("Sparql Query Returned data {data}."+data)