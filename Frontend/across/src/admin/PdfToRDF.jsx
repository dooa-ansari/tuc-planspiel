import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { FiCheckCircle } from 'react-icons/fi';
import { Form, Col, Row, Container, Button } from 'react-bootstrap';
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
        <Container className="file-upload-container">
            <div className='instructions'>
                <p className='instructions-font'>This is utility to update or insert modules in RDF file using PDF files</p>
                <p className='instructions-font-subtext'>How to use this utility</p>
                <ul>
                    <li>Upload PDF files with modules you want to update or insert in RDF file.</li>
                </ul>
            </div>

            <Form>
                <Row>
                    <Col>
                        <Form.Group controlId="courseName">
                            <Form.Label>Course Name:</Form.Label>
                            <Form.Control
                                type="text"
                                name="courseName"
                                value={formData.courseName}
                                onChange={handleChange}
                            />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group controlId="belongsToUniversity">
                            <Form.Label>Belongs To University:</Form.Label>
                            <Form.Control
                                type="text"
                                name="belongsToUniversity"
                                value={formData.belongsToUniversity}
                                onChange={handleChange}
                            />
                        </Form.Group>
                    </Col>
                </Row>

                <Row>
                    <Col>
                        <Form.Group controlId="belongsToProgram">
                            <Form.Label>Belongs To Program:</Form.Label>
                            <Form.Control
                                type="text"
                                name="belongsToProgram"
                                value={formData.belongsToProgram}
                                onChange={handleChange}
                            />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group controlId="belongsToDepartment">
                            <Form.Label>Belongs To Department:</Form.Label>
                            <Form.Control
                                type="text"
                                name="belongsToDepartment"
                                value={formData.belongsToDepartment}
                                onChange={handleChange}
                            />
                        </Form.Group>
                    </Col>
                </Row>

                <Row>
                    <Col>
                        <Form.Group controlId="hasLanguage">
                            <Form.Label>Has Language:</Form.Label>
                            <Form.Control
                                type="text"
                                name="hasLanguage"
                                value={formData.hasLanguage}
                                onChange={handleChange}
                            />
                        </Form.Group>
                    </Col>
                </Row>

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

                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        </Container>
    );
};

export default PdfToRdf;
