from __future__ import annotations
from track import track
from game_basics import Game
from tkinter_menu import TkinterMenu



if __name__ == '__main__':

    menu = TkinterMenu()

    def official_runGame():
        username = menu.entry1.get()
        juego.runGame(username)

    juego = Game()
    track()

    def update():
        juego.update()

    menu.setGameFunction(official_runGame)
    menu.runMenu()

    

    
    

    



    
    



