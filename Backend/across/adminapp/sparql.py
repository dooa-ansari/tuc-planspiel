university_list_query = """
SELECT ?universityName ?hasUniversityId ?university
WHERE {
    ?university <http://across/university#hasUniversityName> ?universityName ;
            <http://across/university#hasUniversityId> ?hasUniversityId .
}
"""

add_module = """INSERT DATA { <%s> rdf:type <http://tuc.web.engineering/module#> ;
                                   <http://tuc.web.engineering/module#hasModuleNumber>  <%s> ;
                                   <http://tuc.web.engineering/module#hasName>  <%s> ;
                                   <http://tuc.web.engineering/module#hasContent>  <%s> ;
                                   <http://tuc.web.engineering/module#hasCreditPoints>  <%s> ;
                                   <http://across/university#hasUniversity>  <%s> ;
                                   <http://tuc/course#hasCourse>  <%s> . }
"""

delete_module = "INSERT DATA { <%s>  <http://tuc.web.engineering/module#hasModules>  <%s> }"
