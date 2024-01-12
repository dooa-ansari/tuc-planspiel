import React, { useEffect, useState } from "react";
import "./TransferCredits.css";
import axios from "axios";
import MainLayout from "../../../components/user/MainLayout/MainLayout";
import Lottie from "react-lottie";
import loadingData from "../../../assets/lotties/loading_transfer_v0.json";
import germany from "../../../assets/lotties/germany_flag.json";
import poland from "../../../assets/lotties/poland_flag.json";
import AwesomeSlider from "react-awesome-slider";
import "react-awesome-slider/dist/styles.css";

const TransferCredits = () => {
  const [universities, setUniversities] = useState([]);
  const [univerisitiesLoading, setUniversitiesLoading] = useState(true);
  const [selectedUniversity, setSelectedUniverity] = useState(true);

  useEffect(() => {
    axios
      .get("http://localhost:8000/adminapp/universitieslist/")
      .then((response) => {
        if (response.status == 200) {
          console.log(response.data)
          const returnedData = response.data
          returnedData.forEach((item) => {
            item.selected = false
          })
          setUniversities(returnedData);
        }
        setUniversitiesLoading(false)
      })
      .catch((error) => {
        console.log(error);
        setUniversitiesLoading(false)
      });
  }, []);

  const defaultOptions = {
    loop: true,
    autoplay: true,
    animationData: loadingData,
    rendererSettings: {
      preserveAspectRatio: "xMidYMid slice",
    },
  };


  const onPressUniversityItem = (item) => {
    setSelectedUniverity(item)
  }
  const getFlagOptions = (id) => {
    if(id == 1){
      return {
        loop: true,
        autoplay: true,
        animationData: germany,
        rendererSettings: {
          preserveAspectRatio: "xMidYMid slice",
        },
      };
    }else if(id == 2){
       return {
        loop: true,
        autoplay: true,
        animationData: poland,
        rendererSettings: {
          preserveAspectRatio: "xMidYMid slice",
        },
      };
    }
  }

  return (
    <>
      <MainLayout>
        <h1>Transfer Credits</h1>
        <AwesomeSlider>
          <div style={{background: "white"}}>
           
           {univerisitiesLoading ? <Lottie options={defaultOptions} height={200} width={200} /> : <div>
              {universities.map((university) => {
                 return <div className={"universityItem " + (university.selected && "universityItemSelected")} key={university.id}>
                  <div className="universityItemFlag">
                  <Lottie options={getFlagOptions(university.id)} height={30} width={30} />
                  
                  </div>
                  <div className="universityItemText">
                  <p>{university.name}</p>
                  </div>
                         
                        </div>
              })}
            </div>}
          </div>
          <div>2</div>
          <div>3</div>
          <div>4</div>
        </AwesomeSlider>
      </MainLayout>
    </>
  );
};

export default TransferCredits;
