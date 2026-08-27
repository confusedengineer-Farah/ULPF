import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getEventStats = async () => {
  const response = await api.get("/events/stats");
  return response.data;
};

export const getEvents = async (params = {}) => {
  const response = await api.get("/events", {
    params,
  });

  return response.data;
};

export const getEvent = async (eventId) => {
  const response = await api.get(`/events/${eventId}`);
  return response.data;
};

export const ingestEvent = async (rawEvent) => {
  const response = await api.post("/events/ingest", {
    raw_event: rawEvent,
  });

  return response.data;
};

export default api;