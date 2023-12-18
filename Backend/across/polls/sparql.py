module_list_query = """
SELECT ?moduleName ?moduleId ?moduleContent ?moduleURI ?module
WHERE {
    ?module <http://tuc.web.engineering/module#hasName> ?moduleName ;
            <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
            <http://tuc.web.engineering/module#hasContent> ?moduleContent .
}
"""

insert_module_similarity = "INSERT DATA { <%s>  <http://tuc.web.engineering/module#hasModules>  <%s> }"