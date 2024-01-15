import React from "react";
import blogBanner from "../assets/images/BlogBanner.png";
import Header from "../components/Header";
import LandingContent from "../components/LandingContent";
import LandingImage from "../components/LandingImage";
import About from "../components/About";
import CourseFinder from "../components/CourseFinder";
import CourseComparison from "../components/CourseComparison";
import Footer from "../components/Footer";

const Home = () => {
  return (
    <>
      <div className="home">
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
      </div>
    </>
  );
};

export default Home;
