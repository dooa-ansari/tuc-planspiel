import React, { useState, useEffect } from "react";
import data_static from "../components/data";
import "../assets/css/ModuleList.css";
import Dropdown from "react-bootstrap/Dropdown";

const ModulesList = () => {
  const [universities, setUniversities] = useState([]);
  const [courses, setCourses] = useState([]);
  const [selectedUniversityUri , setSelectedUniversityUri] = useState(null)
  const [selectedUniversityName , setSelectedUniversityName] = useState(null)
  const [selectedCourse , setSelectedCourse] = useState(null)

  useEffect(() => {
    fetch("http://localhost:8000/adminapp/universitieslist")
      .then((response) => response.json())
      .then((json) => {
        setUniversities(json)
      })
      .catch((error) => console.error(error));
  }, []);

const onClickUniversity = (item) => {
   getCoursesList(item.uri, item.name)
}  
const getCoursesList = (uri, name) => {
    fetch("http://localhost:8000/polls/courses/", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            universityUri: uri,
            universityName: name,
        })
    })
    .then((response) => response.json())
    .then((json) => {
        setCourses(json.courses)
        console.log(json)
        setSelectedUniversityUri(uri)
        setSelectedUniversityName(name)
   
    
    })
    .catch((error) => console.error(error));
}

  return (
    <div style={{ flex: 1 }}>
      <p id="moduleHeading">Similarity Table</p>
      <div className="dropdowns">
      <Dropdown>
        <Dropdown.Toggle variant="secondary" id="dropdown-basic">
          Select Univeristy
        </Dropdown.Toggle>

        <Dropdown.Menu>
          {universities?.map((item) => <Dropdown.Item onClick={() => onClickUniversity(item)} key={item.id}>{item.name}</Dropdown.Item>)}  
        </Dropdown.Menu>
      </Dropdown>
      {universities.length > 0 && selectedUniversityUri && <Dropdown>
        <Dropdown.Toggle variant="success" id="dropdown-basic">
          Select Course
        </Dropdown.Toggle>

        <Dropdown.Menu>
         {courses?.map((item) => <Dropdown.Item key={item.courseNumber}>{item.courseName}</Dropdown.Item>)}  
        </Dropdown.Menu>
      </Dropdown>}
      </div>
      
    </div>
  );
};

export default ModulesList;
