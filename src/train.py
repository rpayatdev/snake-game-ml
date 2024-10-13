import numpy
import pandas
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import utils

features = ['Direction',
            'FoodDirection',
            'DangerLeft', 'DangerUp', 'DangerRight', 'DangerDown','DistanceToFood']

class Status:
    def __init__(self, direction, 
                 food_direction, 
                 danger_left, danger_up, danger_right, danger_down,
                 distance_to_food, alive=True, size=3):
        self.direction = direction
        self.food_direction = food_direction
        self.danger_left = danger_left
        self.danger_up = danger_up
        self.danger_right = danger_right
        self.danger_down = danger_down
        self.distance_to_food = distance_to_food
        self.alive = alive
        self.size = size

    def get_status(self):
        return [{
            'Direction': self.direction,
            'FoodLeft': self.food_direction,
            'DangerLeft': self.danger_left,
            'DangerUp': self.danger_up,
            'DangerRight': self.danger_right,
            'DangerDown': self.danger_down,
            'DistanceToFood': self.distance_to_food,
            'Alive': self.alive,
            'Size': self.size
        }]
    def get_status_for_feature(self):
        return [[self.direction,
                  self.food_direction,
                  self.danger_left, self.danger_up, self.danger_right, self.danger_down,
                  self.distance_to_food]]

class Train:
    def __init__(self):
        self.read()

    def read(self):
        self.df = pandas.read_csv("data.csv")
    def save(self):
        self.df.to_csv("snake_game_data.csv", index=False)
    def add(self, status):
        self.df = self.df.append(status.get_status(), ignore_index=True)
    def predict(self, status):
        X = self.df[features]
        y = self.df[['Alive', 'Size']]  # Multi-output targets
        dtree = DecisionTreeClassifier()
        dtree = dtree.fit(X, y)

        pred = dtree.predict(status.getstatus_for_feature())
        print(f"Prediction for Alive: {pred[0][0]}, Prediction for Size: {pred[0][1]}")
        return pred