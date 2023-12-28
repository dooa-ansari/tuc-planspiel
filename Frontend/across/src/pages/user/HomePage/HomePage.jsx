import React from "react";
import "./HomePage.css";
import MainLayout from "../../../components/user/MainLayout/MainLayout";

const HomePage = () => {
  return (
    <>
      <MainLayout>
        <h2 style={{ textAlign: "center" }}>Contents of HomePage</h2>
        <p style={{ textAlign: "center" }}>
          for testing random images from a source
        </p>

        <h4>Lorem, ipsum.</h4>
        <p>
          Lorem ipsum, dolor sit amet consectetur adipisicing elit. Commodi
          veniam totam enim inventore. Debitis facilis odit enim provident
          dolores magnam, quas nobis suscipit quo porro inventore, cum id
          quaerat, similique ad ratione quasi saepe laudantium consequatur
          dolorum itaque nemo. Facere quisquam cum doloremque ut ipsa illum fuga
          in nisi aliquam alias mollitia blanditiis voluptates odio inventore
          dignissimos maiores, incidunt vel veniam tempora. Labore, nisi
          consequuntur quia ad assumenda obcaecati ut vel aperiam laborum cumque
          quam rem itaque cum est accusamus illo a fugiat corporis aliquid
          beatae totam modi qui consequatur odio. Vitae placeat aliquam
          blanditiis. Architecto ipsum eaque error blanditiis.
        </p>
        <div className="homepage__images">
          <img
            src="https://source.unsplash.com/random/400x400?landscape"
            alt=""
          />
          <img
            src="https://source.unsplash.com/random/400x400?landscape"
            alt=""
          />
          <img
            src="https://source.unsplash.com/random/400x400?landscape"
            alt=""
          />
          <img
            src="https://source.unsplash.com/random/400x400?landscape"
            alt=""
          />
          <img
            src="https://source.unsplash.com/random/400x400?landscape"
            alt=""
          />
          <img
            src="https://source.unsplash.com/random/400x400?landscape"
            alt=""
          />
          <img
            src="https://source.unsplash.com/random/400x400?landscape"
            alt=""
          />
        </div>
      </MainLayout>
    </>
  );
};

export default HomePage;
