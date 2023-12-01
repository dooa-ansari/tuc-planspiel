import React, { useState, useEffect } from 'react';

import "./ShowModules.css";

const ShowModules = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
      fetch('http://127.0.0.1:8000/polls/')
        .then(response => response.json())
        .then(json => setData(json))
        .catch(error => console.error(error));
    }, []);
  
    return (
      <div>
        {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : 'Loading...'}
      </div>
    );
};

export default ShowModules;
