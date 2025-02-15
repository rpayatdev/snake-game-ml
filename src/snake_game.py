from graph import *
from train import *
import random
from tkinter import Label, Canvas, Button
import sys
import copy
from queue import Queue

SQUARE_SIZE = 25
CANVAS_HEIGHT = 700
CANVAS_WIDTH = 900
FIELD_HEIGHT = int(CANVAS_HEIGHT / SQUARE_SIZE)
FIELD_WIDTH = int(CANVAS_WIDTH / SQUARE_SIZE)
MAX_QUEUE_SIZE = 3
INITIAL_DIRECTION = "down"
YELLOW = "#FFFB00"

class Snake:
    def __init__(self, game):
        self.body_size = 3
        self.coordinates = []
        self.squares = []
        self.colour = "#00FF00"

        start_x = 0
        start_y = 0

        for i in range(self.body_size):
            if INITIAL_DIRECTION == "down":
                self.coordinates.append([start_x, start_y - i * SQUARE_SIZE])
            elif INITIAL_DIRECTION == "up":
                self.coordinates.append([start_x, start_y + i * SQUARE_SIZE])
            elif INITIAL_DIRECTION == "right":
                self.coordinates.append([start_x - i * SQUARE_SIZE, start_y])
            elif INITIAL_DIRECTION == "left":
                self.coordinates.append([start_x + i * SQUARE_SIZE, start_y])

        for x, y in self.coordinates:
            square = game.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=self.colour)
            self.squares.append(square)

class Food:
    def __init__(self, game, snake):
        count = 0
        is_on_snake = True
        while is_on_snake:
            count+=1
            if count > 1000:
                break
                #TODO: Spiel ist gewonnen Todoooo!!!!
            is_on_snake = False
            x = random.randint(0, FIELD_WIDTH - 1) * SQUARE_SIZE
            y = random.randint(0, FIELD_HEIGHT - 1) * SQUARE_SIZE
            for snake_x, snake_y in snake.coordinates:
                if snake_x == x and snake_y == y:
                    is_on_snake = True
            
        
        self.coordinates = [x, y]
        self.colour = "#FF0000"
        self.position = game.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=self.colour, tags="food")

