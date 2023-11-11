from track import track
from game_basics import Game

if __name__ == '__main__':
    
    juego = Game()
    track()

    def update():
        juego.update()
        
    juego.runGame()