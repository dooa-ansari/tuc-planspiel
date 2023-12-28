import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ShowModules from "./pages/ShowModules";
import UniversitySelection from "./pages/UniversitySelection";
import HomePage from "./pages/user/HomePage/HomePage";

const App = () => {
  return (
    <div className="app">
      <BrowserRouter>
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/login" exact element={<Login />} />
          <Route path="/register" exact element={<Register />} />
          <Route path="/modules" exact element={<ShowModules />} />
          <Route
            path="/select-university"
            exact
            element={<UniversitySelection />}
          />

          <Route path="/campus-flow/home" exact element={<HomePage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
};

export default App;
