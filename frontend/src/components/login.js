import React from 'react';
import '../styles/login.css'; 

// const CLIENT_ID = process.env.REACT_APP_SPOTIFY_CLIENT_ID;
// const REDIRECT_URI = process.env.REDIRECT_URI;
// const AUTH_ENDPOINT = process.env.AUTH_ENDPOINT;
// const RESPONSE_TYPE = 'token';

const CLIENT_ID = 'c51e5235da0849e3a6b4e04c0b035f2b';
const REDIRECT_URI = 'http://10.196.0.110:3000/redirect';
const AUTH_ENDPOINT = 'http://accounts.spotify.com/authorize';
const RESPONSE_TYPE = 'token';

console.log("CLIENT_ID:", CLIENT_ID); 
console.log("REDIRECT_URI:", REDIRECT_URI); 

function Login() {
  const handleLogin = () => {
    if (!CLIENT_ID || !REDIRECT_URI) {
      console.error("Spotify Client ID or Redirect URI is not set.");
      return;
    }
    
    window.location.href = `${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}&scope=user-read-private user-read-email&show_dialog=true`;
  };


return (
    <div className="login-container">
      <div className="login-content">
        <h2>Welcome to Groove</h2>
        <p>Connect your Spotify account.</p>
        <button className="login-button" onClick={handleLogin}>
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg"
            alt="Spotify Logo"
            className="spotify-logo"
          />
          Connect
        </button>
      </div>
    </div>
  );
}

export default Login;

