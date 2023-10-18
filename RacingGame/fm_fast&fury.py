from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from abc import ABC, abstractmethod
from enum import Enum

class GameUpdates(Entity):
    def input(self,key):
        if key == 'escape':

                #end_time = time.time()
                #elapsed_time = end_time - start_time
                #print("Seconds:",round(elapsed_time,2))

                time.sleep(1)
            
                quit()

class Game():
    '''Clase que crea el juego con Ursina'''
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
        self.sky = Sky()
        self.sky.texture = 'sky_sunset'
        
        #make globals velocity variables
        self.velocity = 0
        self.player_og_speed =5

        self.car  = Entity(
            parent = camera.ui,
            model = 'cube',
            position = (0,0),
            scale = (1.8,1,1),
            texture = 'assets/ferrari1pixel.png'
        )

        #Game realtime updates, with function update and input
        self.updates = GameUpdates()


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
class Ground(TrackElement):

    class Entities(Enum):
        GROUND = EntityGround()

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
    
    piso = EntityGround()
    piso.add((0,0,0),(10,-2,50))

    #ground = entidad.create_element(entidad.Entities.GROUND.value.add((0,0,0),(10,-2,50)))
    #ground = entidad.create_element(entidad.Entities.GROUND.value.add((0,0,0),(10,-2,50)))


    juego.runGame()

