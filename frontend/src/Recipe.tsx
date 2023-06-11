import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Recipe.css";

const api_url = "http://127.0.0.1:8000";

const Step = ({ id, text, handleAddStepAfter }) => {
  const [editing, setEditing] = useState(false);
  const [updatedText, setUpdatedText] = useState(text);

  const handleEditClick = () => {
    setEditing(true);
  };

  const handleInputChange = (e) => {
    setUpdatedText(e.target.value);
  };

  const handleSaveClick = async () => {
    try {
      console.log("Step to save:", updatedText, id);
      // const response = await axios.put(`${api_url}/api/step/${id}`, {
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
            <span className="step-number">Step {id}:</span>
            <p className="step-text">{text}</p>
          </div>
          <div className="step-actions">
            <button className="edit-step-button" onClick={handleEditClick}>
              Edit
            </button>
            <button onClick={handleAddStepAfter}>+</button>
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

const Preparation = ({ id, name, steps, addStep }) => {
  const [newStepText, setNewStepText] = useState("");
  const [selectedStepId, setSelectedStepId] = useState(
    steps[steps.length - 1]?.id
  );

  const handleAddStepAfter = () => {
    console.log("Maybe adding step after:", selectedStepId);
    if (newStepText !== "" && selectedStepId !== null) {
      console.log("Adding step after:", selectedStepId);
      addStep(id, selectedStepId, newStepText);
      setNewStepText("");
      setSelectedStepId(null);
    }
  };

  const moveInputAfterSelectedStep = () => {
    return steps.map((step) => (
      <React.Fragment key={step.id}>
        <Step
          id={step.id}
          text={step.text}
          handleAddStepAfter={() => {
            // If the step is already selected, deselect it
            if (selectedStepId === step.id) {
              return setSelectedStepId(null);
            }
            return setSelectedStepId(step.id);
          }}
        />
        {selectedStepId === step.id && (
          <StepInput
            value={newStepText}
            onChange={(e) => setNewStepText(e.target.value)}
            onAddStepAfter={handleAddStepAfter}
          />
        )}
      </React.Fragment>
    ));
  };

  return (
    <div>
      <h2>{name}</h2>
      <ol className="step-list">{moveInputAfterSelectedStep()}</ol>
    </div>
  );
};

const Recipe = () => {
  const [recipeData, setRecipeData] = useState(null);

  useEffect(() => {
    fetchRecipeData();
  }, []);

  const fetchRecipeData = async () => {
    try {
      const response = await axios.get(`${api_url}/api/recipe`);
      setRecipeData(response.data);
    } catch (error) {
      console.error("Error fetching recipe data:", error);
    }
  };

  const saveRecipeData = async (updatedRecipeData) => {
    try {
      await axios.put(api_url + "/api/recipe", updatedRecipeData);
    } catch (error) {
      console.error("Error saving recipe data:", error);
    }
  };

  const addStep = async (preparationId, stepId, stepText) => {
    try {
      await axios.post(`${api_url}/api/preparation/${preparationId}/steps`, {
        id: stepId,
        text: stepText,
      });
      fetchRecipeData();
    } catch (error) {
      console.error("Error adding step:", error);
    }
  };

  if (!recipeData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{recipeData.title}</h1>
      {recipeData.preparations.map((preparation) => (
        <Preparation
          key={preparation.id}
          id={preparation.id}
          name={preparation.name}
          steps={preparation.steps}
          addStep={addStep}
        />
      ))}
    </div>
  );
};

export default Recipe;
