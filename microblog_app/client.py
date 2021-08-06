class AppInstance:

    def __init__(self):
        pass

    def get_posts(self, username, n):
        return ["Post 1", "Post 2"]

    def get_likes(self, username, n):
        return ['Post 3', 'Post 4']

    def get_reposts(self, username, n):
        return ['Post 5', 'Post 5']

    def post(self, message):
        pass

    def like(self, post_id):
        pass

    def repost(self, post_id):
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

            print()

    def _get_prompt(self, item):
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
