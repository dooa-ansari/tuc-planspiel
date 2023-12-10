import React from "react";
import "../assets/css/Register.css";
import google from "../assets/google_logo_icon.png";
import emailSvg from "../assets/email_icon.svg";
import resigterSvg from "../assets/registerPage_highschool.svg";

const Register = () => {
  return (
    <div className="register">
      <div className="register__wrapper">
        <div className="register__left">
          <h2 className="register__title">Sign up</h2>
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
          <form action="#" className="register__form">
            <input
              type="text"
              className="register__name"
              name=""
              id=""
              placeholder="Name"
              required
            />
            <input
              type="email"
              name="email"
              className="register__email"
              id="email"
              placeholder="Email"
              required
            />
            <input
              type="password"
              className="register__password"
              name="password"
              id="password"
              placeholder="Password"
              required
            />
            <select name="" className="register__universitySelection" id="">
              <option value="" disabled selected hidden>
                Select Your University
              </option>
              <option value="">Technical University of Chemnitz</option>
              <option value="">Other</option>
            </select>
            <button className="register__button" type="button">
              Sign Up
            </button>
          </form>

          <button className="signupgoogle__button" type="button">
            <div className="singupgoogle__image">
              <img src={google} alt="" />
            </div>
            Continue with Google
          </button>
        </div>
        <div className="register__right">
          <img className="register__characterSvg" src={resigterSvg} alt="" />
        </div>
      </div>
    </div>
  );
};

export default Register;
