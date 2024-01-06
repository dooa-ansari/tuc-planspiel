import React from "react";
import "../assets/css/PageNotFound.css";

const PageNotFound = () => {
  return (
    <div className="pnf">
      <h1 className="pnf__title">Page Not Found</h1>
      <p>Oops! Something went wrong..</p>
      <button type="button" className="pnf__button">
        Go back
      </button>
    </div>
  );
};

export default PageNotFound;
