import React, { useState, useEffect } from "react";
import "../assets/css/ModuleList.css";
import Dropdown from "react-bootstrap/Dropdown";
import Table from "react-bootstrap/Table";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Button from "react-bootstrap/Button";
import Spinner from "react-bootstrap/Spinner";
import Modal from "react-bootstrap/Modal";
import Badge from "react-bootstrap/Badge";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Row from "react-bootstrap/Row";

const ModulesList = () => {
  const [universities, setUniversities] = useState([]);
  const [universitiesForAdd, setUniversitiesAdd] = useState([]);
  const [courses, setCourses] = useState([]);
  const [coursesAdd, setCoursesAdd] = useState([]);
  const [selectedUniversityUri, setSelectedUniversityUri] = useState(null);
  const [selectedUniversityName, setSelectedUniversityName] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [modules, setModules] = useState(null);
  const [loadingModule, setLoadingModules] = useState(-1);
  const [currentModule, setCurrentModule] = useState(null);
  const [show, setShow] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [validated, setValidated] = useState(false);
  const [addUniversityUri, setAddUniversityUri] = useState("")
  const [addCourseUri, setAddCourseUri] = useState("")
  const [moduleId, setModuleId] = useState("")
  const [moduleName, setModuleName] = useState("")
  const [modulePoints, setModulePoints] = useState("")
  const [moduleContent, setModuleContent] = useState("")

  const handleSubmit = (event) => {
    const form = event.currentTarget;
    event.preventDefault();
    console.log(moduleId)
    console.log(moduleName)
    console.log(modulePoints)
    console.log(moduleContent)
    postAddData()
    setValidated(true);     
    if (form.checkValidity() === false) {
      
        
    }else{
       
    }
   
   
   
   
  };

  const postAddData = () => {
    fetch("http://127.0.0.1:8000/adminapp/api/insert/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: "dansari@gmail.com",
        university: addUniversityUri,
        course: addCourseUri,
        module_name: moduleName,
        module_number: moduleId,
        module_content: moduleContent,
        module_credit_points: modulePoints
      }),
    })
      .then((response) => response.json())
      .then((json) => {
         console.log(json)
         handleCloseAddModal()
      })
      .catch((error) => console.error(error));
  }

  const deleteModule = (uri) => {
    fetch("http://127.0.0.1:8000/adminapp/api/delete/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: "dansari@gmail.com",
        module_uri: uri,
      }),
    })
      .then((response) => response.json())
      .then((json) => {
         
      })
      .catch((error) => console.error(error));
  } 

  const handleCloseAddModal = () => setShowAddModal(false);
  const handleShowAddModal = () => {
    setShowAddModal(true);
  };

  const handleClose = () => setShow(false);
  const handleShow = (module) => {
    setCurrentModule(module);
    setShow(true);
  };

  useEffect(() => {
    fetch("http://localhost:8000/adminapp/universitieslist")
      .then((response) => response.json())
      .then((json) => {
        setUniversities(json);
        setUniversitiesAdd(json)
      })
      .catch((error) => console.error(error));
  }, []);

  const onClickUniversity = (item) => {
    getCoursesList(item.uri, item.name, false);
  };

  const onClickCourse = (item) => {
    setLoadingModules(1);
    getModuleList(item.courseUri, item.courseName);
  };

  const onClickUniversityAdd = (item) => {
    getCoursesList(item.uri, item.name, true);
    setAddUniversityUri(item.name)
  };

  const onClickCourseAdd = (item) => {
    setAddCourseUri(item.courseName)
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

  const getCoursesList = (uri, name, isAdd) => {
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
          if(!isAdd){

            setCourses(json.courses);
       
            setSelectedUniversityUri(uri);
            setSelectedUniversityName(name); }
            else{
                setCoursesAdd(json.courses);
       
                setSelectedUniversityUri(uri);
                setSelectedUniversityName(name);
          }
         
       
      })
      .catch((error) => console.error(error));
  };

  const getAddModuleFormModal = () => {
    return (
      <Modal show={showAddModal} onHide={handleCloseAddModal}>
        <Modal.Header closeButton>
          <Modal.Title>Add Module</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="dropdowns">
            <Dropdown>
              <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                Select Univeristy
              </Dropdown.Toggle>

              <Dropdown.Menu>
                {universitiesForAdd?.map((item) => (
                  <Dropdown.Item
                    onClick={() => onClickUniversityAdd(item)}
                    key={item.id}
                  >
                    {item.name}
                  </Dropdown.Item>
                ))}
              </Dropdown.Menu>
            </Dropdown>
            {universitiesForAdd.length > 0 && selectedUniversityUri && (
              <Dropdown>
                <Dropdown.Toggle variant="success" id="dropdown-basic">
                  Select Course
                </Dropdown.Toggle>

                <Dropdown.Menu>
                  {coursesAdd?.map((item) => (
                    <Dropdown.Item
                      key={item.courseNumber}
                      onClick={() => onClickCourseAdd(item)}
                    >
                      {item.courseName}
                    </Dropdown.Item>
                  ))}
                </Dropdown.Menu>
              </Dropdown>
            )}
          </div>
          <Form noValidate validated={validated} name="addForm">
            <Row className="mb-3">
              <Form.Group as={Col} md="5" controlId="addForm.id">
                <Form.Label>Id/Number</Form.Label>
                <Form.Control  onChange={(event) => setModuleId(event.target.value)}  name="id" required type="text" placeholder="Module Id" />
                <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
              </Form.Group>
              <Form.Group as={Col} md="5" controlId="addForm.name">
                <Form.Label>Name</Form.Label>
                <Form.Control  onChange={(event) => setModuleName(event.target.value)}  name="name" required type="text" placeholder="Module Name" />
                <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
              </Form.Group>
            </Row>
            <Row className="mb-3">
              <Form.Group as={Col} md="6" controlId="addForm.points">
                <Form.Label>Credit Points</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Credit Points"
                  required
                  name="points"
                  onChange={(event) => setModulePoints(event.target.value)} 
                />
                <Form.Control.Feedback type="invalid">
                  Please provide Credit Points
                </Form.Control.Feedback>
              </Form.Group>
            </Row>

            <Form.Group
              className="mb-3"
              controlId="addForm.content"
            >
              <Form.Label>Content</Form.Label>
              <Form.Control  onChange={(event) => setModuleContent(event.target.value)}  name="content" as="textarea" rows={3} />
            </Form.Group>
            <Button onClick={handleSubmit} type="submit">Submit</Button>
          </Form>
        </Modal.Body>
      </Modal>
    );
  };

  const getModuleDetailsModal = () => {
    return (
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Module Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>
            {" "}
            <Badge bg="secondary">Number</Badge> {currentModule?.moduleNumber}
          </p>
          <p>
            <Badge bg="secondary">Name</Badge> {currentModule?.moduleName}
          </p>
          <p>
            <Badge bg="secondary">Uri</Badge> {currentModule?.moduleUri}
          </p>
          <p>
            <Badge bg="secondary">Credit Points</Badge>{" "}
            {currentModule?.moduleCreditPoints}
          </p>
          <p>{currentModule?.moduleContent}</p>
        </Modal.Body>
      </Modal>
    );
  };
  return (
    <div style={{ flex: 1 }}>
      {getModuleDetailsModal()}
      {getAddModuleFormModal()}

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
        <Button variant="primary" onClick={() => handleShowAddModal()}>
          Add New Module
        </Button>
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
                        <Button
                          onClick={() => handleShow(module)}
                          variant="info"
                        >
                          Details
                        </Button>
                        <Button variant="warning">Update</Button>
                        <Button onClick={() => deleteModule(module.moduleUri)} variant="danger">Delete</Button>
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
