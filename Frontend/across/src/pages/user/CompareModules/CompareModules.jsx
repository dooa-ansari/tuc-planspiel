import React, { useState } from "react";
import "./CompareModules.css";
import MainLayout from "../../../components/user/MainLayout/MainLayout";

import Dropdown from "../../../components/Dropdown/Dropdown";

const CompareModules = () => {
  const [selection, setSelection] = useState(null);

  const handleChange = option => {
    setSelection(option);
  };

  const options = [
    { label: "Red", value: "red" },
    { label: "Green", value: "green" },
    { label: "Blue", value: "blue" },
  ];
  return (
    <>
      <MainLayout>
        <h1>Compare Modules Page</h1>
        <div style={{ display: "flex" }}>
          <Dropdown
            options={options}
            value={selection}
            onChange={handleChange}
          />
          <Dropdown
            options={options}
            value={selection}
            onChange={handleChange}
          />
        </div>
      </MainLayout>
    </>
  );
};

export default CompareModules;
