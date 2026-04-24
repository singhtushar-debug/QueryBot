import { useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000/api";

export const PdfUpload = ({ onSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("file", file);

      await axios.post(`${API_BASE}/ingest/pdf`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      onSuccess(`Ingested: ${file.name}`);
      setFile(null);
    } catch (err) {
      onSuccess(err?.response?.data?.message || "Error ingesting PDF");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full bg-gray-100 p-4 flex flex-col sm:flex-row items-center gap-3 shadow-sm"
    >
      {/* File Input */}
      <label className="flex-1 w-full cursor-pointer">
        <div className="flex items-center justify-between px-4 py-3 border border-dashed border-gray-300 rounded-xl hover:border-blue-400 transition bg-gray-50">
          <span className="text-sm text-gray-600 truncate">
            {file ? file.name : "Choose a PDF file..."}
          </span>
          <span className="text-xs text-blue-500 font-medium">
            Browse
          </span>
        </div>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="hidden"
        />
      </label>

      {/* Upload Button */}
      <button
        type="submit"
        disabled={loading || !file}
        className="px-5 py-3 rounded-xl bg-gray-500 text-white font-medium hover:bg-blue-600 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
      >
        {loading ? (
          <span className="animate-pulse">Uploading...</span>
        ) : (
          "Upload PDF"
        )}
      </button>
    </form>
  );
};
