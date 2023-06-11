import React, { useState, useEffect } from "react";

import { Step, StepInput } from "../Step/Step";

import "./Preparation.css";

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
      <ol className="preparation-list">{moveInputAfterSelectedStep()}</ol>
    </div>
  );
};

export default Preparation;
