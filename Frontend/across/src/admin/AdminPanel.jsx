// AdminPanel.jsx
import React from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';
import Home from './Home';
import FileUpload from './FileUpload';
import Converter from './Converter';

const AdminPanel = () => {
    return (
        <div>
            <Outlet />

            {/* Nested Routes */}
            <Routes>
                <Route path="home" element={<Home />} />
                <Route path="upload" element={<FileUpload />} />
                <Route path="automation" element={<Converter />} />
            </Routes>
        </div>
    );
};

export default AdminPanel;
