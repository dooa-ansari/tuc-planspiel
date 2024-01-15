// AdminPanel.jsx
import React from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';
import Home from './Home';
import CsvToRdf from './CsvToRdf'
import FileUpload from './FileUpload';
import Converter from './Converter';
import ShowSimilarityTable from './ShowSimilarityTable';
import ModulesList from './ModulesList';

const AdminPanel = () => {
  return (
    <div>
      <Outlet />

            {/* Nested Routes */}
            <Routes>
                <Route path="home" element={<Home />} />
                <Route path="csvToRdf" element={<CsvToRdf />} />
                <Route path="upload" element={<FileUpload />} />
                <Route path="automation" element={<Converter />} />
                <Route path="similaritytable" element={<ShowSimilarityTable />} />
                <Route path="modulelist" element={<ModulesList />} />
            </Routes>
        </div>
    );
};

export default AdminPanel;
