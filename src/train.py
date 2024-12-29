import numpy
import pandas
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import copy

features_alive = ['Direction', 'DangerLeft', 'DangerUp', 'DangerRight', 'DangerDown']
features_food = ['Direction','FoodDirection','DistanceToFood']

class Status:
    def __init__(self, direction, 
                 food_direction, 
                 danger_left, danger_up, danger_right, danger_down,
                 distance_to_food, alive=True, increase=False):
        self.direction = direction
        self.food_direction = food_direction
        self.danger_left = danger_left
        self.danger_up = danger_up
        self.danger_right = danger_right
        self.danger_down = danger_down
        self.distance_to_food = distance_to_food
        self.alive = alive
        self.increase = increase

    def get_distance_to_food(self):
        return self.distance_to_food

    def get_status(self):
        return {
            'Direction': self.direction,
            'FoodDirection': self.food_direction,
            'DangerLeft': self.danger_left,
            'DangerUp': self.danger_up,
            'DangerRight': self.danger_right,
            'DangerDown': self.danger_down,
            'DistanceToFood': self.distance_to_food,
            'Alive': self.alive,
            'Increase': self.increase
        }
    def get_status_for_feature_alive(self):
        d = {'none': 0, 'left': 1, 'up': 2, 'right': 3, 'down': 4}
        dBool = {False: 0, True: 1}
        return pandas.DataFrame(data=numpy.array([[d.get(self.direction,self.direction) ,
                  dBool.get(self.danger_left,self.danger_left), dBool.get(self.danger_up,self.danger_up), dBool.get(self.danger_right,self.danger_right), dBool.get(self.danger_down,self.danger_down)
                  ]]), columns=features_alive)
    def get_status_for_feature_food(self):
        d = {'none': 0, 'left': 1, 'up': 2, 'right': 3, 'down': 4}
        dBool = {False: 0, True: 1}
        return pandas.DataFrame(data=numpy.array([[d.get(self.direction,self.direction) ,
                  d.get(self.food_direction,self.food_direction),
                  self.distance_to_food]]), columns=features_food)
class Train:
    def __init__(self):
        self.read()

    def read(self):
        self.df = pandas.read_csv("data.csv")
    def save(self):
        self.df.to_csv("snake_game_data.csv", index=False)
    def add(self, status):
        #self.df = self.df.append(status.get_status(), ignore_index=True)
        #print(f"Dataframe: {self.df} ")
        if self.df.empty:   
            self.df = pandas.DataFrame([status.get_status()])
        else:
            new_row = pandas.DataFrame([status.get_status()])
            self.df = pandas.concat([self.df, new_row], ignore_index=True)

    def predict_alive(self, status):
        shallow_df = copy.deepcopy(self.df)
        d = {'none': 0, 'left': 1, 'up': 2, 'right': 3, 'down': 4}
        shallow_df['Direction'] = shallow_df['Direction'].map(d)
        d = {False: 0, True: 1}
        shallow_df['DangerLeft'] = shallow_df['DangerLeft'].map(d)
        shallow_df['DangerUp'] = shallow_df['DangerUp'].map(d)
        shallow_df['DangerRight'] = shallow_df['DangerRight'].map(d)
        shallow_df['DangerDown'] = shallow_df['DangerDown'].map(d)
        shallow_df['Alive'] = shallow_df['Alive'].map(d)
        if shallow_df[features_alive + ['Alive']].isna().any().any():
            print("Warning: NaN values detected in shallow_df after mapping.")
            print(shallow_df[features_alive + ['Alive']].isna().sum())
        X = shallow_df[features_alive]
        y = shallow_df[['Alive']] 
        dtree = DecisionTreeClassifier()
        dtree = dtree.fit(X, y)

        pred = dtree.predict(status.get_status_for_feature_alive())
        
        if pred[0] == 0:
            return False
        else:
            return True
    
    def predict_increase(self, status):
        shallow_df = copy.deepcopy(self.df)
        d = {'none': 0, 'left': 1, 'up': 2, 'right': 3, 'down': 4}
        shallow_df['Direction'] = shallow_df['Direction'].map(d)
        shallow_df['FoodDirection'] = shallow_df['FoodDirection'].map(d)
        d = {False: 0, True: 1}
        shallow_df['Increase'] = shallow_df['Increase'].map(d)
        if shallow_df[features_food + ['Increase']].isna().any().any():
            print("Warning: NaN values detected in shallow_df after mapping.")
            print(shallow_df[features_food + ['Increase']].isna().sum())
        X = shallow_df[features_food]
        y = shallow_df[['Increase']] 
        dtree = DecisionTreeClassifier()
        dtree = dtree.fit(X, y)

        pred = dtree.predict(status.get_status_for_feature_food())
        
        if pred[0] == 0:
            return False
        else:
            return True