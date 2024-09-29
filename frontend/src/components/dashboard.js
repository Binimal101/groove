import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/dashboard.css';

function Dashboard({ user, onLogout }) {
  const [eventCode, setEventCode] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  // Handles submission of event code by validating it
  const handleEventCodeSubmit = (e) => {
    e.preventDefault();
    const event = localStorage.getItem(`event_${eventCode}`);
    if (event) {
      // Valid event code, navigate to the event page
      console.log(`Navigating to Event with Code: ${eventCode}`);
      setSuccessMessage('Successfully joined the event! Navigating to event...');
      setErrorMessage('');
      setTimeout(() => {
        navigate(`/event/${eventCode}`);
      }, 1000); // Delay navigation for user feedback
    } else {
      // Invalid event code, show an error message
      setSuccessMessage('');
      setErrorMessage('Invalid event code. Please try again.');
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
