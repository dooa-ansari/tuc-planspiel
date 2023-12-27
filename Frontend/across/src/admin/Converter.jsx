import React, { useState, useEffect, useRef } from "react";
import "../assets/css/ShowModules.css";
import useWebSocket from 'react-use-websocket';
import { useNavigate } from 'react-router-dom';

const Converter = () => {
  const [data, setData] = useState("Conversion Process");
  const [progress, setProgress] = useState(0);
  const [messages, setMessages] = useState([]);
  const navigate = useNavigate();
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
  onMessage: (event) => {
    const jsonData = JSON.parse(event.data)
    console.log(jsonData)
    setData(jsonData.message)
    setProgress(jsonData.progress)
    setMessages([jsonData.message, ...messages]);
  },
  //Will attempt to reconnect on all close events, such as server shutting down
  shouldReconnect: (closeEvent) => true,
});

 const onClickSimilarityTable = () => {
    navigate('/tables')
 }
 
  return (
    <div style={{ flex: 1 }}>
      <progress value={progress} max={100} />
      <p style={{color: "#979"}}>{data}</p>
      <div style={{border: "1px solid black"}}>
      {messages.map((message, index) => message.includes("True") ? <p style={{color: 'green', fontWeight: 700}} key={index}>{message}</p> : <p style={{color: 'red'}} key={index}>{message}</p>)}
      </div>
      <button onClick={onClickSimilarityTable}>View Similarity Table</button>
    </div>
  );
};

export default Converter;
