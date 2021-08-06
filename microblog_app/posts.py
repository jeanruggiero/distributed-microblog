import uuid
from typing import Tuple


class Post:
    """
    This class represents a post within the microblogging application. A post can be uniquely identified by the tuple of
    username, post_id. This tuple can be obtained using the id property.
    """

    def __init__(self, message: str, username: str):
        """
        Instantiates a new Post within the microblogging application.

        :param message: the message in the post
        :param username: the username of the user who created the post
        """

        if len(message) > 160:
            raise ValueError("Messages must be 160 characters or less.")

        self.message = message
        self.username = username
        self.post_id = uuid.uuid1()

    @property
    def id(self) -> Tuple[str, uuid.UUID]:
        return self.username, self.post_id
