import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import CreateEvent from './components/createEvent'; 

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/redirect" element={<App />} />
        <Route path="/create-event" element={<CreateEvent />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
