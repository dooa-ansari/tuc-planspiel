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
  const [usersCompleteModules, setUsersCompletedModules] = useState([]);
  const [univerisitiesLoading, setUniversitiesLoading] = useState(true);
  const [usersModulesLoading, setusersModulesLoading] = useState(false);
  const [similarModulesLoading, setsimilarModulesLoading] = useState(false);
  const [similarModules, setSimilarModules] = useState([]);//
  const [selectedUniversity, setSelectedUniverity] = useState(null);
  const [lastSelectedModule, setLastSelectedModule] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);



const buttonStyle = {
  background: "#439a86",
  borderRadius: "10px",
  color: "white",
  width: "60px"
}
  useEffect(() => {
    axios
      .get("http://localhost:8000/adminapp/universitieslist/")
      .then((response) => {
        if (response.status == 200) {
          console.log(response.data);
          const returnedData = response.data;
          returnedData.forEach((item) => {
            item.selected = false;
          });
          setUniversities(returnedData);
        }
        setUniversitiesLoading(false);
      })
      .catch((error) => {
        console.log(error);
        setUniversitiesLoading(false);
      });
  }, []);

  const getUsersCompletedModules = () => {
    axios
    .get("http://localhost:8000/adminapp/universitieslist/")
    .then((response) => {
      if (response.status == 200) {
        console.log(response.data);
        const returnedData = response.data;
        returnedData.forEach((item) => {
          item.selected = false;
        });
        console.log(returnedData)
        setUsersCompletedModules(returnedData);
      }
      setusersModulesLoading(false);
    })
    .catch((error) => {
      setusersModulesLoading(false);
    }); 
  }

  const getSimilarAgainst = async () => {
    const selectedModules = usersCompleteModules.filter((item) => item.selected)
    const list = []
    await selectedModules?.forEach((selected) => {
      axios
      .get("http://localhost:8000/api/similarModules?moduleUri="+encodeURIComponent("http://tuc.web.engineering/module#CWEA"))
      .then((response) => {
        if (response.status == 200) {
          list.push(response.data.modules)
        }
        setsimilarModulesLoading(false);
      })
      .catch((error) => {
        setsimilarModulesLoading(false);
      });
    })
    setSimilarModules(list)
    console.log(list)
     
  }

  const defaultOptions = {
    loop: true,
    autoplay: true,
    animationData: loadingData,
    rendererSettings: {
      preserveAspectRatio: "xMidYMid slice",
    },
  };

  const defaultOptions2 = {
    loop: true,
    autoplay: true,
    animationData: loadingData,
    rendererSettings: {
      preserveAspectRatio: "xMidYMid slice",
    },
  };
  const onPressUniversityItem = (item) => {
    const updateList = [];
    universities.forEach((unis) => {
      unis.selected = item.id == unis.id ? true : false;
      updateList.push(unis);
    });
    setUniversities(updateList);
    setSelectedUniverity(item);
  };
  const onPressCompletedModuleItem = (item) => {
    const updateList = [];
    usersCompleteModules.forEach((unis) => {
      unis.selected = item.id == unis.id ? !unis.selected : unis.selected
      updateList.push(unis);
    });
    setUsersCompletedModules(updateList);
    setLastSelectedModule(item);
  };
  const getFlagOptions = (id) => {
    if (id == 1) {
      return {
        loop: true,
        autoplay: true,
        animationData: germany,
        rendererSettings: {
          preserveAspectRatio: "xMidYMid slice",
        },
      };
    } else if (id == 2) {
      return {
        loop: true,
        autoplay: true,
        animationData: poland,
        rendererSettings: {
          preserveAspectRatio: "xMidYMid slice",
        },
      };
    }
  };
const onPressNextTransition = (event) => {
  console.log(event)
  setCurrentIndex(event.currentIndex)
   if(event.currentIndex == 1){
    setusersModulesLoading(true) 
    getUsersCompletedModules()
   }else if(event.currentIndex == 2){
    getSimilarAgainst()
   }
}
  return (
    <>
      <MainLayout>
        <h1>Transfer Credits</h1>
        <AwesomeSlider 
        onTransitionEnd={(event) => {
          onPressNextTransition(event)
        }}
        infinite={false}  organicArrows={false}
      buttonContentRight={<button style={selectedUniversity && buttonStyle}>Next</button>}
      buttonContentLeft={<p style={{ color: "black" }}>Right</p>}>
          <div style={{ background: "white"}}>
          <p>Please choose university you want to transfer your credits to : </p>
                
            {univerisitiesLoading ? (
              <Lottie options={defaultOptions} height={200} width={200} />
            ) : (
              <div>
                {universities.map((university) => {
                  return (
                    <div
                      onClick={() => onPressUniversityItem(university)}
                      className={
                        "universityItem " +
                        (university.selected && "universityItemSelectedBorder universityItemSelected")
                      }
                      key={university.id}
                    >
                      <div className="universityItemFlag">
                        <Lottie
                          options={getFlagOptions(university.id)}
                          height={30}
                          width={30}
                        />
                      </div>
                      <div  className="universityItemText">
                        <p>{university.name}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
          <div style={{ background: "white"}}>
          <p>We will help choose what credits can be possibly transfer to Bialystok University of Technology From Technische Universität Chemnitz</p>
          <p>Please choose the modules you have already finished at Technische Universität Chemnitz</p>
                
            {usersModulesLoading ? (
              <Lottie options={defaultOptions2} height={200} width={200} />
            ) : (
              <div>
                {usersCompleteModules.map((completedModule , index) => {
                  return (
                    <div
                      onClick={() => onPressCompletedModuleItem(completedModule)}
                      className={
                        "completedCourseItem " +
                        (completedModule.selected && "courseItemSelectedBorder universityItemSelected")
                      }
                      key={completedModule.id}
                    >
                      <div  className="courseItemText">
                        <p>{completedModule.name}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
          <div>3</div>
          <div>4</div>
        </AwesomeSlider>
      </MainLayout>
    </>
  );
};

export default TransferCredits;
