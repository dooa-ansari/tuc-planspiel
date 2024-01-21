import React from "react";
import "../assets/css/Footer.css";
import facebookIcon from "../assets/social_media_icons/facebook.png";
import linkedinIcon from "../assets/social_media_icons/linkedin.png";
import xIcon from "../assets/social_media_icons/x.png";
import companyLogo from "../assets/images/brandLogo.png";
import phoneIcon from "../assets/contact_icons/phone.png";
import messageIcon from "../assets/contact_icons/message.png";
import locationIcon from "../assets/contact_icons/location.png";

const Footer = () => {
  const date = new Date();
  const year = date.getFullYear();
  return (
    <div className="footer">
      <div className="footer__contents">
        <div className="footer__left">
          <h4 className="footer__subHeading">Follow Us</h4>
          <div className="footer__social-handles">
            <img src={facebookIcon} alt="" />
            <img src={linkedinIcon} alt="" />
            <img src={xIcon} alt="" />
          </div>
        </div>
        <div className="footer__middle">
          <div className="company__logo">
            <img src={companyLogo} alt="" />
          </div>
          <h4 className="footer__subHeading company__initiative">
            Student Service for Across European Cross-Border University
          </h4>
        </div>
        <div className="footer__right">
          <h4 className="footer__subHeading">Contact Us</h4>
          <div className="footer__right-contactIcons">
            <img src={phoneIcon} alt="" />
            <img src={messageIcon} alt="" />
            <img src={locationIcon} alt="" />
          </div>
        </div>
      </div>
      <div className="footer__bottom-contents">
        <div className="footer__copyright-text">
          <small>
            Copyright &copy; <span id="copyright"> {year}</span> Web Wizards.
            All rights reserved
          </small>
        </div>
        <div className="footer__disclaimer-text text-center">
          <small>
            Disclaimer: This website is not associated with an actual company
            but is a part of a web engineering project called Planspiel at the
            Technical University of Chemnitz.
          </small>
        </div>
      </div>
    </div>
  );
};

export default Footer;
