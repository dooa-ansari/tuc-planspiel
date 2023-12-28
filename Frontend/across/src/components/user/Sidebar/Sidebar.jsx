import React from "react";
import "./Sidebar.css";
import { Link } from "react-router-dom";

// sidebar top icons imports
import { MdDashboard } from "react-icons/md";
import { FaBook, FaBookOpen, FaServicestack } from "react-icons/fa";
import { RiSchoolFill, RiAppsFill } from "react-icons/ri";

// sidebar bottom icon imports
import { MdSettings } from "react-icons/md";
import { FaUserCircle } from "react-icons/fa";

const Sidebar = () => {
  return (
    <>
      <aside className="sidebar">
        <div className="sidebar__contents">
          <div className="sidebar__top">
            <ul className="sidebar__top__links">
              <Link
                to="https://www.google.com"
                target="_blank"
                className="sidebar__top__link"
              >
                <MdDashboard />
                <span>Dashboard</span>
              </Link>
              <Link className="sidebar__top__link">
                <FaBook />
                <span>Courses</span>
              </Link>
              <Link className="sidebar__top__link">
                <FaBookOpen />
                <span>Courses</span>
              </Link>
              <Link className="sidebar__top__link">
                <RiSchoolFill />
                <span>Universities</span>
              </Link>
              <Link className="sidebar__top__link">
                <RiAppsFill />
                <span>Applications</span>
              </Link>
              <Link className="sidebar__top__link">
                <FaServicestack />
                <span>Services</span>
              </Link>
            </ul>
          </div>
          <div className="sidebar__bottom">
            <ul className="sidebar__bottom__links">
              <Link className="sidebar__bottom__link">
                <FaUserCircle />
                <span> My Profile</span>
              </Link>
              <Link className="sidebar__bottom__link">
                <MdSettings />
                <span>Settings</span>
              </Link>
            </ul>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
