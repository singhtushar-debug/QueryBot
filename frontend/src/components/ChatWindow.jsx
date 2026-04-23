import React, { useState } from "react";
import axios from "axios";
import { MessageBubble } from "./MessageBubble";
import { UrlingestForm } from "./UrlingestForm";

const API_BASE_CHAT = "http://localhost:8000/api";

export const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! Ask me anything.", isUser: false },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, isUser: true };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const { data } = await axios.post(`${API_BASE_CHAT}/query/`, {
        question: input,
      });

      setMessages((prev) => [
        ...prev,
        { text: data?.answer || "No response", isUser: false },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          text: err?.response?.data?.message || "Error fetching response",
          isUser: false,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleUrlSuccess = (msg) => {
    setMessages((prev) => [...prev, { text: msg, isUser: false }]);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-gray-600 text-white p-4 text-lg font-semibold shadow">
        Querybot
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, index) => (
          <MessageBubble key={index} message={msg.text} isUser={msg.isUser} />
        ))}
        {loading && (
          <MessageBubble message="Typing..." isUser={false} />
        )}
      </div>

      {/* Input Box */}
      <div className="p-3  bg-gray-100 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="px-4 py-2 bg-gray-500 text-white rounded-xl hover:bg-blue-600 transition disabled:opacity-50"
        >
          Send
        </button>
      </div>

      {/* URL Ingest */}
      <UrlingestForm onSuccess={handleUrlSuccess} />
    </div>
  );
};

export default ChatWindow;