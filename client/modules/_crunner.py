from subprocess import run

#-------------------------------------- CLASS AND FUNCTIONS

class crunner:
    def __init__(self):
        pass

    def run_sys_command(self, command:str) -> bytes:
        result = run(command,
                    shell=True,
                    capture_output=True)
        return result.stdout if result.stdout else result.stderr
