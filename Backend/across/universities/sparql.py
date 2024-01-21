def get_university_list():
    query = """
    SELECT ?universityName 
        WHERE {
            ?university rdf:type <http://across/university#> .
            ?university <http://across/university#hasUniversityName> ?universityName .        
        }
    """

    return query
