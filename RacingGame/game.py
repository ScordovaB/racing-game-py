from __future__ import annotations
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from track import track
from highscores import HighScore, HighScoreCaretaker, HighScoreMemento


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
dec_audio = Audio('assets/audio/ferrari-488-pista-decelerate.mp3',
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
player_og_speed = 5

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


def check_velocity():
    global velocity
    if velocity > 0:
        time.sleep(0.1)
        velocity -= 1
        player.position -= ((player.forward.x, 0, player.forward.z))
    if velocity < 0:
        velocity = 0


velocity_text2 = Text(text=velocity, position=(-.6, 0.3),
                      scale=2, color=color.white)
timer = Text(text=velocity, position=(-0.6, 0.4), scale=2, color=color.white)


def update():
    global velocity
    global realtime
    # print("Velocidad:", velocity)
    velocity_text2.text = str(round(velocity, 2))
    timer.text = str(round(realtime, 2))

    realtime += time.dt

    if player.intersects(finish_timeline).hit:
        print("Lap time:", round(realtime, 2))
        if round(realtime, 2) > 0.5:
            update_highscore(round(realtime, 2), highscore,
                             caretaker, highscore_file)
        realtime = 0

    if (player.y != 0.0):
        player.y = 0.0

    # Block RIGHT and LEFT movement
    input_handler.bind('a', 'l')
    input_handler.bind('d', 'b')

    # Determine the car texture and velocity changes based on key presses
    key_combinations = {
        ('q', 'w'): ('assets/images/ferrari2pixel.png', (-0.001, 0, -0.001)),
        ('e', 'w'): ('assets/images/ferrari3pixel.png', (0.001, 0, 0.001)),
        ('e', 's'): ('assets/images/ferrari3pixel.png', (-0.001, 0, -0.001)),
        ('q', 's'): ('assets/images/ferrari2pixel.png', (0.001, 0, 0.001)),
        ('q',): ('assets/images/ferrari2pixel.png', (0, 0, 0)),
        ('e',): ('assets/images/ferrari3pixel.png', (0, 0, 0)),
        ('s',): ('assets/images/ferrari1pixel.png', (0, 0, 0)),
        ('w',): ('assets/images/ferrari1pixel.png', (0, 0, 0)),
        ('space',): ('assets/images/ferrari1pixel.png', (0, 0, 0)),
    }

    # Check if any of the key combinations are pressed
    current_keys = [key for key in key_combinations if all(
        held_keys[k] for k in key)]

    # Update car texture and mouse position based on the key combination
    if current_keys:
        # print(current_keys[0])

        texture, mouse_position_change = key_combinations[current_keys[0]]
        car.texture = texture

        if 'w' in current_keys[0] and not acc_from_0_audio.playing:
            dec_audio.stop()
            neutral_audio.stop()
            acc_from_0_audio.play()

        if 'w' in current_keys[0]:
            if velocity < 50:
                velocity += 0.1

            if 'q' in current_keys[0]:
                player.rotate((0, -1, 0))
            if 'e' in current_keys[0]:
                player.rotate((0, 1, 0))

            # player.speed = player_og_speed + velocity
            upadate_player_speed()

        if 's' in current_keys[0]:

            if 'q' in current_keys[0]:
                player.rotate((0, 1, 0))

            if 'e' in current_keys[0]:
                player.rotate((0, -1, 0))

    else:
        # No valid key combination, decrease velocity
        if not neutral_audio.playing and velocity == 0:
            dec_audio.stop()
            acc_from_0_audio.stop()
            neutral_audio.play()

        if not dec_audio.playing and velocity > 0:
            neutral_audio.stop()
            acc_from_0_audio.stop()
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

        time.sleep(1)

        quit()


start_time = time.time()

time_text = Text(text='Time:', position=(-0.8, 0.4),
                 scale=2, color=color.white)
velocity_text = Text(text='Velocity:', position=(-.8, 0.3),
                     scale=2, color=color.white)
# time_text.create_background(padding=(.5,.25),radius=Text.size/2)


# Audio
audioSong = Audio('assets/audio/TokyoDrift.mp3', loop=True, autoplay=False)
mouse.locked = True
# Start game
app.run()
