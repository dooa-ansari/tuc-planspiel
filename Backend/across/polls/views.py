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
data = "<html><body>"
for row in qresponse:
    data = data + f"<p><b>{row.moduleName}</b> has id <i>{row.moduleId}</i> and belongs to department <u>{row.deptName}</u></p>"

data = data + "</html></body>"

def index(request):
    return HttpResponse(data)