import React, { useState, useEffect, useRef } from "react";
import "../assets/css/ShowModules.css";
import useWebSocket from 'react-use-websocket';

const Converter = () => {
  const [data, setData] = useState("Hello");
//   const socket = React.useRef(new WebSocket('ws://localhost:8000/ws/updates')).current; 
  const socketUrl = 'ws://localhost:8000/ws/updates';

const {
  sendMessage,
  sendJsonMessage,
  lastMessage,
  lastJsonMessage,
  readyState,
  getWebSocket,
} = useWebSocket(socketUrl, {
  onOpen: () => console.log('opened'),
  onMessage: (event) => setData(event.data),
  //Will attempt to reconnect on all close events, such as server shutting down
  shouldReconnect: (closeEvent) => true,
});

  console.log("i am being rerendeted")
//   useEffect(() => {
//     socket.onopen = () => {
//         // connection opened
//         socket.send('something'); // send a message
//       };
      
//       socket.onmessage = e => {
//         // a message was received
//         console.log("message")
//         console.log(e.data);
//         // setData(e.data)
//       };
      
//       socket.onerror = e => {
//         // an error occurred
//         console.log(e.message);
//       };
      
//       socket.onclose = e => {
//         // connection closed
//         console.log("Closing connection")
//       }; 
//   }, []);

  
  return (
    <div style={{ flex: 1 }}>
      <p id="moduleHeading">{data}</p>
      {/* <button onClick={startProcessing}>Click Me</button> */}
    </div>
  );
};

export default Converter;
