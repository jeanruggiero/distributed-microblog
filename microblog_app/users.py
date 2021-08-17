from .posts import Post
from typing import Iterable
from threading import Lock


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

        # List containing all of this user's posts
        self.posts = []

        # List containing post ids for all posts this user has re-posted
        self.reposts = []

        # List containing post ids for all posts this user has liked
        self.likes = []

        # Locks for all of the data structures
        self.posts_lock = Lock()
        self.reposts_lock = Lock()
        self.likes_lock = Lock()

    def repost(self, post_id):
        """
        Adds the provided post_id to the list of posts reposted by this user.
        :param post_id: the id of the post to repost
        """
        self.reposts_lock.acquire()
        self.reposts.append(post_id)
        self.reposts_lock.release()

    def post(self, message: str):
        """
        Creates a new Post with the provided message.
        :param message: the message to post
        """
        self.posts_lock.acquire()
        self.posts.append(Post(message, self.username))
        self.posts_lock.release()

    def like(self, post_id):
        """
        Adds the provided post_id to the list of posts liked by this user.
        :param post_id: the id of the post to like
        """
        self.likes_lock.acquire()
        self.likes.append(post_id)
        self.likes_lock.release()

    def get_posts(self, n: int = 10) -> Iterable:
        """
        Returns an iterable of the n most recent posts from this user.

        :param n: the number of posts to return
        :return: an iterable of the n most recent posts from this user
        """
        print("Acquiring posts lock")
        self.posts_lock.acquire()
        print("Posts lock acquired!")
        posts = sorted(self.posts, key=lambda p: p.id)[:n]
        self.posts_lock.release()
        print("returning posts")
        return posts

    def get_likes(self, n: int = 10) -> Iterable:
        """
        Returns an iterable of the n most recent likes from this user.

        :param n: the number of likes to return
        :return: an iterable of the n most recent likes from this user
        """
        self.likes_lock.acquire()
        likes = sorted(self.likes, key=lambda p: p.id)[:n]
        self.likes_lock.release()
        return likes

    def get_reposts(self, n: int = 10) -> Iterable:
        """
        Returns an iterable of the n most recent reposts from this user.

        :param n: the number of reposts to return
        :return: an iterable of the n most recent reposts from this user
        """
        self.reposts_lock.acquire()
        reposts = sorted(self.reposts, key=lambda p: p.id)[:n]
        self.reposts_lock.release()
        return reposts