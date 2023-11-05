from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time

from abc import ABC, abstractmethod, abstractproperty
from enum import Enum

# 3.- Productos
# Los Productos son los objetos resultantes.
# Los productos construidos por distintos objetos constructores no tienen que
# pertenecer a la misma jerarquía de clases o interfaz.


class Structure(ABC):
    def __init__(self, path: str, model=str, collider=str) -> None:
        self._position = (0, 0, 0)
        self._model = model
        self._texture = path
        self._collider = collider
        self._scale = (10, 0, 50)
        print(self._texture)
        print('self._texture?')

    def create_entity(self) -> Entity:
        print('llego create')
        print(self._texture)
        return Entity(
            model=self._model,
            texture=self._texture,
            collider=self._collider,
            scale=self._scale,
            position=self._position
        )


class Asphalt(Structure):
    def __init__(self):
        super().__init__('street.jpg', 'plane', 'mesh')


class FinishLine(Structure):
    def __init__(self):
        super().__init__('finish_line.jpg', 'plane', 'mesh')


class Grass(Structure):
    def __init__(self):
        super().__init__('grass.jpg', 'plane', 'mesh')


class PirelliSign(Structure):
    def __init__(self):
        super().__init__('pirelli.png', 'cube', 'box')


class RolexSign(Structure):
    def __init__(self):
        super().__init__('rolex.png', 'cube', 'box')


class Fence(Structure):
    def __init__(self):
        super().__init__('fence.png', 'cube', 'box')


class Barrier(Structure):
    def __init__(self):
        super().__init__('concrete.jpg', 'cube', 'box')

# 1- Interface constructora (Builder)
# La interfaz Constructora declara pasos de construcción de producto que todos
# los tipos de objetos constructores tienen en común.


class Entities(ABC):
    @property
    def Structure(self):
        return self._structure

    def set_scale(self, scale: tuple) -> None:
        self._structure._scale = scale

    def set_position(self, position: tuple) -> None:
        self._structure._position = position


# 2.- Constructores concretos
# Los Constructores Concretos ofrecen distintas implementaciones de los pasos
# de construcción. Los constructores concretos pueden crear productos que no
# siguen la interfaz común.


class Ground(Entities):

    class GroundType(Enum):
        GRASS = Grass()
        ASPHALT = Asphalt()
        FINISHLINE = FinishLine()

    def __init__(self, tipo: GroundType) -> None:
        self._structure = tipo.value


class Wall(Entities):

    class WallType(Enum):
        BARRIER = Barrier()
        FENCE = Fence()
        PIRELLI = PirelliSign()
        ROLEX = RolexSign()

    def __init__(self, tipo: WallType) -> None:
        self._structure = tipo.value

# 4.- Directores
# La clase Directora define el orden en el que se invocarán los pasos de
# construcción, por lo que puedes crear y reutilizar configuraciones específicas
# de los productos.


class Construction:

    def __init__(self) -> None:
        self._product = None

    @property
    def product(self) -> Entities:
        return self._product

    @product.setter
    def product(self, product: Entities) -> None:
        print(product)
        self._product = product

    def map(self) -> None:
        self.product.set_scale((100, 0, 500))
        self.product.set_position((0, 0, 0))

    def create(self) -> Entity:
        print('llego consturctor')
        print(self._product._structure.create_entity())
        return self._product._structure.create_entity()

    # def long_straight(self) -> None:
    #     self.product.set_position()
    #     self.product.set_scale()

    # def short_straight(self) -> None:
    #     self.product.set_position()
    #     self.product.set_scale()

    class Instructions(Enum):
        MAP = 'self.map()'

    def iniciar_montaje(self, tipo: Instructions):
        eval(tipo.value)


def track():
    track = Construction()
    track.product = Ground(Ground.GroundType.GRASS)
    track.iniciar_montaje(track.Instructions.MAP)
    ground = track.create()

    # print(ground.position)
    # print(ground.texture)
    # print(ground.scale)
    # print('aqui si')

    # app.run()
    # #  Piso
    # ground = Entities(
    #     model='plane',
    #     texture='grass.jpg',
    #     collider='mesh',
    #     scale=(100, 0, 500),
    # )
    # ground1 = Entities(
    #     position=(0, 0.1, 0),
    #     model='plane',
    #     texture='street.jpg',
    #     collider='mesh',
    #     scale=(10, 0, 50),
    # )
    # ground2 = Entities(
    #     position=(0, 0.1, 50),
    #     model='plane',
    #     texture='street.jpg',
    #     collider='mesh',
    #     scale=(10, 0, 50),
    # )

    # # Pared
    # pillar0 = Entities(
    #     model='cube',
    #     texture='concrete.jpg',
    #     scale=(10, 1.2, .1),
    #     position=(0, .5, -25),
    #     collider='box'
    # )
    # pillar1 = Entities(
    #     model='cube',
    #     texture='concrete.jpg',
    #     scale=(.1, 1.2, 50),
    #     position=(5, .5, 0),
    #     collider='box'
    # )

    # pillar2 = Entities(
    #     model='cube',
    #     texture='concrete.jpg',
    #     scale=(.1, 1.2, 50),
    #     position=(-5, .5, 0),
    #     collider='box'
    # )

    # # Finish line
    # finish_line = Entities(
    #     model='cube',
    #     texture='rolex.png',
    #     scale=(20, 6, .1),
    #     position=(0, 13, 25),
    #     collider='box'
    # )
