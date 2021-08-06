from microblog_app import AppInstance, MicroblogCommandLineInterface, User

MicroblogCommandLineInterface(AppInstance(User('jean'))).run()