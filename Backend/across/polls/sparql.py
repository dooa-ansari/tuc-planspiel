module_list_query = """
SELECT ?moduleName ?moduleId ?moduleContent ?moduleURI ?module
WHERE {
    ?module <http://tuc.web.engineering/module#hasName> ?moduleName ;
            <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
            <http://tuc.web.engineering/module#hasContent> ?moduleContent .
}
"""

list_with_similar_modules_query = """
SELECT ?moduleName ?moduleId ?moduleContent ?moduleCreditPoints ?similarModule ?similarModuleName ?similarModuleContent ?similarModuleCreditPoints ?similarModuleId ?universityName ?universityNameSimilar ?courseName ?courseNameSimilar
WHERE {
    ?name <http://tuc.web.engineering/module#hasName> ?moduleName ;
          <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
          <http://tuc.web.engineering/module#hasContent> ?moduleContent ;
          <http://tuc.web.engineering/module#hasCreditPoints> ?moduleCreditPoints ;
          <http://tuc.web.engineering/module#hasModules> ?similarModule ;
          <http://across/university#hasUniversity> ?university ;
          <http://tuc/course#hasCourse> ?course .
    ?university <http://across/university#hasUniversityName> ?universityName .
    ?course <http://tuc/course#hasCourseName> ?courseName .
    ?similarModule <http://tuc.web.engineering/module#hasName> ?similarModuleName;
                   <http://tuc.web.engineering/module#hasModuleNumber> ?similarModuleId ;
                   <http://tuc.web.engineering/module#hasContent> ?similarModuleContent;
                   <http://tuc.web.engineering/module#hasCreditPoints> ?similarModuleCreditPoints ;
                   <http://across/university#hasUniversity> ?similarUniversity ;
                   <http://tuc/course#hasCourse> ?similarCourse .
     ?similarUniversity <http://across/university#hasUniversityName> ?universityNameSimilar .
     ?similarCourse <http://tuc/course#hasCourseName> ?courseNameSimilar .
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

insert_module_univeristy = "INSERT DATA { <%s>  <http://across/university#hasUniversity>  <%s> }"
insert_module_course = "INSERT DATA { <%s>  <http://tuc/course#hasCourse>  <%s> }"