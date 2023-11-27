from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from abc import ABC, abstractmethod, abstractproperty
from enum import Enum


class Structure(ABC):
    ''' Basic structure class of the entities on the map '''

    def __init__(self, path: str, model=str, collider=str) -> Entity:
        self._position = (0, 0, 0)
        self._model = model
        self._texture = path
        self._collider = collider
        self._scale = (10, 0, 50)

    def create_entity(self) -> Entity:
        ''' Method to create entities with their respective properties '''
        return Entity(
            model=self._model,
            texture=self._texture,
            collider=self._collider,
            scale=self._scale,
            position=self._position
        )


class Asphalt(Structure):
    ''' Entity with asphalt floor properties to be created as product '''

    def __init__(self):
        super().__init__('asfaltoPro.jpg', 'plane', 'mesh')


class FinishLine(Structure):
    ''' Entity with finish line floor properties to be created as product '''

    def __init__(self):
        super().__init__('finish_line.jpg', 'plane', 'mesh')


class Grass(Structure):
    ''' Entity with grass floor properties to be created as product '''

    def __init__(self):
        super().__init__('grass.jpg', 'plane', 'mesh')


class PirelliSign(Structure):
    ''' Entity with pirelli wall properties to be created as product '''

    def __init__(self):
        super().__init__('pirelli.png', 'cube', 'box')


class RolexSign(Structure):
    ''' Entity with rolex wall properties to be created as product '''

    def __init__(self):
        super().__init__('rolex.png', 'cube', 'box')


class Fence(Structure):
    ''' Entity with fence wall properties to be created as product '''

    def __init__(self):
        super().__init__('fence.png', 'cube', 'box')


class Barrier(Structure):
    ''' Entity with barrier wall properties to be created as product '''

    def __init__(self):
        super().__init__('concrete.jpg', 'cube', 'box')


class Entities(ABC):
    ''' Builder interface declares methods every entity builders have in common '''

    def structure(self):
        ''' Defines the product structure in which the entity is based '''
        return self._structure

    def set_scale(self, scale: tuple) -> Entity:
        ''' Method to set the entity size '''
        self._structure._scale = scale

    def set_position(self, position: tuple) -> Entity:
        ''' Method to set the entity coordinates '''
        self._structure._position = position


class Ground(Entities):
    ''' Concrete builder of floor type entity '''
    class GroundType(Enum):
        GRASS = Grass()
        ASPHALT = Asphalt()
        FINISHLINE = FinishLine()

    def __init__(self, tipo: GroundType) -> Structure:
        self._structure = tipo.value


class Wall(Entities):
    ''' Concrete builder of wall type entity '''
    class WallType(Enum):
        BARRIER = Barrier()
        FENCE = Fence()
        PIRELLI = PirelliSign()
        ROLEX = RolexSign()

    def __init__(self, tipo: WallType) -> Structure:
        self._structure = tipo.value


