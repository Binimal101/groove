import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../styles/userPage.css'; // Assuming you have a CSS file for this page

function UserEventPage() {
  const { eventCode } = useParams(); // Get the event code from the URL
  const navigate = useNavigate();

  // Retrieve the event details from localStorage
  const event = JSON.parse(localStorage.getItem(`event_${eventCode}`));

  if (!event) {
    return (
      <div className="user-event-page-container">
        <p>Event not found. Please check the code or contact the event host.</p>
        <button onClick={() => navigate('/')} className="back-button">Back to Dashboard</button>
      </div>
    );
  }

  // Check if event is inactive
  if (!event.isActive) {
    return (
      <div className="user-event-page-container">
        <p>This event has ended and is no longer joinable.</p>
        <button onClick={() => navigate('/')} className="back-button">Back to Dashboard</button>
      </div>
    );
  }

  const handleGoBack = () => {
    navigate('/');
  };

  return (
    <div className="user-event-page-container">
      <h2>Event Details</h2>
      <p><strong>Event Name:</strong> {event.eventName}</p>
      <p><strong>Event Location:</strong> {event.eventLocation}</p>
      <p><strong>Start Date:</strong> {event.eventStartDate}</p>
      <p><strong>End Date:</strong> {event.eventEndDate}</p>
      <p><strong>Host:</strong> {event.eventHost}</p>
      <p><strong>Description:</strong> {event.eventDescription}</p>
      <button onClick={handleGoBack} className="back-button">Back to Dashboard</button>
    </div>
  );
}

export default UserEventPage;
