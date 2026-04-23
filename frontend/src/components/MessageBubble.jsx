import React from 'react'

export const MessageBubble = ({message,isUser}) => {
  return (
    <div className= {`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
        <div
            className= {`px-4 py-2 rounded-2xl max-w-xs text-sm shadow-md ${
              isUser
              ? "bg-blue-500 text-white rounded-br-none"
              : "bg-gray-200 text-gray-800 rounded-bl-none"
            }`}
        >
          {message}
        </div>
    </div>
  )
}

