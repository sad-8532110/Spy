from modules import *

#--------------------------------------- CLASS AND FUNCTIONS

class main:
    def __init__(self):
        self._driver = Driver()
    
    def start(self):
        self._driver.make_connection()
        while self._driver._connection_manager.connection_status:
            self._driver.run_command()

obj = main()
obj.start()

