import React, { useEffect, useState } from 'react';
import Login from './components/login';
import { getUserProfile } from './services/spotifyService';
import './App.css'; 
import { useNavigate } from 'react-router-dom';

function App() {
  const [token, setToken] = useState('');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [eventCode, setEventCode] = useState('');
  const navigate = useNavigate(); 

  useEffect(() => {
    // Parsing the access token from the URL after Spotify login
    const hash = window.location.hash;
    let token = window.localStorage.getItem('token');

    if (!token && hash) {
      const parsedToken = hash
        .substring(1)
        .split('&')
        .find(elem => elem.startsWith('access_token'))
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
        .then(userData => {
          setUser(userData);
          setLoading(false);
        })
        .catch(err => {
          console.error('Error fetching user profile:', err);
          setLoading(false);
        });
    }
  }, [token]);

  const logout = () => {
    setToken('');
    setUser(null);
    window.localStorage.removeItem('token');
  };

  const handleEventCodeSubmit = () => {
    console.log(`Entered Event Code: ${eventCode}`);
    navigate(`/event/${eventCode}`);
  };

  const handleCreateEvent = () => {
    navigate('/create-event');
  };

  return (
    <div className="App">
      {!token ? (
        <Login />
      ) : (
        <div>
          <button onClick={logout}>Logout</button>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <div>
              <h1>Welcome, {user ? user.display_name : 'Spotify User'}</h1>
              {user && (
                <div>
                  {user.images.length > 0 && (
                    <img src={user.images[0].url} alt="Profile" width="100" />
                  )}
                  <p>Email: {user.email}</p>
                </div>
              )}
              <div className="event-actions">
                <div className="enter-event">
                  <h3>Enter Event Code</h3>
                  <input
                    type="text"
                    value={eventCode}
                    onChange={e => setEventCode(e.target.value)}
                    placeholder="Enter event code"
                  />
                  <button onClick={handleEventCodeSubmit}>Submit</button>
                </div>
                <div className="create-event">
                  <h3>Or Create a New Event</h3>
                  <button onClick={handleCreateEvent}>Create Event</button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
