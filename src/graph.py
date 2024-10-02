import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

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

        # Ensure the x-axis and y-axis only display integers
        ax = plt.gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=5))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=5))

        # Optionally, set limits for axes if needed
        if self.x:
            plt.xlim(left=0, right=max(self.x) + 1)  # Adjust x-axis limits
        if self.y:
            plt.ylim(bottom=0, top=max(self.y) + 1)  # Adjust y-axis limits

        # Instead of plt.show(), we use plt.pause() to allow the game window to continue functioning
        plt.pause(0.001)  # Short pause to update the graph

    def add(self, score):
        size = len(self.x)
        self.x.append(size)
        self.y.append(score)
