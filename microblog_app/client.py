from .users import User

import requests
import json
from typing import Iterable, Tuple


class AppInstance:

    def __init__(self, user: User):
        # TODO: start lightweight web server in new thread

        self.user = user

        # TODO: register IP address with user directory service
        self._register(user.username)

    @staticmethod
    def _register(username):
        """
        Registers the IP address of the current user with the User Directory Service.

        :param username: the username to register
        """
        ip = requests.get('http://icanhazip.com').text.strip()

        # TODO: Select a UDS instance at random to register with
        # requests.put(uds_url, {username: ip})

    @staticmethod
    def _get_user_address(username: str) -> User:
        # TODO: issue post request to user directory service to get IP address of user
        return 'http://127.0.0.1'

    def _issue_request(self, username: str, request: str) -> requests.Response:
        return requests.get(self._get_user_address(username), request)

    def get_posts(self, username: str, n: int) -> Iterable[str]:
        response = self._issue_request(username, f"GET /posts?n={n}")
        return json.loads(response.text)

    def get_likes(self, username: str, n: int) -> Iterable[str]:
        response = self._issue_request(username, f"GET /likes?n={n}")
        return json.loads(response.text)

    def get_reposts(self, username: str, n: int) -> Iterable[str]:
        response = self._issue_request(username, f"GET /reposts?n={n}")
        return json.loads(response.text)

    def post(self, message: str):
        pass

    def like(self, post_id: str):
        pass

    def repost(self, post_id: str):
        pass


class MicroblogCommandLineInterface:

    menu = """
        Menu:
          0. Show menu
          1. Get a user's posts
          2. Get a user's likes
          3. Get a user's reposts
          4. Create a post
          5. Like a post
          6. Repost a post
    """

    def __init__(self, app_instance: AppInstance):
        self.app_instance = app_instance

    def run(self):
        print("Welcome to the distributed microblogging app!")
        print(self.menu)

        while True:
            option = int(input('> '))

            try:
                if option == 0:
                    print(self.menu)
                elif option == 1:
                    self.get_posts()
                elif option == 2:
                    self.get_likes()
                elif option == 3:
                    self.get_reposts()
                elif option == 4:
                    self.create_post()
                elif option == 5:
                    self.like_post()
                elif option == 6:
                    self.repost_post()
                else:
                    print("Invalid option, please try again.")

            except requests.ConnectionError as e:
                print(f"Error: could not connect to user.")

            print()

    def _get_prompt(self, item: str) -> Tuple[str, str]:
        username = input("Enter a username: ")
        n = input(f"How many {item} would you like to see? ")

        return username, n

    def get_posts(self):
        print(self.app_instance.get_posts(*self._get_prompt('posts')))

    def get_likes(self):
        print(self.app_instance.get_likes(*self._get_prompt('likes')))

    def get_reposts(self):
        print(self.app_instance.get_reposts(*self._get_prompt('reposts')))

    def create_post(self):
        message = input("Enter message: ")
        self.app_instance.post(message)
        print("Message created!")

    def like_post(self):
        id = input("Enter id of the post to like: ")
        self.app_instance.like(id)

    def repost_post(self):
        id = input("Enter id of the post to repost: ")
        self.app_instance.repost(id)
