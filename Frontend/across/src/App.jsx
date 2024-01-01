import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ShowModules from "./pages/ShowModules";
import UniversitySelection from "./pages/UniversitySelection";
import HomePage from "./pages/user/HomePage/HomePage";
import AcrossUniversitiesPage from "./pages/user/AcrossUniversitiesPage/AcrossUniversitiesPage";
import MyProfile from "./pages/user/MyProfile/MyProfile";
import Settings from "./pages/user/Settings/Settings";
import Services from "./pages/user/Services/Services";
import Modules from "./pages/user/Modules/Modules";
import Courses from "./pages/user/Courses/Courses";
import Applications from "./pages/user/Applications/Applications";
import PageNotFound from "./pages/PageNotFound";
import { gapi } from "gapi-script";
import UserPage from "./pages/UserPage";
import AdminPanel from "./admin/AdminPanel";


const App = () => {

  useEffect(() => {
    gapi.load("client:auth2", () => {
      gapi.client.init({
        clientId:
          "939129256680-qe0149eq0b5g9oc14cj3lc78inbue6rq.apps.googleusercontent.com",
        plugin_name: "chat",
      });
    });

  }, []);
  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/campus-flow/login" exact element={<Login />} />
          <Route path="/campus-flow/register" exact element={<Register />} />
          <Route path="/modules" exact element={<ShowModules />} />
          <Route
            path="/select-university"
            exact
            element={<UniversitySelection />}
          />

          <Route path="/campus-flow/user/home" exact element={<HomePage />} />
          <Route
            path="/campus-flow/user/universities"
            exact
            element={<AcrossUniversitiesPage />}
          />
          <Route
            path="/campus-flow/user/profile"
            exact
            element={<MyProfile />}
          />
          <Route
            path="/campus-flow/user/settings"
            exact
            element={<Settings />}
          />
          <Route
            path="/campus-flow/user/services"
            exact
            element={<Services />}
          />
          <Route
            path="/campus-flow/user/applications"
            exact
            element={<Applications />}
          />
          <Route path="/campus-flow/user/modules" exact element={<Modules />} />
          <Route path="/campus-flow/user/courses" exact element={<Courses />} />
          <Route path="*" element={<PageNotFound />} />
          <Route  path="/register"
            element={<Register />}
            onClick={() => {
              const history = useNavigate();
              history("/"); // Update this to the actual path of your homepage
            }}
          />
          <Route path="/user" exact element={<UserPage />} />

          <Route path="/admin/*" element={<AdminPanel />} />
          {/* Other routes */}

        </Routes>
      </BrowserRouter>
    </div>
  );
};

export default App;
