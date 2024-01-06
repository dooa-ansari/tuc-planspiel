// src/admin/Home.js
import React, { useEffect, useState } from 'react';

const Home = () => {
    const [token, setToken] = useState(null)

    useEffect(() => {
        const authToken = localStorage.getItem('authToken');
        setToken(authToken)
    }, [])
    console.log(token)
    return (
        <div>
            <h2>Welcome to the Admin Panel!</h2>
            {token}
            {/* Add more content as needed */}
        </div>
    );
};

export default Home;
