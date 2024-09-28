import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/createEvent.css';


function CreateEvent() {
  const navigate = useNavigate(); 

  const handleBackClick = () => {
    navigate(-1); 
  };

  return (
    <div>
      <h2>Create a New Event</h2>
      {}
      <form>
        <div>
          <label>Event Name:</label>
          <input type="text" placeholder="Enter event name" />
        </div>
        <div>
          <label>Description:</label>
          <textarea placeholder="Enter event description" />
        </div>
        <button type="submit">Create Event</button>
      </form>
      {/* Back Button */}
      <button onClick={handleBackClick} style={{ marginTop: '20px' }}>Back</button>
    </div>
  );
}

export default CreateEvent;
