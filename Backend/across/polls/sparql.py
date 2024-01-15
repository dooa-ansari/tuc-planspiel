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

def get_similar_module_against_module_uri_query(moduleUri):
    list_all_against_uri_with_similar_modules_query = f"""
        SELECT ?moduleId ?moduleName ?moduleContent ?moduleCreditPoints ?universityName ?courseName ?similarModule ?similarModuleName ?similarModuleContent ?similarModuleCreditPoints ?similarModuleId ?universityNameSimilar ?courseNameSimilar
        WHERE {{
            ?module <http://tuc.web.engineering/module#hasName> ?moduleName ;
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

            BIND(str(?module) AS ?moduleUri)
            
            FILTER (
                    ?moduleUri = "{moduleUri}"
                    )
        }}
    """
    return list_all_against_uri_with_similar_modules_query


def get_course_from_university_query(universityUri, universityName):
    query = f"""
        SELECT ?courseName ?courseUri ?courseNumber
        WHERE {{
            ?course rdf:type <http://tuc/course#> .
            ?course <http://across/university#belongsToUniversity> ?university .
            ?university rdf:type <http://across/university#> .
            ?university <http://across/university#hasUniversityName> ?universityName .
            ?course <http://tuc/course#hasCourseName> ?courseName .
            ?course <http://tuc/course#hasCourseNumber> ?courseNumber .
            
            BIND(str(?course) AS ?courseUri)
            BIND(str(?university) AS ?universityUri)

            FILTER (
                ?universityUri = "{universityUri}" &&
                ?universityName = "{universityName}"^^<http://www.w3.org/2001/XMLSchema#string>
            )
        }}
        """
    return query


def get_modules_from_course_and_university_query(courseUri, courseName, universityUri):
    query = f"""
        SELECT ?moduleName (SAMPLE (?moduleUri) as ?sampleModuleUri) (SAMPLE(?moduleNumber) as ?sampleModuleNumber) (SAMPLE(?moduleContent) as ?sampleModuleContent) (SAMPLE(?moduleCreditPoints) as ?sampleModuleCreditPoints)
        WHERE {{       
            ?module rdf:type <http://tuc.web.engineering/module#> .
            ?module <http://tuc.web.engineering/module#hasName> ?moduleName .
            ?module <http://tuc.web.engineering/module#hasModuleNumber> ?moduleNumber .
            ?module <http://tuc.web.engineering/module#hasContent> ?moduleContent .
            ?module <http://tuc.web.engineering/module#hasCreditPoints> ?moduleCreditPoints .
            ?course rdf:type <http://tuc/course#> .
            ?module <http://tuc/course#hasCourse> ?course .
          	?course <http://tuc/course#hasCourseName> ?courseName .
            ?university rdf:type <http://across/university#> .
            ?course <http://across/university#belongsToUniversity> ?university .  
          
          	BIND(str(?course) AS ?courseUri)
            BIND(str(?university) AS ?universityUri)
            BIND(str(?module) AS ?moduleUri)
            
            FILTER (
              (?courseUri = "{courseUri}" && ?courseName = "{courseName}"^^<http://www.w3.org/2001/XMLSchema#string>) &&
              ?universityUri = "{universityUri}"
            )
        }}
        GROUP BY ?moduleName
        """
    return query


def add_individual_module_by_admin(formatted_module_name, module_name, formatted_module_number, module_content, module_credit_points, university_uri, course_uri):
    query = f"""
    INSERT DATA {{
    <http://tuc.web.engineering/module#{formatted_module_name}> rdf:type <http://tuc.web.engineering/module#> .
    <http://tuc.web.engineering/module#{formatted_module_name}> <http://tuc.web.engineering/module#hasModuleNumber> "{formatted_module_number}"^^<http://www.w3.org/2001/XMLSchema#string> .
    <http://tuc.web.engineering/module#{formatted_module_name}> <http://tuc.web.engineering/module#hasName> "{module_name}"^^<http://www.w3.org/2001/XMLSchema#string> .
    <http://tuc.web.engineering/module#{formatted_module_name}> <http://tuc.web.engineering/module#hasContent> "{module_content}"^^<http://www.w3.org/2001/XMLSchema#string> .
    <http://tuc.web.engineering/module#{formatted_module_name}> <http://tuc.web.engineering/module#hasCreditPoints> "{module_credit_points}"^^<http://www.w3.org/2001/XMLSchema#string> .
    <http://tuc.web.engineering/module#{formatted_module_name}> <http://across/university#hasUniversity> <{university_uri}>.
    <http://tuc.web.engineering/module#{formatted_module_name}> <http://tuc/course#hasCourse> <{course_uri}> .
    }}
    """

    return query

