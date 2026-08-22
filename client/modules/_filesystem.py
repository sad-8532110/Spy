from os import listdir, replace
from os.path import isfile, abspath, getsize

#--------------------------------------- CLASS AND FUNCTIONS

class filesystem:
    def __init__(self):
        self.__buffer_size = 1024*1024
        self.__files = {}
    
    def open_file(self, file_path:str):
        """
        open a file if it is close
        """
        if file_path not in self.__files:
            open(file_path, 'a+b').close()
            self.__files[file_path] = open(file_path, 'r+b')
    
    def read_file(self, file_path:str):
        """
        read the file chunk by chunk
        """
        if getsize(file_path) < 10:
            yield self.__files[file_path].read()
        else:
            while chunk := self.__files[file_path].read(self.__buffer_size):
                yield chunk
    
    def write_file(self, file_path:str, data:bytes):
        """
        write data to an opened file
        """
        self.__files[file_path].write(data)
    
    def close_file(self, file_path:str):
        """
        close a file
        """
        self.__files[file_path].close()
        del self.__files[file_path]
    
    def replace_file(self, src_file:str, dst_file:str):
        """
        make an atomic replace
        """
        replace(src_file, dst_file)
    
    def get_size(self, file_path:str):
        return getsize(file_path)
    
    def list_files(self, paths:list):
        """
        Make a list of the files of a directory and its subdirectories
        """
        for path in paths:
            if not path:
                #path = '.'
                #SO So dangerous do not active this line
                continue
            try:
                if isfile(path):
                    yield abspath(path)
                else:
                    items = listdir(path+'/')
                    for item in items:
                        yield from self.list_files([f'{path}/{item}'])
            except:
                None

