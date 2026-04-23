import React from 'react'
import ChatWindow from "./components/ChatWindow"

export const  App = () => {

  return (
    <>
      <div className='h-screen w-full bg-gray-100 flex items-center justify-center'>
          <div className='w-2/3 shadow-xl rounded-2xl overflow-hidden  bg-white '>
            <ChatWindow />
          </div>
      </div>
      
    </>
  )
}

export default App;
