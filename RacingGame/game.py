from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time


# Instanciamos la clase Ursina

app = Ursina()

# Player
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

# Cielo oscurecido
sky = Sky()
sky.texture = 'sky_sunset'

#  Piso
ground = Entity(
    model='plane',
    texture='street.jpg',
    collider='mesh',
    scale=(10, -2, 50),
)
ground1 = Entity(
    position=(0, 0, 50),
    model='plane',
    texture='street.jpg',
    collider='mesh',
    scale=(10, -2, 50),
)

# sw = Sprite('assets/f1car1.png',parent=camera.ui, scale=0.3, position=(0,-0.1)) #, scale=1, position=(0,0)

# Pared
pillar0 = Entity(
    model='cube',
    texture='concrete.jpg',
    scale=(10, 1.2, .1),
    position=(0, .5, -25),
    collider='box'
)
pillar1 = Entity(
    model='cube',
    texture='concrete.jpg',
    scale=(.1, 1.2, 50),
    position=(5, .5, 0),
    collider='box'
)

pillar2 = Entity(
    model='cube',
    texture='concrete.jpg',
    scale=(.1, 1.2, 50),
    position=(-5, .5, 0),
    collider='box'
)

# Finish line
finish_line = Entity(
    model='cube',
    texture='finish_line.jpg',
    scale=(10, 1.2, .1),
    position=(0, 10, 25),
    collider='box'
)


acc_audio = Audio('assets/ferrari-488-pista-primera.mp3',
                  loop=False, autoplay=False)
neutral_audio = Audio('assets/ferrari-488-pista-neutral.mp3',
                      loop=False, autoplay=False)
acce_audio = Audio('assets/ferrari-488-pista-acceleration.mp3',
                   loop=False, autoplay=False)


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

def upadate_player_speed():
    player.speed = player_og_speed + velocity

def check_velocity():
    global velocity
    if velocity > 0:
            velocity -= 1
    if velocity < 0:
        velocity = 0


def update():
    global velocity
    print("Velocidad:", velocity)

    # Determine the car texture and velocity changes based on key presses
    key_combinations = {
        ('q', 'w'): ('assets/ferrari2pixel.png', (-0.001, 0, -0.001)),
        ('e', 'w'): ('assets/ferrari3pixel.png', (0.001, 0, 0.001)),
        ('e', 's'): ('assets/ferrari3pixel.png', (0.001, 0, 0.001)),
        ('q', 's'): ('assets/ferrari2pixel.png', (-0.001, 0, -0.001)),
        ('q',): ('assets/ferrari2pixel.png', (0, 0, 0)),
        ('e',): ('assets/ferrari3pixel.png', (0, 0, 0)),
        ('s',): ('assets/ferrari1pixel.png', (0, 0, 0)),
        ('w',): ('assets/ferrari1pixel.png', (0, 0, 0)),
        ('space',): ('assets/ferrari1pixel.png', (0, 0, 0)),
    }

    #Check if any of the key combinations are pressed
    current_keys = [key for key in key_combinations if all(held_keys[k] for k in key)]

    # Update car texture and mouse position based on the key combination
    if current_keys:
        #print(current_keys[0])

        texture, mouse_position_change = key_combinations[current_keys[0]]
        car.texture = texture
        
        if 'w' in current_keys[0] and not acc_audio.playing:
            neutral_audio.stop()
            acc_audio.play()

        if 'w' not in current_keys[0] and not neutral_audio.playing:
            acc_audio.stop()
            neutral_audio.play()
        
        if 'w' in current_keys[0]:
            if velocity < 50:
                velocity += 0.1
                
            #player.speed = player_og_speed + velocity
            upadate_player_speed()

        if 'q' in current_keys[0] or 'e' in current_keys[0]:
            mouse.position += mouse_position_change

    else:
        # No valid key combination, decrease velocity
        if not neutral_audio.playing:
            acc_audio.stop()
            neutral_audio.play()

        #player.speed = player_og_speed + velocity
        upadate_player_speed()
        check_velocity()

# mouse.locked= True

# Close button game
def input(key):
    if key == 'escape':

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Seconds:", round(elapsed_time, 2))

        time.sleep(1)

        quit()


start_time = time.time()

time_text = Text(text='Time:',position=(-0.8,0.4),scale=2,color=color.black)
#time_text.create_background(padding=(.5,.25),radius=Text.size/2)


# Audio
audioSong = Audio('assets/TokyoDrift.mp3',loop=True, autoplay=False)
mouse.locked = True
# Start game
app.run()
