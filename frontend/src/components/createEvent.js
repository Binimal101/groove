import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createEvent } from '../services/eventService'; // Import createEvent function
import '../styles/createEvent.css';

function CreateEvent() {
  const navigate = useNavigate();

  // Form fields state
  const [eventName, setEventName] = useState('');
  const [eventLocation, setEventLocation] = useState('');
  const [eventStartDate, setEventStartDate] = useState('');
  const [eventEndDate, setEventEndDate] = useState('');
  const [eventHost, setEventHost] = useState('');
  const [eventDescription, setEventDescription] = useState('');

  const handleBackClick = () => {
    navigate(-1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Generate a unique event code
    const eventCode = Math.random().toString(36).substr(2, 8).toUpperCase();
    console.log('Event Code Upon Creation: ', eventCode); 

    // Store event details
    const eventDetails = {
      eventCode,
      eventName,
      eventLocation,
      eventStartDate,
      eventEndDate,
      eventHost,
      eventDescription,
      isActive: true, // Indicates that the event is active
    };

    console.log('Event Details Being Created: ', eventDetails);

    // Save to localStorage for now
    localStorage.setItem(`event_${eventCode}`, JSON.stringify(eventDetails));

    // Send event details to backend (optional)
    try {
      console.log('Sending event details to backend...');
      const response = await createEvent(eventDetails); // Use the createEvent function
      console.log('Event successfully created on backend:', response);
    } catch (error) {
      console.error('Error sending event details to backend:', error);
    }

    // Navigate to AdminPage with event code
    navigate(`/admin/${eventCode}`);
  };

  return (
    <div className="create-event-container">
      <h2>Create a New Event</h2>
      <form className="create-event-form" onSubmit={handleSubmit}>
        {/* Event Name */}
        <div className="form-group">
          <label>Event Name:</label>
          <input
            type="text"
            value={eventName}
            onChange={(e) => setEventName(e.target.value)}
            placeholder="Enter event name"
            required
          />
        </div>

        {/* Event Location */}
        <div className="form-group">
          <label>Event Location:</label>
          <input
            type="text"
            value={eventLocation}
            onChange={(e) => setEventLocation(e.target.value)}
            placeholder="Enter event location"
            required
          />
        </div>

        {/* Event Start Date */}
        <div className="form-group">
          <label>Event Start Date:</label>
          <input
            type="datetime-local"
            value={eventStartDate}
            onChange={(e) => setEventStartDate(e.target.value)}
            required
          />
        </div>

        {/* Event End Date */}
        <div className="form-group">
          <label>Event End Date:</label>
          <input
            type="datetime-local"
            value={eventEndDate}
            onChange={(e) => setEventEndDate(e.target.value)}
            required
          />
        </div>

        {/* Event Host */}
        <div className="form-group">
          <label>Event Host:</label>
          <input
            type="text"
            value={eventHost}
            onChange={(e) => setEventHost(e.target.value)}
            placeholder="Enter host name"
            required
          />
        </div>

        {/* Event Description */}
        <div className="form-group">
          <label>Description:</label>
          <textarea
            value={eventDescription}
            onChange={(e) => setEventDescription(e.target.value)}
            placeholder="Enter event description"
            required
          />
        </div>

        {/* Submit Button */}
        <button type="submit" className="create-event-button">Create Event</button>
      </form>

      {/* Back Button */}
      <button onClick={handleBackClick} className="back-button" style={{ marginTop: '20px' }}>Back</button>
    </div>
  );
}

export default CreateEvent;
