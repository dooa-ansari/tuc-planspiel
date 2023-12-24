import React, { useState, useEffect } from "react";
import data_static from "../components/data";
import "../assets/css/ShowModules.css";

const Converter = () => {
  const [data, setData] = useState(null);
  const ws = new WebSocket('ws://localhost:8000/ws/updates')

  ws.onopen = () => {
    // connection opened
    ws.send('something'); // send a message
  };
  
  ws.onmessage = e => {
    // a message was received
    console.log(e.data);
  };
  
  ws.onerror = e => {
    // an error occurred
    console.log(e.message);
  };
  
  ws.onclose = e => {
    // connection closed
    console.log(e.code, e.reason);
  };
  useEffect(() => {
    
  }, []);

  return (
    <div style={{ flex: 1 }}>
      <p id="moduleHeading">Convert Modules</p>
      
    </div>
  );
};

export default Converter;
