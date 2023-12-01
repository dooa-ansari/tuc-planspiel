import React from "react";
import "../assets/css/LandingContent.css";

const LandingContent = ({ title, description }) => {
  return (
    <>
      <section id="home">
        <div className="landingContent" style={{ paddingTop: "230px" }}>
          <div className="landingContent__div1"></div>
          <div className="landingContent__div2"></div>
          <div className="landingContent__details">
            <h2>{title}</h2>
            <p>{description}</p>
          </div>
        </div>
      </section>
    </>
  );
};

export default LandingContent;
