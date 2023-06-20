"""Instagram post and profile structures."""

import requests

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import jsons
from be.data.utils import get_resource
from instaloader.structures import Post, Profile
from instaloader.instaloader import Instaloader

MEDIA_FOL = get_resource("media_fol")
IG_FOL = MEDIA_FOL / "ig"


@dataclass
class PostIg:
    """Instagram post, saved as json."""

    shortcode: str
    caption: str
    title: str
    profile: str
    has_url_media: bool
    has_video_url_media: bool

    @classmethod
    def load_post(cls, shortcode: str, L: Instaloader | None = None) -> Self:
        """Load a post, from the cache if possible."""
        # try to load from a JSON file
        post_ig = cls.from_json(shortcode)
        if post_ig:
            return post_ig
        # check that we have a valid L
        if L is None:
            raise ValueError("L must be provided if the post is not cached")
        # if it doesn't exist, load it from the internet
        post_ig = cls.from_shortcode(shortcode, L)
        return post_ig

    @classmethod
    def from_shortcode(cls, shortcode: str, L: Instaloader) -> Self:
        """Initialize from a shortcode."""
        print(f"Loading post from shortcode {shortcode}...")
        # get the Post
        post = Post.from_shortcode(L.context, shortcode)
        # turn it into a PostIg
        post_ig = cls.from_post(post)
        # save it to a JSON file
        post_ig.to_json()
        return post_ig

    @classmethod
    def from_post(cls, post: Post) -> Self:
        """Initialize from a Post, downloading media as well.

        https://instaloader.github.io/module/structures.html#posts

        Useful properties:
        - post.caption
        - post.title
        - post.profile
        - post.url
        - post.video_url

        E.g. shortcode = "CsEj0n9Kefd"
            p.caption: "🔥 sweet..."
            p.title: ""
            p.profile: "rhi.scran"
            p.url: "https://instagram.fmxp7-2.fna.fbcdn.net/v/ ..."
            p.video_url: "https://instagram.fmxp7-2.fna.fbcdn.net/v/ ..."
        """
        # caption and title are empty strings if they don't exist
        caption = post.caption if post.caption else ""
        title = post.title if post.title else ""

        # download the media here
        post_fol = IG_FOL / f"{post.shortcode}"
        if not post_fol.exists():
            post_fol.mkdir(parents=True)

        # save the url content here
        # TODO are those always jpg?
        r = requests.get(post.url, allow_redirects=True)  # FIXME
        if r.status_code == 200:
            url_media_fp = post_fol / "p_url.jpg"  # FIXME
            url_media_fp.write_bytes(r.content)  # FIXME
            has_url_media = True
        else:
            has_url_media = False

        # save the video content here
        # TODO are those always mp4?
        if post.video_url is not None:
            r = requests.get(post.video_url, allow_redirects=True)  # FIXME
            if r.status_code == 200:
                video_url_media_fp = post_fol / "p_video_url.mp4"  # FIXME
                video_url_media_fp.write_bytes(r.content)  # FIXME
                has_video_url_media = True
            else:
                has_video_url_media = False
        else:
            has_video_url_media = False

        # we have to download the media first to
        # post_fol = IG_FOL / f"{post.shortcode}"
        # then we save the path to the media in this class
        return cls(
            post.shortcode,
            caption,
            title,
            post.profile,
            has_url_media,
            has_video_url_media,
        )

    @classmethod
    def from_json(cls, shortcode: str) -> Self | None:
        """Initialize from a JSON file, if it exists."""
        print(f"Loading post from json {shortcode}...")
        json_fol = IG_FOL / f"{shortcode}"
        # load the data and turn it into a PostIg
        json_fp = json_fol / "data.json"
        if not json_fp.exists():
            return None
        json_str = json_fp.read_text()
        json_obj = json.loads(json_str)
        post_ig = jsons.load(json_obj, cls=cls)

        # check that the media files still exist
        post_ig.has_url_media = (json_fol / "p_url.jpg").exists()
        post_ig.has_video_url_media = (json_fol / "p_video_url.mp4").exists()

        return post_ig

    def to_json(self) -> None:
        """Save to a JSON file."""
        print(f"Saving post to json {self.shortcode}...")
        json_str = jsons.dumps(
            self,
            jdkwargs=dict(indent=4),
        )
        post_fol = IG_FOL / f"{self.shortcode}"
        if not post_fol.exists():
            post_fol.mkdir(parents=True)
        json_fp = post_fol / "data.json"
        json_fp.write_text(json_str)

    def __repr__(self) -> str:
        """Return a string representation of this object."""
        clean_cap = self.caption.replace("\n", " ")
        clean_cap = f"{clean_cap[:40]}{' ...' if len(self.caption)>40 else ''}"
        return (
            f"PostIg("
            f"shortcode={self.shortcode}, "
            f"title={self.title}, "
            f"profile={self.profile}, "
            f"caption={clean_cap}, "
            f"url={self.has_url_media}, "
            f"video_url={self.has_video_url_media})"
        )

    def __str__(self) -> str:
        """Return a string representation of this object."""
        return self.__repr__()
