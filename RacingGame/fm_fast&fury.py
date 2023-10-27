from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from abc import ABC, abstractmethod
from enum import Enum

class GameUpdates(Entity):
    
    # def __init__(self, game):
    #     self.acc_audio = game.acc_audio
    #     self.neutral_audio = game.neutral_audio
    #     self.acce_audio = game.acce_audio
    #     self.player = game.player
    #     self.car = game.car
    #     self.velocity = game.velocity
    #     self.player_og_speed = game.player_og_speed

    def change_speed(self):
        return self.player_og_speed + self.velocity

    def check_velocity(self):
        '''Funcion que revisa velocidad y la disminuye en tiempo real'''
        if self.velocity > 0:
                self.velocity -= 1
        if self.velocity < 0:
            self.velocity = 0

    def update(self):
        print("self.velocity")

    # def update(self):
    #     '''Metodo que actualiza el juego en tiempo real'''
    
    #     # Determine the car texture and velocity changes based on key presses
    #     key_combinations = {
    #         ('q', 'w'): ('assets/ferrari2pixel.png', (-0.001, 0, -0.001)),
    #         ('e', 'w'): ('assets/ferrari3pixel.png', (0.001, 0, 0.001)),
    #         ('e', 's'): ('assets/ferrari3pixel.png', (0.001, 0, 0.001)),
    #         ('q', 's'): ('assets/ferrari2pixel.png', (-0.001, 0, -0.001)),
    #         ('q',): ('assets/ferrari2pixel.png', (0, 0, 0)),
    #         ('e',): ('assets/ferrari3pixel.png', (0, 0, 0)),
    #         ('s',): ('assets/ferrari1pixel.png', (0, 0, 0)),
    #         ('w',): ('assets/ferrari1pixel.png', (0, 0, 0)),
    #         ('space',): ('assets/ferrari1pixel.png', (0, 0, 0)),
    #     }

    #     #Check if any of the key combinations are pressed
    #     current_keys = [key for key in key_combinations if all(held_keys[k] for k in key)]

    #     # Update car texture and mouse position based on the key combination
    #     if current_keys:
    #         #print(current_keys[0])

    #         texture, mouse_position_change = key_combinations[current_keys[0]]
    #         self.car.texture = texture
            
    #         if 'w' in current_keys[0] and not self.acc_audio.playing:
    #             self.neutral_audio.stop()
    #             self.acc_audio.play()

    #         if 'w' not in current_keys[0] and not self.neutral_audio.playing:
    #             self.acc_audio.stop()
    #             self.neutral_audio.play()
            
    #         if 'w' in current_keys[0]:
    #             if self.velocity < 50:
    #                 self.velocity += 0.1
    #             self.player.speed = self.change_speed()

    #         if 'q' in current_keys[0] or 'e' in current_keys[0]:
    #             self.mouse.position += mouse_position_change

    #     else:
    #         # No valid key combination, decrease velocity
    #         if not self.neutral_audio.playing:
    #             self.acc_audio.stop()
    #             self.neutral_audio.play()

    #         self.player.speed = self.change_speed()
    #         self.check_velocity()
        
    #     print("Velocidad:", self.velocity)

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
            texture = 'assets/ferrari1pixel.png'
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
        
        self.acc_audio = self.instance_audios('assets/ferrari-488-pista-primera.mp3')
        self.neutral_audio = self.instance_audios('assets/ferrari-488-pista-neutral.mp3')
        self.acce_audio = self.instance_audios('assets/ferrari-488-pista-acceleration.mp3')


        #self.acc_audio = Audio('assets/ferrari-488-pista-primera.mp3', loop=False, autoplay=False)
        #self.neutral_audio = Audio('assets/ferrari-488-pista-neutral.mp3', loop=False, autoplay=False)
        #self.acce_audio = Audio('assets/ferrari-488-pista-acceleration.mp3', loop=False, autoplay=False)

        #Game realtime updates, with function update and input
        self.updates = GameUpdates()
        #self.app._update = self.updates.update
        self.inputs = GameInputs()
        
    def runGame(self):
        self.app.run()
        


#Factory Interface
class Entity(ABC, Entity):
    '''Interfaz de Productos'''
    def add(self):
        pass

class EntityElement(Entity):
    '''Interfaz de Entidad Cubo que extiende de la interface Entity '''
    def add(self,model,collider,texture, scale, position):
        ''' Metodo que inserta entidad, model es un string, collider es un string, texture es un string, scale y position son tuplas'''
        return Entity(
            model=model,
            texture = texture,
            scale=scale,
            position=position,
            collider=collider
        )


#Factory Method(Clase Abstracta)
class TrackElement:
    '''TrackElement clase abstracta'''

    @abstractmethod
    def create_element(self, entity)-> Entity:
        '''Metodo que inserta un elemento del juego'''
        return entity.value

    def add(self,entity)-> None:
        return self.create_element(entity).add()




#Productos concretos
class EntityFence(EntityElement):
    '''Clase crea Entidad Fence que extiende de la interface Entity '''

    def add(self, position, scale)-> None:
        '''Metodo que inserta un elemento del juego, scale y position son tuplas'''
        #print("Se ejecuto add de FinishLine")
        return EntityElement.add(self, 'cube', 'box','assets/concrete.jpg',scale=scale,position=position)

class EntityWall(EntityElement):
    '''Clase crea Entidad Fence que extiende de la interface Entity '''

    def add(self, position, scale)-> None:
        '''Metodo que inserta un elemento del juego, scale y position son tuplas'''
        #print("Se ejecuto add de FinishLine")
        return EntityElement.add(self, 'cube', 'box','assets/concrete.jpg',scale=scale,position=position)

class EntityFinishLine(EntityElement):
    '''Clase crea Entidad Finish Line que extiende de la interface Entity '''
    def add(self, position, scale)-> None:
        '''Metodo que inserta un elemento del juego, scale y position son tuplas'''
        #print("Se ejecuto add de FinishLine")
        return EntityElement.add(self, 'cube', 'box','assets/finish_line.jpg',scale=scale,position=position)


class EntityGround(EntityElement):
    '''Clase crea Entidad Ground que extiende de la interface Entity '''

    def add(self,position,scale)-> Entity:
        '''Metodo que inserta un elemento del juego, scale y position son tuplas'''
        #print("Se ejecuto add de Ground")
        return EntityElement.add(self, 'plane', 'mesh','assets/street.jpg',scale=scale,position=position)


#Fabricas Concretas
# class Ground(TrackElement):

#     class Entities(Enum):
#         GROUND = EntityGround()

class Ground(TrackElement):

    class Entities(Enum):
        @classmethod
        def GROUND(cls, arg1, arg2):
            return EntityGround.add(cls,arg1, arg2)


class FinishLine(TrackElement):

    class Entities(Enum):
        FINISHLINE = EntityFinishLine()

class Barrier(TrackElement):

    class Entities(Enum):
        WALL = EntityWall()

class Decoration(TrackElement):

    class Entities(Enum):
        FENCE = EntityFence()

if __name__ == '__main__':
    
    
    juego = Game()
    
    #piso = EntityGround()
    #piso.add((0,0,0),(10,-2,50))

    ground_entity = Ground.Entities.GROUND((0,0,0),(10,-2,50))

    
    pared_trasera = EntityWall()
    pared_trasera.add((0, .5, -25),(10, 1.2, .1))



    #ground = entidad.create_element(entidad.Entities.GROUND.value.add((0,0,0),(10,-2,50)))
    #ground = entidad.create_element(entidad.Entities.GROUND.value.add((0,0,0),(10,-2,50)))

    juego.runGame()