class Construction:
    ''' Director class to define set of steps to create specific entities '''

    def __init__(self) -> product:
        self._product = None

    @property
    def product(self) -> Entities:
        return self._product

    @product.setter
    def product(self, product: Entities) -> Entities:
        self._product = product

    def map(self) -> Entity:
        ''' Method to place surface where the rest of entities are going to be deployed '''
        self.product.set_scale((380, 0, 400))
        self.product.set_position((165, 0, 30))
        return self.create()

    def create(self) -> Entity:
        ''' Method to deploy entity after getting its properties assign '''
        return self._product._structure.create_entity()

    def x_long_straight(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy a long straight floor according to x axel '''
        self.product.set_position(position)
        self.product.set_scale((15, 0, 50))
        return self.create()

    def x_short_straight(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy a short straight floor according to x axel '''
        self.product.set_position(position)
        self.product.set_scale((15, 0, 30))
        return self.create()

    def z_long_straight(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy a long straight floor according to z axel '''
        self.product.set_position(position)
        self.product.set_scale((50, 0, 15))
        return self.create()

    def z_short_straight(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy a short straight floor according to z axel '''
        self.product.set_position(position)
        self.product.set_scale((30, 0, 15))
        return self.create()

    def z_diagonal(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy a small floor to create diagonal track effect according to z axel '''
        self.product.set_position(position)
        self.product.set_scale((15, 0, 2))
        return self.create()

    def x_diagonal(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy a small floor to create diagonal track effect according to x axel '''
        self.product.set_position(position)
        self.product.set_scale((2, 0, 15))
        return self.create()

    def z_pirelli_sign(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy Pirelli sign according to z axel '''
        self.product.set_position(position)
        self.product.set_scale((5, 2, 0.1))
        return self.create()

    def x_pirelli_sign(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy Pirelli sign according to x axel '''
        self.product.set_position(position)
        self.product.set_scale((0.1, 2, 5))
        return self.create()

    def z_rolex_sign(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy Rolex sign according to z axel '''
        self.product.set_position(position)
        self.product.set_scale((5, 10, 30))
        return self.create()

    def x_rolex_sign(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy Rolex sign according to x axel '''
        self.product.set_position(position)
        self.product.set_scale((30, 10, 5))
        return self.create()

    def x_barrier(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy barrier according to x axel '''
        self.product.set_position(position)
        self.product.set_scale((50, 3, 0.1))
        return self.create()

    def z_barrier(self, position: tuple) -> Entity:
        ''' Method with the steps to deploy barrier according to z axel '''
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
        ''' Method with the steps to deploy entity according to Enum instruction selected '''
        if (position != None):
            return eval(type.value.format(position))
        return eval(type.value)


def track():
    ''' Method to deploy whole track '''
    track = Construction()

    # Map
    track.product = Ground(Ground.GroundType.GRASS)

    # Floors
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

    # Walls
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
    barrier6_2 = track.start_construction(
        track.Instructions.X_BARRIER, (140, 0.1, 145))
    barrier7_2 = track.start_construction(
        track.Instructions.X_BARRIER, (190, 0.1, 145))
    track.product.set_position((185, 0.1, 189))
    track.product.set_scale((0.1, 3, 35))
    track.create()
    barrier9 = track.start_construction(
        track.Instructions.X_BARRIER, (210, 0.1, 206.5))
    barrier10 = track.start_construction(
        track.Instructions.X_BARRIER, (260, 0.1, 206.5))

    barrier11 = track.start_construction(
        track.Instructions.Z_BARRIER, (259, 0.1, 181.5))
    barrier12 = track.start_construction(
        track.Instructions.Z_BARRIER, (259, 0.1, 131.5))
    barrier13 = track.start_construction(
        track.Instructions.Z_BARRIER, (259, 0.1, 81.5))
    barrier14 = track.start_construction(
        track.Instructions.Z_BARRIER, (259, 0.1, 31.5))
    barrier15 = track.start_construction(
        track.Instructions.Z_BARRIER, (259, 0.1, -18.5))
    barrier16 = track.start_construction(
        track.Instructions.Z_BARRIER, (259, 0.1, -68.5))
    barrier17 = track.start_construction(
        track.Instructions.X_BARRIER, (265, 0.1, 66))

    barrier8_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (210, 0.1, 116))
    barrier8_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (222.5, 0.1, 156))
    barrier9_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (210, 0.1, 66))
    barrier10_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (210, 0.1, 48))
    barrier11_2 = track.start_construction(
        track.Instructions.X_BARRIER, (205, 0.1, 23))
    barrier12_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (230, 0.1, -2))
    barrier13_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (230, 0.1, -22))

    barrier17 = track.start_construction(
        track.Instructions.X_BARRIER, (240, 0.1, -74.5))
    barrier18 = track.start_construction(
        track.Instructions.Z_BARRIER, (240, 0.1, -99.5))
    barrier19 = track.start_construction(
        track.Instructions.Z_BARRIER, (240, 0.1, -149.5))

    barrier14_2 = track.start_construction(
        track.Instructions.X_BARRIER, (205, 0.1, -47))
    barrier15_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (180, 0.1, -72))
    barrier16_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (180, 0.1, -112))
    barrier17_2 = track.start_construction(
        track.Instructions.X_BARRIER, (190, 0.1, -109))

    barrier20 = track.start_construction(
        track.Instructions.X_BARRIER, (215, 0.1, -160.5))
    barrier21 = track.start_construction(
        track.Instructions.X_BARRIER, (165, 0.1, -160.5))
    barrier22 = track.start_construction(
        track.Instructions.X_BARRIER, (115, 0.1, -160.5))
    barrier23 = track.start_construction(
        track.Instructions.X_BARRIER, (65, 0.1, -160.5))
    barrier24 = track.start_construction(
        track.Instructions.X_BARRIER, (15, 0.1, -160.5))
    barrier24 = track.start_construction(
        track.Instructions.X_BARRIER, (-35, 0.1, -160.5))

    barrier18_2 = track.start_construction(
        track.Instructions.X_BARRIER, (155, 0.1, -137))
    barrier19_2 = track.start_construction(
        track.Instructions.X_BARRIER, (105, 0.1, -137))
    barrier20_2 = track.start_construction(
        track.Instructions.X_BARRIER, (55, 0.1, -137))
    barrier21_2 = track.start_construction(
        track.Instructions.X_BARRIER, (55, 0.1, -137))

    track.product.set_position((30, 0.1, -126.5))
    track.product.set_scale((0.1, 3, 21))
    track.create()
    track.product.set_position((19.5, 0.1, -116))
    track.product.set_scale((21, 3, 0.1))
    track.create()

    barrier22_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (15, 0.1, -91))
    barrier23_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (15, 0.1, -41))
    barrier24_2 = track.start_construction(
        track.Instructions.Z_BARRIER, (15, 0.1, 9))

    barrier25 = track.start_construction(
        track.Instructions.Z_BARRIER, (-15, 0.1, -135.5))
    barrier27 = track.start_construction(
        track.Instructions.Z_BARRIER, (-15, 0.1, -85.5))
    barrier28 = track.start_construction(
        track.Instructions.Z_BARRIER, (-15, 0.1, -35.5))
    barrier29 = track.start_construction(
        track.Instructions.Z_BARRIER, (-15, 0.1, -10.5))

    # barrier6_2 = track.start_construction(
    #     track.Instructions.X_BARRIER, (110, 0.1, 171.5))
    # barrier7_2 = track.start_construction(
    #     track.Instructions.X_BARRIER, (160, 0.1, 171.5))

    # Decorations
    track.product = Wall(Wall.WallType.ROLEX)
    rolex1 = track.start_construction(
        track.Instructions.X_ROLEX_SIGN, (0, 15, 0))
    rolex2 = track.start_construction(
        track.Instructions.X_ROLEX_SIGN, (243, 15, -20))
    rolex3 = track.start_construction(
        track.Instructions.Z_ROLEX_SIGN, (138.5, 15, -147.5))
    rolex4 = track.start_construction(
        track.Instructions.Z_ROLEX_SIGN, (167.5, 15, 162.5))

    track.product = Wall(Wall.WallType.PIRELLI)
    pirelli1 = track.start_construction(
        track.Instructions.Z_PIRELLI_SIGN, (0, 1.1, 171.4))
    pirelli2 = track.start_construction(
        track.Instructions.Z_PIRELLI_SIGN, (5, 1.1, 171.4))
    pirelli3 = track.start_construction(
        track.Instructions.Z_PIRELLI_SIGN, (217.5, 1.1, 145))
    pirelli4 = track.start_construction(
        track.Instructions.Z_PIRELLI_SIGN, (245, 1.1, -74.4))
    pirelli5 = track.start_construction(
        track.Instructions.Z_PIRELLI_SIGN, (250, 1.1, -74.4))
    pirelli6 = track.start_construction(
        track.Instructions.X_PIRELLI_SIGN, (-14.9, 1.1, -135.5))
    pirelli7 = track.start_construction(
        track.Instructions.X_PIRELLI_SIGN, (-14.9, 1.1, -140.5))
