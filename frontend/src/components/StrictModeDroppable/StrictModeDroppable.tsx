import React from "react";
import { useEffect, useState } from "react";

import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

// fix strict mode failure
// https://github.com/atlassian/react-beautiful-dnd/issues/2399
const StrictModeDroppable = ({ children, ...props }) => {
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

export default StrictModeDroppable;
