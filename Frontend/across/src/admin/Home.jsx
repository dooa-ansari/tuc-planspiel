import React from 'react';
import { Card, Col, Row } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { CgProfile } from "react-icons/cg";
import { IoIosLogOut } from "react-icons/io";
import "../assets/css/AdminHome.css";
import "../assets/css/Footer.css";
import Footer from "../components/Footer";


const Home = () => {
    return (
        <div style={{ backgroundColor: '#EDEDED', minHeight: '100vh' }}>
            <NavScrollExample />
            <PageBody />
            <Footer />
        </div >
    );
};
function PageBody() {
    const cardData = [
        {
            title: 'Users',
            description: 'Effortlessly oversee and manage user accounts, ensuring smooth access and interactions within the platform.',
            buttonText: 'Show Users',
            link: '/manage-users',
        },
        {
            title: 'Modules',
            description: 'Take control of the courses and learning modules, ensuring a seamless and organized educational experience for students.',
            buttonText: 'Show Modules',
            link: '/manage-modules',
        },
        {
            title: 'Universities',
            description: 'Facilitate the management and coordination of universities, fostering collaboration and excellence across educational institutions.',
            buttonText: 'Show Universitites',
            link: '/manage-universities',
        },
        {
            title: 'Show Similar Modules',
            description: 'Facilitate the management and coordination of universities, fostering collaboration and excellence across educational institutions.',
            buttonText: 'Check Similarity',
            link: '/manage-universities',
        },
        {
            title: 'Automation Tool',
            description: 'Facilitate the management and coordination of universities, fostering collaboration and excellence across educational institutions.',
            buttonText: 'Run Automation',
            link: '/manage-universities',
        },
        {
            title: 'CSV to RDF',
            description: 'Facilitate the management and coordination of universities, fostering collaboration and excellence across educational institutions.',
            buttonText: 'Convert to RDF',
            link: '/manage-universities',
        },
        {
            title: 'Similarity Table',
            description: 'Facilitate the management and coordination of universities, fostering collaboration and excellence across educational institutions.',
            buttonText: 'Show Similarity Table',
            link: '/manage-universities',
        },
    ];
    return (
        <Container style={{ backgroundColor: '#EDEDED' }}>
            <h1 className="my-4 text-left">Hi John, Welcome to the ADMIN panel</h1>

            {/* Introductory Section */}
            <div className="intro-container mb-4 p-4 border rounded bg-light" style={{ boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)', marginLeft: '5px', marginRight: '5px' }}>
                <h2 className="text-left text-primary mb-4">Admin Activities</h2>
                <p className="justify-content-left" style={{ fontFamily: 'monospace', textAlign: "justify" }}>
                    Welcome to the heart of the cross-university platform! As administrators, you hold the key to shaping the educational landscape.
                    In your role, you have various responsibilities, such as managing users, organizing courses and learning materials, and promoting collaboration among universities. Your dynamic role involves breaking down barriers, ensuring a smooth educational experience, and shaping the future for our students.
                </p>
            </div>

            {/* Cards Section */}
            <div className="mb-4 bg-light" style={{ padding: '20px', borderRadius: '10px', marginLeft: '5px', marginRight: '5px', boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)' }}>
                <h2 className="text-left text-primary mb-4">Manage</h2>
                <Row className="justify-content-center bg-light" style={{}}>
                    {cardData.map((card, index) => (
                        <Col key={index} xs={12} sm={6} md={3} className="d-flex align-items-stretch" style={{ marginBottom: '10px' }}>
                            <Card className="mb-4 w-100" style={{ backgroundColor: "#e5f1f4", color: "#000" }}>
                                <Card.Body className="d-flex flex-column align-items-center" style={{ backgroundColor: "#e5f1f4", }}>
                                    <Card.Title className="text-center" style={{ backgroundColor: "#e5f1f4", marginBottom: '14px', fontSize: '20px' }}>{card.title}</Card.Title>
                                    <Button style={{ backgroundColor: '#b2d6de', color: "#000", border: '#b2d6de', marginBottom: '3px', fontSize: '16px' }} href={card.link}>{card.buttonText}</Button>
                                </Card.Body>
                            </Card>
                        </Col>
                    ))}
                </Row>
            </div>
        </Container >
    );
}

function NavScrollExample() {
    return (
        <Navbar expand="lg" style={{ backgroundColor: '#007991', width: '100%', margin: 'auto' }}>
            <Navbar.Brand href="#" style={{ fontSize: "30px", color: "#fff" }}>campus<b>flow</b></Navbar.Brand>
            <Navbar.Toggle aria-controls="navbarScroll" />
            <Navbar.Collapse id="navbarScroll" style={{ backgroundColor: '#007991' }}>
                <Nav className="mx-auto" style={{ maxHeight: '100px', textAlign: "center", backgroundColor: '#007991', }} navbarScroll>
                    <Nav.Link href="#action1" style={{ color: "#fff" }}>Home</Nav.Link>
                    <Nav.Link href="#action2" style={{ color: "#fff" }}>About</Nav.Link>
                    <Nav.Link href="#action3" style={{ color: "#fff" }}>Universities</Nav.Link>
                    <Nav.Link href="#action4" style={{ color: "#fff" }}>ACROSS</Nav.Link>
                    <Nav.Link href="#action5" style={{ color: "#fff" }}>Reach Us</Nav.Link>
                </Nav>
                <Nav.Link className="text-black d-flex flex-column align-items-left" >
                    <span className="ms-0 mb-0" style={{ color: "#fff", margin: "1px" }}><b>John Doe</b></span>
                    <span style={{ color: "#fff" }}>Admin</span>
                </Nav.Link>
                <a href="/profile" className="avatar-emoji" style={{ backgroundColor: '#007991', textDecoration: 'none', cursor: 'pointer', color: 'black' }}>
                    <CgProfile />
                </a>
                <a href="/logout" className="logout-icon" style={{ backgroundColor: '#007991', textDecoration: 'none', cursor: 'pointer', color: 'black' }}>
                    <IoIosLogOut />
                </a>
            </Navbar.Collapse>
        </Navbar >
    );
}


export default Home;