class Game:
    def __init__(self, root, graph, train, is_ml, free_borders):
        self.root = root
        self.canvas = None
        self.label = None
        self.direction = INITIAL_DIRECTION
        self.score = 0
        self.graph = graph
        self.graph.show()
        self.train = train
        self.is_ml = is_ml
        self.free_borders = free_borders
        self.direction_queue = Queue(maxsize = MAX_QUEUE_SIZE)
        self.decision_method = "self"

        self.speed = 10 if self.is_ml else 100

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def gameover(self):
        self.train.save()

        self.direction_queue = Queue(maxsize = MAX_QUEUE_SIZE)

        self.canvas.delete("all")
        self.label.config(text=f"GAME OVER", fg="red")

        self.graph.add(self.score)
        self.graph.show()

        play_again = Button(self.root, text="Play Again", font=("Helvetica", 20), width=15, command=self.play)
        self.canvas.create_window(CANVAS_WIDTH/2, 370, window=play_again)
        self.canvas.create_text(CANVAS_WIDTH/2, 450, text=f"{self.score}",font=("Helvetica",20),fill="white")

        if self.is_ml:
            self.root.after(100, self.play)

    def make_decision(self, snake, food):
        decision = self.direction
        DANGER_WEIGHT = -10
        INCREASE_WEIGHT = 5
        DISTANCE_WEIGHT = -1

        move_scores = {}

        def calculate_score(danger, increase, distance):
            return ((DANGER_WEIGHT * danger) +
                    (INCREASE_WEIGHT * increase) +
                    (DISTANCE_WEIGHT * distance))
            
        possible_moves = {
            'up': ['up', 'left', 'right'],
            'down': ['down', 'left', 'right'],
            'left': ['up', 'left', 'down'],
            'right': ['up', 'down', 'right']
        }

        surviving_moves = []
        
        for move in possible_moves[self.direction]:
            simulated_record = self.record_status(self.simulate_step(snake, food, move), food, False)

            distance = simulated_record.get_distance_to_food()
            danger = simulated_record.get_danger()
            
            alive = self.train.predict_alive(simulated_record)
            increase = self.train.predict_increase(simulated_record)
            print(f"move: {move}, danger: {danger}, alive: {alive}")
            if alive > 0.5:
                surviving_moves.append(move)
                move_scores[move] = calculate_score(danger, increase, distance)
                print(f"Score: {move_scores[move]}")

        if surviving_moves:
            max_score = max(move_scores[move] for move in surviving_moves)
            best_moves = [move for move in surviving_moves if move_scores[move] == max_score]
            decision = random.choice(best_moves)
            self.decision_method = "surviving"
        else:
            decision = random.choice(possible_moves[self.direction])
            self.decision_method = "random"

        return decision

    def next_turn(self, snake, food):
        
        if self.is_ml:
            self.change_direction(self.make_decision(snake,food))
        elif not self.direction_queue.empty():
            self.change_direction(self.direction_queue.get())
        x, y = snake.coordinates[0]

        if self.direction == 'up':
            y = (y - SQUARE_SIZE) if y != 0 or not self.free_borders else CANVAS_HEIGHT-SQUARE_SIZE
        if self.direction == 'down':
            y = (y + SQUARE_SIZE) if y != CANVAS_HEIGHT-SQUARE_SIZE or not self.free_borders else 0
        if self.direction == 'left':
            x = (x - SQUARE_SIZE) if x != 0 or not self.free_borders else CANVAS_WIDTH-SQUARE_SIZE
        if self.direction == 'right':
            x = (x + SQUARE_SIZE) if x != CANVAS_WIDTH-SQUARE_SIZE or not self.free_borders else 0

        snake.coordinates.insert(0, [x, y])
        square = self.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=snake.colour)
        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            self.train.add(self.record_status(snake, food, True))
            self.score += 1
            snake.body_size +=1
            self.label.config(text=f"Score is : {self.score}")

            last_x, last_y = snake.coordinates[-1]
            snake.coordinates.insert(-1, [last_x, last_y])
            square = self.canvas.create_rectangle(last_x, last_y, last_x + SQUARE_SIZE, last_y + SQUARE_SIZE, fill=snake.colour)
            snake.squares.insert(-1, square)

            self.canvas.delete(food.position)
            food = Food(self, snake)
        else:
            self.train.add(self.record_status(snake, food, False))

        del snake.coordinates[-1]
        self.canvas.delete(snake.squares[-1])
        del snake.squares[-1]
   
        if self.check_collision(snake):
            self.gameover()
        else:
            self.root.after(self.speed, self.next_turn, snake, food)

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        if new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        if new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        if new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction
    
    def get_distance_to_food(self, snake_head_x, snake_head_y, food_x, food_y):
        if self.free_borders:
            x_distance = min(abs(snake_head_x - food_x), CANVAS_WIDTH - abs(snake_head_x - food_x))
            y_distance = min(abs(snake_head_y - food_y), CANVAS_HEIGHT - abs(snake_head_y - food_y))
        else:
            x_distance = abs(snake_head_x - food_x)
            y_distance = abs(snake_head_y - food_y)

        distance = (x_distance + y_distance) / SQUARE_SIZE
        return distance
    
    def get_food_direction(self, snake_head_x, snake_head_y, food_x, food_y):
        if self.free_borders:
            if snake_head_x == food_x:
                if (snake_head_y + SQUARE_SIZE) % CANVAS_HEIGHT == food_y: # example % 700 = 0...699
                    return 'down'
                elif (snake_head_y - SQUARE_SIZE) % CANVAS_HEIGHT == food_y: # example -25 % 700 = 675
                    return 'up'
            elif snake_head_y == food_y:
                if (snake_head_x + SQUARE_SIZE) % CANVAS_WIDTH == food_x:
                    return 'right'
                elif (snake_head_x - SQUARE_SIZE) % CANVAS_WIDTH == food_x:
                    return 'left'  
        else:
            if snake_head_x == food_x:
                if snake_head_y - food_y == SQUARE_SIZE:
                    return 'up'
                elif snake_head_y - food_y == -SQUARE_SIZE:
                    return 'down'
            elif snake_head_y == food_y:
                if snake_head_x - food_x == SQUARE_SIZE:
                    return 'left'
                elif snake_head_x - food_x == -SQUARE_SIZE:
                    return 'right'

        return 'none'

    def check_collision(self, snake):
        x, y = snake.coordinates[0]

        for x_pos, y_pos in snake.coordinates[1:]:
            if x_pos == x and y_pos == y:
                return True

        if not self.free_borders and ( x >= CANVAS_WIDTH-SQUARE_SIZE or y >= CANVAS_HEIGHT-SQUARE_SIZE or x < 0 or y < 0 ):
            return True

        return False
    
    def simulate_step(self, snake, food, direction):
        shallow_snake = copy.deepcopy(snake)
        x, y = shallow_snake.coordinates[0]
        match direction:
            case 'up':
                y = (y - SQUARE_SIZE) if y != 0 or not self.free_borders else CANVAS_HEIGHT-SQUARE_SIZE
            case 'down':
                y = (y + SQUARE_SIZE) if y != CANVAS_HEIGHT-SQUARE_SIZE or not self.free_borders else 0
            case 'left':
                x = (x - SQUARE_SIZE) if x != 0 or not self.free_borders else CANVAS_WIDTH-SQUARE_SIZE
            case 'right':
                x = (x + SQUARE_SIZE) if x != CANVAS_WIDTH-SQUARE_SIZE or not self.free_borders else 0
        
        shallow_snake.coordinates.insert(0, [x, y])
        
        if x == food.coordinates[0] and y == food.coordinates[1]:
            shallow_snake.body_size +=1
        
            last_x, last_y = shallow_snake.coordinates[-1]
            shallow_snake.coordinates.insert(-1, [last_x, last_y])
   
        del shallow_snake.coordinates[-1]

        return shallow_snake
    
    def record_status(self, snake, food, increase):
        snake_head_x, snake_head_y = snake.coordinates[0]
        food_x, food_y = food.coordinates

        distance_to_food = self.get_distance_to_food(snake_head_x, snake_head_y, food_x, food_y)
        food_direction = self.get_food_direction(snake_head_x, snake_head_y, food_x, food_y)

        danger_up = False
        danger_down = False
        danger_right = False
        danger_left = False

        simulated_snake_up = snake
        simulated_snake_left = snake
        simulated_snake_right = snake
        simulated_snake_down = snake

        match self.direction:
            case 'up':
                simulated_snake_up = self.simulate_step(snake, food, 'up')
                simulated_snake_left = self.simulate_step(snake, food, 'left')
                simulated_snake_right = self.simulate_step(snake, food, 'right')
            case 'down':
                simulated_snake_down = self.simulate_step(snake, food, 'down')
                simulated_snake_left = self.simulate_step(snake, food, 'left')
                simulated_snake_right = self.simulate_step(snake, food, 'right')
            case 'left':
                simulated_snake_up = self.simulate_step(snake, food, 'up')
                simulated_snake_left = self.simulate_step(snake, food, 'left')
                simulated_snake_down = self.simulate_step(snake, food, 'down')
            case 'right':
                simulated_snake_up = self.simulate_step(snake, food, 'up')
                simulated_snake_down = self.simulate_step(snake, food, 'down')
                simulated_snake_right = self.simulate_step(snake, food, 'right')

        if self.check_collision(simulated_snake_up):
            danger_up = True
        if self.check_collision(simulated_snake_down):
            danger_down = True
        if self.check_collision(simulated_snake_right):
            danger_right = True
        if self.check_collision(simulated_snake_left):
            danger_left = True

        alive = not self.check_collision(snake)

        self.status = Status(self.direction, food_direction, danger_left, danger_up, danger_right, danger_down, distance_to_food, self.decision_method, alive, increase)

        return self.status
    
    def add_direction_to_queue(self, direction):
        if not self.direction_queue.full():
            self.direction_queue.put(direction)

    def play(self):
        # Reset the direction to the initial one
        self.direction = INITIAL_DIRECTION

        # Clear any previous canvas or label to avoid multiple instances
        if self.label:
            self.label.destroy()
        if self.canvas:
            self.canvas.destroy()

        # Reset score and create new label and canvas
        self.score = 0
        self.label = Label(self.root, text=f"Score is : {self.score}", font=('consolas', 50))
        self.label.pack()

        self.canvas = Canvas(self.root, bg="#000000", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.pack()

        # Re-bind the arrow keys to control the snake
        if not self.is_ml:
            self.root.bind('<Left>', lambda event: self.add_direction_to_queue('left'))
            self.root.bind('<Right>', lambda event: self.add_direction_to_queue('right'))
            self.root.bind('<Down>', lambda event: self.add_direction_to_queue('down'))
            self.root.bind('<Up>', lambda event: self.add_direction_to_queue('up'))


        # Create new instances of Food and Snake for the new game
        snake = Snake(self)
        food = Food(self, snake)

        self.train.add(self.record_status(snake, food, False))
        
        # Start the next turn
        self.next_turn(snake, food)
    
    def on_closing(self):
        # Gracefully exit the Tkinter mainloop
        self.root.destroy()
        # Optionally close the Python process if needed
        sys.exit()