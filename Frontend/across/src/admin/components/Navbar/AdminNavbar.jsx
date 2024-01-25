import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { CgProfile } from "react-icons/cg";
import { IoIosLogOut } from "react-icons/io";

const AdminNavbar = () => {
    return (
        <Navbar
            expand="lg"
            style={{
                backgroundColor: "#007991",
                width: "100%",
                margin: "auto",
                padding: "0 20px",
            }}
        >
            <Navbar.Brand href="#" style={{ fontSize: "30px", color: "#fff", textShadow: "2px 2px 4px rgba(0, 0, 0, 0.5)" }}>
                campus<b>flow</b>
                <sup style={{ fontSize: "14px", margin: "0 px 0px 0px 2px" }}>Admin Panel</sup>
            </Navbar.Brand>

            <Navbar.Toggle aria-controls="navbarScroll" />
            <Navbar.Collapse id="navbarScroll" style={{ backgroundColor: "#007991" }}>
                <Nav
                    className="mx-auto"
                    style={{
                        maxHeight: "100px",
                        textAlign: "center",
                        backgroundColor: "#007991",
                    }}
                // navbarScroll
                >
                    <Nav.Link href="#action1" style={{ color: "#fff" }}>
                        Home
                    </Nav.Link>
                    <Nav.Link href="#action2" style={{ color: "#fff" }}>
                        About
                    </Nav.Link>
                    <Nav.Link href="#action3" style={{ color: "#fff" }}>
                        Universities
                    </Nav.Link>
                    <Nav.Link href="#action4" style={{ color: "#fff" }}>
                        ACROSS
                    </Nav.Link>
                    <Nav.Link href="#action5" style={{ color: "#fff" }}>
                        Reach Us
                    </Nav.Link>
                </Nav>
                <Nav.Link className="text-black d-flex flex-column align-items-left">
                    <span className="ms-0 mb-0" style={{ color: "#fff", margin: "1px" }}>
                        <b>John Doe</b>
                    </span>
                    <span style={{ color: "#fff" }}>Admin</span>
                </Nav.Link>
                <a
                    href="/profile"
                    className="avatar-emoji"
                    style={{
                        backgroundColor: "#007991",
                        textDecoration: "none",
                        cursor: "pointer",
                        color: "black",
                    }}
                >
                    <CgProfile />
                </a>
                <a
                    href="/logout"
                    className="logout-icon"
                    style={{
                        backgroundColor: "#007991",
                        textDecoration: "none",
                        cursor: "pointer",
                        color: "black",
                    }}
                >
                    <IoIosLogOut />
                </a>
            </Navbar.Collapse>
        </Navbar>
    );
};

export default AdminNavbar;