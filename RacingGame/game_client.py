from __future__ import annotations
from track import track
from game_basics import Game
from menu_facade import TkinterMenuFacade



if __name__ == '__main__':

    juego = Game()
    track()
    def update():
        juego.update()

    def official_runGame():
        username = menu.get_username()
        juego.runGame(username)

    menu = TkinterMenuFacade()
    menu.setup_menu()
    menu.set_game_function(official_runGame)
    
    menu.run_menu()

    

    
    

    



    
    



