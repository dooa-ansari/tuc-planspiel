import React, { useState, useEffect } from "react";
import "../assets/css/ShowModules.css";

const Converter = () => {
  const [data, setData] = useState(null);
  const ws = new WebSocket('ws://localhost:8000/ws/updates')

//   useEffect(() => {
//     console.log("called")
//     fetch('http://localhost:8000/polls/translator')
//       .catch(error => console.error(error));
//   }, []);

  ws.onopen = () => {
    // connection opened
    ws.send('something'); // send a message
  };
  
  ws.onmessage = e => {
    // a message was received
    console.log("message")
    console.log(e.data);
    setData(e.data)
  };
  
  ws.onerror = e => {
    // an error occurred
    console.log(e.message);
  };
  
  ws.onclose = e => {
    // connection closed
    console.log("Closing connection")
  };
  return (
    <div style={{ flex: 1 }}>
      <p id="moduleHeading">{data}</p>
      
    </div>
  );
};

export default Converter;
