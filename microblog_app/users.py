from .posts import Post
from typing import Iterable, Tuple
from threading import Lock

import json


class User:
    """
    Represents a user of the microblogging platform.
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
        try:
            with open(f"state/{self.username}_posts", "r") as f:
                return [Post.loads(post) for post in f]
        except FileNotFoundError:
            return []

    @property
    def reposts(self) -> Iterable[str]:
        try:
            with open(f"state/{self.username}_reposts", "r") as f:
                return [post_id for post_id in f]
        except FileNotFoundError:
            return []

    @property
    def likes(self) -> Iterable[str]:
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
        self.reposts_lock.acquire()

        with open(f"state/{self.username}_reposts", "a") as f:
            f.write(post_id + "\n")

        self.reposts_lock.release()

    def post(self, message: str):
        """
        Creates a new Post with the provided message.
        :param message: the message to post
        """
        self.posts_lock.acquire()

        with open(f"state/{self.username}_posts", "a") as f:
            f.write(Post(message, self.username).dumps() + "\n")

        self.posts_lock.release()

    def like(self, post_id: str):
        """
        Adds the provided post_id to the list of posts liked by this user.
        :param post_id: the id of the post to like
        """
        self.likes_lock.acquire()

        with open(f"state/{self.username}_likes", "a") as f:
            f.write(post_id + "\n")

        self.likes_lock.release()

    def get_posts(self, n: int = 10) -> Iterable[Post]:
        """
        Returns an iterable of the n most recent posts from this user.

        :param n: the number of posts to return
        :return: an iterable of the n most recent posts from this user
        """
        self.posts_lock.acquire()
        posts = sorted(self.posts, key=lambda p: p.id)[:n]
        self.posts_lock.release()
        return posts

    def get_likes(self, n: int = 10) -> Iterable[str]:
        """
        Returns an iterable of the n most recent likes from this user.

        :param n: the number of likes to return
        :return: an iterable of the n most recent likes from this user
        """
        self.likes_lock.acquire()
        likes = sorted(self.likes)[:n]
        self.likes_lock.release()
        return likes

    def get_reposts(self, n: int = 10) -> Iterable[str]:
        """
        Returns an iterable of the n most recent reposts from this user.

        :param n: the number of reposts to return
        :return: an iterable of the n most recent reposts from this user
        """
        self.reposts_lock.acquire()
        reposts = sorted(self.reposts)[:n]
        self.reposts_lock.release()
        return reposts

