"""
This program serves as the entry point for the peer-to-peer microblogging application client interface. It serves as
the controller in the MVC design pattern.

Run with:

python microblog_client.py <username> <port>
"""

from microblog_app import AppInstance, MicroblogCommandLineInterface, User
import argparse

parser = argparse.ArgumentParser(description='Run the microblogging command line client!')
parser.add_argument('username', metavar='u', type=str, nargs=1, help='The username to connect with.')
parser.add_argument('port', metavar='p', type=int, nargs=1, help='The port on which to run the application.')

if __name__ == "__main__":

    # Parse command line arguments
    args = parser.parse_args()
    username = args.username[0]
    port = args.port[0]

    # Run the application
    MicroblogCommandLineInterface(AppInstance(User(username), port)).run()
