module_list_query = """
SELECT ?moduleName ?moduleId ?moduleContent
WHERE {
    ?name <http://tuc.web.engineering/module#hasName> ?moduleName ;
          <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
          <http://tuc.web.engineering/module#hasContent> ?moduleContent .
}
"""