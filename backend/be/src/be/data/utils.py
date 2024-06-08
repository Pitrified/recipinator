"""Utility functions for the whole package."""

from pathlib import Path
from typing import Literal

from loguru import logger as lg


def get_resource(
    which_res: Literal[
        "root_fol",
        "data_fol",
        "media_fol",
        "ig_fol",
        "database_fp",
    ]
) -> Path:
    """Get the path of the requested resource."""
    # # resources
    # if which_res == "hand_landmarker.task":
    #     mp_model_fol = Path("~/.mediapipe/models").expanduser()
    #     hand_landmark_model_path = mp_model_fol / "hand_landmarker.task"
    #     return hand_landmark_model_path

    # # folders that are not in the package
    # if which_res == "hand_fol":
    #     return Path.home() / "data" / "hand"

    # folders that are in the package
    if which_res == "root_fol":
        return Path(__file__).absolute().parents[3]
    elif which_res == "data_fol":
        return get_resource("root_fol") / "data"
    elif which_res == "media_fol":
        return get_resource("data_fol") / "media"
    elif which_res == "ig_fol":
        return get_resource("data_fol") / "ig"
    elif which_res == "database_fp":
        return get_resource("data_fol") / "database.db"


def check_create_fol(fol: Path) -> None:
    """Check if the folder exists, if not create it."""
    if not fol.exists():
        fol.mkdir(parents=True)
