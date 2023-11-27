from __future__ import annotations
import json

# Clase Originadora/Originator


class HighScore:
    '''Originator class for HighScoreMemento objects, it can save and load highscores from a json file'''

    def __init__(self, score: int = 0) -> int:
        self.score = score

    def getMemento(self) -> HighScoreMemento:
        '''Method to get the highscore (memento) saved '''
        return HighScoreMemento(self.score)

    def saveMemento(self, memento: HighScoreMemento) -> HighScoreMemento:
        '''Method to save the highscore (memento)'''
        self.score = memento.score

# Memento


class HighScoreMemento:
    '''Memento class for HighScore objects'''

    def __init__(self, score: int) -> int:
        self.score = score

# Clase cuidadora/ Caretaker


class HighScoreCaretaker:
    '''Caretaker class for HighScoreMemento objects, it can save and load highscores from a json file'''

    def save_lap_time(self, highscore: HighScore, filename: str) -> json:
        '''Method to save the highscore in a json file'''
        with open(filename, 'w') as file:
            json.dump(highscore.getMemento().__dict__, file)

    def load_lap_time(self, highscore: HighScore, filename: str) -> HighScoreMemento:
        '''Method to load the highscore from a json file to display it'''
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                memento = HighScoreMemento(data['score'])
                highscore.saveMemento(memento)

        except FileNotFoundError:
            self.save_lap_time(highscore, filename)


if __name__ == "__main__":
    high = HighScore()
    caretaker = HighScoreCaretaker()

    caretaker.load_lap_time(high, './RacingGame/highscores.json')

    # Se actualiza el score
    new_high = 160
    if new_high < high.score:
        high.score = new_high
        caretaker.save_lap_time(high, './RacingGame/highscores.json')
