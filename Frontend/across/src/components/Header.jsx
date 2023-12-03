import React from "react";
import "../assets/css/Header.css";
import { Link } from "react-scroll";
import { NavLink } from "react-router-dom";
import brandLogo from "../assets/brandLogo.png";

const duration = 500;
const Header = ({ brandName }) => {
  return (
    <div className="header">
      <div className="header__contents">
        <div className="header__left">
          <NavLink to="/">
            <img src={brandLogo} className="header__brandImage" />
          </NavLink>
        </div>
        <div className="header__middle">
          <ul className="header__links">
            <li className="header__link">
              <Link activeClass="active" to="#" spy smooth duration={duration}>
                Home
              </Link>
            </li>
            <li className="header__link">
              <Link activeClass="active" to="#" spy smooth duration={duration}>
                About
              </Link>
            </li>
            <li className="header__link">
              <Link activeClass="active" to="#" spy smooth duration={duration}>
                Universities
              </Link>
            </li>
            <li className="header__link">
              <Link activeClass="active" to="#" spy smooth duration={duration}>
                ACROSS
              </Link>
            </li>
            <li className="header__link">
              <Link activeClass="active" to="#" spy smooth duration={duration}>
                Reach Us
              </Link>
            </li>
          </ul>
        </div>
        <div className="header__right">
          <li className="header__link">
            <NavLink className="login__link" to="login">
              Log in
            </NavLink>
          </li>
          <li className="header__link header__signup-btn">
            <NavLink className="register__link" to="register">
              Sign Up
            </NavLink>
          </li>
        </div>
      </div>
    </div>
  );
};

export default Header;
