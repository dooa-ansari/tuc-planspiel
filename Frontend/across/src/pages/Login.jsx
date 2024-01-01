import React from "react";
import { useNavigate } from "react-router-dom";
import "../assets/css/Login.css";
import googleSvg from "../assets/google_icon.svg";
import loginSvg from "../assets/loginPage_characterSet.svg";

const Login = () => {
  const navigate = useNavigate();
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

          {/* snapple separator with or text in the middle */}
          {/* start */}
          <div className="login__alternate-signin-container">
            <div className="login__or-separator snapple-seperator">
              <span class="login__or-text">or</span>
            </div>
            <img className="login__image" src={googleSvg} alt="" />
          </div>
          {/* end */}

          <p className="login__register-redirect">
            Don’t have an account?{" "}
            <span
              style={{
                color: "#439a86",
                fontWeight: "500",
                cursor: "pointer",
                textDecoration: "underline",
              }}
            >
              <a onClick={() => navigate("/campus-flow/register")}>Sign up</a>
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
