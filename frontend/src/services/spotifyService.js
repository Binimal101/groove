import axios from 'axios';

// Base URL for Spotify API
const SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1';

// Function to fetch the user's Spotify profile
export const getUserProfile = async (accessToken) => {
  console.log('Fetching Spotify user profile...');
  try {
    const response = await axios.get(`${SPOTIFY_API_BASE_URL}/me`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    console.log('Successfully fetched Spotify user profile:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error fetching Spotify user profile:', error);
    return null;
  }
};

// Function to send user information to backend
export const sendUserInfoToBackend = async (userData) => {
  try {
    const backendUrl = 'https://backend-service-453549355181.us-central1.run.app/event/create'; // Update this URL to your backend endpoint
    console.log('Sending user info to backend:', userData);
    const response = await axios.post(backendUrl, userData);
    console.log('Successfully sent user info to backend:', response.data);
  } catch (error) {
    console.error('Error sending user information to backend:', error);
  }
};
