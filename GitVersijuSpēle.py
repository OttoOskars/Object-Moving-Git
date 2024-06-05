import viz
import vizshape
import vizcam
import vizact
import math
import random
import vizinput
import time

viz.go()
viz.clearcolor(viz.SKYBLUE)

collection_sound = viz.addAudio('C:\\Users\\nmrom\\Downloads\\ballon_pops.mp3')

# Floor
floor = vizshape.addPlane(size=(200, 200), axis=vizshape.AXIS_Y, cullFace=False)
floor.setPosition(0, 0, 0)
floor.color(viz.GRAY)

# Player name
player1 = vizinput.input('Enter name for Player 1:')
player2 = vizinput.input('Enter name for Player 2:')

# Player default scores, time limit
players = [player1, player2]
scores = [0, 0]
current_player = 0
round_time_limit = 10

# Text display
score_text = viz.addText('', parent=viz.SCREEN, pos=(0.1, 0.9, 0))
timer_text = viz.addText('', parent=viz.SCREEN, pos=(0.1, 0.8, 0))
winner_text = viz.addText('', parent=viz.SCREEN, pos=(0.5, 0.5, 0))

# Color function
def random_color():
    return random.choice([viz.RED, viz.GREEN, viz.BLUE, viz.YELLOW, viz.ORANGE, viz.PURPLE, viz.WHITE, viz.BLACK])

# Random size function
def random_size():
    return random.uniform(0.1, 0.5)

def update_score_text():
    score_text.message(f"{players[0]}: {scores[0]} {players[1]}: {scores[1]}")

collected_objects = []

def handle_collision():
    global scores
    camera_pos = camera.getPosition()
    for obj in objects:
        obj_pos = obj.getPosition()
        distance = math.sqrt((obj_pos[0] - camera_pos[0]) ** 2 + (obj_pos[1] - camera_pos[1]) ** 2 + (obj_pos[2] - camera_pos[2]) ** 2)
        if distance < 2.5:  # Distance for picking
            if obj not in collected_objects:  # Check if not already collected
                obj.visible(viz.OFF)
                scores[current_player] += 1
                update_score_text()
                collected_objects.append(obj)
                collection_sound.play()

def switch_turns():
    global current_player
    global round_start_time
    current_player = (current_player + 1) % 2
    round_start_time = time.time()
    print(f"Now it's {players[current_player]}'s turn")
    
    # Reset objects for next play
    for obj in collected_objects:
        obj.visible(viz.ON)
    collected_objects.clear()
    
    if current_player == 0 and round_start_time > round_time_limit * len(players):
        determine_winner()

def update_timer():
    elapsed = time.time() - round_start_time
    remaining = round_time_limit - elapsed
    if remaining <= 0:
        switch_turns()
        remaining = round_time_limit
    timer_text.message(f"Time left: {int(remaining)} seconds")

def determine_winner():
    if scores[0] > scores[1]:
        winner_text.message(f"{players[0]} wins!")
    elif scores[1] > scores[0]:
        winner_text.message(f"{players[1]} wins!")
    else:
        winner_text.message("It's a tie!")
    winner_text.visible(viz.ON)

camera = viz.MainView
objects = []
num_objects = 2000
grid_size = 200
spacing = 1.0

for i in range(num_objects):
    object_type = random.choice(['sphere', 'cube', 'cylinder'])
    if object_type == 'sphere':
        obj = vizshape.addSphere(radius=random_size())
    elif object_type == 'cube':
        obj = vizshape.addCube(size=random_size())
    else:
        obj = vizshape.addCylinder(height=random_size(), radius=random_size() * 0.5)
    
    x = random.uniform(-grid_size / 2, grid_size / 2)
    z = random.uniform(-grid_size / 2, grid_size / 2)
    x = round(x / spacing) * spacing
    z = round(z / spacing) * spacing
    obj.setPosition(x, random.uniform(0.1, 0.5), z)
    obj.color(random_color())
    objects.append(obj)

def handle_navigation():
    move_speed = 200.0

    def move_forward():
        camera.move(0, 0, move_speed * viz.elapsed(), viz.ABS_GLOBAL)

    def move_backward():
        camera.move(0, 0, -move_speed * viz.elapsed(), viz.ABS_GLOBAL)

    def strafe_left():
        camera.move(-move_speed * viz.elapsed(), 0, 0, viz.ABS_GLOBAL)

    def strafe_right():
        camera.move(move_speed * viz.elapsed(), 0, 0, viz.ABS_GLOBAL)

    vizact.onkeydown('w', move_forward)
    vizact.onkeydown('s', move_backward)
    vizact.onkeydown('a', strafe_left)
    vizact.onkeydown('d', strafe_right)

handle_navigation()

# Start the first turn
round_start_time = time.time()

vizact.ontimer(0.1, handle_collision)
vizact.ontimer(1, update_timer)

viz.mouse(viz.OFF)
viz.go()
#test