import React from "react";

import "./App.css";
import blogBanner from "./assets/BlogBanner.png";
import Header from "./components/Header";
import LandingContent from "./components/LandingContent";
import LandingImage from "./components/LandingImage";
import About from "./components/About";
import ShowModules from "./screens/show_modules/ShowModules";

const App = () => {
  return (
    <>
      <ShowModules/>
      <Header brandName="Across" />
      <div className="siteContents">
        <LandingImage source={blogBanner} title="Student Service" />
        {/* <LandingContent
          title="Across Student Service"
          description=" Lorem ipsum, dolor sit amet consectetur adipisicing elit."
        /> */}
        <About />
      </div>
    </>
  );
};

export default App;
