This is Martizianos War, a space invaders-style game project made using Python and Pygame library. It's a work in progress and I'll be upgrading it and adding new features.


![Screenshot](./img/screenshot.png)

## Features

 - Use the Left Arrow and Right Arrow keys to move Spaceship
 - Use the Space Bar to shoot your enemies
 - You can Mute music with 'm' key and play it with 'p' key
 - Use Escape key to exit game
 - If you lose, yo can press space bar key to restart


## Requirements:

- Python 3

- Pygame

## Usage

Open a terminal and navigate to the directory called 'Martzianos' which contains all project files.
Enter this command to install dependencies: 
``` bash
pip install -r requirements
```

Enter this command to run the application:
``` bash
python main.py
```

## Customization
You have the flexibility to customize various aspects of the game by adjusting the constants located at the beginning of the code. These constants include:

```python
# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SPEED = 3
ENEMY_SPEED = 2.5
NUMBER_ENEMIES = 8
FPS = 60
```
Feel free to experiment with these values to customize the gameplay experience according to your preferences. Modify the player's speed, the number of enemies, screen dimensions, and other parameters to create a game that suits your vision.

