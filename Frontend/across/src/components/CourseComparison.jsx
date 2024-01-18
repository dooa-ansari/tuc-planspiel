import React from "react";
import "../assets/css/CourseComparison.css";
import courseCompareImage from "../assets/compare_modules.png";

const CourseComparison = () => {
  return (
    <div className="courseComparison">
      <img
        className="courseComparison__image"
        src={courseCompareImage}
        alt=""
      />
      <div className="courseComparison__contents">
        <h2 className="courseComparison__title">
          Elevating Education: Unmatched Modules, Unique Features
        </h2>
        <p className="courseComparison__description">
          Lorem, ipsum dolor sit amet consectetur adipisicing elit.
        </p>
        <button type="button" className="courseComparison__button">
          Explore Here
        </button>
      </div>
    </div>
  );
};

export default CourseComparison;
