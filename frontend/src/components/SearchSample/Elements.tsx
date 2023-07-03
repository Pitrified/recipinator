import React, { useState } from 'react';

import "./Elements.css";

const SearchBox = () => {
  const [inputValue, setInputValue] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [disabledTags, setDisabledTags] = useState<string[]>([]);
  const availableTags = ['Tag1', 'Tag2', 'Tag3']; // Replace with your own available tags

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    console.log("inputValue: ", inputValue);
  };

  const handleTagClick = (tag: string) => {
    // sort tags alphabetically
    const sortedTags = [...selectedTags, tag].sort((a, b) => a.localeCompare(b));
    setSelectedTags(sortedTags);
    setDisabledTags([...disabledTags, tag]);
  };

  const handleRemoveTag = (tag: string) => {
    setSelectedTags(selectedTags.filter((selectedTag) => selectedTag !== tag));
    setDisabledTags(disabledTags.filter((disabledTag) => disabledTag !== tag));
  };

  return (
    <div>
      <input
        type="text"
        value={inputValue}
        className="input-bar"
        onChange={handleInputChange}
        placeholder="Search..."
      />

      <div>
        <h3>Available Tags:</h3>
        {availableTags.map((tag) => (
          <button
            key={tag}
            onClick={() => handleTagClick(tag)}
            disabled={disabledTags.includes(tag)}
            style={{ backgroundColor: disabledTags.includes(tag) ? 'gray' : 'white' }}
          >
            {tag}
          </button>
        ))}
      </div>

      <div>
        <h3>Selected Tags:</h3>
        {selectedTags.map((tag) => (
          <div key={tag}>
            {tag}{' '}
            <button onClick={() => handleRemoveTag(tag)}>X</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchBox;

