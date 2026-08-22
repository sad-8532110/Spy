from time import sleep
from modules import *

#-------------------------------------- CLASS AND FUNCTIONS

class main:
    def __init__(self):
        """
        get the printer obj and pass to driver
        """
        self._prompt_manager = prompt_manager()
        self._driver = Driver(self._prompt_manager)
    
    def start(self):
        self.welcome()
        self.mode = input('please enter an option: ')
        match self.mode.lower():
            case 'help' | 'h':
                self.help()
            case '' | 'run':
                self.run()
            case _:
                pass

    def welcome(self):
        self._prompt_manager.cbcprint('Hello, Dear User !\nWelcome to Spy\nhere is what I wrote, do you like it ?')
    
    def menu(self):
        self._prompt_manager.print("1. run\n2. help\n3. exit")
    
    def help(self):
        pass
    
    def run(self):
        self._driver.make_connection()
        while self._driver._connection_manager.connection_status:
            self._driver.run_command()

#-------------------------------------- PROGRAM

obj = main()
obj.start()
