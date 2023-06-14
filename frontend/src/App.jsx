import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar/Navbar';
import Recipe from "./components/Recipe/Recipe.tsx";
import About from './pages/about';
import DragMe from './pages/sample_drag';

import './App.css';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path='/' element={<Recipe />} />
        <Route path='/about' element={<About />} />
        <Route path='/dragme' element={<DragMe />} />
      </Routes>
    </Router>
  );
}

export default App;