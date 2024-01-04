import "../assets/css/Login.css";
import googleSvg from "../assets/google_icon.svg";
import loginSvg from "../assets/loginPage_characterSet.svg";
import GoogleLogin from "react-google-login";
import axios from "axios";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import the useNavigate hook
import Button from "../components/Button/Button";
import { login } from "../api/userApi";

const Login = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleFormSubmit = async evt => {
    evt.preventDefault();

    const data = { email, password };

    try {
      const response = await login(data);

      console.log(response.data);
      console.log(response.data.user);

      // const authToken = response.data.token;
      // localStorage.setItem("authToken", authToken);

      // const role = response.data.data.role;
      // if (role === "ADMIN") {
      //   navigate("/admin/home");
      // } else {
      //   navigate("/campus-flow/user/home");
      // }
    } catch (error) {
      console.error("Error during login:", error);
    }

    // const handleGoogleLogin = async googleUser => {
    //   try {
    //     const response = await axios.post(
    //       "http://127.0.0.1:8000/polls/google/signin",
    //       {
    //         access_token: googleUser.getAuthResponse().id_token,
    //         email,
    //         password,
    //       }
    //     );
    //     const role = response.data.data.role;

    //     if (role === "ADMIN") {
    //       // If the role is ADMIN, navigate to /admin/home
    //       navigate("/admin/home");
    //     } else {
    //       // If the role is not ADMIN, navigate to /user
    //       navigate("/user");
    //     }

    //     const authToken = response.data.token;
    //     localStorage.setItem("authToken", authToken);

    //     console.log(response);
    //   } catch (error) {
    //     console.error("Error during Google login:", error);
    //   }
    // };
  };

  return (
    <div className="login">
      <div className="login__wrapper">
        <div className="login__left">
          <img className="login__characterSvg" src={loginSvg} alt="" />
        </div>
        <div className="login__right">
          <h2 className="login__title">Log in</h2>
          <form onSubmit={handleFormSubmit} className="login__form">
            <input
              type="email"
              className="login__email"
              placeholder="Email"
              value={email}
              onChange={evt => setEmail(evt.target.value)}
              required
            />
            <input
              type="password"
              className="login__password"
              placeholder="Password"
              value={password}
              onChange={evt => setPassword(evt.target.value)}
              required
            />
            <Button primary rounded={true}>
              Let's Start
            </Button>
          </form>

          {/* snapple separator with or text in the middle */}
          {/* start */}
          <div className="login__alternate-signin-container">
            <div className="login__or-separator snapple-seperator">
              <span className="login__or-text">or</span>
            </div>
            <GoogleLogin
              clientId="939129256680-qe0149eq0b5g9oc14cj3lc78inbue6rq.apps.googleusercontent.com"
              buttonText={
                <img className="login__image" src={googleSvg} alt="" />
              }
              // onSuccess={handleGoogleLogin}
              onFailure={error =>
                console.error("Google Sign-In failed:", error)
              }
              cookiePolicy="single_host_origin"
            />
          </div>
          {/* end */}

          {/*  */}
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
