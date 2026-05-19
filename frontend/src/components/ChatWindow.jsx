import React, { useState } from "react";
import { MessageBubble } from "./MessageBubble";

const API_BASE_CHAT = "http://localhost:8000/api";

export const ChatWindow = () => {

  const [messages, setMessages] = useState([
    { text: "Hello! Ask me anything.", isUser: false },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [thinking, setThinking] = useState("");
  const [showThinking, setShowThinking] = useState(false);

  const sendMessage = async () => {

    if (!input.trim()) return;

    const userMessage = {
      text: input,
      isUser: true,
    };

    setMessages((prev) => [...prev, userMessage]);

    setInput("");
    setLoading(true);

    setThinking("");
    setShowThinking(true);

    try {

      const res = await fetch(`${API_BASE_CHAT}/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: input,
        }),
      });

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      // Placeholder assistant message
      setMessages((prev) => [
        ...prev,
        {
          text: "",
          isUser: false,
        },
      ]);

      let firstContentReceived = false;

      while (true) {

        const { done, value } = await reader.read();

        if (done) break;

        // console.log(`Value : ${value}`)
        const chunk = decoder.decode(value);
        // console.log(`Chunk: ${chunk}`)
        const lines = chunk.split("\n");
        // console.log(lines)
        for (const line of lines) {

          if (!line.trim()) continue;

          let data;

          try {
            data = JSON.parse(line);
            // console.log(data)
          } catch {
            continue;
          }

          // THINKING STREAM
          if (data.type === "thinking") {
            // console.log(data.content)
            setThinking((prev) => prev + data.content);
          }

          // FINAL CONTENT STREAM
          else if (data.type === "content") {

            // Hide thinking once actual response starts
            if (!firstContentReceived) {
              setShowThinking(false);
              firstContentReceived = true;
            }

            setMessages((prev) => {

              const updated = [...prev];

              updated[updated.length - 1].text += data.content;

              return updated;
            });
          }

          
          // TOOL EVENTS
          else if (data.type === "tool_start") {

            setThinking(
            (prev) => prev +  `🔧 Running ${data.tool}...\n`
            );
          }

          else if (data.type === "tool_end") {

            setThinking(
              (prev) => prev + `✅ ${data.tool} completed\n`
            );
          }
        }
      }

    } catch (err) {

      setMessages((prev) => [
        ...prev,
        {
          text: "Error fetching response",
          isUser: false,
        },
      ]);

    } finally {

      setLoading(false);
      setShowThinking(false);
    }
  };

  return (

    <div className="flex flex-col h-screen bg-gray-100">

      {/* Header */}
      <div className="bg-gray-600 text-white p-4 text-lg font-semibold shadow">
        Querybot
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">

        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            message={msg.text}
            isUser={msg.isUser}
          />
        ))}

        {/* Thinking Bubble */}
        {showThinking && (
          <div className="flex justify-start">

            <div className="bg-white px-4 py-3 rounded-2xl shadow max-w-md">

              <div className="text-xs text-gray-500 mb-1">
                Thinking...
              </div>

              <div className="text-sm whitespace-pre-wrap">
                {thinking || "Analyzing request..."}
              </div>

            </div>

          </div>
        )}

      </div>

      {/* Input */}
      <div className="p-3 bg-gray-100 flex gap-2">

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
          onKeyDown={(e) =>
            e.key === "Enter" && sendMessage()
          }
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="px-4 py-2 bg-gray-500 text-white rounded-xl hover:bg-blue-600 transition disabled:opacity-50"
        >
          Send
        </button>

      </div>

    </div>
  );
};

export default ChatWindow;