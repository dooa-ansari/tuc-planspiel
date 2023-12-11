import React from "react";
import "../assets/css/Register.css";
import google from "../assets/google_logo_icon.png";
import emailSvg from "../assets/email_icon.svg";
import resigterSvg from "../assets/registerPage_highschool.svg";
import axios from "axios";
import GoogleLogin from "react-google-login";


const Register = () => {
  const handleGoogleSignup = async (googleUser) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/polls/google/signin', {
        access_token: googleUser.getAuthResponse().id_token,
      });

      console.log(response.data);
    } catch (error) {
      console.error('Error during Google login:', error);
    }
  };

  return (
    <div className="register">
      <div className="register__wrapper">
        <div className=" register__left">
          <h2 className="register__title">Sign up</h2>
          <form action="#" className="register__form">
            <button className="signupgoogle__button" type="button">
              <GoogleLogin
                clientId="939129256680-qe0149eq0b5g9oc14cj3lc78inbue6rq.apps.googleusercontent.com"
                buttonText="Sign up with Google"
                onSuccess={handleGoogleSignup}
                onFailure={(error) => console.error("Google Sign-In failed:", error)}
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
