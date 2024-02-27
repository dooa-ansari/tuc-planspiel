import React, { useState, useEffect } from "react";
import MainLayout from "../../../components/user/MainLayout/MainLayout";
import { useAuth } from "../../../context/AuthContext";
import {
    retrieveTransferCreditRequestsforUser
} from "../../../api/externalApi";
import Table from "react-bootstrap/Table";
import Badge from "react-bootstrap/Badge";
import "./Notifications.css";
const Notifications = () => {
    const [auth, setAuth] = useAuth();
    const [transferRequests, setTransferRequests] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await retrieveTransferCreditRequestsforUser({
                    email: auth.user.email
                });
                setTransferRequests(response.data.user_data.transferCreditsRequests);
            } catch (error) {
                console.error("Error fetching transfer requests:", error);
            }
        };
        fetchData();
    }, []);
    return (
        <>
            <MainLayout>
                <div className="notifications">
                    <h1>Latest Notifications</h1>
                    <RequestsTable transferRequests={transferRequests} setTransferRequests={setTransferRequests} />
                </div>
            </MainLayout>
        </>
    );
};


function RequestsTable({ transferRequests }) {
    return (
        <div style={{ padding: "10px 30px 10px 30px" }}>
            <Table responsive="lg" borderless>
                <thead>
                    <tr>
                        <th>Transfer initiated from module</th>
                        <th>Transfer initiated to module</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {transferRequests.length === 0 ? (
                        <tr>
                            <td colSpan="4">No transfer credit requests available.</td>
                        </tr>
                    ) : (
                        transferRequests.map((request, index) => (
                            <tr key={index}>
                                <td>
                                    {request.fromModules.map((module, index) => (
                                        <div key={index}>
                                            {module.moduleName} - {module.credits} credits
                                        </div>
                                    ))}
                                </td>
                                <td>
                                    {request.toModules.map((module, index) => (
                                        <div key={index}>
                                            {module.moduleName} - {module.credits} credits
                                        </div>
                                    ))}
                                </td>
                                <td>
                                    {request.status === 'PENDING' ? (
                                        <Badge variant="primary">{request.status}</Badge>
                                    ) : request.status === 'ACCEPTED' ? (
                                        <Badge variant="success" className="bg-success">{request.status}</Badge>
                                    ) : (
                                        <Badge variant="danger" className="bg-danger">{request.status}</Badge>
                                    )}
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </Table>
        </div>
    );
}
export default Notifications;