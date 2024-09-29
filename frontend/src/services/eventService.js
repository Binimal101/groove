import axios from 'axios';

const API_BASE_URL = 'https://backend-service-453549355181.us-central1.run.app/event/create'; // Replace with your backend URL

export const joinEvent = async (eventCode, user) => {
  console.log('Sending POST request to join event:', {
    eventCode,
    user,
  });
  try {
    const response = await axios.post(`${API_BASE_URL}`, {
      eventCode,
      user,
    });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : new Error('Network Error');
  }
};

export const createEvent = async (eventDetails) => {
  console.log('Sending POST request to create event:', eventDetails);
  try {
    // Sending POST request to backend API with eventDetails as the body
    const response = await axios.post(`${API_BASE_URL}`, eventDetails, {
        eventCode: eventDetails.eventCode,
        eventDetails,
    });

    console.log('Response from backend:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error creating event:', error.response ? error.response.data : 'Network Error');
    throw error.response ? error.response.data : new Error('Network Error');
  }
};
