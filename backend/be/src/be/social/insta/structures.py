"""Instagram post and profile structures."""


import json
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import jsons
from be.data.utils import get_resource
from instaloader.structures import Post, Profile

MEDIA_FOL = get_resource("media_fol")
IG_FOL = MEDIA_FOL / "ig"


@dataclass
class PostIg:
    """Instagram post, saved as json."""

    shortcode: str
    caption: str
    title: str
    profile: str
    url_media: str
    video_url_media: str

    @classmethod
    def from_post(cls, post: Post) -> Self:
        """Initialize from a post."""
        caption = post.caption if post.caption else ""
        title = post.title if post.title else ""
        video_url = post.video_url if post.video_url else ""
        # FIXME: do not save the urls, but the media
        # we have to download the media first to
        # post_fol = IG_FOL / f"{post.shortcode}"
        # then we save the path to the media in this class
        return cls(
            post.shortcode,
            caption,
            title,
            post.profile,
            post.url,
            video_url,
        )

    @classmethod
    def from_post_save(cls, post: Post) -> Self:
        """Initialize from a post and save to a JSON file."""
        post_ig = cls.from_post(post)
        post_ig.to_json()
        return post_ig

    @classmethod
    def from_json(cls, shortcode: str) -> Self | None:
        """Initialize from a JSON file, if it exists."""
        json_fp = IG_FOL / f"{shortcode}" / "data.json"
        if not json_fp.exists():
            return None
        json_str = json_fp.read_text()
        json_obj = json.loads(json_str)
        post_ig = jsons.load(json_obj, cls=cls)
        return post_ig

    def to_json(self) -> None:
        """Save to a JSON file."""
        json_str = jsons.dumps(self)
        post_fol = IG_FOL / f"{self.shortcode}"
        if not post_fol.exists():
            post_fol.mkdir(parents=True)
        json_fp = post_fol / "data.json"
        json_fp.write_text(json_str)

    def __repr__(self) -> str:
        """Return a string representation of this object."""
        return (
            f"PostIg("
            f"shortcode={self.shortcode}, "
            f"caption={self.caption}, "
            f"title={self.title}, "
            f"profile={self.profile}, "
            f"url={self.url_media}, "
            f"video_url={self.video_url_media})"
        )

    def __str__(self) -> str:
        """Return a string representation of this object."""
        return self.__repr__()
