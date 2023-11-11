from __future__ import annotations
import json

#Clase Originadora/Originator
class HighScore:
    def __init__(self, score:int =0 ) -> None:
        self.score = score

    def getMemento(self) -> HighScoreMemento:
        return HighScoreMemento(self.score)

    def saveMemento(self, memento:HighScoreMemento) -> None:
        self.score = memento.score

#Memento
class HighScoreMemento:
    def __init__(self, score:int) -> None:
        self.score = score

#Clase cuidadora/ Caretaker
class HighScoreCaretaker:

    def save_lap_time(self, highscore:HighScore, filename:str) -> None:
        with open(filename, 'w') as file:
            json.dump(highscore.getMemento().__dict__, file)

    def load_lap_time(self, highscore:HighScore, filename:str) -> None:
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
