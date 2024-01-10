import React, { useState } from "react";
import "./CompareModules.css";
import MainLayout from "../../../components/user/MainLayout/MainLayout";

import Dropdown from "../../../components/Dropdown/Dropdown";
import SearchBox from "../../../components/user/SearchBox/SearchBox";

const CompareModules = () => {
  const [selectedUniversity, setSelectedUniversity] = useState(null);
  const [selectedModule, setSelectedModule] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState(null);

  const handleUniversityChange = university => {
    setSelectedUniversity(university);
  };
  const handleModuleChange = module => {
    setSelectedModule(module);
  };
  const handleCourseChange = course => {
    setSelectedCourse(course);
  };

  const universities = [
    {
      label: "Bialystok University of Technology",
      value: "Bialystok University of Technology",
    },
    {
      label: "Chemnitz University of Technology",
      value: "Chemnitz University of Technology",
    },
    { label: "University of Craiova", value: "University of Craiova" },
    { label: "University of Girona", value: "University of Girona" },
    { label: "University of Lleida", value: "University of Lleida" },
  ];

  const modules = [
    { label: "Module1", value: "module1" },
    { label: "Module2", value: "module2" },
  ];

  const courses = [
    { label: "Course1", value: "course1" },
    { label: "Course2", value: "course2" },
  ];
  return (
    <>
      <MainLayout>
        <SearchBox />
        <h1 style={{ textAlign: "center" }}>Compare Modules Page</h1>
        <div
          style={{
            display: "flex",
            justifyContent: "space-around",
            alignItems: "center",
            marginBottom: "40px",
            paddingTop: "70px",
          }}
        >
          <h4 style={{ width: "10%" }}>Universities</h4>
          <Dropdown
            options={universities}
            value={selectedUniversity}
            onChange={handleUniversityChange}
          />
          <Dropdown
            options={universities}
            value={selectedUniversity}
            onChange={handleUniversityChange}
          />
        </div>
        <div
          style={{
            display: "flex",
            justifyContent: "space-around",
            alignItems: "center",
            marginBottom: "40px",
          }}
        >
          <h4 style={{ width: "10%" }}>Modules</h4>
          <Dropdown
            options={modules}
            value={selectedModule}
            onChange={handleModuleChange}
          />
          <Dropdown
            options={modules}
            value={selectedModule}
            onChange={handleModuleChange}
          />
        </div>
        <div
          style={{
            display: "flex",
            justifyContent: "space-around",
            alignItems: "center",
            marginBottom: "40px",
          }}
        >
          <h4 style={{ width: "10%" }}>Courses</h4>
          <Dropdown
            options={courses}
            value={selectedCourse}
            onChange={handleCourseChange}
          />
          <Dropdown
            options={courses}
            value={selectedCourse}
            onChange={handleCourseChange}
          />
        </div>
      </MainLayout>
    </>
  );
};

export default CompareModules;
