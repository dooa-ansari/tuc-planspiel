import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getAllModules = async () => {
  let response;
  try {
    response = await api.get("/modules/getAllModules");
  } catch (error) {
    return error;
  }
  return response;
};
