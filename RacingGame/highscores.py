from __future__ import annotations
import json

#Clase Originadora/Originator
class HighScore:
    '''Originator class for HighScoreMemento objects, it can save and load highscores from a json file'''
    def __init__(self, score:int =0 ) -> None:
        self.score = score

    def getMemento(self) -> HighScoreMemento:
        '''Method to get the memento of the highscore '''
        return HighScoreMemento(self.score)

    def saveMemento(self, memento:HighScoreMemento) -> None:
        '''Method to save the memento of the highscore '''
        self.score = memento.score

#Memento
class HighScoreMemento:
    '''Memento class for HighScore objects'''
    def __init__(self, score:int) -> None:
        self.score = score

#Clase cuidadora/ Caretaker
class HighScoreCaretaker:
    '''Caretaker class for HighScoreMemento objects, it can save and load highscores from a json file'''

    def save_lap_time(self, highscore:HighScore, filename:str) -> None:
        '''Method to save the highscore in a json file'''
        with open(filename, 'w') as file:
            json.dump(highscore.getMemento().__dict__, file)

    def load_lap_time(self, highscore:HighScore, filename:str) -> None:
        '''Method to load the highscore from a json file'''
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                memento = HighScoreMemento(data['score'])
                highscore.saveMemento(memento)
                print(f"Loaded high score: {highscore.score}")
                
        except FileNotFoundError:
            print("Highscore file not found. Creating a new highscore file")
            self.save_lap_time(highscore, filename)

if __name__ == "__main__":
    high = HighScore()
    caretaker = HighScoreCaretaker()

    caretaker.load_lap_time(high, './RacingGame/highscores.json')

    #Se actualiza el score
    new_high = 160
    if new_high < high.score:
        high.score = new_high
        caretaker.save_lap_time(high, './RacingGame/highscores.json')
        print(f"New high score: {high.score}")

    #save something in json
    # dict = {'score': 100}
    # with open('./RacingGame/highscores.json', 'w') as file:
    #         json.dump(dict, file)
