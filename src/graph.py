import matplotlib.pyplot as plt

class Graph:
    
    def __init__(self):
        self.x = []
        self.y = []

    def show(self):
        # clear the plot before showing
        plt.clf()
        # plot the data
        plt.bar(self.x, self.y)
        # naming the x axis
        plt.xlabel('Turn')
        # naming the y axis
        plt.ylabel('Score points')
        # Instead of plt.show(), we use plt.pause() to allow the game window to continue functioning
        plt.pause(0.001)  # Short pause to update the graph

    def add(self, score):
        size = len(self.x)
        self.x.append(size)
        self.y.append(score)