import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar/Navbar';
import Recipe from "./components/Recipe/Recipe.tsx";
import About from './pages/about';

import './App.css';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path='/' element={<Recipe />} />
        <Route path='/about' element={<About />} />
      </Routes>
    </Router>
  );
}

export default App;