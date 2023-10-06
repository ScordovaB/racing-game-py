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

def update():
    
    #Block RIGHT and LEFT movement
    input_handler.bind('a','l')
    input_handler.bind('b','b')


#Close button game
def input(key):
  if key == 'escape':

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Seconds:",round(elapsed_time,2))
    
    #Sleep for 1 seconds, and print time before quitting
    #new_time = Text(text='Time:'+str(round(elapsed_time,2)),position=(-0.8,0.4),scale=2,color=color.black)
    time.sleep(1)
    
    quit()


#Start game
start_time = time.time()
#elapsed_time = 0
#Print realtime on screen
time_text = Text(text='Time:',position=(-0.8,0.4),scale=2,color=color.black)

#Audio
audio = Audio('assets/TokyoDrift.mp3',loop=True, autoplay=True)

app.run()