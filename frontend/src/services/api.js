import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // Update with your backend URL

// Get car details by VIN
export const getCarDetailsByVin = async (vin) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/vin/${vin}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching VIN details:", error);
    throw error;
  }
};

// Upload PDF
export const uploadPdf = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading PDF:", error);
    throw error;
  }
};
