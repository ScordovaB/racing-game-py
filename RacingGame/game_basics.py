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
        self.timeline = Entity(model='cube', scale=(18, .3, .5), position=(0, 0, -30), collider='box', texture=f'{PATH_IMAGES}finish_line.jpg')

class InGameText(Text):
    '''Clase que crea el texto en pantalla del juego, recibe el texto y la posicion'''
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
        self.rpm = 0
        self.gear = 1
        self.first_gear = True
        self.realtime = 0

        #Car
        self.car  = GameCar()
        
        #Audios
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

        #Speedometer and in game texts
        self.speedometer = Sprite(texture=f'{PATH_IMAGES}speedometer.png', scale=(0.1,0.1), parent=camera.ui, position=(.7, -.3))
        self.velocity_text = InGameText('0',position=(0.65, -0.23))
        self.rpm_text = InGameText('0',position=(0.66,-0.3))
        self.gear_text = InGameText('0',position=(0.72, -0.42))
        self.timer = InGameText('0',position=(-0.55, 0.4))

        self.time_text = InGameText('Lap Time: ',position=(-0.8, 0.4))


        #Game realtime updates, with function update and input
        self.inputs = GameInputs()
    
    def check_velocity(self):
        '''Metodo que verifica la velocidad del carro y ayuda con inercia del mismo'''
        #global velocity
        if self.velocity > 0:
            self.velocity -= .2
            held_keys['p'] = True
        if self.velocity < 0:
            self.velocity = 0
            held_keys['p'] = False

    def upadate_player_speed(self):
        '''Metodo que actualiza la velocidad del carro'''
        self.player.speed = self.player_og_speed + self.velocity

    def change_rpm_gear(self):
        '''Metodo que cambia el el RPM y el Gear del carro, segun la velocidad'''
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
        '''Metodo que llama a la Memento de HighScore y actualiza el highscore del juego'''
        # Load highscore
        caretaker.load_lap_time(highscore, filename)
        # Update highscore with new one
        new_high = score
        if new_high < highscore.score or highscore.score == 0:
            highscore.score = new_high
            caretaker.save_lap_time(highscore, filename)
            print(f"New high score: {highscore.score}")

    def check_finish_line(self):
        '''Metodo que verifica si el jugador ha pasado la linea de meta y llama a la funcion de actualizar el highscore'''
        if self.player.intersects(self.finish_timeline.timeline).hit:
            print("Lap time:", round(self.realtime, 2))
            if round(self.realtime, 2) > 0.5:
                self.update_highscore(round(self.realtime, 2), self.highscore,
                                 self.caretaker, self.highscore_file)
            self.realtime = 0

    def update(self):
        #self.velocity = self.velocity + 1 if held_keys['w'] else self.velocity - 1 if held_keys['s'] else self.velocity
        #print(self.velocity)
        
        # print In Game Texts
        self.velocity_text.gameText.text = str(round(self.velocity, 2))
        self.timer.gameText.text = str(round(self.realtime, 2))
        self.rpm_text.gameText.text = str(int(self.rpm))
        self.gear_text.gameText.text = str(int(self.gear))

        #Real time for time laps
        self.realtime += time.dt
        #print(self.realtime)

        #Check if the player has passed the finish line
        self.check_finish_line()

        #Prevent from going under the map (ursina bug)
        self.player.y = 0.0 if self.player.y != 0.0 else self.player.y

        #Update Gear and RPM of the car
        self.change_rpm_gear()

        # Block RIGHT and LEFT movement (Ursina standard)
        input_handler.bind('a', 'l')
        input_handler.bind('d', 'b')

        # Determine the car texture and velocity changes based on key presses
        key_combinations = {
            ('q', 'w'): (f'{PATH_IMAGES}ferrari2pixel.png'),
            ('e', 'w'): (f'{PATH_IMAGES}ferrari3pixel.png'),
            ('e', 's'): (f'{PATH_IMAGES}ferrari3pixel.png'),
            ('q', 's'): (f'{PATH_IMAGES}ferrari2pixel.png'),
            ('q',): (f'{PATH_IMAGES}ferrari2pixel.png'),
            ('e',): (f'{PATH_IMAGES}ferrari3pixel.png'),
            ('s',): (f'{PATH_IMAGES}ferrari1pixel.png'),
            ('w',): (f'{PATH_IMAGES}ferrari1pixel.png'),
            ('p',): (f'{PATH_IMAGES}ferrari1pixel.png'),
            ('space',): (f'{PATH_IMAGES}ferrari1pixel.png'),
        }
        # Check if any of the key combinations are pressed, save the key combination in current_keys
        current_keys = [key for key in key_combinations if all(
            held_keys[k] for k in key)]

        if current_keys:
            # print(current_keys[0])
            self.car.changeTexture(key_combinations[current_keys[0]])

            if 'w' in current_keys[0] and not self.acc_from_0_audio.playing:

                held_keys['p'] = False

            if 'w' in current_keys[0]:
                held_keys['p'] = False

                if self.velocity < 100:
                    self.velocity += 0.1

                if not self.acc_from_0_audio.playing and self.velocity < 30:
                    self.dec_to_0.stop()
                    self.dec_audio.stop()
                    self.neutral_audio.stop()
                    self.acce_audio.stop()
                    self.acc_from_0_audio.play()
                if not self.acce_audio.playing and not self.shift_audio.playing and self.velocity > 30:
                    self.neutral_audio.stop()
                    self.dec_audio.stop()
                    self.acc_from_0_audio.stop()
                    self.dec_to_0.stop()
                    self.shift_audio.play()
                    self.acce_audio.play()
                if not self.acce_audio.playing and not self.shift_audio.playing and self.velocity > 50:
                    self.neutral_audio.stop()
                    self.dec_audio.stop()
                    self.acc_from_0_audio.stop()
                    self.dec_to_0.stop()
                    self.shift_audio.play()
                    self.acce_audio.play()
                if not self.acce_audio.playing and not self.shift_audio.playing and self.velocity > 70:
                    self.neutral_audio.stop()
                    self.dec_audio.stop()
                    self.acc_from_0_audio.stop()
                    self.dec_to_0.stop()
                    self.shift_audio.play()
                    self.acce_audio.play()

                self.player.rotate((0, (held_keys['e'] - held_keys['q'])*1.5, 0))

                self.upadate_player_speed()

            if 's' in current_keys[0]:
                self.player.rotate((0, (held_keys['q'] - held_keys['e'])*1.5, 0))

            if held_keys['p']:
                self.player.rotate((0, (held_keys['e'] - held_keys['q'])*1.5, 0))
                self.check_velocity()
                if self.velocity == 0:
                    self.dec_to_0.stop()
                    self.acc_from_0_audio.stop()
                    self.acce_audio.stop()
                    self.dec_audio.stop()
                    self.neutral_audio.play()

            if not 'w' in current_keys[0] and not self.dec_to_0.playing and self.velocity < 30 and self.velocity > 0:
                self.neutral_audio.stop()
                self.acc_from_0_audio.stop()
                self.shift_audio.stop()
                self.acce_audio.stop()
                self.dec_audio.stop()
                self.shift_audio.play()
                self.dec_to_0.play()

        else:
            #No valid key combination, no keys being pressed
            if not self.neutral_audio.playing and self.velocity == 0:
                self.dec_to_0.stop()
                self.acc_from_0_audio.stop()
                self.shift_audio.stop()
                self.acce_audio.stop()
                self.dec_audio.stop()
                self.neutral_audio.play()

            if not self.dec_to_0.playing and self.velocity < 30 and self.velocity > 0:
                self.neutral_audio.stop()
                self.acc_from_0_audio.stop()
                self.shift_audio.stop()
                self.acce_audio.stop()
                self.dec_audio.stop()
                self.shift_audio.play()
                self.dec_to_0.play()

            if not self.dec_audio.playing and self.velocity > 30:
                self.neutral_audio.stop()
                self.acc_from_0_audio.stop()
                self.shift_audio.stop()
                self.acce_audio.stop()
                self.dec_to_0.stop()
                self.shift_audio.play()
                self.dec_audio.play()

            # player.speed = player_og_speed + velocity
            self.upadate_player_speed()
            self.check_velocity()

        
    def runGame(self):
        '''Run game method '''
        self.app.run()
        