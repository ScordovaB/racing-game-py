from ursina import *

class QuitMenu(Entity):
    '''In game menu for quitting the game'''
    def __init__(self, title:str):
        self.quitMenu = Button(text=title, color=color.red, scale=(0.2,0.1), position=(0,0.2),on_click=application.quit)

class MainMenu(Entity):
    '''In game menu for starting the game'''
    pass