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
    userid: int
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
        print(f"Loading post from shortcode {shortcode} ...")
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
        post_fol = IG_FOL / "posts" / f"{post.shortcode}"
        if not post_fol.exists():
            post_fol.mkdir(parents=True)

        # save the url content here
        # TODO are those always jpg?
        has_url_media = False
        r = requests.get(post.url, allow_redirects=True)
        if r.status_code == 200:
            url_media_fp = post_fol / "p_url.jpg"
            url_media_fp.write_bytes(r.content)
            has_url_media = True

        # save the video content here
        # TODO are those always mp4?
        has_video_url_media = False
        if post.video_url is not None:
            r = requests.get(post.video_url, allow_redirects=True)
            if r.status_code == 200:
                video_url_media_fp = post_fol / "p_video_url.mp4"
                video_url_media_fp.write_bytes(r.content)
                has_video_url_media = True

        # we have to download the media first to
        # post_fol = IG_FOL/'posts' / f"{post.shortcode}"
        # then we save the path to the media in this class
        return cls(
            post.shortcode,
            caption,
            title,
            post.profile,
            post.owner_id,
            has_url_media,
            has_video_url_media,
        )

    @classmethod
    def from_json(cls, shortcode: str) -> Self | None:
        """Initialize from a JSON file, if it exists."""
        print(f"Loading post from json {shortcode} ...")
        json_fol = IG_FOL / "posts" / f"{shortcode}"
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
        post_fol = IG_FOL / "posts" / f"{self.shortcode}"
        if not post_fol.exists():
            post_fol.mkdir(parents=True)
        json_fp = post_fol / "data.json"
        json_fp.write_text(json_str)

    @staticmethod
    def has_json(shortcode: str) -> bool:
        """Check if a JSON file exists."""
        json_fol = IG_FOL / "posts" / f"{shortcode}"
        json_fp = json_fol / "data.json"
        return json_fp.exists()

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


@dataclass
class ProfileIg:
    """Instagram profile, saved as json."""

    # username can change for a given author
    username: str
    userid: int
    full_name: str
    biography: str
    followers: int
    has_profile_pic_url_media: bool

    @classmethod
    def load_profile(cls, username: str, L: Instaloader | None = None) -> Self:
        """Load a profile, from the cache if possible."""
        # try to load from a JSON file
        profile_ig = cls.from_json(username)
        if profile_ig:
            return profile_ig
        # check that we have a valid L
        if L is None:
            raise ValueError("L must be provided if the profile is not cached")
        # if it doesn't exist, load it from the internet
        profile_ig = cls.from_username(username, L)
        return profile_ig

    @classmethod
    def from_username(cls, username: str, L: Instaloader) -> Self:
        """Initialize from a username."""
        print(f"Loading profile from username {username} ...")
        # get the Profile
        profile = Profile.from_username(L.context, username)
        # turn it into a ProfileIg
        profile_ig = cls.from_profile(profile)
        # save it to a JSON file
        profile_ig.to_json()
        return profile_ig

    @classmethod
    def from_profile(cls, profile: Profile) -> Self:
        """Initialize from a Profile, downloading media as well.

        https://instaloader.github.io/module/structures.html#profiles

        Useful properties:
        - profile.full_name
        - profile.biography
        - profile.followers
        - profile.profile_pic_url
        """
        # download the media here
        profile_fol = IG_FOL / "profiles" / f"{profile.username}"
        if not profile_fol.exists():
            profile_fol.mkdir(parents=True)

        # save the profile pic here
        has_profile_pic_url_media = False
        r = requests.get(profile.profile_pic_url, allow_redirects=True)
        if r.status_code == 200:
            profile_pic_url_media_fp = profile_fol / "profile_pic_url.jpg"
            profile_pic_url_media_fp.write_bytes(r.content)
            has_profile_pic_url_media = True

        return cls(
            profile.username,
            profile.userid,
            profile.full_name,
            profile.biography,
            profile.followers,
            has_profile_pic_url_media,
        )

    @classmethod
    def from_json(cls, username: str) -> Self | None:
        """Initialize from a JSON file, if it exists."""
        print(f"Loading profile from json {username} ...")
        json_fol = IG_FOL / "profiles" / f"{username}"
        json_fp = json_fol / f"data.json"
        if not json_fp.exists():
            return None
        json_str = json_fp.read_text()
        json_obj = json.loads(json_str)
        profile_ig = jsons.load(json_obj, cls=cls)

        # check that the media files still exist
        profile_ig.has_profile_pic_url_media = (
            json_fol / "profile_pic_url.jpg"
        ).exists()

        return profile_ig

    def to_json(self) -> None:
        """Save to a JSON file."""
        print(f"Saving profile to json {self.username}...")
        json_str = jsons.dumps(
            self,
            jdkwargs=dict(indent=4),
        )
        profile_fol = IG_FOL / "profiles" / f"{self.username}"
        if not profile_fol.exists():
            profile_fol.mkdir(parents=True)
        json_fp = profile_fol / "data.json"
        json_fp.write_text(json_str)

    @staticmethod
    def has_json(username: str) -> bool:
        """Check if a JSON file exists."""
        json_fol = IG_FOL / "profiles" / f"{username}"
        json_fp = json_fol / "data.json"
        return json_fp.exists()

    def __repr__(self) -> str:
        """Return a string representation of this object."""
        clean_bio = self.biography.replace("\n", " ")
        clean_bio = f"{clean_bio[:40]}{' ...' if len(self.biography)>40 else ''}"
        return (
            f"ProfileIg("
            f"username={self.username}, "
            f"full_name={self.full_name}, "
            f"biography={clean_bio}, "
            f"followers={self.followers}, "
            f"profile_pic_url={self.has_profile_pic_url_media})"
        )

    def __str__(self) -> str:
        """Return a string representation of this object."""
        return self.__repr__()
