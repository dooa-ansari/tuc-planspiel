import React, { useEffect, useState } from "react";
import "../assets/css/Register.css";
import google from "../assets/google_logo_icon.png";

import resigterSvg from "../assets/registerPage_highschool.svg";
import axios from "axios";
import GoogleLogin from "react-google-login";
import { useNavigate } from "react-router-dom";
import Button from "../components/Button/Button";
import { useAuth } from "../context/AuthContext";

const Register = () => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [auth, setAuth] = useAuth();

  const handleRegister = async evt => {
    evt.preventDefault();
    const data = { name, email, password, confirmPassword };
  };

  // const handleGoogleSignup = async googleUser => {
  //   try {
  //     const response = await axios.post(
  //       "http://127.0.0.1:8000/polls/google/signin",
  //       {
  //         access_token: googleUser.getAuthResponse().id_token,
  //       }
  //     );
  //     const authToken = response.data.token;
  //     localStorage.setItem("authToken", authToken);

  //     console.log(response.data);
  //     navigate("/user");
  //   } catch (error) {
  //     console.error("Error during Google login:", error);
  //   }
  // };
  // const handleGoogleLogout = async () => {
  //   localStorage.removeItem("authToken");
  //   window.location.href = "/login";
  // };

  // useEffect(() => {
  //   // Check if the user is already authenticated
  //   // If yes, redirect them to the user profile page
  //   const checkAuthentication = async () => {
  //     try {
  //       const response = await axios.get(
  //         "http://127.0.0.1:8000/polls/user/profile",
  //         {
  //           withCredentials: true,
  //         }
  //       );

  //       if (response.data.username) {
  //         // User is authenticated, redirect to the user profile page
  //         navigate("/user");
  //       }
  //     } catch (error) {
  //       console.error("Error checking authentication:", error);
  //     }
  //   };

  //   checkAuthentication();
  // }, [navigate]);

  return (
    <div className="register">
      <div className="register__wrapper">
        <div className="register__left">
          <h2 className="register__title">Sign up</h2>
          <form action="#" className="register__form">
            {/* <button className="signupgoogle__button" type="button">
              <GoogleLogin
                clientId="939129256680-qe0149eq0b5g9oc14cj3lc78inbue6rq.apps.googleusercontent.com"
                buttonText="Sign up with Google"
                onSuccess={handleGoogleSignup}
                onFailure={error =>
                  console.error("Google Sign-In failed:", error)
                }
                cookiePolicy="single_host_origin"
              />
            </button> */}
          </form>
          <p className="register__already-account">
            Already have account?{" "}
            <span
              style={{
                color: "#439a86",
                fontWeight: "500",
                cursor: "pointer",
                textDecoration: "underline",
              }}
            >
              <a onClick={() => navigate("/campus-flow/login")}>Log in</a>
            </span>
          </p>
          <form action="#" className="register__form">
            <input
              type="text"
              value={name}
              onChange={evt => setName(evt.target.value)}
              className="register__name"
              name="name"
              id="name"
              placeholder="Name"
              required
            />
            <input
              type="email"
              value={email}
              onChange={evt => setEmail(evt.target.value)}
              name="email"
              className="register__email"
              id="email"
              placeholder="Email"
              required
            />
            <input
              type="password"
              value={password}
              onChange={evt => setPassword(evt.target.value)}
              className="register__password"
              name="password"
              id="password"
              placeholder="Password"
              required
            />
            <input
              type="password"
              value={confirmPassword}
              onChange={evt => setConfirmPassword(evt.target.value)}
              className="register__confirmPassword"
              name="confirmPassword"
              id="confirmPassword"
              placeholder="Confirm Password"
              required
            />

            <Button primary rounded onClick={handleRegister}>
              Sign Up
            </Button>
          </form>

          {/* snapple separator with or text in between */}
          {/* start */}
          <div className="register__alternate-signin-container">
            <div className="register__or-separator">
              <span className="register__or-text">or</span>
            </div>
            <button className="signupgoogle__button" type="button">
              <div className="singupgoogle__image">
                <img src={google} alt="" />
              </div>
              Continue with Google
            </button>
          </div>
          {/* end */}
          {/* <button onClick={handleGoogleLogout}>Logout from Google</button> */}
        </div>
        <div className="register__right">
          <img className="register__characterSvg" src={resigterSvg} alt="" />
        </div>
      </div>
    </div>
  );
};

export default Register;
