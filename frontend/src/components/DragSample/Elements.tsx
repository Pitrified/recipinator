import React from "react";

import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

// fix strict mode failure
// https://github.com/atlassian/react-beautiful-dnd/issues/2399
import { useEffect, useState } from "react";
export const StrictModeDroppable = ({ children, ...props }) => {
  const [enabled, setEnabled] = useState(false);
  useEffect(() => {
    const animation = requestAnimationFrame(() => setEnabled(true));
    return () => {
      cancelAnimationFrame(animation);
      setEnabled(false);
    };
  }, []);
  if (!enabled) {
    return null;
  }
  return <Droppable {...props}>{children}</Droppable>;
};

// a simple step in a recipe
const StepMini = ({ step }) => {
  return (
    <div>
      <span>
        {step.idString}:&nbsp;
      </span>
      <span>
        {step.text}
      </span>
    </div>
  );
};

// a draggable preparation
const PreparationMini = ({ prep }) => {
  const [steps, setSteps] = useState(prep.steps);

  const handleDragEnd = (result) => {
    console.log(result);
    console.log('moving from', result.source.index, 'to', result.destination.index);

    if (!result.destination) return; // Not dropped in a valid location

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
      <div>
        <h2>{prep.name}</h2>
        <StrictModeDroppable droppableId="preparation-steps">
          {(provided) => (
            <ol
              {...provided.droppableProps}
              ref={provided.innerRef}
              className="preparation-list"
            >
              {steps.map((step, index) => (
                <Draggable
                  key={step.idString} draggableId={step.idString}
                  index={index}
                >
                  {(provided) => (
                    <li
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      ref={provided.innerRef}
                    >
                      <StepMini step={step} />
                    </li>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </ol>
          )}
        </StrictModeDroppable>
      </div>
    </DragDropContext>
  );
};


export default PreparationMini;
