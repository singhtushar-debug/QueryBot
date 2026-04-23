import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000/api";

export const UrlingestForm = ({ onSuccess }) => {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url.trim()) return;

    try {
      setLoading(true);
      await axios.post(`${API_BASE}/ingest/`, { url });
      onSuccess(`Ingested: ${url}`);
      setUrl("");
    } catch (err) {
      onSuccess(err?.response?.data?.message || "Error ingesting URL");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center gap-2 p-3 bg-gray-100"
    >
      <input
        type="text"
        placeholder="Paste a URL to ingest..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="flex-1 px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        type="submit"
        disabled={loading}
        className="px-4 py-2 bg-gray-500 text-white rounded-xl hover:bg-blue-600 transition disabled:opacity-50"
      >
        {loading ? "..." : "Ingest"}
      </button>
    </form>
  );
};
