import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import Maker from './components/Maker';
import Breaker from './components/Breaker';
import Home from './components/Home';

function App(): JSX.Element {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            {/* Added these for easier navigation */}
            <li>
              <Link to="/maker">Maker</Link>
            </li>
            <li>
              <Link to="/breaker">Breaker</Link>
            </li>
            {/* Navigation end */}
          </ul>
        </nav>
        <Routes>
          <Route path="/maker" element={<Maker />} />
          <Route path="/breaker" element={<Breaker />} />
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
