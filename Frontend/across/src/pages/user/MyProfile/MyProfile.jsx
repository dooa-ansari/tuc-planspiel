import React from "react";
import MainLayout from "../../../components/user/MainLayout/MainLayout";
import { useAuth } from "../../../context/AuthContext";
import "./MyProfile.css";

const MyProfile = () => {
  const [auth] = useAuth();

  return (
    <>
      <MainLayout>
        <div className="myProfile">
          <h1>this is the profile page...</h1>

          <h2>Name: {auth.user.full_name}</h2>
          <h2>Email: {auth.user.email}</h2>
          <h2>Your Current Role: {auth.user.role}</h2>
        </div>
      </MainLayout>
    </>
  );
};

export default MyProfile;
