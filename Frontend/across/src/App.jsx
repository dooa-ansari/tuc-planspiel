import React from "react";

import "./App.css";
import Header from "./components/Header";
import LandingContent from "./components/LandingContent";
import About from "./components/About";

const App = () => {
  return (
    <>
      <Header brandName="Across" />
      <div className="siteContents">
        <LandingContent
          title="Across Student Service"
          description=" Lorem ipsum, dolor sit amet consectetur adipisicing elit."
        />
        <About />
      </div>
    </>
  );
};

export default App;
