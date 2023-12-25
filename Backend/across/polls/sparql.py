module_list_query = """
SELECT ?moduleName ?moduleId ?moduleContent ?moduleURI ?module
WHERE {
    ?module <http://tuc.web.engineering/module#hasName> ?moduleName ;
            <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
            <http://tuc.web.engineering/module#hasContent> ?moduleContent .
}
"""

list_with_similar_modules_query = """
SELECT ?moduleName ?moduleId ?moduleContent ?moduleCreditPoints ?similarModule ?similarModuleName ?similarModuleContent ?similarModuleCreditPoints ?similarModuleId
WHERE {
    ?name <http://tuc.web.engineering/module#hasName> ?moduleName ;
          <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
          <http://tuc.web.engineering/module#hasContent> ?moduleContent ;
          <http://tuc.web.engineering/module#hasCreditPoints> ?moduleCreditPoints ;
          <http://tuc.web.engineering/module#hasModules> ?similarModule .
    ?similarModule <http://tuc.web.engineering/module#hasName> ?similarModuleName;
                   <http://tuc.web.engineering/module#hasModuleNumber> ?similarModuleId ;
                   <http://tuc.web.engineering/module#hasContent> ?similarModuleContent;
                   <http://tuc.web.engineering/module#hasCreditPoints> ?similarModuleCreditPoints.
}
"""

module_list_query_first_item_only = """
SELECT ?moduleContent
WHERE {
    ?module <http://tuc.web.engineering/module#hasContent> ?moduleContent .
   
}
LIMIT 1
"""

insert_module_similarity = "INSERT DATA { <%s>  <http://tuc.web.engineering/module#hasModules>  <%s> }"