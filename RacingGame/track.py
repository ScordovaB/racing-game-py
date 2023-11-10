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

    def create_entity(self) -> Entity:
        return Entity(
            model=self._model,
            texture=self._texture,
            collider=self._collider,
            scale=self._scale,
            position=self._position
        )


class Asphalt(Structure):
    def __init__(self):
        super().__init__('asphalt.jpg', 'plane', 'mesh')


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
    def structure(self):
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

    def map(self) -> Entity:
        self.product.set_scale((400, 0, 400))
        self.product.set_position((185, 0, 0))
        return self.create()

    def create(self) -> Entity:
        return self._product._structure.create_entity()

    def x_long_straight(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((15, 0, 50))
        return self.create()

    def x_short_straight(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((15, 0, 30))
        return self.create()

    def z_long_straight(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((50, 0, 15))
        return self.create()

    def z_short_straight(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((30, 0, 15))
        return self.create()

    def z_diagonal(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((15, 0, 2))
        return self.create()

    def x_diagonal(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((2, 0, 15))
        return self.create()

    def z_pirelli_sign(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((5, 2, 0.1))
        return self.create()

    def x_pirelli_sign(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((0.1, 2, 5))
        return self.create()

    def z_rolex_sign(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((5, 10, 30))
        return self.create()

    def x_rolex_sign(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((30, 10, 5))
        return self.create()

    def x_barrier(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((50, 3, 0.1))
        return self.create()

    def z_barrier(self, position: tuple) -> Entity:
        self.product.set_position(position)
        self.product.set_scale((0.1, 3, 50))
        return self.create()

    class Instructions(Enum):
        MAP = 'self.map()'
        X_L_STRAIGHT = 'self.x_long_straight({})'
        Z_L_STRAIGHT = 'self.z_long_straight({})'
        X_S_STRAIGHT = 'self.x_short_straight({})'
        Z_S_STRAIGHT = 'self.z_short_straight({})'
        Z_DIAGONAL = 'self.z_diagonal({})'
        X_DIAGONAL = 'self.x_diagonal({})'
        Z_PIRELLI_SIGN = 'self.z_pirelli_sign({})'
        X_PIRELLI_SIGN = 'self.x_pirelli_sign({})'
        Z_ROLEX_SIGN = 'self.z_rolex_sign({})'
        X_ROLEX_SIGN = 'self.x_rolex_sign({})'
        X_BARRIER = 'self.x_barrier({})'
        Z_BARRIER = 'self.z_barrier({})'

    def start_construction(self, type: Instructions, position: tuple):
        if (position != None):
            return eval(type.value.format(position))
        return eval(type.value)


def track():
    track = Construction()

    # Map
    track.product = Ground(Ground.GroundType.GRASS)

    # Road
    ground = track.start_construction(track.Instructions.MAP, None)
    track.product = Ground(Ground.GroundType.ASPHALT)

    straight1 = track.start_construction(
        track.Instructions.X_L_STRAIGHT, (0, 0.1, 0))
    straight2 = track.start_construction(
        track.Instructions.X_L_STRAIGHT, (0, 0.1, 50))
    straight3 = track.start_construction(
        track.Instructions.X_L_STRAIGHT, (0, 0.1, 100))

    curve1 = track.start_construction(
        track.Instructions.Z_S_STRAIGHT, (7.5, 0.1, 132.5))
    curve2 = track.start_construction(
        track.Instructions.Z_S_STRAIGHT, (37.5, 0.1, 132.5))
    curve3 = track.start_construction(
        track.Instructions.X_S_STRAIGHT, (60, 0.1, 140))
    curve4 = track.start_construction(
        track.Instructions.Z_L_STRAIGHT, (77.5, 0.1, 162.5))

    straight4 = track.start_construction(
        track.Instructions.Z_L_STRAIGHT, (127.5, 0.1, 162.5))
    straight5 = track.start_construction(
        track.Instructions.Z_L_STRAIGHT, (167.5, 0.1, 162.5))

    curve5 = track.start_construction(
        track.Instructions.X_L_STRAIGHT, (200, 0.1, 180))
    curve6 = track.start_construction(
        track.Instructions.Z_S_STRAIGHT, (222.5, 0.1, 197.5))
    curve7 = track.start_construction(
        track.Instructions.X_L_STRAIGHT, (245, 0.1, 180))

    straight6 = track.start_construction(
        track.Instructions.X_L_STRAIGHT, (245, 0.1, 130))

    s1 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (243, 0.1, 104))
    s2 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (241, 0.1, 102))
    s3 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (239, 0.1, 100))
    s4 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (237, 0.1, 98))
    s5 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (235, 0.1, 96))
    s6 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (233, 0.1, 94))
    s7 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (231, 0.1, 92))
    s8 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (229, 0.1, 90))
    s9 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (227, 0.1, 88))
    s10 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (225, 0.1, 86))
    s11 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (223, 0.1, 84))
    s12 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (221, 0.1, 82))

    straight7 = track.start_construction(
        track.Instructions.X_S_STRAIGHT, (219, 0.1, 66))

    s13 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (221, 0.1, 50))
    s14 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (223, 0.1, 48))
    s15 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (225, 0.1, 46))
    s16 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (227, 0.1, 44))
    s17 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (229, 0.1, 42))
    s18 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (231, 0.1, 40))
    s19 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (233, 0.1, 38))
    s20 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (235, 0.1, 36))
    s21 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (237, 0.1, 34))
    s22 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (239, 0.1, 32))
    s23 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (241, 0.1, 30))
    s24 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (243, 0.1, 28))

    straight8 = track.start_construction(
        track.Instructions.X_L_STRAIGHT, (243, 0.1, 2))
    straight9 = track.start_construction(
        track.Instructions.X_S_STRAIGHT, (243, 0.1, -38))

    curve8 = track.start_construction(
        track.Instructions.Z_L_STRAIGHT, (225.5, 0.1, -60.5))
    curve9 = track.start_construction(
        track.Instructions.X_S_STRAIGHT, (193, 0.1, -68))

    d1 = track.start_construction(
        track.Instructions.X_DIAGONAL, (201.5, 0.1, -77.5))
    d2 = track.start_construction(
        track.Instructions.X_DIAGONAL, (203.5, 0.1, -79.5))
    d3 = track.start_construction(
        track.Instructions.X_DIAGONAL, (205.5, 0.1, -81.5))
    d4 = track.start_construction(
        track.Instructions.X_DIAGONAL, (207.5, 0.1, -83.5))
    d5 = track.start_construction(
        track.Instructions.X_DIAGONAL, (209.5, 0.1, -85.5))
    d6 = track.start_construction(
        track.Instructions.X_DIAGONAL, (211.5, 0.1, -87.5))
    d7 = track.start_construction(
        track.Instructions.X_DIAGONAL, (213.5, 0.1, -89.5))
    d8 = track.start_construction(
        track.Instructions.X_DIAGONAL, (215.5, 0.1, -91.5))
    d9 = track.start_construction(
        track.Instructions.X_DIAGONAL, (217.5, 0.1, -93.5))
    d10 = track.start_construction(
        track.Instructions.X_DIAGONAL, (219.5, 0.1, -95.5))

    curve10 = track.start_construction(
        track.Instructions.X_S_STRAIGHT, (228, 0.1, -105))

    d11 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (226, 0.1, -121))
    d12 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (224, 0.1, -123))
    d13 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (222, 0.1, -125))
    d14 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (220, 0.1, -127))
    d15 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (218, 0.1, -129))
    d16 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (216, 0.1, -131))
    d17 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (214, 0.1, -133))
    d18 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (212, 0.1, -135))
    d19 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (210, 0.1, -137))
    d20 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (208, 0.1, -139))

    straight10 = track.start_construction(
        track.Instructions.Z_L_STRAIGHT, (188.5, 0.1, -147.5))
    straight11 = track.start_construction(
        track.Instructions.Z_L_STRAIGHT, (138.5, 0.1, -147.5))
    straight12 = track.start_construction(
        track.Instructions.Z_L_STRAIGHT, (88.5, 0.1, -147.5))

    d21 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (2, 0.1, -126))
    d22 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (4, 0.1, -128))
    d23 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (6, 0.1, -130))
    d24 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (8, 0.1, -132))
    d25 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (10, 0.1, -134))
    d26 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (12, 0.1, -136))
    d27 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (14, 0.1, -138))
    d28 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (16, 0.1, -140))
    d29 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (18, 0.1, -142))
    d30 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (20, 0.1, -144))
    d31 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (22, 0.1, -146))
    d32 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (24, 0.1, -148))
    d33 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (26, 0.1, -150))
    d34 = track.start_construction(
        track.Instructions.Z_DIAGONAL, (28, 0.1, -152))

    straight14 = track.start_construction(
        track.Instructions.X_L_STRAIGHT, (0, 0.1, -50))
    straight15 = track.start_construction(
        track.Instructions.X_L_STRAIGHT, (0, 0.1, -100))

    track.product.set_position((43.5, 0.1, -147.5))
    track.product.set_scale((40, 0, 15)),
    straight13 = track.create()

    # Barriers
    track.product = Wall(Wall.WallType.BARRIER)
    barrier1 = track.start_construction(
        track.Instructions.Z_BARRIER, (-15, 0.1, -4))
    barrier2 = track.start_construction(
        track.Instructions.Z_BARRIER, (-15, 0.1, 46))
    barrier3 = track.start_construction(
        track.Instructions.Z_BARRIER, (-15, 0.1, 96))
    barrier4 = track.start_construction(
        track.Instructions.Z_BARRIER, (-15, 0.1, 146))

    barrier1_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (15, 0.1, -5))
    barrier2_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (15, 0.1, 45))
    barrier3_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (15, 0.1, 95))

    barrier5 = track.start_construction(
        track.Instructions.X_BARRIER, (10, 0.1, 171.5))
    barrier6 = track.start_construction(
        track.Instructions.X_BARRIER, (60, 0.1, 171.5))
    barrier7 = track.start_construction(
        track.Instructions.X_BARRIER, (110, 0.1, 171.5))
    barrier8 = track.start_construction(
        track.Instructions.X_BARRIER, (160, 0.1, 171.5))

    barrier4_2 = track.start_construction(
        track.Instructions.X_BARRIER, (40, 0.1, 120))
    barrier5_2 = track.start_construction(
        track.Instructions.X_BARRIER, (90, 0.1, 120))
    track.product.set_position((115, 0.1, 132.5))
    track.product.set_scale((0.1, 3, 25))
    track.create()
    barrier5_2 = track.start_construction(
        track.Instructions.X_BARRIER, (140, 0.1, 145))

    # barrier6_2 = track.start_construction(
    #     track.Instructions.X_BARRIER, (110, 0.1, 171.5))
    # barrier7_2 = track.start_construction(
    #     track.Instructions.X_BARRIER, (160, 0.1, 171.5))

    track.product = Wall(Wall.WallType.ROLEX)
    pirelli1 = track.start_construction(
        track.Instructions.X_ROLEX_SIGN, (0, 15, 0))

    track.product = Wall(Wall.WallType.PIRELLI)
    pirelli1 = track.start_construction(
        track.Instructions.Z_PIRELLI_SIGN, (0, 1.1, 171.4))
    track.product = Wall(Wall.WallType.PIRELLI)
    pirelli1 = track.start_construction(
        track.Instructions.Z_PIRELLI_SIGN, (5, 1.1, 171.4))
