import axios from "axios";

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"}/api/v1`,
  timeout: 30000
});

export async function uploadPdf(file) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return response.data;
}

export async function submitDocument(documentId, formulas) {
  const response = await api.post(`/documents/${documentId}/submit`, { formulas });
  return response.data;
}
