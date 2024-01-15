import React from "react";
import "./Navbar.css";
import { Link } from "react-router-dom";
import { FaUserGraduate } from "react-icons/fa";
import { FaBell } from "react-icons/fa";
import { RiLogoutBoxRFill } from "react-icons/ri";

import enLanSvg from "../../../assets/en.svg";

import { useAuth } from "../../../context/AuthContext";

const Navbar = () => {
  const [auth, setAuth] = useAuth();

  const handleSignOut = () => {
    setAuth({ ...auth, user: null, token: "" });
    localStorage.removeItem("auth");
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  };

  return (
    <>
      <section id="navbar">
        <div className="navbar__container">
          <header className="navbar__contents">
            <h1 className="navbar__brand">
              campus<span>flow</span>
            </h1>
            <nav>
              <ul className="navbar__links">
                {auth.token && (
                  <Link className="navbar__link userName">
                    {auth.user.full_name}
                    <span>Student</span>
                  </Link>
                )}

                <Link className="navbar__link" to="/campus-flow/user/profile">
                  <FaUserGraduate />
                </Link>
                <Link className="navbar__link">
                  <FaBell />
                </Link>
                <Link
                  onClick={handleSignOut}
                  className="navbar__link"
                  to="/campus-flow/login"
                >
                  <RiLogoutBoxRFill />
                </Link>
                <Link className="navbar__link">
                  <img src={enLanSvg} alt="great britain flag" />
                </Link>
              </ul>
            </nav>
          </header>
        </div>
      </section>
    </>
  );
};

export default Navbar;
