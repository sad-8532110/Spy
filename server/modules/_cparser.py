#-------------------------------------- CLASS AND FUNCTIONS

class Command(str):
    """
    A class for parsing commands
    """
    def __init__(self, /, *args, **kwargs):
        super().__init__()
        self.main_command = ''
        self.switches = {}
    
    def __split(self, sep):
        """
        Try to split given command by space and
        ignore characters which are between "
        """
        result = []
        index = 0
        part = ''
        while index < len(self):
            if self[index:index+len(sep)] == sep:
                result.append(part)
                part = ''
            elif self[index] == '"':
                index += 1
                while index < len(self):
                    if self[index] == '"':
                        break
                    part += self[index]
            else:
                part += self[index]
            index += 1
        result.append(part)
        return result
    
    def parse_command(self):
        """
        Try to parse command and return a dictionary of switches and values
        """
        command = self.__split(' ')
        if len(command) > 0:
            self.main_command = command[0]
            self.switches = {'command': []}
            key = 'command'
            for index in range(1, len(command)):
                if command[index].startswith('-') and len(command[index]) < 10:
                    key = command[index][1:]
                    self.switches[key] = []
                else:
                    self.switches[key].append(command[index])
