from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import gethostname

#--------------------------------------- CLASS AND FUNCTIONS

class connection:
    def __init__(self, cryptor):
        self.__config_data()
        self.__main_data = ''.encode('utf-8')
        self.__cryptor = cryptor
    
    def __config_data(self):
        self.connection_status = False
        self.server_ip = '127.0.0.1'
        self.server_port = 1234
        self.buffer_size = 1024
        self._main_socket = socket(AF_INET, SOCK_STREAM)

    def connect_server(self):
        """
        Connect to the server and set the
        buffer size and then send the system name
        """
        loop = 1
        while loop < 6:
            try:
                self._main_socket.connect((self.server_ip, self.server_port))
            except:
                loop += 1
            else:
                self.__key_exchange()
                self.buffer_size = self.receive_data('SENT_BUFFER_SIZE')
                self.buffer_size = int(self.buffer_size)
                
                name = gethostname().encode('utf-8')
                self.send({'NAME': name})
                self.connection_status = True
                break
    
    def __key_exchange(self):
        self.__cryptor.register_key('asym_connection_key', 'asymetric')
        self._main_socket.sendall(str(len(self.__cryptor.return_key_bytes('asym_connection_key'))).encode('utf-8'))
        self._main_socket.recv(1024)
        self._main_socket.sendall(self.__cryptor.return_key_bytes('asym_connection_key'))
        length = int(self._main_socket.recv(1024).decode('utf-8'))
        self._main_socket.sendall('ok'.encode('utf-8'))
        key = self._main_socket.recv(length)
        key = self.__cryptor.decrypt('asym_connection_key', key)
        self.__cryptor.remove_key('asym_connection_key')
        self.__cryptor.register_key('sym_connection_key', 'symetric', key)
    
    def send(self, data:dict):
        """
        Send the given data use a
        dictionary for understanding data flags
        """
        for f, v in data.items():
            v = self.__cryptor.encrypt('sym_connection_key', v)
            self._main_socket.sendall(v)
            self._main_socket.sendall(f'SENT_{f}'.encode('utf-8'))

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
        self.connection_status = False
