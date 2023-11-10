from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from track import track
from highscores import HighScore, HighScoreCaretaker, HighScoreMemento
from menus import QuitMenu


# Instanciamos la clase Ursina

app = Ursina()

# Player
player = FirstPersonController(
    collider='box',
    jump_height=0,
    speed=5
)
finish_timeline = Entity(model='cube', scale=(18, .3, .5), position=(
    0, 0, -30), collider='box', texture='assets/images/finish_line.jpg')
# Player position at the start
player.position = (0, 10, -20)
# Cursor invisible
player.cursor.visible = False
player.cursor.enabled = False

camera.fov = 90

# Cielo oscurecido
sky = Sky()
sky.texture = 'sky_sunset'


track()

acc_from_0_audio = Audio('assets/audio/ferrari-488-pista-primera.mp3',
                         loop=False, autoplay=False)
neutral_audio = Audio('assets/audio/ferrari-488-pista-neutral.mp3',
                      loop=False, autoplay=False)
acce_audio = Audio('assets/audio/ferrari-488-pista-acceleration.mp3',
                   loop=False, autoplay=False)
dec_to_0 = Audio('assets/audio/ferrari-488-pista-dec_primera.mp3',
                 loop=False, autoplay=False)
dec_audio = Audio('assets/audio/ferrari-488-pista-decelerate.mp3',
                  loop=False, autoplay=False)
shift_audio = Audio('assets/audio/ferrari-488-pista-shift.mp3',
                    loop=False, autoplay=False)


car = Entity(
    parent=camera.ui,
    model='cube',
    position=(0, 0),
    scale=(1.8, 1, 1),
    texture='assets/images/ferrari1pixel.png'
)
# make a global variables for velocity, time and player speed
velocity = 0
realtime = 0
rpm = 0
gear = 1
player_og_speed = 5
first_gear = True

highscore = HighScore()
caretaker = HighScoreCaretaker()
highscore_file = './RacingGame/highscores.json'


def update_highscore(score: float, highscore: HighScore, caretaker: HighScoreCaretaker, filename: str) -> None:
    # Load highscore
    caretaker.load_lap_time(highscore, filename)
    # Update highscore with new one
    new_high = score
    if new_high > highscore.score:
        highscore.score = new_high
        caretaker.save_lap_time(highscore, filename)
        print(f"New high score: {highscore.score}")


def upadate_player_speed():
    player.speed = player_og_speed + velocity
    

