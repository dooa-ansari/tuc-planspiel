import React from "react";
import "./AcrossUniversitiesPage.css";
import MainLayout from "../../../components/user/MainLayout/MainLayout";
import SearchBox from "../../../components/user/SearchBox/SearchBox";

import { AcrossUniversitiesData } from "./AcrossUniversitiesData";

const AcrossUniversitiesPage = () => {
  return (
    <>
      <MainLayout>
        <SearchBox />
        <div className="across-universities">
          <h1>List of Universities - Across Universities</h1>
          <div className="universitiesWrapper">
            {AcrossUniversitiesData.map((val, key) => {
              return (
                <div className="university" key={key}>
                  <h4 className="university-name">{val.universityName}</h4>
                  <div className="university-photo">
                    <img src={val.universityImage} alt="university in europe" />
                  </div>
                  <smalll className="university-location">
                    {val.universityLocation}
                  </smalll>
                </div>
              );
            })}
          </div>
        </div>
      </MainLayout>
    </>
  );
};

export default AcrossUniversitiesPage;
