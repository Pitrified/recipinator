import React from "react";

import PreparationMini from "../components/DragSample/Elements";

const DragMe = () => {
  return (
    <PreparationMini prep={{
      "id": 1,
      "name": "Peanut Butter and Jelly Sandwich",
      "steps": [
        {
          "id": 1,
          "idString": "s1",
          "text": "Get two slices of bread"
        },
        {
          "id": 2,
          "idString": "s2",
          "text": "Spread peanut butter on one slice"
        },
        {
          "id": 3,
          "idString": "s3",
          "text": "Spread jelly on the other slice"
        },
        {
          "id": 4,
          "idString": "s4",
          "text": "Put the two slices together"
        }
      ]
    }} />
  );
};

export default DragMe;
