from .posts import Post
from typing import Iterable, Tuple
from threading import Lock


class User:
    """
    Represents a user of the microblogging platform. The user's data is stored on disk so that it is retrievable
    after an application failure. Locking is used to prevent concurrent access to the individual data structures.
    """

    def __init__(self, username):
        """
        Instantiates a new User.
        :param username: the unique username of this user
        """
        self.username = username

        # Locks for all of the data structures
        self.posts_lock = Lock()
        self.reposts_lock = Lock()
        self.likes_lock = Lock()

    @property
    def posts(self) -> Iterable[Post]:
        """Returns an iterable containing all of this user's posts."""
        try:
            with open(f"state/{self.username}_posts", "r") as f:
                return [Post.loads(post) for post in f]
        except FileNotFoundError:
            return []

    @property
    def reposts(self) -> Iterable[str]:
        """Returns an iterable containing the post ids of all of this user's reposts."""
        try:
            with open(f"state/{self.username}_reposts", "r") as f:
                return [post_id for post_id in f]
        except FileNotFoundError:
            return []

    @property
    def likes(self) -> Iterable[str]:
        """Returns an iterable containing the post ids of all of this user's likes."""
        try:
            with open(f"state/{self.username}_likes", "r") as f:
                return [post_id for post_id in f]
        except FileNotFoundError:
            return []

    def repost(self, post_id: str):
        """
        Adds the provided post_id to the list of posts reposted by this user.
        :param post_id: the id of the post to repost
        """
        with self.reposts_lock:
            with open(f"state/{self.username}_reposts", "a") as f:
                f.write(post_id + "\n")

    def post(self, message: str):
        """
        Creates a new Post with the provided message.
        :param message: the message to post
        """
        with self.posts_lock:
            with open(f"state/{self.username}_posts", "a") as f:
                f.write(Post(message, self.username).dumps() + "\n")

    def like(self, post_id: str):
        """
        Adds the provided post_id to the list of posts liked by this user.
        :param post_id: the id of the post to like
        """
        with self.likes_lock:
            with open(f"state/{self.username}_likes", "a") as f:
                f.write(post_id + "\n")

    def get_posts(self, n: int = 10) -> Iterable[Post]:
        """
        Returns an iterable of the n most recent posts from this user.
        :param n: the number of posts to return
        :return: an iterable of the n most recent posts from this user
        """
        with self.posts_lock:
            return sorted(self.posts, key=lambda p: p.id)[:n]

    def get_likes(self, n: int = 10) -> Iterable[str]:
        """
        Returns an iterable of the n most recent likes from this user.
        :param n: the number of likes to return
        :return: an iterable of the n most recent likes from this user
        """
        with self.likes_lock:
            return sorted(self.likes)[:n]

    def get_reposts(self, n: int = 10) -> Iterable[str]:
        """
        Returns an iterable of the n most recent reposts from this user.
        :param n: the number of reposts to return
        :return: an iterable of the n most recent reposts from this user
        """
        with self.reposts_lock:
            return sorted(self.reposts)[:n]
