import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_API,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export const convertCsvToRdf = async data => {
  let response;
  try {
    response = await api.post("/adminapp/csvToRdf", data);
  } catch (error) {
    return error;
  }
  return response;
};

export const telecastFile = async data => {
  let response;
  try {
    response = await api.post("/adminapp/upload", data);
  } catch (error) {
    return error;
  }
  return response;
};

export const listSimilarModules = async () => {
  let response;
  try {
    response = await api.get("/modules/listSimilarModules");
  } catch (error) {
    return error;
  }

  return response;
};

export const retrieveTransferCreditRequests = async data => {
  let response;
  try {
    response = await api.post("/adminapp/fetchTransferCreditRequests", data);
  } catch (error) {
    return error;
  }
  return response;
};

export const updateTransferCreditRequests = async data => {
  let response;
  try {
    response = await api.put("/adminapp/updateTransferRequest", data);
  } catch (error) {
    return error;
  }
  return response;
};

export const fetchUserData = async () => {
  let response;
  try {
    response = await api.get("/adminapp/fetchUserData");
  } catch (error) {
    return error;
  }
  return response;
};

export const fetchDepartmentsData = async () => {
  let response;
  try {
    response = await api.get("/adminapp/fetchDepartments");
  } catch (error) {
    return error;
  }
  return response;
};
