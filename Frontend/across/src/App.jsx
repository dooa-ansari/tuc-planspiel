import React from "react";
import "./App.css";
import blogBanner from "./assets/BlogBanner.png";
import Header from "./components/Header";
import LandingContent from "./components/LandingContent";
import LandingImage from "./components/LandingImage";
import About from "./components/About";
import CourseFinder from "./components/CourseFinder";
import CourseComparison from "./components/CourseComparison";
import Footer from "./components/Footer";

const App = () => {
  return (
    <>
      <Header brandName="Across" />
      <div className="siteContents">
        <LandingImage source={blogBanner} title="Student Service" />
        {/* <LandingContent
          title="Across Student Service"
          description=" Lorem ipsum, dolor sit amet consectetur adipisicing elit."
        /> */}
        <About />
        <CourseFinder />
        <CourseComparison />
        <Footer />
      </div>
    </>
  );
};

export default App;
