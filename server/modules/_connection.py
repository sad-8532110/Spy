from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM

#--------------------------------------- CLASS AND FUNCTIONS

class connection:
    def __init__(self, cryptor):
        self.__config_data()
        self.client_name = ''
        self.client_address = None
        self.__main_data = ''.encode('utf-8')
        self.__cryptor = cryptor
    
    def __config_data(self):
        """
        here can be a config file to read
        """
        self.connection_status = False
        self.server_ip = '127.0.0.1'
        self.server_port = 1234
        self.buffer_size = 1024
        self._server_socket = socket(AF_INET, SOCK_STREAM)
        self._main_socket = None
    
    def make_connection(self):
        """
        Listen for the requests, send the
        buffer size and receive the client name
        """
        try:
            self._server_socket.bind((self.server_ip, self.server_port))
            self._server_socket.listen()
            self._main_socket, self.client_address = self._server_socket.accept()

            self.__key_exchange()
            self.send({'BUFFER_SIZE': str(self.buffer_size).encode('utf-8')})

            self.client_name = self.receive_data('SENT_NAME').decode('utf-8')
            self.connection_status = True
        
        except:
            pass
    
    def __key_exchange(self):
        """
        exchange the fernet key (symmetric key) using rsa (asymmetric key)
        """
        length = int(self._main_socket.recv(1024).decode('utf-8'))
        self._main_socket.sendall('ok'.encode('utf-8'))
        public_key = self._main_socket.recv(length)
        self.__cryptor.register_key('asym_connection_key', 'asymetric', public_key)
        self.__cryptor.register_key('sym_connection_key', 'symetric')
        
        encrypted_key = self.__cryptor.encrypt('asym_connection_key', self.__cryptor.return_key_bytes('sym_connection_key'))
        self._main_socket.sendall(str(len(encrypted_key)).encode('utf-8'))
        self._main_socket.recv(1024)
        self._main_socket.sendall(encrypted_key)
        self.__cryptor.remove_key('asym_connection_key')
        
    def send(self, data:dict):
        """
        Send the given data use a
        dictionary for understanding data flags
        """
        for f, v in data.items():
            v = self.__cryptor.encrypt('sym_connection_key', v)
            self._main_socket.sendall(v)
            self._main_socket.sendall(f'SENT_{f}'.encode('utf8'))

    def receive_data(self, sign:str) -> bytes:
        """
        Receive the data with the specified flag
        """
        sign = sign.encode('utf-8')
        
        while sign not in self.__main_data:
            data = self._main_socket.recv(self.buffer_size)
            if not data:
                break
            self.__main_data += data
        else:
            self.__main_data = self.__main_data.split(sign, maxsplit=1)
            data = self.__main_data[0]
            self.__main_data = self.__main_data[1]
            
            data = self.__cryptor.decrypt('sym_connection_key', data)
            return data
        return ''.encode('utf-8')
    
    def close_connection(self):
        """
        Close the connection
        """
        self._main_socket.close()
        self._server_socket.close()
        self.connection_status = False
