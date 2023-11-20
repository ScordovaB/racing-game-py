# racing-game-py
# 3D Racing Game created with Ursina

## Game buttons: press "W" to speed up, press "Q" to turn left, press "E" to turn right, press "S" to go in reverse and press "space" to brake
## 
# To RUN the GAME:
## Run the game from the "__init__.py" file, make sure you have the whole folder, INCLUDING the folder VENV , to get the modified Ursina library. RUN it from the Virtual Environment
### In case you can't run it from the venv foler, the game will open, BUT not function correctly (meaning the car's inertia will be affected), then add manually to the FirstPersonController.py which its inside the Ursina library where all your python packages are, THEN add this on the line 44. 
```
self.forward * ((held_keys['w'] or held_keys['p']) - held_keys['s'])
```
