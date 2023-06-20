"""Load data from Instagram.

This could be done directly into the database,
but I'm scared of SQL so I'm caching it in a json file,
so that I can load it into the database later (as many times as needed).

* https://instaloader.github.io/as-module.html#python-module-instaloader
* https://instaloader.github.io/module/structures.html#posts
* https://instaloader.github.io/module/structures.html#profiles
"""

from be.social.insta.structures import PostIg
from instaloader import instaloader
from instaloader.structures import Post, Profile


class InstaLoader:
    """Load data from instagram.

    Returns data as PostIg objects.
    """

    def __init__(self, username: str) -> None:
        """Initialize the class."""
        self.username = username
        self.L = instaloader.Instaloader()

    def login(self) -> None:
        """Login."""
        # MAYBE should we check if the session is still valid?
        # MAYBE should we save in a custom location?
        try:
            self.L.load_session_from_file(self.username)
        except FileNotFoundError:
            self.L.interactive_login(self.username)
            self.L.save_session_to_file()

    # def _load_post(self, shortcode: str) -> Post:
    #     r"""Load a Post.
    #     """
    #     return Post.from_shortcode(self.L.context, shortcode)

    def load_post(self, shortcode: str) -> PostIg:
        """Load a post from the cache."""
        post_ig = PostIg.load_post(shortcode, self.L)
        return post_ig

    def load_profile(self, username: str) -> Profile:
        """Load a profile.

        https://instaloader.github.io/module/structures.html#profiles

        Useful properties:
        - profile.full_name
        - profile.biography
        - profile.followers
        - profile.profile_pic_url
        - profile.external_url
        """
        return Profile.from_username(self.L.context, username)


def main() -> None:
    """Login, load a post and print some info."""
    # create an instance of InstaLoader
    my_username = input("Instagram username: ")
    il = InstaLoader(my_username)

    # login
    il.login()

    # load a post
    p = il.load_post("CsEj0n9Kefd")
    print(p.caption)
    print(p.title)
    print(p.profile)
    print(p.has_url_media)
    print(p.has_video_url_media)


if __name__ == "__main__":
    main()