def change_rpm_gear():
    global rpm
    global gear
    global velocity

    # maximum of 8 gears
    new_gear = min((velocity - 1) // 10 + 1, 8) if velocity >= 0 else 1

    # Check if the gear has changed
    if new_gear != gear:
        rpm = 0
        gear = new_gear
    else:
        rpm += velocity /2
        # Set rpm based on velocity
        #rpm = min(velocity * 10, 1000)
    if rpm > 8000:
        rpm = 8000


def check_velocity():
    global velocity
    if velocity > 0:
        velocity -= .2
        held_keys['p'] = True
    if velocity < 0:
        velocity = 0
        held_keys['p'] = False

#On screen variable TEXT
speedometer = Sprite(texture='assets/images/speedometer.png', scale=(0.1,0.1), parent=camera.ui, position=(.7, -.3))
velocity_text2 = Text(text=velocity, position=(0.65, -0.23), scale=2, color=color.white)
timer = Text(text=velocity, position=(-0.55, 0.4), scale=2, color=color.white)
rpm_text = Text(text=rpm, position=(0.66,-0.3), scale=2, color=color.white)
gear_text = Text(text=gear, position=(0.72, -0.42), scale=2, color=color.white)



def update():
    global velocity
    global realtime
    global rpm
    global gear

    # print("Velocidad:", velocity)
    velocity_text2.text = str(round(velocity, 2))
    timer.text = str(round(realtime, 2))
    rpm_text.text = str(int(rpm))
    gear_text.text = str(int(gear))

    realtime += time.dt

    if player.intersects(finish_timeline).hit:
        print("Lap time:", round(realtime, 2))
        if round(realtime, 2) > 0.5:
            update_highscore(round(realtime, 2), highscore,
                             caretaker, highscore_file)
        realtime = 0

    if (player.y != 0.0):
        player.y = 0.0
    
    change_rpm_gear()

    # Block RIGHT and LEFT movement
    input_handler.bind('a', 'l')
    input_handler.bind('d', 'b')

    # Determine the car texture and velocity changes based on key presses
    key_combinations = {
        ('q', 'w'): ('assets/images/ferrari2pixel.png'),
        ('e', 'w'): ('assets/images/ferrari3pixel.png'),
        ('e', 's'): ('assets/images/ferrari3pixel.png'),
        ('q', 's'): ('assets/images/ferrari2pixel.png'),
        ('q',): ('assets/images/ferrari2pixel.png'),
        ('e',): ('assets/images/ferrari3pixel.png'),
        ('s',): ('assets/images/ferrari1pixel.png'),
        ('w',): ('assets/images/ferrari1pixel.png'),
        ('p',): ('assets/images/ferrari1pixel.png'),
        ('space',): ('assets/images/ferrari1pixel.png'),
    }

    # Check if any of the key combinations are pressed
    current_keys = [key for key in key_combinations if all(
        held_keys[k] for k in key)]

    # Update car texture and mouse position based on the key combination
    if current_keys:
        # print(current_keys[0])

        texture = key_combinations[current_keys[0]]
        car.texture = texture

        if 'w' in current_keys[0] and not acc_from_0_audio.playing:

            held_keys['p'] = False

        if 'w' in current_keys[0]:
            held_keys['p'] = False
            if velocity < 100:
                velocity += 0.1
            if not acc_from_0_audio.playing and velocity < 30:
                dec_to_0.stop()
                dec_audio.stop()
                neutral_audio.stop()
                acce_audio.stop()
                acc_from_0_audio.play()
            if not acce_audio.playing and not shift_audio.playing and velocity > 30:
                neutral_audio.stop()
                dec_audio.stop()
                acc_from_0_audio.stop()
                dec_to_0.stop()
                shift_audio.play()
                acce_audio.play()
            if not acce_audio.playing and not shift_audio.playing and velocity > 50:
                neutral_audio.stop()
                dec_audio.stop()
                acc_from_0_audio.stop()
                dec_to_0.stop()
                shift_audio.play()
                acce_audio.play()
            if not acce_audio.playing and not shift_audio.playing and velocity > 70:
                neutral_audio.stop()
                dec_audio.stop()
                acc_from_0_audio.stop()
                dec_to_0.stop()
                shift_audio.play()
                acce_audio.play()

            player.rotate((0, (held_keys['e'] - held_keys['q'])*1.5, 0))

            upadate_player_speed()

        if 's' in current_keys[0]:
            player.rotate((0, (held_keys['q'] - held_keys['e'])*1.5, 0))

        if held_keys['p']:
            player.rotate((0, (held_keys['e'] - held_keys['q'])*1.5, 0))
            check_velocity()
            if velocity == 0:
                dec_to_0.stop()
                acc_from_0_audio.stop()
                acce_audio.stop()
                dec_audio.stop()
                neutral_audio.play()

        if not 'w' in current_keys[0] and not dec_to_0.playing and velocity < 30 and velocity > 0:
            neutral_audio.stop()
            acc_from_0_audio.stop()
            shift_audio.stop()
            acce_audio.stop()
            dec_audio.stop()
            shift_audio.play()
            dec_to_0.play()
    else:
        # No valid key combination, decrease velocity
        if not neutral_audio.playing and velocity == 0:
            dec_to_0.stop()
            acc_from_0_audio.stop()
            shift_audio.stop()
            acce_audio.stop()
            dec_audio.stop()
            neutral_audio.play()

        if not dec_to_0.playing and velocity < 30 and velocity > 0:
            neutral_audio.stop()
            acc_from_0_audio.stop()
            shift_audio.stop()
            acce_audio.stop()
            dec_audio.stop()
            shift_audio.play()
            dec_to_0.play()

        if not dec_audio.playing and velocity > 30:
            neutral_audio.stop()
            acc_from_0_audio.stop()
            shift_audio.stop()
            acce_audio.stop()
            dec_to_0.stop()
            shift_audio.play()
            dec_audio.play()

        # player.speed = player_og_speed + velocity
        upadate_player_speed()
        check_velocity()



# Close button game
def input(key):
    if key == 'escape':

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Seconds:", round(elapsed_time, 2))

        time.sleep(.5)
        #Show mouse in screen for quitMenu interaction
        mouse.locked = not mouse.locked
        quitMenu = QuitMenu("Exit Game")


start_time = time.time()

time_text = Text(text='Lap Time:', position=(-0.8, 0.4),
                 scale=2, color=color.white)


# Audio
audioSong = Audio('assets/audio/TokyoDrift.mp3', loop=True, autoplay=False)
mouse.locked = True
# Start game
app.run()
