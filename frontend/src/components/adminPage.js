import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../styles/adminPage.css';

function AdminPage() {
  const { eventCode } = useParams(); // Get the event code from the URL
  const navigate = useNavigate();

  // Handles ending the event
  const handleEndEvent = () => {
    // Remove event from local storage to make it unjoinable
    localStorage.removeItem(`event_${eventCode}`);
    // Navigate back to Dashboard
    navigate('/');
  };

  const handleGoBack = () => {
    navigate('/');
  };

  // Retrieve the event details from localStorage
  const event = JSON.parse(localStorage.getItem(`event_${eventCode}`));

  if (!event) {
    return <p>Event not found. Please check the code or contact the event host.</p>;
  }

  return (
    <div className="admin-page-container">
      <h2>Admin Page</h2>
      <p><strong>Event Code:</strong> {eventCode}</p>
      <p>Share this code with users so they can join the event.</p>
      
      <div className="event-details">
        <p><strong>Event Name:</strong> {event.eventName}</p>
        <p><strong>Event Location:</strong> {event.eventLocation}</p>
        <p><strong>Start Date:</strong> {event.eventStartDate}</p>
        <p><strong>End Date:</strong> {event.eventEndDate}</p>
        <p><strong>Host:</strong> {event.eventHost}</p>
        <p><strong>Description:</strong> {event.eventDescription}</p>
      </div>

      <button className="end-event-button" onClick={handleEndEvent}>End Event</button>
      <button className="back-button" onClick={handleGoBack}>Back to Dashboard</button>
    </div>
  );
}

export default AdminPage;
