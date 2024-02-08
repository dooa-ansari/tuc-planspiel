module_list_query = """
SELECT ?moduleName ?moduleId ?moduleContent ?moduleURI ?module
WHERE {
    ?module <http://tuc.web.engineering/module#hasName> ?moduleName ;
            <http://tuc.web.engineering/module#hasModuleNumber> ?moduleId ;
            <http://tuc.web.engineering/module#hasContent> ?moduleContent .
}
"""


module_list_query_first_item_only = """
SELECT ?moduleContent
WHERE {
    ?module <http://tuc.web.engineering/module#hasContent> ?moduleContent .
   
}
LIMIT 1
"""

insert_module_similarity = """INSERT {
    ?subject <http://tuc.web.engineering/module#hasModules> ?resource
}
WHERE {
  BIND(<%s> AS ?subject)
  BIND(<%s> AS ?resource)
}"""

insert_module_univeristy = "INSERT DATA { <%s>  <http://across/university#hasUniversity>  <%s> }"

insert_module_course = "INSERT DATA { <%s>  <http://tuc/course#hasCourse>  <%s> }"


def add_course(course_uri, course_name, belongs_to_program, belongs_to_department, university_uri,has_language):
    query = f"""
        INSERT DATA {{ 
            <{course_uri}> rdf:type <http://tuc/course#> ;
                    <http://tuc/course#hasCourseName> "{course_name}" ;
                    <http://tuc/course#belongsToProgram> "{belongs_to_program}" ;
                    <http://tuc/course#hasLanguage> "{has_language}" ;
                    <http://tuc/course#belongsToDepartment> "{belongs_to_department}" ;
                    <http://across/university#belongsToUniversity>  <{university_uri}> .
               }}
    """
    return query