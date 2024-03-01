import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import tucImage from "../../../assets/universities_images/tucImage.jpg";
import bialystokImage from "../../../assets/universities_images/bialystokImage.jpg";
import { ListGroup } from "react-bootstrap";
import { MdTranslate } from "react-icons/md";

const ModuleDetailsPage = () => {
  const location = useLocation();
  const { moduleData } = location.state || "";
  console.log(moduleData);
  const navigate = useNavigate();

  const handleBtnClick = () => {
    navigate(-1);
  };
  return (
    <div>
      {moduleData.belongs_to_university === "Bialystok University" ? (
        <img
          style={{ width: "100%", height: "60vh", objectFit: "cover" }}
          src={bialystokImage}
          alt=""
        />
      ) : (
        <img
          style={{ width: "100%", height: "60vh", objectFit: "cover" }}
          src={tucImage}
          alt=""
        />
      )}
      <ListGroup>
        <ListGroup.Item>
          Module Number: {moduleData.module_number}
        </ListGroup.Item>
        <ListGroup.Item>Module Name: {moduleData.module_name}</ListGroup.Item>
        <ListGroup.Item>
          Module Offered By: {moduleData.belongs_to_university}
        </ListGroup.Item>
        <ListGroup.Item>
          Module Content: {moduleData.module_content}
        </ListGroup.Item>
        <ListGroup.Item>
          Credit Points: {moduleData.module_credit_points}
        </ListGroup.Item>
        <ListGroup.Item>
          Module Workload: {moduleData.module_workload}
        </ListGroup.Item>
        <ListGroup.Item>Language: {moduleData.has_language}</ListGroup.Item>
      </ListGroup>
      <h2 style={{ textAlign: "center" }}>Styling to be done</h2>
      <div
        style={{
          position: "relative",
        }}
      >
        <button
          style={{
            display: "block",
            border: "none",
            outline: "none",
            padding: " 9px 16px 10px 18px",
            background: "#bcd8c1",
            borderRadius: "25px",
            color: "#121212",
            fontWeight: "500",
            marginBottom: 0,
            position: "absolute",
            left: "50%",
            transform: "translate(-50%)",
          }}
          type="button"
          onClick={handleBtnClick}
        >
          Go back
        </button>
      </div>
    </div>
  );
};

export default ModuleDetailsPage;
