import React, { useEffect, useState } from 'react';
import Login from './components/login';
import Dashboard from './components/dashboard';
import CreateEvent from './components/createEvent';
import AdminPage from './components/adminPage';
import UserEventPage from './components/userPage'; // Assuming this exists
import { getUserProfile, sendUserInfoToBackend } from './services/spotifyService'; // Add your sendUserInfoToBackend logic here
import './styles/App.css'; 
import { Routes, Route, useNavigate } from 'react-router-dom';

function App() {
  const [token, setToken] = useState('');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Parsing the access token from the URL after Spotify login
    const hash = window.location.hash;
    let token = window.localStorage.getItem('token');

    if (!token && hash) {
      const parsedToken = hash
        .substring(1)
        .split('&')
        .find((elem) => elem.startsWith('access_token'))
        ?.split('=')[1];

      if (parsedToken) {
        token = parsedToken;
        window.location.hash = '';
        window.localStorage.setItem('token', token);
        navigate('/');
      }
    }

    setToken(token);
  }, [navigate]);

  useEffect(() => {
    if (token) {
      setLoading(true);
      getUserProfile(token)
        .then((userData) => {
          setUser(userData);
          console.log('User Profile Data:', userData);
          // Send the user information to the backend
          sendUserInfoToBackend(userData);
          setLoading(false);
        })
        .catch((err) => {
          console.error('Error fetching user profile:', err);
          setLoading(false);
        });
    }
  }, [token]);

  const logout = () => {
    setToken('');
    setUser(null);
    window.localStorage.removeItem('token');
    navigate('/'); // Redirect to home after logging out
  };

  return (
    <div className="App">
      {!token ? (
        <Login />
      ) : (
        loading ? (
          <p>Loading...</p>
        ) : (
          <Routes>
            <Route path="/" element={<Dashboard user={user} onLogout={logout} />} />
            <Route path="/create-event" element={<CreateEvent />} />
            <Route path="/admin/:eventCode" element={<AdminPage />} />
            <Route path="/event/:eventCode" element={<UserEventPage />} />
            <Route path="*" element={<p>Page not found</p>} />
          </Routes>
        )
      )}
    </div>
  );
}

export default App;
