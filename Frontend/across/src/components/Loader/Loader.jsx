import React from "react";
import { RotatingLines } from "react-loader-spinner";
import "./Loader.css";

const Loader = ({ text }) => {
  return (
    <div className="loader">
      <h2>Loading {text}</h2>
      <RotatingLines
        visible={true}
        height="106"
        width="200"
        color="gray"
        strokeWidth="4"
        animationDuration="1"
        ariaLabel="rotating-lines-loading"
        wrapperStyle={{}}
        wrapperClass=""
      />
    </div>
  );
};

export default Loader;
