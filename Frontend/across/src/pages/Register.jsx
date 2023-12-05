import React from "react";
import "../assets/css/Register.css";
import google from "../assets/google_logo_icon.png";
import emailSvg from "../assets/email_icon.svg";
import resigterSvg from "../assets/registerPage_highschool.svg";

const Register = () => {
  return (
    <div className="register">
      <div className="register__wrapper">
        <div className=" register__left">
          <h2 className="register__title">Sign up</h2>
          <form action="#" className="register__form">
            <button className="signupgoogle__button" type="button">
              <div className="singupgoogle__image">
                <img src={google} alt="" />
              </div>
              Sign up with Google
            </button>
            <button className="signupemail__button" type="button">
              <div className="singupemail__image">
                <img src={emailSvg} alt="" />
              </div>
              Sign up with Email
            </button>
          </form>
          <p className="register__already-account">
            Already have account?{" "}
            <span
              style={{
                color: "#439a86",
                fontWeight: "600",
                cursor: "pointer",
                textDecoration: "underline",
              }}
            >
              Log in
            </span>
          </p>
        </div>
        <div className="register__right">
          <img className="register__characterSvg" src={resigterSvg} alt="" />
        </div>
      </div>
    </div>
  );
};

export default Register;
