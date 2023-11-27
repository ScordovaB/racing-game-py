from ursina import *


class QuitMenu(Entity):
    '''Displays in game menu for quitting the game'''

    def __init__(self, title: str):
        self.quitMenu = Button(text=title, color=color.red, scale=(
            0.2, 0.1), position=(0, 0.2), on_click=application.quit)

    def resumeGame(self) -> Button:
        '''Creates resume game buton when in pause menu'''
        self.resumeMenu = Button(text="Resume", color=color.azure, scale=(
            0.2, 0.1), position=(0, -0.2), on_click=self.disableMenus)

    def disableMenus(self) -> Button:
        '''Disable quit menu to restart game'''
        mouse.locked = not mouse.locked
        self.quitMenu.disable()
        self.resumeMenu.disable()
