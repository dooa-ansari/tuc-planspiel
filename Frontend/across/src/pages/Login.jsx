import React from "react";
import "../assets/css/Login.css";
import googleSvg from "../assets/google_icon.svg";
import loginSvg from "../assets/loginPage_characterSet.svg";

const Login = () => {
  return (
    <div className="login">
      <div className="login__wrapper">
        <div className="login__left">
          <img className="login__characterSvg" src={loginSvg} alt="" />
        </div>
        <div className="login__right">
          <h2 className="login__title">Log in</h2>
          <form action="#" className="login__form">
            <input
              type="email"
              className="login__email"
              name=""
              id=""
              placeholder="Email"
              required
            />
            <input
              type="password"
              className="login__password"
              name=""
              id=""
              placeholder="Password"
              required
            />
            <button className="login__button" type="button">
              Let's Start
            </button>
          </form>
          <img className="login__image" src={googleSvg} alt="" />
          <p className="login__register-redirect">
            Don’t have an account?{" "}
            <span
              style={{ color: "#439a86", fontWeight: "600", cursor: "pointer" }}
            >
              Sign up
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
