from __future__ import annotations
from track import track
from game_basics import Game
from menu_facade import TkinterMenuFacade



if __name__ == '__main__':

    #Create a new game
    juego = Game()
    #Import the track
    track()
    #Set the update ursina method
    def update():
        juego.update()
    #set the game to run in the main thread
    def official_runGame():
        username = menu.get_username()
        juego.runGame(username)
        
    #Run the menu game
    menu = TkinterMenuFacade()
    menu.setup_menu()
    menu.set_game_function(official_runGame)
    
    menu.run_menu()