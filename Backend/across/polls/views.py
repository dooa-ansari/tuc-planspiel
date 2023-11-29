import rdflib
from django.http import HttpResponse
graph = rdflib.Graph()
graph.parse("web_engineering_modules.rdf")
graph.parse("departments.rdf")

module_list = """
SELECT ?moduleName ?moduleId ?deptName ?dName
WHERE {
    ?name <http://tuc.web.engineering/module#hasName> ?moduleName ;
          <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
          <http://tuc.web.engineering/department#hasName> ?deptName .
    ?deptName <http://tuc.web.engineering/department#hasName> ?dName .
}"""

qresponse = graph.query(module_list)
data = "<html><body>"
for row in qresponse:
    data = data + f"<p><b>{row.moduleName}</b> has id <i><b>{row.moduleId}</b></i> and belongs to department <u><b>{row.dName}</b></u></p>"

data = data + "</html></body>"

def index(request):
    return HttpResponse(data)