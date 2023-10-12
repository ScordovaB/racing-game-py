from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from abc import ABC, abstractmethod
from enum import Enum


#Factory Interface
class Entity(ABC, Entity):
    '''Interfaz de Productos'''
    def add(self):
        pass

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
class EntityFence(Entity):
    '''Clase crea Entidad Fence que extiende de la interface Entity '''

    def add(self, position, scale)-> None:
        '''Metodo que inserta un elemento del juego, scale y position son tuplas'''
        #print("Se ejecuto add de FinishLine")
        return Entity(
            model='cube',
            texture = 'concrete.jpg',
            scale=scale,
            position=position,
            collider='box'
        )

class EntityWall(Entity):
    '''Clase crea Entidad Fence que extiende de la interface Entity '''

    def add(self, position, scale)-> None:
        '''Metodo que inserta un elemento del juego, scale y position son tuplas'''
        #print("Se ejecuto add de FinishLine")
        return Entity(
            model='cube',
            texture = 'concrete.jpg',
            scale=scale,
            position=position,
            collider='box'
        )

class EntityFinishLine(Entity):
    '''Clase crea Entidad Finish Line que extiende de la interface Entity '''
    def add(self, position, scale)-> None:
        '''Metodo que inserta un elemento del juego, scale y position son tuplas'''
        #print("Se ejecuto add de FinishLine")
        return Entity(
            model='cube',
            texture='finish_line.jpg',
            collider = 'box',
            scale=scale,
            position=position,
        )

class EntityGround(Entity):
    '''Clase crea Entidad Ground que extiende de la interface Entity '''

    def add(self,position,scale)-> Entity:
        '''Metodo que inserta un elemento del juego, scale y position son tuplas'''
        #print("Se ejecuto add de Ground")
        return Entity(
            model='plane',
            texture='street.jpg',
            collider = 'mesh',
            scale=scale,
            position=position,
        )


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
    
    #app = Ursina()

    
    entidad = Ground()

    #ground = entidad.create_element(entidad.Entities.GROUND.value.add((0,0,0),(10,-2,50)))
    ground = entidad.create_element(entidad.Entities.GROUND)

