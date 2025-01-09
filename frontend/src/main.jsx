import { StrictMode } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Use Routes for React Router v6
import { createRoot } from 'react-dom/client';
import Create from './Create.jsx';
import './index.css';
import App from './App.jsx';

// Define the main Routes component
const AppRoutes = () => (
  <Routes>
    <Route path="/new/" element={<Create />} />
    <Route path="/" element={<App />} />
  </Routes>
);

// Render the application
const root = createRoot(document.getElementById('root'));
root.render(
  <StrictMode>
    <Router>
      <AppRoutes />
    </Router>
  </StrictMode>
);
