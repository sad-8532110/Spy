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
        while True:
            self.mode = input('please enter an option: ')
            match self.mode.lower():
                case 'help' | 'h':
                    self.help()
                case '' | 'run':
                    self.run()
                case 'exit' | 'quit':
                    break

    def welcome(self):
        self._prompt_manager.cbcprint('Hello, Dear User !\nWelcome to Spy\nhere is what I wrote, do you like it ?')
    
    def menu(self):
        """
        need help to make it pretty
        """
        self._prompt_manager.print("1. run\n2. help\n3. exit")
    
    def help(self):
        """
        need to help to make it pretty
        """
        pass
    
    def run(self):
        self._driver.make_connection()
        while self._driver._connection_manager.connection_status:
            self._driver.run_command()

#-------------------------------------- PROGRAM

obj = main()
obj.start()
