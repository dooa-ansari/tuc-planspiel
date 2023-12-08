import React, { useState, useEffect } from "react";
import data_static from "../components/data";
import "../assets/css/ShowModules.css";

const ShowModules = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/polls/')
      .then(response => response.json())
      .then(json => setData(json))
      .catch(error => console.error(error));
  }, []);

  return (
    <div style={{ flex: 1 }}>
      <p id="moduleHeading">Web Engineering Modules</p>
      {data?.map((item) => {
        return (
          <div id="module" key={item.moduleId}>
            <div id="moduleid">{item.moduleId} - {item.moduleName}</div>
            <div id="dept">Department of {item.deptName}</div>
            <div id="creditPoints">Credit Points : {item.moduleCreditPoints}</div>
            <div>{item.moduleContent}</div>
           
          </div>
        );
      })}
    </div>
  );
};

export default ShowModules;
