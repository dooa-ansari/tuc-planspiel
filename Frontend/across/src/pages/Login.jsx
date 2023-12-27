import "../assets/css/Login.css";
import googleSvg from "../assets/google_icon.svg";
import loginSvg from "../assets/loginPage_characterSet.svg";
import GoogleLogin from "react-google-login";
import axios from "axios";
import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";  // Import the useNavigate hook


const Login = () => {
  const navigate = useNavigate(); // Import and use useNavigate

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const handleGoogleLogin = async (googleUser) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/polls/google/signin', {
        access_token: googleUser.getAuthResponse().id_token,
        email,
        password,
      });
      const role = response.data.data.role;

      if (role === 'ADMIN') {
        // If the role is ADMIN, navigate to /admin/home
        navigate('/admin/home');
      } else {
        // If the role is not ADMIN, navigate to /user
        navigate('/user');
      }

      const authToken = response.data.token;
      localStorage.setItem('authToken', authToken);

      console.log(response);
    } catch (error) {
      console.error('Error during Google login:', error);
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    try {
      // Send email and password to the backend
      const response = await axios.post('http://127.0.0.1:8000/polls/login', {
        email,
        password,
      });

      // Handle the response as needed
      console.log(response);

      // Assuming there's a token in the response, you can store it in localStorage
      const authToken = response.data.token;
      localStorage.setItem('authToken', authToken);

      // Redirect the user based on their role
      const role = response.data.data.role;
      if (role === 'ADMIN') {
        navigate('/admin/home');
      } else {
        navigate('/user');
      }
    } catch (error) {
      console.error('Error during login:', error);
    }
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
              value={email} // Add this line to bind the value to the state
              onChange={(e) => setEmail(e.target.value)} // Add this line to handle changes
              required
            />
            <input
              type="password"
              className="login__password"
              placeholder="Password"
              value={password} // Add this line to bind the value to the state
              onChange={(e) => setPassword(e.target.value)} // Add this line to handle changes
              required
            />
            <button className="login__button" type="submit">
              Let's Start
            </button>
          </form>
          <GoogleLogin
            clientId="939129256680-qe0149eq0b5g9oc14cj3lc78inbue6rq.apps.googleusercontent.com"
            buttonText="Sign up with Google"
            onSuccess={handleGoogleLogin}
            onFailure={(error) => console.error("Google Sign-In failed:", error)}
            cookiePolicy="single_host_origin"
          />
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
