import React, { useState } from "react";

import "./SearchBox.css";

const SearchBox = ({
  availableTags,
  selectedTags,
  searchBarValue,
  handleSearchBarChange,
  handleTagAdd,
  handleTagRemove,
}) => {
  const [disabledTags, setDisabledTags] = useState<string[]>([]);

  const onTagAdd = (tag: string) => {
    setDisabledTags([...disabledTags, tag]);
    handleTagAdd(tag);
  };

  const onTagRemove = (tag: string) => {
    setDisabledTags(disabledTags.filter((disabledTag) => disabledTag !== tag));
    handleTagRemove(tag);
  };

  return (
    <div className="search-box-container">
      <input
        type="text"
        value={searchBarValue}
        className="search-box-input-bar"
        onChange={handleSearchBarChange}
        placeholder="Search..."
      />

      <div>
        <h3>Available Tags:</h3>
        {availableTags.map((tag) => (
          <button
            key={tag}
            onClick={() => onTagAdd(tag)}
            disabled={disabledTags.includes(tag)}
            style={{
              backgroundColor: disabledTags.includes(tag) ? "gray" : "white",
            }}
          >
            {tag}
          </button>
        ))}
      </div>

      <div>
        <h3>Selected Tags:</h3>
        {selectedTags.map((tag) => (
          <div key={tag}>
            {tag} <button onClick={() => onTagRemove(tag)}>X</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchBox;
