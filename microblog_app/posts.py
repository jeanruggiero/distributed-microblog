import uuid
import json
from typing import Tuple


class Post:
    """
    This class represents a post within the microblogging application. A post can be uniquely identified by the tuple of
    username, post_id. This tuple can be obtained using the id property.
    """

    def __init__(self, message: str, username: str, post_id: str = None):
        """
        Instantiates a new Post within the microblogging application.

        :param message: the message in the post
        :param username: the username of the user who created the post
        """

        if len(message) > 160:
            raise ValueError("Messages must be 160 characters or less.")

        self.message = message
        self.username = username
        self.post_id = uuid.UUID(hex=post_id) if post_id else uuid.uuid1()

    @property
    def id(self) -> Tuple[str, uuid.UUID]:
        """Returns the unique identifier of this Post."""
        return self.username, self.post_id

    def __str__(self):
        return f"Post(id={self.post_id.hex}, user={self.username}, '{self.message}')"

    def serialize(self) -> dict:
        """Serializes this Post into a dictionary."""
        return {'post_id': self.post_id.hex, 'username': self.username, 'message': self.message}

    def dumps(self) -> str:
        """Serializes this Post into a string."""
        return json.dumps(self.serialize())

    @classmethod
    def deserialize(cls, post: dict):
        """
        Creates a new Post object based on the serialized post in the provided dictionary object.
        :param post: a dict containing a serialized Post
        :return: the new Post object
        """
        return cls(**post)

    @classmethod
    def loads(cls, post: str):
        """
        Creates a new Post object based on the serialized post in the provided string.
        :param post: a string containing a serialized Post
        :return: the new Post object
        """
        return cls.deserialize(json.loads(post))
