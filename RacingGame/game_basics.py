from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from highscores import HighScore, HighScoreCaretaker, HighScoreMemento
from menus import QuitMenu

PATH_IMAGES = 'assets/images/'
PATH_AUDIO = 'assets/audio/'

class FinishLapLine(Entity):
    '''Clase que crea la linea de meta del juego'''

    def __init__(self):
        self.finish_timeline = Entity(model='cube', scale=(18, .3, .5), position=(0, 0, -30), collider='box', texture=f'{PATH_IMAGES}finish_line.jpg')

class InGameText(Text):
    def __init__(self, text:str, position:tuple):
        self.gameText = Text(text=text, position=position, scale=2, color=color.white)

class GameInputs(Entity):

    def input(self,key):
        '''Metodo que recibe el input del teclado y mouse en tiempo real'''

        if key == 'escape':
            time.sleep(.5)
            #Show mouse in screen for quitMenu interaction
            mouse.locked = not mouse.locked
            quitMenu = QuitMenu("Exit Game")
            resumeMenu = quitMenu.resumeGame()

class GameSky():
    '''Clase que crea el cielo del juego'''

    def __init__(self):
        self.sky = Sky()
        self.sky.texture = 'sky_sunset'

    def change_sky_default(self):
        '''Metodo que cambia el cielo del juego'''
        self.sky.texture = 'sky_default'

class GameCar(Entity):
    '''Clase que crea el carro del juego'''

    def __init__(self):
        
        self.car = Entity(
            parent = camera.ui,
            model = 'cube',
            position = (0,0),
            scale = (1.8,1,1),
            texture = f'{PATH_IMAGES}ferrari1pixel.png'
        )
    def changeTexture(self, texture):
        '''Metodo que cambia la textura del carro'''
        self.car.texture = texture


class Game():
    '''Clase que crea el juego con Ursina'''

    def instance_audios(self, audio_path):
        return Audio(audio_path, loop=False, autoplay=False)

    def __init__(self):

        self.app = Ursina()
        self.player = FirstPersonController(
            collider='box',
            jump_height=0,
            speed=5
        )
        #Player position at the start
        self.player.position = (0,10,-20)
        #Invisible Cursor 
        self.player.cursor.visible = False
        self.player.cursor.enabled = False

        #self.camera.fov = 90

        self.finish_timeline = FinishLapLine()

        #Darker Sky
        self.sky = GameSky()
        
        #make globals velocity variables
        self.velocity = 0
        self.player_og_speed =5

        self.car  = GameCar()
        #self.car.changeTexture('assets/ferrari2pixel.png')
        
        self.acc_audio = self.instance_audios(f'{PATH_AUDIO}ferrari-488-pista-primera.mp3')
        self.neutral_audio = self.instance_audios(f'{PATH_AUDIO}ferrari-488-pista-neutral.mp3')
        self.acce_audio = self.instance_audios(f'{PATH_AUDIO}ferrari-488-pista-acceleration.mp3')
        self.acc_from_0_audio = self.instance_audios(f'{PATH_AUDIO}ferrari-488-pista-primera.mp3')
        self.dec_to_0 = self.instance_audios(f'{PATH_AUDIO}ferrari-488-pista-dec_primera.mp3')
        self.dec_audio = self.instance_audios(f'{PATH_AUDIO}ferrari-488-pista-decelerate.mp3')
        self.shift_audio = self.instance_audios(f'{PATH_AUDIO}ferrari-488-pista-shift.mp3')

        #Highscores for the game
        self.highscore = HighScore()
        self.caretaker = HighScoreCaretaker()
        self.highscore_file = './RacingGame/highscores.json'

        self.speedometer = Sprite(texture=f'{PATH_IMAGES}speedometer.png', scale=(0.1,0.1), parent=camera.ui, position=(.7, -.3))
        self.velocity_text = InGameText('',position=(0.65, -0.23))
        self.rpm_text = InGameText('',position=(0.66,-0.3))
        self.gear_text = InGameText('',position=(0.72, -0.42))
        self.timer = InGameText('',position=(-0.55, 0.4))

        self.time_text = InGameText('Lap Time: ',position=(-0.8, 0.4))


        #Game realtime updates, with function update and input
        self.inputs = GameInputs()
    
    def check_velocity():
        #global velocity
        if self.velocity > 0:
            self.velocity -= .2
            held_keys['p'] = True
        if self.velocity < 0:
            self.velocity = 0
            held_keys['p'] = False
    def upadate_player_speed():
        self.player.speed = self.player_og_speed + self.velocity

    def change_rpm_gear():

        # maximum of 8 gears
        new_gear = min((self.velocity - 1) // 10 + 1, 8) if self.velocity >= 0 else 1

        # Check if the gear has changed
        if new_gear != self.gear:
            self.rpm = 0
            self.gear = new_gear
        else:
            self.rpm += self.velocity /2
            # Set rpm based on velocity
            #rpm = min(velocity * 10, 1000)
        if self.rpm > 8000:
            self.rpm = 8000

    def update_highscore(self, score: float, highscore: HighScore, caretaker: HighScoreCaretaker, filename: str) -> None:
        # Load highscore
        caretaker.load_lap_time(highscore, filename)
        # Update highscore with new one
        new_high = score
        if new_high < highscore.score and new_high > 0:
            highscore.score = new_high
            caretaker.save_lap_time(highscore, filename)
            print(f"New high score: {highscore.score}")


    def update(self):
        #self.velocity = self.velocity + 1 if held_keys['w'] else self.velocity - 1 if held_keys['s'] else self.velocity
        print(self.velocity)


        
    def runGame(self):
        self.app.run()
        