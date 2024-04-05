import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import ManageTeamPage from './ManageTeamPage';
import ManageRotaPage from './ManageRotaPage';
import SettingsPage from './SettingsPage';
import Test from './Test';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/manage-team" element={<ManageTeamPage />} />
        <Route path="/manage-rota" element={<ManageRotaPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/test" element={<Test />} />
      </Routes>
    </Router>
  );
};

export default App;
