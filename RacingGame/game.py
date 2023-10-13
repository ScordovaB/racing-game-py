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
    speed=5
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
    texture = 'assets/ferrari1pixel.png'
)

#make a global velocity variable
velocity = 0
player_og_speed =5


def update():
    #mouse.locked= True
    global velocity
    #Block RIGHT and LEFT movement
    input_handler.bind('a','l')
    input_handler.bind('d','b')
    
    
    if held_keys['q'] and held_keys['w']:

        if velocity<50:
            velocity +=0.1
        player.speed = player_og_speed + velocity
        
        car.texture = 'assets/ferrari1pixel.png'
        car.texture = 'assets/ferrari2pixel.png'
        mouse.position -= (0.001,0,0.001)
        
    
    elif held_keys['e'] and held_keys['w']:
        
        if velocity<50:
            velocity +=0.1
        player.speed = player_og_speed + velocity

        car.texture = 'assets/ferrari1pixel.png'
        car.texture = 'assets/ferrari3pixel.png'
        mouse.position += (0.001,0,0.001)

    elif held_keys['e'] and held_keys['s']:
        
        #velocity -=0.01
    
        car.texture = 'assets/ferrari1pixel.png'
        car.texture = 'assets/ferrari3pixel.png'
        mouse.position += (0.001,0,0.001)

    elif held_keys['q'] and held_keys['s']:

        #velocity -=0.01

        car.texture = 'assets/ferrari1pixel.png'
        car.texture = 'assets/ferrari2pixel.png'
        mouse.position -= (0.001,0,0.001)

    elif held_keys['q'] :
        
        #print("presionando q")
        car.texture = 'assets/ferrari1pixel.png'
        car.texture = 'assets/ferrari2pixel.png'
        
    elif held_keys['e']:
        #mouse.position += (0.001,0,0.001)
        car.texture = 'assets/ferrari1pixel.png'
        car.texture = 'assets/ferrari3pixel.png'

    elif held_keys['s']:
        
        #velocity -=0.01
        

        car.texture = 'assets/ferrari1pixel.png'
    
    elif held_keys['w']:

        if velocity<50:
            velocity +=0.1
        player.speed = player_og_speed + velocity

        car.texture = 'assets/ferrari1pixel.png'
    
    elif held_keys['space']:
        velocity =0
        car.texture = 'assets/ferrari1pixel.png'
    
    else:
        #print("nada")
        print("Velocidad:",velocity)
        
        
        if velocity>0:
            velocity-=1
        if velocity<0:
            velocity=0
    
    player.speed = player_og_speed + velocity

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
#time_text.create_background(padding=(.5,.25),radius=Text.size/2)


#Audio
audio = Audio('assets/TokyoDrift.mp3',loop=True, autoplay=False)
mouse.locked= True
#Start game
app.run()