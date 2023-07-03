import React, { useState, useEffect } from "react";

import { Step, StepInput } from "../Step/Step";

import "./Preparation.css";

const Preparation = ({ prep, addStep }) => {
  const [newStepText, setNewStepText] = useState("");
  const [selectedStepId, setSelectedStepId] = useState(
    prep.steps[prep.steps.length - 1]?.id
  );
  console.log(
    "Selected step:",
    selectedStepId,
    " for ",
    prep.id,
    prep.steps.length
  );

  const handleAddStepAfter = () => {
    console.log("Maybe adding step after:", selectedStepId);
    if (newStepText !== "" && selectedStepId !== null) {
      console.log("Adding step after:", selectedStepId);
      addStep(prep.id, selectedStepId, newStepText);
      setNewStepText("");
      setSelectedStepId(null);
    }
  };

  const handleSelectWhichStepAfter = (stepId) => {
    // If the step is already selected, deselect it
    if (selectedStepId === stepId) {
      return setSelectedStepId(null);
    }
    return setSelectedStepId(stepId);
  };

  const moveInputAfterSelectedStep = () => {
    return prep.steps.map((step) => (
      <React.Fragment key={step.id}>
        <Step
          step={step}
          handleSelectWhichStepAfter={() => handleSelectWhichStepAfter(step.id)}
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
      <h2>{prep.name}</h2>
      <ol className="preparation-list">{moveInputAfterSelectedStep()}</ol>
    </div>
  );
};

export default Preparation;
