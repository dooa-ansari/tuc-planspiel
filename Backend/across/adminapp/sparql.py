university_list_query = """
SELECT ?universityName ?hasUniversityId ?university
WHERE {
    ?university <http://across/university#hasUniversityName> ?universityName ;
            <http://across/university#hasUniversityId> ?hasUniversityId .
}
"""


# add_module = """INSERT DATA { <%s> rdf:type <http://tuc.web.engineering/module#> .
#                               <%s> <http://tuc.web.engineering/module#hasModuleNumber>  %s .
#                              }
# """
# add_module_1 = """ INSERT DATA { <http://tuc.web.engineering/module#jhlkh1> rdf:type <http://tuc.web.engineering/module#> .
#              <http://tuc.web.engineering/module#jhlkh1> <http://tuc.web.engineering/module#hasModuleNumber>  789 .
#             }
                             
# """
# add_module = """INSERT DATA { <%s> rdf:type <http://tuc.web.engineering/module#> ;
#                                    <http://tuc.web.engineering/module#hasModuleNumber>  <%s> ;
#                                    <http://tuc.web.engineering/module#hasName>  <%s> ;
#                                    <http://tuc.web.engineering/module#hasContent>  <%s> ;
#                                    <http://tuc.web.engineering/module#hasCreditPoints>  <%s> ;
#                                    <http://across/university#hasUniversity>  <%s> ;
#                                    <http://tuc/course#hasCourse>  <%s> . }
# """


def add_module(moduleUri, moduleNumber, moduleName, moduleContent, modulePoints, courseUri, universityUri):
    query = f"""
        INSERT DATA {{ <{moduleUri}> rdf:type <http://tuc.web.engineering/module#> ;
                                   <http://tuc.web.engineering/module#hasModuleNumber>  "{moduleNumber}" ;
                                   <http://tuc.web.engineering/module#hasName>  "{moduleName}" ;
                                   <http://tuc.web.engineering/module#hasContent>  "{moduleContent}" ;
                                   <http://tuc.web.engineering/module#hasCreditPoints>  "{modulePoints}" ;
                                   <http://across/university#hasUniversity>  <{universityUri}> ;
                                   <http://tuc/course#hasCourse>  <{courseUri}> . }}
        """
    return query


delete_module = "INSERT DATA { <%s>  <http://tuc.web.engineering/module#hasModules>  <%s> }"
