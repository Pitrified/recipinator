import React from "react";
import { useEffect, useState } from "react";

import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";

import StrictModeDroppable from "../StrictModeDroppable/StrictModeDroppable";

import "./Elements.css";

// a simple step in a recipe
const StepMini = ({ step }) => {
  return (
    <div className="step-container">
      <span className="step-id">{step.idString}:</span>
      <span className="step-text">{step.text}</span>
      <a href={`/about/${step.id}`} className="step-link">
        Go to {step.id}
      </a>
    </div>
  );
};

// a draggable preparation
const PreparationMini = ({ prep }) => {
  const [steps, setSteps] = useState(prep.steps);

  const handleDragEnd = (result) => {
    console.log(result);

    if (!result.destination) return; // Not dropped in a valid location

    console.log(
      "moving from",
      result.source.index,
      "to",
      result.destination.index
    );

    const updatedSteps = Array.from(steps);
    // reorderedStep is the one we are popping off the array
    // delete 1 from position result.source.index
    const [reorderedStep] = updatedSteps.splice(result.source.index, 1);
    // then we insert it at position result.destination.index, deleting 0
    // kinda weird that we define updatedSteps as a const and promptly mutate it
    updatedSteps.splice(result.destination.index, 0, reorderedStep);
    // console.log('updatedSteps', updatedSteps.map(step => step.idString));

    setSteps(updatedSteps);
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className="drag-drop-context">
        <h2>{prep.name}</h2>
        <StrictModeDroppable droppableId="preparation-steps">
          {(provided) => (
            <div
              {...provided.droppableProps}
              ref={provided.innerRef}
              className="preparation-list"
            >
              {steps.map((step, index) => (
                <Draggable
                  key={step.idString}
                  draggableId={step.idString}
                  index={index}
                >
                  {(provided) => (
                    <div
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      ref={provided.innerRef}
                      className="draggable-step"
                    >
                      <StepMini step={step} />
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </StrictModeDroppable>
      </div>
    </DragDropContext>
  );
};

export default PreparationMini;
