import React from "react";
import "./Navbar.css";
import { Link } from "react-router-dom";
import { FaUserGraduate } from "react-icons/fa";
import { FaBell } from "react-icons/fa";
import { RiLogoutBoxRFill } from "react-icons/ri";

import enLanSvg from "../../../assets/images/en.svg";

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
                <button id="menu-button">
                  <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                    <rect
                      width="40"
                      height="40"
                      rx="20"
                      fill="black"
                      fillOpacity="0.1"
                    />
                    <path
                      d="M12.9719 16H25C25.5531 16 26 15.5531 26 15C26 14.4469 25.5531 14 25 14H12.9719C12.4478 14 12 14.4478 12 14.9719C12 15.4959 12.4478 16 12.9719 16ZM27 19H14.9719C14.4478 19 14 19.4469 14 20C14 20.5531 14.4478 21 14.9719 21H26.9719C27.5531 21 28 20.5531 28 20C28 19.4469 27.5531 19 27 19ZM25 24H12.9719C12.4478 24 12 24.4469 12 24.9719C12 25.4969 12.4478 26 12.9719 26H25C25.5531 26 26 25.5531 26 25C26 24.4469 25.5531 24 25 24Z"
                      fill="black"
                      fillOpacity="0.6"
                    />
                  </svg>
                </button>
                <button id="menu-close-button">
                  <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                    <rect
                      width="40"
                      height="40"
                      rx="20"
                      fill="black"
                      fillOpacity="0.1"
                    />

                    <path
                      d="M12.9719 16H30C30.5531 16 31 15.5531 31 15C31 14.4469 30.5531 14 30 14H12.9719C12.4478 14 12 14.4478 12 14.9719C12 15.4959 12.4478 16 12.9719 16Z"
                      fill="black"
                      fillOpacity="0.6"
                      transform="translate(-6, 25) rotate(-45)"
                    />
                    <path
                      d="M12.9719 26H30C30.5531 26 31 25.5531 31 25C31 24.4469 30.5531 24 30 24H12.9719C12.4478 24 12 24.4478 12 24.9719C12 25.4959 12.4478 26 12.9719 26Z"
                      fill="black"
                      fillOpacity="0.6"
                      transform="translate(21, -12) rotate(45)"
                    />
                  </svg>
                </button>
              </ul>
            </nav>
          </header>
        </div>
      </section>
    </>
  );
};

export default Navbar;
