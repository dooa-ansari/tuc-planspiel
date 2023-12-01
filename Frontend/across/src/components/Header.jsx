import React from "react";
import "../assets/css/Header.css";
import { Link } from "react-scroll";

const duration = 500;
const Header = ({ brandName }) => {
  return (
    <div className="header">
      <div className="header__contents">
        <h2 className="header__brandName">{brandName}</h2>
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
          <li className="header__link header__signup-btn">
            <Link to="#" spy smooth duration={duration}>
              Create Account
            </Link>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Header;
