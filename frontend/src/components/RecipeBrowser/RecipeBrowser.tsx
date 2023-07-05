import React, { useState, useEffect } from "react";
import axios from "axios";

import { API_URL } from "../../config";
import RecipeSorter from "../RecipeSorter/RecipeSorter";
import SearchBox from "../SearchBox/SearchBox";

const RecipeBrowser = () => {
  // list of recipes to show
  const [recipes, setRecipes] = useState<any[]>([]);

  // all the tags available to filter by
  const [availableTags, setAvailableTags] = useState<any[]>([]);
  // tags that are currently selected
  const [selectedTags, setSelectedTags] = useState<any[]>([]);
  // current search bar value
  const [searchBarValue, setSearchBarValue] = useState<string>("");

  useEffect(() => {
    fetchRecipes();
    fetchTags();
  }, []);

  const fetchRecipes = async () => {
    try {
      // TODO: fetch considering tags and search bar status
      const response = await axios.get(`${API_URL}/recipes`);
      console.log("response.data:", response.data);
      setRecipes(response.data);
    } catch (error) {
      console.error("Error fetching recipe data:", error);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await axios.get(`${API_URL}/tags`);
      console.log("response.data:", response.data);
      setAvailableTags(response.data);
    } catch (error) {
      console.error("Error fetching tag data:", error);
    }
  };

  // receive the shortcodes to shuffle the recipes
  const handleDragEnd = async (shortcodeClicked, shortcodeReplaced) => {
    console.log(shortcodeClicked, shortcodeReplaced);
    const response = await axios.post(`${API_URL}/recipes/shuffle`, {
      shortcodeClicked: shortcodeClicked,
      shortcodeReplaced: shortcodeReplaced,
      shuffle_type: "drag_and_drop",
    });
    console.log(response);
    // we already updated the frontend, the list is already in the correct order
    // fetchRecipes();
  };

  // TODO: here we receive the tags to filter the recipes
  const handleTagAdd = (tag: string) => {
    // sort tags alphabetically
    const sortedTags = [...selectedTags, tag].sort((a, b) =>
      a.localeCompare(b)
    );
    setSelectedTags(sortedTags);
    // TODO: filter recipes
    // is that being async a problem? what happens lol?
    fetchRecipes();
  };

  const handleTagRemove = (tag: string) => {
    const sortedTags = selectedTags.filter((t) => t !== tag);
    setSelectedTags(sortedTags);
    fetchRecipes();
  };

  const handleSearchBarChange = (event) => {
    console.log(event.target.value);
    setSearchBarValue(event.target.value);
    fetchRecipes();
  };

  return (
    <div className="recipe-browser-container">
      <SearchBox
        availableTags={availableTags}
        selectedTags={selectedTags}
        searchBarValue={searchBarValue}
        handleSearchBarChange={handleSearchBarChange}
        handleTagAdd={handleTagAdd}
        handleTagRemove={handleTagRemove}
      />
      <RecipeSorter
        recipes={recipes}
        handleDragEnd={handleDragEnd}
        setRecipes={setRecipes}
      />
      {/* TODO: add pagination, leave some overlap between pages
      so that a recipe can be sent to another page */}
    </div>
  );
};

export default RecipeBrowser;
