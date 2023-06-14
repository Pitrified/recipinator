from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing) to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this list with the appropriate frontend URL(s)
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class Step(BaseModel):
    id: int
    text: str


class Preparation(BaseModel):
    id: int
    name: str
    steps: List[Step]


class Recipe(BaseModel):
    title: str
    preparations: List[Preparation]


# Mock data
recipe_data = Recipe(
    title="Rep",
    preparations=[
        Preparation(
            id=1,
            name="Preparation 1",
            steps=[
                Step(id=1, text="Do 1"),
                Step(id=2, text="Do 2"),
                Step(id=3, text="Do 3"),
                Step(id=4, text="Do 4"),
                Step(id=5, text="Do 5"),
            ],
        ),
        Preparation(
            id=2,
            name="Preparation 2",
            steps=[Step(id=1, text="Do 1"), Step(id=2, text="Do 2")],
        ),
        Preparation(
            id=3,
            name="Preparation 3",
            steps=[],
        ),
    ],
)


@app.get("/api/recipe")
def get_recipe() -> Recipe:
    return recipe_data


@app.post("/api/preparation/{preparation_id}/steps")
def add_step(preparation_id: int, step: Step):
    print(f"got step: {step}")
    for preparation in recipe_data.preparations:
        if preparation.id == preparation_id:
            if step.id is None:
                # Generate a new step ID
                step_id = len(preparation.steps) + 1
            else:
                step_id = step.id

            insert_index = None
            for i, existing_step in enumerate(preparation.steps):
                if existing_step.id == step_id:
                    # Insert after the selected step
                    insert_index = i + 1
                    break

            # If the selected step is not found, insert at the beginning
            if insert_index is None:
                insert_index = 0

            # Update the step IDs in the list
            for i, existing_step in enumerate(preparation.steps):
                if i >= insert_index:
                    existing_step.id += 1

            # Insert the new step with the updated ID
            new_step = Step(id=step_id + 1, text=step.text)
            preparation.steps.insert(insert_index, new_step)
            return {"message": "Step added successfully"}

    return {"message": "Preparation not found"}


# @app.post("/api/preparation/{preparation_id}/steps")
# def add_step(preparation_id: int, step: Step):
#     print(f"got step: {step}")
#     for preparation in recipe_data.preparations:
#         if preparation.id == preparation_id:
#             if step.id is None:
#                 # Generate a new step ID
#                 step_id = len(preparation.steps) + 1
#             else:
#                 step_id = step.id
#             insert_index = None
#             for i, existing_step in enumerate(preparation.steps):
#                 if existing_step.id == step_id:
#                     # Insert after the selected step
#                     insert_index = i + 1
#                     break
#             # If the selected step is not found, insert at the beginning
#             if insert_index is None:
#                 insert_index = 0
#             # Insert the new step
#             preparation.steps.insert(insert_index, step)
#             return {"message": "Step added successfully"}
#     return {"message": "Preparation not found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