def get_course_uri_by_course_and_university_name(course_name, university_name):
    query = f"""
    SELECT ?courseUri
        WHERE {{
            ?course rdf:type <http://tuc/course#> .
            ?course <http://across/university#belongsToUniversity> ?university .
            ?university rdf:type <http://across/university#> .
            ?university <http://across/university#hasUniversityName> ?universityName .
            ?course <http://tuc/course#hasCourseName> ?courseName .
            
            BIND(str(?course) AS ?courseUri)

            FILTER (
                ?courseName = "{course_name}"^^<http://www.w3.org/2001/XMLSchema#string> &&
                ?universityName = "{university_name}"^^<http://www.w3.org/2001/XMLSchema#string>
            )
        }}
    """
    return query

def get_university_uri_by_university_name(university_name):
    query = f"""
    SELECT ?universityUri 
        WHERE {{
            ?university rdf:type <http://across/university#> .
            ?university <http://across/university#hasUniversityName> ?universityName .
            
            BIND(str(?university) AS ?universityUri)

            FILTER (
                ?universityName = "{university_name}"^^<http://www.w3.org/2001/XMLSchema#string>
            )
        }}
    """
    return query

def is_module_already_present(module_name, module_number, university_uri, course_uri):
    query = f"""
    ASK {{
    ?module rdf:type <http://tuc.web.engineering/module#> .
    ?module <http://tuc.web.engineering/module#hasName> "{module_name}"^^<http://www.w3.org/2001/XMLSchema#string> .
    ?module <http://tuc.web.engineering/module#hasModuleNumber> "{module_number}"^^<http://www.w3.org/2001/XMLSchema#string> .
    ?module <http://across/university#hasUniversity> <{university_uri}> .
    ?module <http://tuc/course#hasCourse> <{course_uri}> .
    }}
    """

    return query

def delete_individual_module(module_uri):
    query = f"""
    DELETE WHERE {{
    <{module_uri}> ?predicate ?object .
    }}
    """

    return query  


def update_individual_module_by_admin(module_uri, updated_module_name, updated_module_number, updated_module_content, updated_module_credit_points, university_uri, course_uri):
    query = f"""
    DELETE {{
    <{module_uri}> <http://tuc.web.engineering/module#hasModuleNumber> ?oldModuleNumber .
    <{module_uri}> <http://tuc.web.engineering/module#hasName> ?oldName .
    <{module_uri}> <http://tuc.web.engineering/module#hasContent> ?oldContent.
    <{module_uri}> <http://tuc.web.engineering/module#hasCreditPoints> ?oldCreditPoints .
    
    }}
    INSERT {{
    <{module_uri}> <http://tuc.web.engineering/module#hasModuleNumber> "{updated_module_number}"^^<http://www.w3.org/2001/XMLSchema#string> .
    <{module_uri}> <http://tuc.web.engineering/module#hasName> "{updated_module_name}"^^<http://www.w3.org/2001/XMLSchema#string> .
    <{module_uri}> <http://tuc.web.engineering/module#hasContent> "{updated_module_content}"^^<http://www.w3.org/2001/XMLSchema#string> .
    <{module_uri}> <http://tuc.web.engineering/module#hasCreditPoints> "{updated_module_credit_points}"^^<http://www.w3.org/2001/XMLSchema#string> .
    }}
    WHERE {{
    <{module_uri}> rdf:type <http://tuc.web.engineering/module#> .
    <{module_uri}> <http://across/university#hasUniversity> <{university_uri}> .
    <{module_uri}> <http://tuc/course#hasCourse> <{course_uri}> .
    OPTIONAL {{
    <{module_uri}> <http://tuc.web.engineering/module#hasModuleNumber> ?oldModuleNumber .
    <{module_uri}> <http://tuc.web.engineering/module#hasName> ?oldName .
    <{module_uri}> <http://tuc.web.engineering/module#hasContent> ?oldContent.
    <{module_uri}> <http://tuc.web.engineering/module#hasCreditPoints> ?oldCreditPoints .
    }}
    }}
    """

    return query