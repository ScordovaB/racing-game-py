from __future__ import annotations
from typing import List
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from highscores import HighScore, HighScoreCaretaker, HighScoreMemento
from ingame_menus import QuitMenu

#Paths for the assets
PATH_IMAGES = 'assets/images/'
PATH_AUDIO = 'assets/audio/'

class FinishLapLine(Entity):
    '''Class that creates the finish line in the game'''

    def __init__(self):
        self.timeline = Entity(model='cube', scale=(18, .3, .5), position=(0, 0, -30), collider='box', texture=f'{PATH_IMAGES}finish_line.jpg')

class InGameText(Text):
    '''Class that creates the in game texts'''
    def __init__(self, text:str, position:tuple, color=color.white):
        self.gameText = Text(text=text, position=position, scale=2, color=color)

class GameInputs(Entity):

    def input(self,key):
        '''Method that handles the inputs of the game'''

        if key == 'escape':
            time.sleep(.5)
            #Show mouse in screen for quitMenu interaction
            mouse.locked = not mouse.locked
            quitMenu = QuitMenu("Exit Game")
            resumeMenu = quitMenu.resumeGame()

class GameSky():
    '''Class that creates the sky in the game'''

    def __init__(self):
        self.sky = Sky()
        self.sky.texture = 'sky_sunset'

    def change_sky_default(self):
        '''Method that changes the sky to the default one'''
        self.sky.texture = 'sky_default'

class GameCar(Entity):
    '''Class that creates the car in the game'''

    def __init__(self):
        self.car = Entity(
            parent = camera.ui,
            model = 'cube',
            position = (0,0),
            scale = (1.8,1,1),
            texture = f'{PATH_IMAGES}ferrari1pixel.png'
        )
    def changeTexture(self, texture):
        '''Method that updates the texture of the car'''
        self.car.texture = texture


class Game():
    '''Class that creates the game,
     it has all the game's logic, variables and methods to function properly'''

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
        #self.acc_audio = self.instance_audios(f'{PATH_AUDIO}ferrari-488-pista-primera.mp3')
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
        self.highscore_text = InGameText('Highscore: ',position=(-0.8, 0.34), color = color.gold)
        self.highscore_value = InGameText('0',position=(-0.54, 0.34), color = color.gold)

        #Username
        self.username = InGameText('Username: ',position=(-0.8, 0.46))
        self.username_text = InGameText('',position=(-0.54, 0.46))

        self.time_text = InGameText('Lap Time: ',position=(-0.8, 0.4))

        #Get for first time highscore from json
        self.caretaker.load_lap_time(self.highscore, self.highscore_file)

        #Game realtime updates, with function update and input
        self.inputs = GameInputs()
    
    def check_velocity(self):
        '''Method that verifies the speed of the car and helps with its inertia'''
        #global velocity
        if self.velocity > 0:
            self.velocity -= .2
            held_keys['p'] = True
        if self.velocity < 0:
            self.velocity = 0
            held_keys['p'] = False
    
    def pause_game(self):
        self.player.speed = 0

    def update_player_rotation(self):
        '''Method that updates the car rotation'''
        self.player.rotate((0, (held_keys['e'] - held_keys['q'])*1.5, 0))

    def upadate_player_speed(self):
        '''Method that updates the speed of the car'''
        self.player.speed = self.player_og_speed + self.velocity

    def change_rpm_gear(self):
        '''Method that changes the RPM and Gear of the car, depending on the speed'''
        # maximum of 8 gears
        new_gear = min((self.velocity - 1) // 20 + 1, 5) if self.velocity >= 0 else 1

        # Check if the gear has changed
        if new_gear != self.gear:
            if new_gear < self.gear and new_gear != 0:
                self.play_audio([self.shift_audio, self.dec_to_0])
                
            elif new_gear > self.gear:
                self.play_audio([self.shift_audio, self.acce_audio])

            self.rpm = 0
            self.gear = new_gear

        else:
            self.rpm += self.velocity /2
            # Set rpm based on velocity
            #rpm = min(velocity * 10, 1000)
        if self.rpm > 8000:
            self.rpm = 8000

    def update_highscore(self, score: float, highscore: HighScore, caretaker: HighScoreCaretaker, filename: str) -> None:
        '''Method that calls the High Score Memento and updates the game's highscore'''
        # Load highscore
        caretaker.load_lap_time(highscore, filename)
        # Update highscore with new one
        new_high = score
        if new_high < highscore.score or highscore.score == 0:
            highscore.score = new_high
            caretaker.save_lap_time(highscore, filename)
            print(f"New high score: {highscore.score}")

    def check_finish_line(self):
        '''Method that checks if the player has crossed the finish line and calls the function to update the highscore'''
        if self.player.intersects(self.finish_timeline.timeline).hit:
            print("Lap time:", round(self.realtime, 2))
            if round(self.realtime, 2) > 0.5:
                self.update_highscore(round(self.realtime, 2), self.highscore,
                                 self.caretaker, self.highscore_file)
            self.realtime = 0
    
    def stop_all_audio(self):
        '''Method to stop all audio in the game '''
        self.neutral_audio.stop()
        self.acce_audio.stop()
        self.acc_from_0_audio.stop()
        self.dec_to_0.stop()
        self.dec_audio.stop()
        self.shift_audio.stop()

    def play_audio(self, audios:List[Audio], stop_others=True):
        '''Method to play specific audios in the game '''
        if(stop_others):
            self.stop_all_audio()
        for audio in audios:
            audio.play()

    def update(self):
        '''UPDATE URSINA METHOD, this method makes all the games changes in real time,
        this method is called by the main loop of the game,
        verything inside its executing itself all the time'''
        # print In Game Texts
        self.velocity_text.gameText.text = str(round(self.velocity, 2))
        self.timer.gameText.text = str(round(self.realtime, 2))
        self.rpm_text.gameText.text = str(int(self.rpm))
        self.gear_text.gameText.text = str(int(self.gear))
        self.highscore_value.gameText.text = str(round(self.highscore.score, 2))

        #Real time for time laps
        self.realtime += time.dt

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

                self.update_player_rotation()
                self.upadate_player_speed()

            if 's' in current_keys[0]:
                self.player.rotate((0, (held_keys['q'] - held_keys['e'])*1.5, 0))

            if held_keys['p']:
                self.update_player_rotation()
                self.check_velocity()

                if self.velocity == 0:
                    self.play_audio([self.neutral_audio])


        else:
            #No valid key combination, no keys being pressed
            if not self.neutral_audio.playing and self.velocity == 0:
                self.play_audio([self.neutral_audio])

            #Play audios for deceleration
            elif ((not self.dec_audio.playing) or (not self.dec_to_0.playing)) and self.velocity > 0:
                self.play_audio([self.dec_to_0])

            self.upadate_player_speed()
            self.check_velocity()

        
    def runGame(self, name:str)->None:
        '''Run game method '''
        window.size = window.fullscreen_size
        window.position = Vec2(0, 0)
        self.username_text.gameText.text = name
        self.app.run()
        