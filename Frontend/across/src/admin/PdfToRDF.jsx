import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { FiCheckCircle } from 'react-icons/fi';
import '../assets/css/FileUpload.css';


const PdfToRdf = () => {
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [uploadStatus, setUploadStatus] = useState(null);
    const [formData, setFormData] = useState({
        courseName: '',
        belongsToUniversity: '',
        belongsToProgram: '',
        belongsToDepartment: '',
        hasLanguage: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const onDrop = useCallback(async (acceptedFiles) => {
        try {
            const filesFormData = new FormData();

            acceptedFiles.forEach((file) => {
                filesFormData.append('files', file);
            });

            // Create a JSON object with the required data
            const jsonData = {
                courseName: formData.courseName,
                belongsToUniversity: formData.belongsToUniversity,
                belongsToProgram: formData.belongsToProgram,
                belongsToDepartment: formData.belongsToDepartment,
                hasLanguage: formData.hasLanguage,
            };

            // Append JSON data to FormData
            filesFormData.append('jsonData', JSON.stringify(jsonData));

            const response = await axios.post('http://127.0.0.1:8000/pdf_To_rdf/api/pdfToRdf', filesFormData);

            console.log('Upload response:', response.data);

            setUploadedFiles(acceptedFiles);
            setUploadStatus('Files uploaded successfully!');
        } catch (error) {
            console.error('Error uploading files:', error);
            setUploadStatus('Error uploading files. Please try again.');
        }
    }, [formData]);


    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

    return (
        <div className="file-upload-container">
            <div className='instructions'>
                <p className='instructions-font'>This is utility to update or insert modules in RDF file using PDF files</p>
                <p className='instructions-font-subtext'>How to use this utility</p>
                <ul>
                    <li>Upload PDF files with modules you want to update or insert in RDF file.</li>
                </ul>
            </div>

            <form>
                <label>
                    Course Name:
                    <input
                        type="text"
                        name="courseName"
                        value={formData.courseName}
                        onChange={handleChange}
                    />
                </label>
                <label>
                    Belongs To University:
                    <input
                        type="text"
                        name="belongsToUniversity"
                        value={formData.belongsToUniversity}
                        onChange={handleChange}
                    />
                </label>
                <label>
                    Belongs To Program:
                    <input
                        type="text"
                        name="belongsToProgram"
                        value={formData.belongsToProgram}
                        onChange={handleChange}
                    />
                </label>
                <label>
                    Belongs To Department:
                    <input
                        type="text"
                        name="belongsToDepartment"
                        value={formData.belongsToDepartment}
                        onChange={handleChange}
                    />
                </label>
                <label>
                    Has Language:
                    <input
                        type="text"
                        name="hasLanguage"
                        value={formData.hasLanguage}
                        onChange={handleChange}
                    />
                </label>
            </form>


            <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
                <input {...getInputProps()} />
                {isDragActive ? (
                    <p>Drop the files here ...</p>
                ) : (
                    <p>Drag 'n' drop University module files here, or click to select files</p>
                )}
            </div>

            {uploadedFiles.length > 0 && (
                <div className="upload-info">
                    <h3>Uploaded Files:</h3>
                    <ul>
                        {uploadedFiles.map((file) => (
                            <li key={file.name}>{file.name}</li>
                        ))}
                    </ul>
                    <div className="upload-status">
                        <FiCheckCircle size={24} color="#4CAF50" />
                        <p>{uploadStatus}</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PdfToRdf;
