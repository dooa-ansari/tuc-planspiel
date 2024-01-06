import React from "react";
import "./Navbar.css";
import { Link } from "react-router-dom";
import { FaUserGraduate } from "react-icons/fa";
import { FaBell } from "react-icons/fa";
import { RiLogoutBoxRFill } from "react-icons/ri";

import enLanSvg from "../../../assets/en.svg";

const Navbar = () => {
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
                <Link className="navbar__link userName">
                  John Doe
                  <span>Student</span>
                </Link>
                <Link className="navbar__link">
                  <FaUserGraduate />
                </Link>
                <Link className="navbar__link">
                  <FaBell />
                </Link>
                <Link className="navbar__link">
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
