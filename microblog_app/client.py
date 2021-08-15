from .users import User

import requests
import socket
import json
from typing import Iterable, Tuple


class AppRequestServer:

    def __init__(self, port: int, user: User):
        if not 0 < port < 65536:
            raise ValueError("Port number must be between 1 and 65535.")

        self.user = user

    def serve(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((socket.gethostname(), 80))
        server_socket.listen(5)

        while True:
            (peer_socket, peer_address) = server_socket.accept()
            request = peer_socket.recv(1024).decode()

            method = self._get_method(request)
            entity = self._get_entity(request)

            if method.lower() == 'get':
                if entity == 'posts':
                    pass
                # TODO: write code to handle requests from peers


    @staticmethod
    def _get_method(request: str) -> str:
        return request.split(' ')[0]

    @staticmethod
    def _get_entity(request: str) -> str:
        return request.split(' ')[1][1:].split('?')[0]

    @staticmethod
    def _get_query_params(request: str) -> dict[str: str]:
        params = request.split(' ')[1][1:].split('?')[1]
        return {s.split('=')[0]: s.split('=')[1] for s in params.split('&')}


class AppInstance:

    def __init__(self, user: User, port: int):

        # Load user data
        self.user = user

        # Start app server
        self.server = AppRequestServer(8000, user)

        # TODO: register IP address with user directory service
        self._register(user.username)

        # TODO set app server to run in a separate thread




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
        if username == self.user.username:
            return self.user.get_posts(n)
        else:
            response = self._issue_request(username, f"GET /posts?n={n}")
            return json.loads(response.text)

    def get_likes(self, username: str, n: int) -> Iterable[str]:
        if username == self.user.username:
            return self.user.get_likes(n)
        else:
            response = self._issue_request(username, f"GET /likes?n={n}")
            return json.loads(response.text)

    def get_reposts(self, username: str, n: int) -> Iterable[str]:
        if username == self.user.username:
            return self.user.get_reposts(n)
        else:
            response = self._issue_request(username, f"GET /reposts?n={n}")
            return json.loads(response.text)

    def post(self, message: str):
        self.user.post(message)

    def like(self, post_id: str):
        self.user.like(post_id)

    def repost(self, post_id: str):
        self.user.repost(post_id)


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
