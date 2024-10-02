from graph import *
import random
from tkinter import Tk, Label, Canvas, Button

SQUARE_SIZE = 25
CANVAS_HEIGHT = 700
CANVAS_WIDTH = 900
FIELD_HEIGHT = int(CANVAS_HEIGHT / SQUARE_SIZE)
FIELD_WIDTH = int(CANVAS_WIDTH / SQUARE_SIZE)
INITIAL_DIRECTION = "down"

class Snake:
    def __init__(self, game):
        self.body_size = 3
        self.coordinates = []
        self.squares = []
        self.colour = "#00FF00"

        for i in range(0, self.body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = game.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=self.colour)
            self.squares.append(square)

class Food:
    def __init__(self, game):
        x = random.randint(0, FIELD_WIDTH - 1) * SQUARE_SIZE
        y = random.randint(0, FIELD_HEIGHT - 1) * SQUARE_SIZE
        self.coordinates = [x, y]
        self.colour = "#FF0000"
        self.position = game.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=self.colour, tags="food")

class Game:
    def __init__(self, root, graph):
        self.root = root
        self.canvas = None
        self.label = None
        self.direction = INITIAL_DIRECTION
        self.score = 0
        self.graph = graph

    def gameover(self):
        self.canvas.delete("all")
        self.label.config(text=f"GAME OVER", fg="red")

        self.graph.add(self.score)
        self.graph.show()

        play_again = Button(self.root, text="Play Again", font=("Helvetica", 20), width=15, command=self.play)
        self.canvas.create_window(CANVAS_WIDTH/2, 370, window=play_again)
        self.canvas.create_text(CANVAS_WIDTH/2, 450, text=f"{self.score}",font=("Helvetica",20),fill="white")

    def next_turn(self, snake, food):
        x, y = snake.coordinates[0]

        if self.direction == 'up':
            y -= SQUARE_SIZE
        if self.direction == 'down':
            y += SQUARE_SIZE
        if self.direction == 'left':
            x -= SQUARE_SIZE
        if self.direction == 'right':
            x += SQUARE_SIZE

        snake.coordinates.insert(0, [x, y])
        square = self.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=snake.colour)
        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"Score is : {self.score}")

            last_x, last_y = snake.coordinates[-1]
            snake.coordinates.insert(-1, [last_x, last_y])
            square = self.canvas.create_rectangle(last_x, last_y, last_x + SQUARE_SIZE, last_y + SQUARE_SIZE, fill=snake.colour)
            snake.squares.insert(-1, square)

            self.canvas.delete(food.position)
            food = Food(self)

        del snake.coordinates[-1]
        self.canvas.delete(snake.squares[-1])
        del snake.squares[-1]

        if self.check_collision(snake):
            self.gameover()
        else:
            self.root.after(100, self.next_turn, snake, food)

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        if new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        if new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        if new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def check_collision(self, snake):
        x, y = snake.coordinates[0]

        for x_pos, y_pos in snake.coordinates[1:]:
            if x_pos == x and y_pos == y:
                return True

        if x >= CANVAS_WIDTH or y >= CANVAS_HEIGHT or x < 0 or y < 0:
            return True

        return False

    def play(self):
        if self.label:
            self.label.destroy()
        if self.canvas:
            self.canvas.destroy()

        self.score = 0
        self.label = Label(self.root, text=f"Score is : {self.score}", font=('consolas', 50))
        self.label.pack()

        self.canvas = Canvas(self.root, bg="#000000", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.pack()

        self.root.bind('<Left>', lambda event: self.change_direction('left'))
        self.root.bind('<Right>', lambda event: self.change_direction('right'))
        self.root.bind('<Down>', lambda event: self.change_direction('down'))
        self.root.bind('<Up>', lambda event: self.change_direction('up'))

        food = Food(self)
        snake = Snake(self)
        self.next_turn(snake, food)

# Main game setup
root = Tk()
root.title("Snake Game")

graph = Graph()
game = Game(root, graph)
game.play()

root.mainloop()
