from .posts import Post
from typing import Iterable


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
        self.posts = []

        # List containing post ids for all posts this user has re-posted
        self.reposts = []

        # List containing post ids for all posts this user has liked
        self.likes = []

    def repost(self, post_id):
        """
        Adds the provided post_id to the list of posts reposted by this user.
        :param post_id: the id of the post to repost
        """
        self.reposts.append(post_id)

    def post(self, message: str):
        """
        Creates a new Post with the provided message.
        :param message: the message to post
        """
        self.posts.append(Post(message, self.username))

    def like(self, post_id):
        """
        Adds the provided post_id to the list of posts liked by this user.
        :param post_id: the id of the post to like
        """
        self.likes.append(post_id)

    def get_posts(self, n: int = 10) -> Iterable:
        """
        Returns an iterable of the n most recent posts from this user.

        :param n: the number of posts to return
        :return: an iterable of the n most recent posts from this user
        """
        return sorted(self.posts, key= lambda p: p.id)[:n]

    def get_likes(self, n: int = 10) -> Iterable:
        """
        Returns an iterable of the n most recent likes from this user.

        :param n: the number of likes to return
        :return: an iterable of the n most recent likes from this user
        """
        return sorted(self.likes, key=lambda p: p.id)[:n]

    def get_reposts(self, n: int = 10) -> Iterable:
        """
        Returns an iterable of the n most recent reposts from this user.

        :param n: the number of reposts to return
        :return: an iterable of the n most recent reposts from this user
        """
        return sorted(self.reposts, key=lambda p: p.id)[:n]