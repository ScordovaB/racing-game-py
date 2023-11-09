from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time



class GameInputs(Entity):

    def input(self,key):
        '''Metodo que recibe el input del teclado y mouse en tiempo real'''

        if key == 'escape':
            time.sleep(1)
            quit()

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
            texture = 'assets/images/ferrari1pixel.png'
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

        #Darker Sky
        self.sky = GameSky()
        
        #make globals velocity variables
        self.velocity = 0
        self.player_og_speed =5

        self.car  = GameCar()
        #self.car.changeTexture('assets/ferrari2pixel.png')
        
        self.acc_audio = self.instance_audios('assets/audio/ferrari-488-pista-primera.mp3')
        self.neutral_audio = self.instance_audios('assets/audio/ferrari-488-pista-neutral.mp3')
        self.acce_audio = self.instance_audios('assets/audio/ferrari-488-pista-acceleration.mp3')


        #self.acc_audio = Audio('assets/ferrari-488-pista-primera.mp3', loop=False, autoplay=False)
        #self.neutral_audio = Audio('assets/ferrari-488-pista-neutral.mp3', loop=False, autoplay=False)
        #self.acce_audio = Audio('assets/ferrari-488-pista-acceleration.mp3', loop=False, autoplay=False)

        #Game realtime updates, with function update and input
        self.inputs = GameInputs()
        
    def runGame(self):
        self.app.run()
        