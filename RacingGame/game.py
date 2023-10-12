from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time





#Instanciamos la clase Ursina

app = Ursina()

#Player 
player = FirstPersonController(
    collider='box',
    jump_height=0,
    speed=30
)
#Player position at the start
player.position = (0,10,-20)
#Cursor invisible
player.cursor.visible = False
player.cursor.enabled = False
camera.fov = 90

#Cielo oscurecido
sky = Sky()
sky.texture = 'sky_sunset'

#Piso
ground = Entity(
    model='plane',
    texture='street.jpg',
    collider = 'mesh',
    scale=(10,-2,50),
)

#sw = Sprite('assets/f1car1.png',parent=camera.ui, scale=0.3, position=(0,-0.1)) #, scale=1, position=(0,0)

#Pared
pillar0 = Entity(
    model='cube',
    texture = 'concrete.jpg',
    scale=(10,1.2,.1),
    position=(0,.5,-25),
    collider='box'
)
pillar1 = Entity(
    model='cube',
    texture = 'concrete.jpg',
    scale=(.1,1.2,50),
    position=(5,.5,0),
    collider='box'
)

pillar2 = Entity(
    model='cube',
    texture = 'concrete.jpg',
    scale=(.1,1.2,50),
    position=(-5,.5,0),
    collider='box'
)

#Finish line
finish_line = Entity(
    model='cube',
    texture = 'finish_line.jpg',
    scale=(10,1.2,.1),
    position=(0,10,25),
    collider='box'
)
car  = Entity(
    parent = camera.ui,
    model = 'cube',
    position = (0,0),
    scale = (1.8,1,1),
    texture = 'assets/ferrari1.png'
)

def update():
    #mouse.locked= True
    
    #Block RIGHT and LEFT movement
    input_handler.bind('a','l')
    input_handler.bind('d','b')
    
    if held_keys['left arrow'] and held_keys['w']:

        car.texture = 'assets/ferrari1.png'
        car.texture = 'assets/ferrari2.png'
        mouse.position -= (0.001,0,0.001)

    elif held_keys['left arrow'] and held_keys['s']:

        car.texture = 'assets/ferrari1.png'
        car.texture = 'assets/ferrari2.png'
        mouse.position -= (0.001,0,0.001)

    elif held_keys['left arrow'] :

        car.texture = 'assets/ferrari1.png'
        car.texture = 'assets/ferrari2.png'
        
    elif held_keys['right arrow']:

        car.texture = 'assets/ferrari1.png'
        car.texture = 'assets/ferrari3.png'
        
    elif held_keys['right arrow'] and held_keys['w']:
        car.texture = 'assets/ferrari1.png'
        car.texture = 'assets/ferrari3.png'
        mouse.position += (0.001,0,0.001)
        #pass

    elif held_keys['right arrow'] and held_keys['s']:
        #pass

        car.texture = 'assets/ferrari1.png'
        car.texture = 'assets/ferrari3.png'
        mouse.position += (0.001,0,0.001)



#mouse.locked= True

#Close button game
def input(key):
    if key == 'escape':

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Seconds:",round(elapsed_time,2))

        time.sleep(1)
    
        quit()

#sw =Sprite('assets/final458/458recto.png',parent=camera.ui, scale=0.2, position=(0,-0.1)) #, scale=1, position=(0,0)


start_time = time.time()
time_text = Text(text='Time:',position=(-0.8,0.4),scale=2,color=color.black)


#Audio
audio = Audio('assets/TokyoDrift.mp3',loop=True, autoplay=False)
mouse.locked= True
#Start game
app.run()