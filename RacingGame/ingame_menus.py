from ursina import *

class QuitMenu(Entity):
    '''In game menu for quitting the game'''
    def __init__(self, title:str):
        self.quitMenu = Button(text=title, color=color.red, scale=(0.2,0.1), position=(0,0.2),on_click=application.quit)
    
    def resumeGame(self):
        '''Resume game from pause menu'''
        self.resumeMenu = Button(text="Resume", color=color.azure, scale=(0.2,0.1), position=(0,-0.2),on_click=self.disableMenus)
    
    def disableMenus(self):
        '''Disable quit menu'''
        mouse.locked = not mouse.locked
        self.quitMenu.disable()
        self.resumeMenu.disable()

class MainMenu(Entity):
    '''In game menu for starting the game'''
    pass