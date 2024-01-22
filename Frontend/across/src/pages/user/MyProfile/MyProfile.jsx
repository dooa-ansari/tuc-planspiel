import React from "react";
import MainLayout from "../../../components/user/MainLayout/MainLayout";
import { useAuth } from "../../../context/AuthContext";
import "./MyProfile.css";
import Gravatar from "../../../components/Gravatar/Gravatar";
import { Tab } from "react-bootstrap";
import { Tabs } from "react-bootstrap";
import { FaTrash } from "react-icons/fa6";

const MyProfile = () => {
  const [auth] = useAuth();

  return (
    <>
      <MainLayout>
        <div className="myProfile">
          <Tabs
            defaultActiveKey="profileDetails"
            id="myProfile-tab"
            className="mb-3"
          >
            <Tab eventKey="profileDetails" title="Profile Details">
              <div className="myProfile__contents">
                <div className="myProfile__userDetails">
                  <div>
                    <Gravatar fullName={auth.user.full_name} size={80} />
                  </div>

                  <h4
                    style={{
                      padding: "0.5rem 0",
                      margin: "0.5rem 0",
                      textAlign: "center",
                    }}
                  >
                    {auth.user.full_name}
                  </h4>
                  <div className="myProfile__dataList">
                    <div className="myProfile__emailGroup">
                      <h4>Email</h4>
                      <p>{auth.user.email}</p>
                    </div>
                    <div className="myProfile__roleGroup">
                      <h4>Current Role</h4>
                      <p>{auth.user.role}</p>
                    </div>
                  </div>
                </div>
                <div className="optedCourses">
                  <h4>Completed Modules List</h4>
                  <table>
                    <thead>
                      <tr>
                        <th>Modules</th>
                        <th>Credits Earned</th>
                        <th>Options</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Advance Management of Data</td>
                        <td>5</td>
                        <td className="tdTrashIcon">
                          <FaTrash />
                        </td>
                      </tr>
                      <tr>
                        <td>Seminar Web Engineering</td>
                        <td>5</td>
                        <td className="tdTrashIcon">
                          <FaTrash />
                        </td>
                      </tr>
                      <tr>
                        <td>Module 3</td>
                        <td>2</td>
                        <td className="tdTrashIcon">
                          <FaTrash />
                        </td>
                      </tr>
                      <tr>
                        <td>Module 4</td>
                        <td>4</td>
                        <td className="tdTrashIcon">
                          <FaTrash />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </Tab>
            <Tab eventKey="profile" title="Academic Data">
              <p>
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Iusto
                suscipit quae voluptate magnam esse quibusdam repellendus
                aspernatur nisi necessitatibus accusantium commodi saepe,
                officiis, nam iste porro laboriosam ratione. Obcaecati
                voluptatum voluptas dolore iusto. Mollitia architecto cupiditate
                eum quasi ipsa obcaecati necessitatibus, delectus rerum labore,
                sint ea adipisci quia eaque possimus.#
              </p>
            </Tab>
          </Tabs>
        </div>
      </MainLayout>
    </>
  );
};

export default MyProfile;
