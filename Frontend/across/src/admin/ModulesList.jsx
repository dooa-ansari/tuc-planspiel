import React, { useState, useEffect } from "react";
import "../assets/css/ModuleList.css";
import Dropdown from "react-bootstrap/Dropdown";
import Table from "react-bootstrap/Table";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Button from "react-bootstrap/Button";
import Spinner from "react-bootstrap/Spinner";
import Modal from "react-bootstrap/Modal";
import Badge from 'react-bootstrap/Badge';

const ModulesList = () => {
  const [universities, setUniversities] = useState([]);
  const [courses, setCourses] = useState([]);
  const [selectedUniversityUri, setSelectedUniversityUri] = useState(null);
  const [selectedUniversityName, setSelectedUniversityName] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [modules, setModules] = useState(null);
  const [loadingModule, setLoadingModules] = useState(-1);
  const [currentModule, setCurrentModule] = useState(null);
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = (module) => {
    setCurrentModule(module)
    setShow(true);
  } 

  useEffect(() => {
    fetch("http://localhost:8000/adminapp/universitieslist")
      .then((response) => response.json())
      .then((json) => {
        setUniversities(json);
      })
      .catch((error) => console.error(error));
  }, []);

  const onClickUniversity = (item) => {
    getCoursesList(item.uri, item.name);
  };

  const onClickCourse = (item) => {
    setLoadingModules(1);
    getModuleList(item.courseUri, item.courseName);
  };

  const getModuleList = (uri, name) => {
    fetch("http://localhost:8000/polls/modules/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        universityUri: selectedUniversityUri,
        courseUri: uri,
        courseName: name,
      }),
    })
      .then((response) => response.json())
      .then((json) => {
        setModules(json.modules);
        setLoadingModules(0);
      })
      .catch((error) => console.error(error));
  };

  const getCoursesList = (uri, name) => {
    fetch("http://localhost:8000/polls/courses/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        universityUri: uri,
        universityName: name,
      }),
    })
      .then((response) => response.json())
      .then((json) => {
        setCourses(json.courses);
        console.log(json);
        setSelectedUniversityUri(uri);
        setSelectedUniversityName(name);
      })
      .catch((error) => console.error(error));
  };

  return (
    <div style={{ flex: 1 }}>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Modal Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <p> <Badge bg="secondary">Number</Badge> {currentModule?.moduleNumber}</p>
            <p><Badge bg="secondary">Name</Badge> {currentModule?.moduleName}</p>
            <p><Badge bg="secondary">Uri</Badge> {currentModule?.moduleUri}</p>
            <p><Badge bg="secondary">Credit Points</Badge> {currentModule?.moduleCreditPoints}</p>
            <p>{currentModule?.moduleContent}</p>

        </Modal.Body>
      </Modal>
      <p id="moduleHeading">Modules Table</p>
      <div className="dropdowns">
        <Dropdown>
          <Dropdown.Toggle variant="secondary" id="dropdown-basic">
            Select Univeristy
          </Dropdown.Toggle>

          <Dropdown.Menu>
            {universities?.map((item) => (
              <Dropdown.Item
                onClick={() => onClickUniversity(item)}
                key={item.id}
              >
                {item.name}
              </Dropdown.Item>
            ))}
          </Dropdown.Menu>
        </Dropdown>
        {universities.length > 0 && selectedUniversityUri && (
          <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
              Select Course
            </Dropdown.Toggle>

            <Dropdown.Menu>
              {courses?.map((item) => (
                <Dropdown.Item
                  key={item.courseNumber}
                  onClick={() => onClickCourse(item)}
                >
                  {item.courseName}
                </Dropdown.Item>
              ))}
            </Dropdown.Menu>
          </Dropdown>
        )}
        <Button variant="primary">Add New Module</Button>
      </div>
      {loadingModule == 0 && modules?.length > 0 && (
        <div>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>#</th>
                <th>Module Name</th>
                <th>Module Uri</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {modules.map((module) => {
                return (
                  <tr key={module.moduleNumber}>
                    <td>{module.moduleNumber}</td>
                    <td>{module.moduleName}</td>
                    <td>{module.moduleUri}</td>
                    <td>
                      <ButtonGroup size="sm">
                        <Button onClick={() => handleShow(module)} variant="info">
                          Details
                        </Button>
                        <Button variant="warning">Update</Button>
                        <Button variant="danger">Delete</Button>
                      </ButtonGroup>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </Table>
        </div>
      )}
      {loadingModule == 0 && loadingModule != -1 && (
        <div className="spinner">
          <Spinner animation="grow" variant="success" />
        </div>
      )}
    </div>
  );
};

export default ModulesList;
