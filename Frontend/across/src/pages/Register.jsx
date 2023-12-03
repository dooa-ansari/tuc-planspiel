import React from "react";
import "../assets/css/register.css"
import google from "../assets/google_icon.svg";
import emailSvg from "../assets/email_icon.svg";
import eclips from "../assets/eclipse_image.svg";
import resigterSvg from "../assets/registerPage_highschool.svg";

const Register = () => {
  return (
  <div className="register">
    < div className="register__wrapper">
      <div className=" register__left">
        <h2 className="register__title">Sign up</h2>
        <from action= "#" className ="register__from">
          <button className="signupgoogle__button" type="button">
          <img className="singupgoogle__image" src={google} alt="" />
          <img className="eclips__image" src={eclips} alt="" />
            Sign up with Google
          </button>
          <button className="signupemail__button" type="button">
          <img className="singupemail__image" src={emailSvg} alt="" />
          <img className="eclips__image" src={eclips} alt="" />
            Sign up with Email
          </button>
        </from>
        <p className="register__already-account">
          Already have account?{" "}
            <span
              style={{ color: "#439a86", fontWeight: "600", cursor: "pointer" }}>
              Log in
            </span>
            </p>
      </div>
      <div className="register__right">
          <img className="register__characterSvg" src={resigterSvg} alt="" />
        </div>
   </div>
  </div>
  )
};

export default Register;
