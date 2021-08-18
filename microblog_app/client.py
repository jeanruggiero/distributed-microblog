from .users import User
from .posts import Post

import requests
import socket
import json
from typing import Iterable, Tuple
from threading import Thread


class BadRequestError(Exception):
    """
    This error indicates that the client has sent an illegal or malformed request and will result in an HTTP 400 Bad
    Request error being returned to the requesting client.
    """
    pass


class AppRequestServer(Thread):
    """
    This class represents a lightweight application TCP server to handle incoming requests from peers in the distributed
    microblogging application. This server can be set to run ina new thread by calling its start() method. It can
    handle GET requests of the following form:
        GET /posts?n=<number_of_posts_to_get>
        GET /likes?n=<number_of_likes_to_get>
        GET /reposts?n=<number_of_reposts_to_get>

    All other requests will result in a 400 Bad Request Error.
    """

    def __init__(self, port: int, user: User):
        """
        Instantiates a new AppRequestServer.

        :param port: the port on which to run the server
        :param user: the username of the user whose data this server is responsible for managing
        """
        super().__init__()

        if not 0 < port < 65536:
            raise ValueError("Port number must be between 1 and 65535.")

        self.port = port
        self.user = user

    def run(self):
        """
        Runs this AppRequestServer.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', self.port))
        server_socket.listen(5)

        while True:

            # Accept a peer connection
            (peer_socket, peer_address) = server_socket.accept()
            request = peer_socket.recv(1024).decode()

            # print(request)

            try:
                # Handle the peer request and send a response to the peer
                response = self.handle_request(request)
                peer_socket.send(self.package_response(response))
            except BadRequestError:
                peer_socket.send(f"HTTP/1.1 400 Bad Request\n\n".encode())
            except Exception:
                peer_socket.send(f"HTTP/1.1 500 Internal Server Error\n\n".encode())

            peer_socket.close()

    @staticmethod
    def package_response(response: str) -> bytes:
        """
        Packages up a response as a properly formatted and utf-8 encoded HTTP response.
        :param response: the response body
        :return: a properly formatted and utf-8 encoded HTTP response
        """
        return f"HTTP/1.1 200 OK\n\n{response}".encode()

    def handle_request(self, request: str) -> str:
        """
        Handles the peer request and returns a string containing the response body.
        :param request: the peer request
        :return: a string containing the response body
        :raises BadRequestError: if the peer request is illegal or malformed
        """

        method = self._get_method(request)
        entity = self._get_entity(request)

        if method.lower() == 'get':

            if entity == 'posts':
                return json.dumps([post.serialize() for post in self.user.get_posts(**self._get_query_params(request))])
            elif entity == 'reposts':
                return json.dumps(self.user.get_reposts(**self._get_query_params(request)))
            elif entity == 'likes':
                return json.dumps(self.user.get_likes(**self._get_query_params(request)))

        raise BadRequestError("Bad request.")

    @staticmethod
    def _get_method(request: str) -> str:
        """
        Extracts the request method from the provided peer request.
        :param request: the peer request
        :return: the extracted method
        """
        return request.split(' ')[0]

    @staticmethod
    def _get_entity(request: str) -> str:
        return request.split(' ')[1][1:].split('?')[0]

    @staticmethod
    def _get_query_params(request: str) -> dict[str: str]:
        params = request.split(' ')[1][1:].split('?')[1]
        return {s.split('=')[0]: int(s.split('=')[1]) for s in params.split('&')}


class AppInstance:
    """
    This class represents an application instance which acts as a peer in the peer-to-peer microblogging application.
    It constitutes the "model" in the MVC design pattern.
    """

    # Address of the User Directory Service gateway
    uds_gateway_address = "http://localhost:8080/store"

    def __init__(self, user: User, port: int):
        """
        Instantiates a new AppInstance with the provided user and port number.
        :param user: the user of this AppInstance
        :param port: the port on which to run this
        """

        # Load user data
        self.user = user

        # Start app server & register with UDS
        self.server = AppRequestServer(port, user)
        self._register(user.username)

        # Start app server in a new thread
        self.server.start()

    def _register(self, username):
        """
        Registers the IP address of the current user with the User Directory Service.
        :param username: the username to register
        """
        ip = f"localhost:{self.server.port}"
        requests.put(self.uds_gateway_address, json.dumps({"key": username, "value": ip}))

    def _get_user_address(self, username: str) -> User:
        """
        Contacts the User Directory Service to obtain the IP address and port of the peer microblogging server
        associated with the user with the provided username.
        :param username: username of the user to get an address for
        :return: the URL of the user's app server of the form host:port
        """
        return json.loads(requests.get(self.uds_gateway_address, json={'key': username}).text.strip())['value']

    def _issue_request(self, username: str, request: str) -> requests.Response:
        """
        Issues the provided GET request to the app server associated with the provided username. The UDS is queried to
        obtain the IP address and port of the user's app server and the request is then submitted to that request.
        :param username: the username of the user whose app server to send the request to
        :param request: the request to issue
        :return: the HTTP response from the app server
        """
        return requests.get(f"http://{self._get_user_address(username)}/{request}")

    def get_posts(self, username: str, n: int) -> Iterable[Post]:
        """
        Returns an iterable of the n most recent posts by the user with the specified username.
        :param username: the username of the user whose posts to get
        :param n: the number of posts to get
        :return: an iterable of the n most recent posts by the user with the specified username
        """
        if username == self.user.username:
            return self.user.get_posts(n)
        else:
            response = self._issue_request(username, f"posts?n={n}")
            return [Post.deserialize(post) for post in json.loads(response.text)]

    def get_likes(self, username: str, n: int) -> Iterable[str]:
        """
        Returns an iterable of the n most recent likes by the user with the specified username.
        :param username: the username of the user whose likes to get
        :param n: the number of likes to get
        :return: an iterable of the n most recent likes by the user with the specified username
        """
        if username == self.user.username:
            return self.user.get_likes(n)
        else:
            response = self._issue_request(username, f"likes?n={n}")
            return json.loads(response.text)

    def get_reposts(self, username: str, n: int) -> Iterable[str]:
        """
        Returns an iterable of the n most recent reposts by the user with the specified username.
        :param username: the username of the user whose reposts to get
        :param n: the number of reposts to get
        :return: an iterable of the n most recent reposts by the user with the specified username
        """
        if username == self.user.username:
            return self.user.get_reposts(n)
        else:
            response = self._issue_request(username, f"reposts?n={n}")
            return json.loads(response.text)

    def post(self, message: str):
        """
        Adds a new post to the user currently logged into this microblogging AppInstance.
        :param message: the message to include in the post
        """
        self.user.post(message)

    def like(self, post_id: str):
        """
        Adds a new post to the list of posts liked by the user currently logged into this microblogging AppInstance.
        :param post_id: the id of the post to like
        """
        self.user.like(post_id)

    def repost(self, post_id: str):
        """
        Adds a new post to the list of posts reposted by the user currently logged into this microblogging AppInstance.
        :param post_id: the id of the post to repost
        """
        self.user.repost(post_id)


class MicroblogCommandLineInterface:
    """
    This class encapsulates a command line interface (CLI) to the distributed microblogging application. This
    interface is one possible view for the application, which was constructed following the MVC design pattern. The
    user interacts with the application via the CLI through the use of menu items. Typing an integer from the menu
    followed by <enter> will display prompts for the selected menu option.
    """

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
        """
        Instantiates a new MicroblogCommandLineInterface to the provided microblogging app instance.
        :param app_instance: the app instance to interact with
        """
        self.app_instance = app_instance

    def run(self):
        """
        Runs the user input loop of this MicroblogCommandLineInterface, allowing the user to interact with the app.
        """
        print("Welcome to the distributed microblogging app!")
        print(self.menu)

        while True:

            try:
                option = int(input('> '))

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

            except ValueError:
                print("Please enter an integer!")

            print()

    @staticmethod
    def _get_prompt(item: str) -> Tuple[str, int]:
        """
        Given an item (posts, likes, or reposts), this method displays a series of prompts to get the username and
        number of items desired from the user.
        :param item: the entity to ask the user about: posts, likes, or reposts
        :return: the username and number of posts provided by the user
        """
        username = input("Enter a username: ")
        n = input(f"How many {item} would you like to see? ")

        return username, int(n)

    def get_posts(self):
        """
        This method handles the "Get a user's posts" menu item by requesting the required input from the user and
        forwarding the request for posts to the AppInstance, which contains the business logic of the application.
        The requested posts will be printed to the command line, if available.
        """
        try:
            for post in self.app_instance.get_posts(*self._get_prompt('posts')):
                print(post)
        except KeyError:
            print("Error: User does not exist.")

    def get_likes(self):
        """
        This method handles the "Get a user's likes" menu item by requesting the required input from the user and
        forwarding the request for likes to the AppInstance, which contains the business logic of the application.
        The requested likes will be printed to the command line, if available.
        """
        try:
            for like in self.app_instance.get_likes(*self._get_prompt('likes')):
                print(like)
        except KeyError:
            print("Error: User does not exist.")

    def get_reposts(self):
        """
        This method handles the "Get a user's reposts" menu item by requesting the required input from the user and
        forwarding the request for reposts to the AppInstance, which contains the business logic of the application.
        The requested reposts will be printed to the command line, if available.
        """
        try:
            for repost in self.app_instance.get_reposts(*self._get_prompt('reposts')):
                print(repost)
        except KeyError:
            print("Error: User does not exist.")

    def create_post(self):
        """
        This method handles the "Create a post" menu item by requesting the required input from the user and
        forwarding the request to create a post to the AppInstance, which contains the business logic of the
        application. A success message will be displayed if the post is created successfully.
        """
        message = input("Enter message: ")
        self.app_instance.post(message)
        print("Message created!")

    def like_post(self):
        """
        This method handles the "Like a post" menu item by requesting the required input from the user and
        forwarding the request to like a post to the AppInstance, which contains the business logic of the
        application.
        """
        id = input("Enter id of the post to like: ")
        self.app_instance.like(id)

    def repost_post(self):
        """
        This method handles the "Repost a post" menu item by requesting the required input from the user and
        forwarding the request to repost a post to the AppInstance, which contains the business logic of the
        application.
        """
        id = input("Enter id of the post to repost: ")
        self.app_instance.repost(id)
