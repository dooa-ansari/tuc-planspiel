import React, { useEffect, useState } from "react";
import MainLayout from "../../../components/user/MainLayout/MainLayout";
import { useAuth } from "../../../context/AuthContext";
import "./MyProfile.css";
import Gravatar from "../../../components/Gravatar/Gravatar";
import { Tab, Tabs, Form } from "react-bootstrap";

import { FaTrash } from "react-icons/fa6";
import { getUniversityUri } from "../../../api/externalApi";
import Dropdown from "../../../components/Dropdown/Dropdown";
import {
  getCoursesOfParticularUniversity,
  getModulesOfCourse,
} from "../../../api/compareModuleApi";

const MyProfile = () => {
  const [auth] = useAuth();
  const [university, setUniversity] = useState(null);
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [modules, setModules] = useState([]);
  const [selectedModules, setSelectedModules] = useState([]);

  const handleCourseChange = course => {
    setSelectedCourse(course);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const universityResponse = await getUniversityUri({
          university_name: auth.user.university_name,
        });

        if (
          universityResponse.status === 200 &&
          universityResponse.statusText === "OK"
        ) {
          setUniversity(universityResponse.data.universityDetails);

          const universityName =
            universityResponse.data.universityDetails.university_name;
          const universityUri =
            universityResponse.data.universityDetails.university_uri;

          const coursesResponse = await getCoursesOfParticularUniversity({
            universityName,
            universityUri,
          });

          if (
            coursesResponse.status === 200 &&
            coursesResponse.statusText === "OK"
          ) {
            setCourses(coursesResponse.data.courses);
          } else {
            console.error("Error fetching courses");
          }
        } else {
          console.error("Error retrieving university");
        }
      } catch (error) {
        console.error("Error fetching data", error);
      }
    };

    fetchData();

    if (university !== null && selectedCourse !== null) {
      fetchModulesOfCourse();
    }
  }, [auth.user.university_name, selectedCourse]);

  const dropdownOptionsForCourses = courses.map(course => ({
    id: course.courseNumber,
    value: course.courseUri,
    label: course.courseName,
  }));

  const fetchModulesOfCourse = async () => {
    try {
      const courseUri = selectedCourse.value;
      const universityUri = university.university_uri;
      const courseName = selectedCourse.label;

      const data = { courseUri, universityUri, courseName };

      const retrievedModules = await getModulesOfCourse(data);
      setModules(retrievedModules.data.modules);
    } catch (error) {
      console.log("error fetching modules");
    }
  };

  console.log(modules);
  console.log(selectedCourse);

  return (
    <>
      <MainLayout>
        <div className="myProfile">
          <Tabs
            defaultActiveKey="profileDetails"
            id="myProfile-tab"
            className="mb-3"
          >
            <Tab eventKey="profileDetails" title="Profile Details">
              <div className="myProfile__contents">
                <div className="myProfile__userDetails">
                  <div>
                    <Gravatar fullName={auth.user.full_name} size={80} />
                  </div>

                  <h4
                    style={{
                      padding: "0.5rem 0",
                      margin: "0.5rem 0",
                      textAlign: "center",
                    }}
                  >
                    {auth.user.full_name}
                  </h4>
                  <div className="myProfile__dataList">
                    <div className="myProfile__emailGroup">
                      <h4>Email</h4>
                      <p>{auth.user.email}</p>
                    </div>
                    <div className="myProfile__roleGroup">
                      <h4>Current Role</h4>
                      <p>{auth.user.role}</p>
                    </div>
                  </div>
                </div>
                <div className="optedCourses">
                  <h4>Completed Modules List</h4>
                  <table>
                    <thead>
                      <tr>
                        <th>Modules</th>
                        <th>Credits Earned</th>
                        <th>Options</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Advance Management of Data</td>
                        <td>5</td>
                        <td className="tdTrashIcon">
                          <FaTrash />
                        </td>
                      </tr>
                      <tr>
                        <td>Seminar Web Engineering</td>
                        <td>5</td>
                        <td className="tdTrashIcon">
                          <FaTrash />
                        </td>
                      </tr>
                      <tr>
                        <td>Module 3</td>
                        <td>2</td>
                        <td className="tdTrashIcon">
                          <FaTrash />
                        </td>
                      </tr>
                      <tr>
                        <td>Module 4</td>
                        <td>4</td>
                        <td className="tdTrashIcon">
                          <FaTrash />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </Tab>
            <Tab eventKey="profile" title="Academic Data">
              <div className="myProfile__dropdownWrapper">
                <h2>Your University: {auth.user.university_name}</h2>
                <h4>Select one of the Courses Offered by your university</h4>
                <Dropdown
                  options={dropdownOptionsForCourses}
                  value={selectedCourse}
                  onChange={handleCourseChange}
                  placeholderText="Select your course..."
                />
              </div>
              {selectedCourse && (
                <>
                  <h2 className="text-center m-3">
                    List of modules offered in the {selectedCourse.label}{" "}
                    department
                  </h2>
                  <table>
                    <thead>
                      <tr>
                        <th>Module Number</th>
                        <th>Module Name</th>
                        <th>Credits Points</th>
                        <th>Options</th>
                      </tr>
                    </thead>

                    {modules &&
                      modules.map((module, idx) => {
                        return (
                          <tbody>
                            <tr>
                              <td>{module.moduleNumber}</td>
                              <td>{module.moduleName}</td>
                              <td>{module.moduleCreditPoints}</td>
                              <td>
                                <Form.Check>
                                  <Form.Check.Input type="checkbox" isValid />
                                </Form.Check>
                              </td>
                            </tr>
                          </tbody>
                        );
                      })}
                  </table>
                </>
              )}
            </Tab>
          </Tabs>
        </div>
      </MainLayout>
    </>
  );
};

export default MyProfile;
