from time import sleep
from rich.live import Live
from rich.console import Console
from rich.table import Table

#-------------------------------------- CLASS AND FUNCTIONS

class prompt_manager:
    def __init__(self):
        self.styles = ('cyan', 'magenta', 'bold green')
        self.console = Console()
        self.table = None
        self.live = None
        self.prompt = ''
    
    def set_prompt(self, name, address):
        self.prompt = f"┌─── <<{name}:{address[1]}>>\n│\n└─── "
    
    def cbcprint(self, text):
        for i in text:
            self.console.print(i, end='')
            sleep(0.05)
        self.console.print()
    
    def input(self, text=''):
        return input(self.prompt + text + '~$ ')
    
    def print(self, text):
        self.console.print(text, markup=False)
    
    def make_table(self, title:str, columns):
        self.table = Table(title=title)
        self.live = Live(self.table, console=self.console, auto_refresh=False)
        self.live.start()
        n = len(self.styles)
        for i in range(len(columns)):
            self.table.add_column(columns[i], justify="center", style=self.styles[i%n])
    
    def add_to_table(self, *data):
        self.table.add_row(*data)
        self.live.refresh()
    
    def stop_live(self):
        self.live.stop()
