import React from "react";
import "../assets/css/UniversitySelection.css";

const UniversitySelection = () => {
  return (
    <div className="universitySelection">
      <div className="universitySelection__wrapper">
        <h2 className="universitySelection__title">
          Please tell us about your current university
        </h2>
        <select className="universitySelection__select">
          <option value="" disabled selected hidden>
            Select Your University
          </option>
          <option value="">Technical University of Chemnitz</option>
          <option value="">Other</option>
        </select>
        <button className="universitySelection__button" type="submit">
          Submit
        </button>
      </div>
    </div>
  );
};

export default UniversitySelection;
