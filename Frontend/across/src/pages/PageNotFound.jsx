import React from "react";
import "../assets/css/PageNotFound.css";
import pnfImage from "../assets/images/pnf-image.svg";

const PageNotFound = () => {
  return (
    <div className="pnf">
      <img className="pnf__image" src={pnfImage} alt="" />
      <h1 className="pnf__title">Page Not Found</h1>
      <p>Something went wrong..</p>
      <button type="button" className="pnf__button">
        Go back
      </button>
    </div>
  );
};

export default PageNotFound;
