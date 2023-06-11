import React, { useState, useEffect } from "react";

import "./Step.css";

const Step = ({ step, handleSelectWhichStepAfter }) => {
  const [editing, setEditing] = useState(false);
  const [updatedText, setUpdatedText] = useState(step.text);

  const handleEditClick = () => {
    setEditing(true);
  };

  const handleInputChange = (e) => {
    setUpdatedText(e.target.value);
  };

  const handleSaveClick = async () => {
    try {
      console.log("Step to save:", updatedText, step.id);
      // const response = await axios.put(`${api_url}/api/step/${stepId}`, {
      //   text: updatedText,
      // });
      // console.log("Step saved:", response.data);
      // You can perform any additional actions after the step is successfully saved
      setEditing(false);
    } catch (error) {
      console.error("Error saving step:", error);
    }
  };

  return (
    <li className="step-item">
      {editing ? (
        <div className="step-item-cont">
          <input
            type="text"
            className="step-text"
            value={updatedText}
            onChange={handleInputChange}
          />
          <button className="save-step-button" onClick={handleSaveClick}>
            Save
          </button>
        </div>
      ) : (
        <div className="step-item-cont">
          <div className="step-header">
            <span className="step-number">Step {step.id}:</span>
            <p className="step-text">{step.text}</p>
          </div>
          <div className="step-actions">
            <button className="edit-step-button" onClick={handleEditClick}>
              Edit
            </button>
            <button onClick={handleSelectWhichStepAfter}>+</button>
          </div>
        </div>
      )}
    </li>
  );
};

const StepInput = ({ value, onChange, onAddStepAfter }) => {
  return (
    <div className="step-input">
      <input
        type="text"
        className="step-input-text"
        value={value}
        onChange={onChange}
      />
      <button className="step-input-button" onClick={onAddStepAfter}>
        Add Step
      </button>
    </div>
  );
};

export { Step, StepInput };