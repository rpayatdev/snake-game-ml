from snake_game import *
from graph import *

root = Tk()
root.title("Snake Game")

graph = Graph()
graph.show()

game = Game(root, graph)
game.play()

root.mainloop()


"""
TEST = 10
def newHelloWorldPrinter(aList):
    #x = 5
    #y = 10
    TEST = 15
    TEST = 1+2
    for a in aList:
        print(f"Hello World {a}")

aList = ["Hans", "Payat", "Lea", "Simon", "Hexa", "Jordan", "Timeo"]

newHelloWorldPrinter(aList)
"""