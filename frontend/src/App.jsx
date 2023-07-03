import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar/Navbar";
import Recipe from "./components/Recipe/Recipe.tsx";
import About from "./pages/about";
import DragMe from "./pages/sample_drag";
import SearchMe from "./pages/sample_search";
import ShowRecipeList from "./pages/recipe_list";
import BrowseRecipes from "./pages/recipe_browser";

import "./App.css";

function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Recipe />} />
          <Route path="/about" element={<About />} />
          <Route path="/dragme" element={<DragMe />} />
          <Route path="/searchme" element={<SearchMe />} />
          <Route path="/recipelist" element={<ShowRecipeList />} />
          <Route path="/recipebrowse" element={<BrowseRecipes />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
