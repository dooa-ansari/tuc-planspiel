list_with_similar_modules_query = """
SELECT ?name ?moduleName ?moduleId ?moduleContent ?moduleCreditPoints ?similarModule ?similarModuleName ?similarModuleContent ?similarModuleCreditPoints ?similarModuleId ?universityName ?universityNameSimilar ?courseName ?courseNameSimilar
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

def get_similar_module_against_module_uri_query(moduleUri):
    list_all_against_uri_with_similar_modules_query = f"""
        SELECT ?module ?moduleId ?moduleName ?moduleContent ?moduleCreditPoints ?universityName ?courseName ?similarModule ?similarModuleName ?similarModuleContent ?similarModuleCreditPoints ?similarModuleId ?universityNameSimilar ?courseNameSimilar
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

def get_modules_from_course_and_university_query(courseUri, courseName, universityUri):
    query = f"""
        SELECT ?moduleUri (SAMPLE (?moduleName) as ?sampleModuleName) (SAMPLE(?moduleNumber) as ?sampleModuleNumber) (SAMPLE(?moduleContent) as ?sampleModuleContent) (SAMPLE(?moduleCreditPoints) as ?sampleModuleCreditPoints)
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
        GROUP BY ?moduleUri
        ORDER BY ?sampleModuleName
        """
    return query

def get_all_modules_query():
    query = f"""
        SELECT ?moduleUri (SAMPLE(?moduleNumber) as ?sampleModuleNumber) (SAMPLE(?moduleName) as ?sampleModuleName) (SAMPLE(?moduleContent) as ?sampleModuleContent) (SAMPLE(?moduleCreditPoints) as ?sampleModuleCreditPoints) (SAMPLE(?universityName) as ?sampleUniversityName) (SAMPLE(?courseName) as ?sampleCourseName)
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
                    ?university <http://across/university#hasUniversityName> ?universityName .

                    BIND(str(?module) AS ?moduleUri)
        }}
        GROUP BY ?moduleUri
    """
    return query