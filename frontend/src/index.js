import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import CreateEvent from './components/createEvent';
import AdminPage from './components/adminPage';
import UserEventPage from './components/userPage'; // Import UserEventPage
import './styles/index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/redirect" element={<App />} />
        <Route path="/create-event" element={<CreateEvent />} />
        <Route path="/admin/:eventCode" element={<AdminPage />} />
        <Route path="/event/:eventCode" element={<UserEventPage />} /> {/* Add UserEventPage route */}
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
