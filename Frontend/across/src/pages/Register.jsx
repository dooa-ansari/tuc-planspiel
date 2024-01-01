import React from "react";
import { useNavigate } from "react-router-dom";

// @css imports
import React, { useEffect } from "react";
import "../assets/css/Register.css";

// @image imports
import google from "../assets/google_logo_icon.png";
import resigterSvg from "../assets/registerPage_highschool.svg";
import axios from "axios";
import GoogleLogin from "react-google-login";
import { useNavigate } from "react-router-dom"; // Import the useNavigate hook

const Register = () => {
  const navigate = useNavigate(); // Use the useNavigate hook

  const handleGoogleSignup = async googleUser => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/polls/google/signin",
        {
          access_token: googleUser.getAuthResponse().id_token,
        }
      );
      const authToken = response.data.token;
      localStorage.setItem("authToken", authToken);

      console.log(response.data);
      navigate("/user");
    } catch (error) {
      console.error("Error during Google login:", error);
    }
  };
  const handleGoogleLogout = async () => {
    localStorage.removeItem("authToken");
    window.location.href = "/login";
  };

  useEffect(() => {
    // Check if the user is already authenticated
    // If yes, redirect them to the user profile page
    const checkAuthentication = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/polls/user/profile",
          {
            withCredentials: true,
          }
        );

        if (response.data.username) {
          // User is authenticated, redirect to the user profile page
          navigate("/user");
        }
      } catch (error) {
        console.error("Error checking authentication:", error);
      }
    };

    checkAuthentication();
  }, [navigate]);

  return (
    <div className="register">
      <div className="register__wrapper">
        <div className="register__left">
          <h2 className="register__title">Sign up</h2>
          <form action="#" className="register__form">
            <button className="signupgoogle__button" type="button">
              <GoogleLogin
                clientId="939129256680-qe0149eq0b5g9oc14cj3lc78inbue6rq.apps.googleusercontent.com"
                buttonText="Sign up with Google"
                onSuccess={handleGoogleSignup}
                onFailure={error =>
                  console.error("Google Sign-In failed:", error)
                }
                cookiePolicy="single_host_origin"
              />
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
              <option value="">
                Technical University of Chemnitz (Germany)
              </option>
              <option value="">
                Bialystok University of Technology (Poland)
              </option>
              <option value="">University of Craiova (Romania)</option>
              <option value="">University of Girona (Catalonia/Spain)</option>
              <option value="">University of Nova Gorica (Slovenia)</option>
              <option value="">University of Perpignan (France)</option>
              <option value="">University of Ruse (Bulgaria)</option>
              <option value="">Other</option>
            </select>
            <button className="register__button" type="button">
              Sign Up
            </button>
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
        </div>
        <div className="register__right">
          <img className="register__characterSvg" src={resigterSvg} alt="" />
        </div>
        <button onClick={handleGoogleLogout}>Logout from Google</button>
      </div>
    </div>
  );
};

export default Register;
