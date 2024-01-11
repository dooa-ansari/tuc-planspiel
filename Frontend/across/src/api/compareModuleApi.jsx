import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_API,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getUniversities = async () => {
  let response;
  try {
    response = await api.get("/adminapp/universitieslist/");
  } catch (error) {
    return error;
  }
  return response;
};

export const getCoursesOfParticularUniversity = async data => {
  let response;
  try {
    response = await api.post("/api/courses/", data);
  } catch (error) {
    return error;
  }
  return response;
};

export const getModulesOfCourse = async data => {
  let response;
  try {
    response = await api.post("/api/modules/", data);
  } catch (error) {
    return error;
  }

  return response;
};

export const getSimilarModules = async data => {
  let response;
  try {
    response = await api.post("/api/similarModules/", data);
  } catch (error) {
    return error;
  }

  return response;
};
