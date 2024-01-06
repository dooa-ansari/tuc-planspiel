import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ShowModules from "./pages/ShowModules";
import { gapi } from "gapi-script";
import UserPage from "./pages/UserPage";
import AdminPanel from "./admin/AdminPanel";
import 'bootstrap/dist/css/bootstrap.min.css';


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
          <Route path="/login" exact element={<Login />} />
          <Route path="/register" exact element={<Register />} />
          <Route path="/modules" exact element={<ShowModules />} />
          <Route
            path="/register"
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
