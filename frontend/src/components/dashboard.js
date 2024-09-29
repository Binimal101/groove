import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { joinEvent } from '../services/eventService';
import '../styles/dashboard.css';

function Dashboard({ user, onLogout }) {
  const [eventCode, setEventCode] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  // Handles submission of event code by validating it
  const handleEventCodeSubmit = async (e) => {
    e.preventDefault();

    // Log the data before sending the POST request
    console.log('Attempting to join event with the following data:', {
      eventCode,
      user: user ? user.display_name : 'Anonymous',
    });

    try {
      const response = await joinEvent(eventCode, user ? user.display_name : 'Anonymous');
      console.log('Received response from joinEvent request:', response);
      setSuccessMessage('Successfully joined the event! Navigating to event...');
      setErrorMessage('');
      
      // Navigate to user page after successful response
      setTimeout(() => {
        navigate(`/event/${eventCode}`);
      }, 1000); // Delay navigation for user feedback

    } catch (error) {
      console.error('Error joining event:', error);
      setErrorMessage(error.message || 'Invalid event code. Please try again.');
      setSuccessMessage('');
    }
  };

  // Handles navigation to the Create Event page
  const handleCreateEvent = () => {
    setErrorMessage('');
    setSuccessMessage('');
    navigate('/create-event');
  };

  // Reset success and error messages when the event code changes
  const handleEventCodeChange = (e) => {
    setEventCode(e.target.value);
    setErrorMessage('');
    setSuccessMessage('');
  };

  return (
    <div className="dashboard-container">
      <button className="logout-button" onClick={onLogout}>Logout</button>

      <div className="welcome-section">
        <h1>Welcome, {user ? user.display_name : 'Spotify User'}</h1>
        {user && (
          <div>
            {user.images.length > 0 && (
              <img
                src={user.images[0].url}
                alt="Profile"
                width="100"
                className="profile-picture"
              />
            )}
            <p className="email">Email: {user.email}</p>
          </div>
        )}
      </div>

      <div className="event-section">
        <h2>Enter Event Code</h2>
        <form onSubmit={handleEventCodeSubmit} className="event-code-form">
          <input
            type="text"
            value={eventCode}
            onChange={handleEventCodeChange}
            placeholder="Enter event code"
            className="event-code-input"
            required
          />
          <button type="submit" className="submit-button">Submit</button>
        </form>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}
      </div>

      <div className="create-event-section">
        <h3>Or Create a New Event</h3>
        <button className="create-event-button" onClick={handleCreateEvent}>
          Create Event
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
